import { db } from "../../helpers/db";
import { getServerUserSession } from "../../helpers/getServerUserSession";
import { studioProjectModel } from "../../helpers/studioProjectModel";
import { studioTemplates } from "../../helpers/studioTemplates";
import { schema } from "./save_POST.schema";
import superjson from "superjson";
export async function handle(request:Request) {
  let user;
  try { ({user}=await getServerUserSession(request)); } catch {
    return new Response(superjson.stringify({error:"Sessão necessária para salvar."}),{status:401});
  }
  try {
    const input=schema.parse(superjson.parse(await request.text()));
    studioTemplates.assertDocument(input.files["index.html"],input.files["style.css"],input.files["script.js"]);
    const row=await db.updateTable("studioProjects").set({
      html:input.files["index.html"],css:input.files["style.css"],javascript:input.files["script.js"],
      updatedAt:new Date()
    }).where("id","=",input.id).where("ownerUserId","=",user.id).returningAll().executeTakeFirst();
    if(!row)return new Response(superjson.stringify({error:"Projeto não encontrado."}),{status:404});
    return new Response(superjson.stringify({project:studioProjectModel.toClient(row)}));
  }catch(error){const msg=error instanceof Error && (error.name==="ZodError"||error.message.includes("100 KB"))?error.message:"Falha na validação dos arquivos.";
    return new Response(superjson.stringify({error:msg}),{status:400});}
}
