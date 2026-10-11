import {z} from "zod";
import superjson from "superjson";
import {studioProjectModel} from "../../helpers/studioProjectModel";
export const schema=z.object({name:z.string().trim().min(2).max(80),description:z.string().trim().max(240).default("")});
export type OutputType={project:ReturnType<typeof studioProjectModel.toClient>};
export async function postStudioCreate(input:z.infer<typeof schema>):Promise<OutputType>{
  const r=await fetch("/_api/studio/create",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json"},body:superjson.stringify(schema.parse(input))});
  const data=superjson.parse<OutputType & {error?:string}>(await r.text());
  if(!r.ok)throw new Error(data.error||"Falha ao criar projeto");
  return data;
}
