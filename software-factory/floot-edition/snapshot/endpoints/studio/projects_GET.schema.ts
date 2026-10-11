import {z} from "zod";
import superjson from "superjson";
import {studioProjectModel} from "../../helpers/studioProjectModel";
export const schema=z.object({});
export type OutputType={projects:Array<ReturnType<typeof studioProjectModel.toClient>>};
export async function getStudioProjects():Promise<OutputType> {
  const r=await fetch("/_api/studio/projects",{method:"GET",credentials:"same-origin"});
  const data=superjson.parse<OutputType & {error?:string}>(await r.text());
  if(!r.ok)throw new Error(data.error||"Não foi possível carregar projetos");
  return data;
}
