import { db } from "../../helpers/db";
import { getServerUserSession } from "../../helpers/getServerUserSession";
import { studioProjectModel } from "../../helpers/studioProjectModel";
import { studioTemplates } from "../../helpers/studioTemplates";
import { schema } from "./create_POST.schema";
import superjson from "superjson";
export async function handle(request:Request) {
  let user;
  try { ({user}=await getServerUserSession(request)); } catch {
    return new Response(superjson.stringify({error:"Faça login para criar projetos."}),{status:401});
  }
  try {
    const input=schema.parse(superjson.parse(await request.text()));
    const amount=await db.selectFrom("studioProjects").select(({fn})=>fn.count<number>("id").as("count")).where("ownerUserId","=",user.id).executeTakeFirstOrThrow();
    if(Number(amount.count)>=30)return new Response(superjson.stringify({error:"Limite de 30 projetos por conta."}),{status:429});
    const code=studioTemplates.starter(input.name);
    const row=await db.insertInto("studioProjects").values({
      ownerUserId:user.id,name:input.name,description:input.description,
      html:code.html,css:code.css,javascript:code.javascript
    }).returningAll().executeTakeFirstOrThrow();
    return new Response(superjson.stringify({project:studioProjectModel.toClient(row)}),{status:201});
  }catch(error){const msg=error instanceof Error && error.name==="ZodError"?"Nome ou descrição inválidos.":"Não foi possível criar o projeto.";
    return new Response(superjson.stringify({error:msg}),{status:400});}
}
