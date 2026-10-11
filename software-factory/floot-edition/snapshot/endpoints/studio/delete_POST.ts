import {db} from "../../helpers/db";
import {getServerUserSession} from "../../helpers/getServerUserSession";
import {schema} from "./delete_POST.schema";
import superjson from "superjson";
export async function handle(request:Request){
 let user;
 try{({user}=await getServerUserSession(request));}catch{return new Response(superjson.stringify({error:"Login necessário."}),{status:401});}
 try{
  const input=schema.parse(superjson.parse(await request.text()));
  const deleted=await db.deleteFrom("studioProjects").where("id","=",input.id).where("ownerUserId","=",user.id).returning("id").executeTakeFirst();
  if(!deleted)return new Response(superjson.stringify({error:"Projeto não encontrado."}),{status:404});
  return new Response(superjson.stringify({ok:true}));
 }catch{return new Response(superjson.stringify({error:"Identificador inválido."}),{status:400});}
}
