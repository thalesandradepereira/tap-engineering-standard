import { flootAi, FlootAiOutOfCreditsError, FlootAiRateLimitError } from "@floot/ai";
import { db } from "../../helpers/db";
import { sql } from "kysely";
import { getServerUserSession } from "../../helpers/getServerUserSession";
import { makeAiInstructions, parseGeneratedPage, validateGenerationRequest, extractGeneratedText, AiOutputIssue } from "../../helpers/studioAiGeneration";
import { schema } from "./ai_generate_POST.schema";
import superjson from "superjson";

const MAX_GENERATIONS_PER_DAY=3;
const encode=(obj:unknown,status=200)=>new Response(superjson.stringify(obj),{status,headers:{"Content-Type":"application/json","Cache-Control":"no-store"}});
export async function handle(request:Request){
 let user;
 try{({user}=await getServerUserSession(request));}catch{return encode({error:"Faça login para usar a geração por IA."},401);}
 let input;
 try{input=schema.parse(superjson.parse(await request.text()));validateGenerationRequest(input.prompt);}
 catch{return encode({error:"Descreva o aplicativo em 12 a 1500 caracteres e confirme os créditos Floot."},400);}
 const project=await db.selectFrom("studioProjects").select(["id","name"])
   .where("id","=",input.projectId).where("ownerUserId","=",user.id).executeTakeFirst();
 if(!project)return encode({error:"Projeto não encontrado."},404);
 const entitlement=await db.selectFrom("studioAiEntitlements").select("enabled").where("userId","=",user.id).executeTakeFirst();
 if(entitlement?.enabled!==true)return encode({error:"A geração por IA está restrita à conta autorizada.",code:"AI_NOT_AUTHORIZED"},403);
 const dateStart=new Date();dateStart.setUTCHours(0,0,0,0);
 let allowance:{id:string,remaining:number}|null=null;
 try{
  allowance=await db.transaction().execute(async trx=>{
   await sql`SELECT pg_advisory_xact_lock(${user.id}::bigint + 8395100000)`.execute(trx);
   const count=await trx.selectFrom("studioAiRequests").select(({fn})=>fn.count<number>("id").as("n"))
     .where("userId","=",user.id).where("requestedAt",">=",dateStart).executeTakeFirstOrThrow();
   const used=Number(count.n);
   if(used>=MAX_GENERATIONS_PER_DAY)return null;
   const created=await trx.insertInto("studioAiRequests").values({
      userId:user.id,projectId:project.id,status:"started"
   }).returning("id").executeTakeFirstOrThrow();
   return {id:String(created.id),remaining:MAX_GENERATIONS_PER_DAY-used-1};
  });
 }catch{return encode({error:"Não foi possível verificar o limite de geração. Nenhuma IA foi chamada."},503);}
 if(!allowance)return encode({error:"Limite de três gerações por dia atingido. Tente novamente amanhã (UTC).",code:"AI_DAILY_LIMIT"},429);
 let credits=0;
 try{
  const response=await flootAi.chat({
    model:"gpt-6-luna",
    instructions:makeAiInstructions(project.name),
    input:input.prompt,
    reasoning:{effort:"medium"},
    text:{format:{
      type:"json_schema",name:"tap_site_files_v1",strict:true,
      schema:{type:"object",additionalProperties:false,required:["html","css","javascript"],
        properties:{html:{type:"string"},css:{type:"string"},javascript:{type:"string"}}}
    }},
    // No automatic retry: each user-approved call can use Floot credits.
    max_output_tokens:6000,
  });
  credits=Number(response.flootCredits?.consumed??0);
  const text=extractGeneratedText(response);
  const candidate=parseGeneratedPage(text);
  await db.updateTable("studioAiRequests").set({status:"completed",creditsConsumed:credits}).where("id","=",allowance.id).execute();
  return encode({candidate,model:"gpt-6-luna",creditsConsumed:credits,remainingToday:allowance.remaining});
 }catch(error){
  try{await db.updateTable("studioAiRequests").set({status:"failed",creditsConsumed:credits}).where("id","=",allowance.id).execute();}catch{}
  if(error instanceof FlootAiOutOfCreditsError)return encode({error:"Créditos Floot esgotados.",code:"OUT_OF_CREDITS"},503);
  if(error instanceof FlootAiRateLimitError)return encode({error:"O serviço de IA atingiu o limite por minuto. Aguarde antes de tentar novamente.",code:"AI_RATE_LIMIT"},429);
  if(error instanceof AiOutputIssue)return encode({error:error.message+" A tentativa pode ter consumido créditos Floot.",code:error.code,creditsConsumed:credits},422);
  if(error instanceof Error && /inválid|excedeu|vazio|permitid|JSON/i.test(error.message))return encode({error:error.message,code:"INVALID_AI_OUTPUT"},422);
  return encode({error:"Não foi possível concluir a geração. Verifique o histórico de uso e tente mais tarde.",code:"AI_PROVIDER_ERROR"},502);
 }
}
