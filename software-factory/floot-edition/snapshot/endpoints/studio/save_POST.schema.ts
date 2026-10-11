import {z} from "zod";
import superjson from "superjson";
import {studioProjectModel} from "../../helpers/studioProjectModel";
export const schema=z.object({
 id:z.string().regex(/^\d+$/),
 files:z.object({"index.html":z.string().max(100000),"style.css":z.string().max(100000),"script.js":z.string().max(100000)}).strict()
});
export type OutputType={project:ReturnType<typeof studioProjectModel.toClient>};
export async function postStudioSave(input:z.infer<typeof schema>):Promise<OutputType>{
  const r=await fetch("/_api/studio/save",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json"},body:superjson.stringify(schema.parse(input))});
  const data=superjson.parse<OutputType & {error?:string}>(await r.text());
  if(!r.ok)throw new Error(data.error||"Falha ao salvar arquivos");
  return data;
}
