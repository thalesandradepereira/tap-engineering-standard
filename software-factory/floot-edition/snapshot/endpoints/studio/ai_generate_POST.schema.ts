import { z } from "zod";
import superjson from "superjson";
export const schema=z.object({
 projectId:z.string().regex(/^\d+$/),
 prompt:z.string().trim().min(12).max(1500),
 consentToCredits:z.literal(true),
}).strict();
export type GeneratedFiles={"index.html":string,"style.css":string,"script.js":string};
export type OutputType={candidate:GeneratedFiles,model:string,creditsConsumed:number,remainingToday:number};
export async function postAiGenerate(input:z.input<typeof schema>):Promise<OutputType>{
 const r=await fetch("/_api/studio/ai_generate",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json"},body:superjson.stringify(schema.parse(input))});
 const data=superjson.parse<OutputType & {error?:string,code?:string,creditsConsumed?:number}>(await r.text());
 if(!r.ok){const e=new Error(data.error||"A geração de IA falhou.") as Error&{code?:string};e.code=data.code;(e as Error&{creditsConsumed?:number}).creditsConsumed=data.creditsConsumed;throw e;}
 return data;
}
