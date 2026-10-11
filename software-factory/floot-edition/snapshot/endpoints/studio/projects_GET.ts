import { db } from "../../helpers/db";
import { getServerUserSession } from "../../helpers/getServerUserSession";
import { studioProjectModel } from "../../helpers/studioProjectModel";
import superjson from "superjson";
export async function handle(request: Request) {
  try {
    const { user }=await getServerUserSession(request);
    const rows=await db.selectFrom("studioProjects").selectAll().where("ownerUserId","=",user.id).orderBy("updatedAt","desc").limit(30).execute();
    return new Response(superjson.stringify({projects:rows.map(studioProjectModel.toClient)}),{headers:{"Content-Type":"application/json"}});
  } catch {
    return new Response(superjson.stringify({error:"Sessão inválida ou indisponível."}),{status:401,headers:{"Content-Type":"application/json"}});
  }
}
