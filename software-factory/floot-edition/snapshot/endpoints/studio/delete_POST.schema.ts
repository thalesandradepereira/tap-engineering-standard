import {z} from "zod";
import superjson from "superjson";
export const schema=z.object({id:z.string().regex(/^\d+$/)});
export type OutputType={ok:boolean};
export async function postStudioDelete(input:z.infer<typeof schema>):Promise<OutputType>{
 const r=await fetch("/_api/studio/delete",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json"},body:superjson.stringify(schema.parse(input))});
 const data=superjson.parse<OutputType & {error?:string}>(await r.text());
 if(!r.ok)throw new Error(data.error||"Falha ao excluir");
 return data;
}
