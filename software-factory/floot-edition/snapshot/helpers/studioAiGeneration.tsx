import { z } from "zod";

const outputSchema = z.object({
  html: z.string().max(40000),
  css: z.string().max(40000),
  javascript: z.string().max(40000),
}).strict();

export function validateGenerationRequest(prompt: string): string {
  const trimmed=prompt.trim();
  if(trimmed.length<12||trimmed.length>1500)throw new Error("Descreva a página em 12 a 1500 caracteres.");
  return trimmed;
}

export function makeAiInstructions(name:string):string {
  const safeName=name.replace(/[<>\r\n]/g," ").slice(0,80);
  return `You are TAP Studio's single-page app builder. Return ONLY JSON with EXACTLY these string fields: html, css, javascript. No Markdown, no preamble. Build a polished, accessible, self-contained, responsive HTML/CSS/JS page for project: ${safeName}. The html is only the BODY fragment (no document/head/style/script tags). CSS must be standalone without @import or external resources. JavaScript must be vanilla JS, no imports, no eval, no network access, no localStorage/cookies, no secret/token handling, no user account collection. Do not request secrets, credentials, API keys, payment details, or personal data. Do not emit external script src, iframe, javascript: links, meta-refresh, inline onload handlers, or third-party tracking. Preserve working HTML semantics, contrast, and responsive layout. The page will run in an isolated sandbox with network access disabled. Do not claim this generates a server, database, native app or deployed website.`;
}

export function parseGeneratedPage(raw:string):Record<"index.html"|"style.css"|"script.js",string>{
  if(raw.length>130000)throw new Error("A resposta da IA excedeu o limite permitido.");
  const text=raw.trim();
  const match=text.match(/\`\`\`(?:json)?\s*([\s\S]*?)\`\`\`/i);
  const json=match?match[1].trim():text;
  let parsed:unknown;
  try{parsed=JSON.parse(json);}catch{throw new Error("A IA não retornou JSON válido; tente novamente.");}
  const result=outputSchema.safeParse(parsed);
  if(!result.success)throw new Error("A IA retornou estrutura inválida; nenhuma alteração foi aplicada.");
  const {html,css,javascript}=result.data;
  if(!html.trim())throw new Error("A IA retornou HTML vazio.");
  if(/<script\b[^>]*\bsrc\s*=|\bjavascript\s*:|<iframe\b|<object\b|<embed\b|\bon\w+\s*=/i.test(html))throw new Error("HTML gerado contém recursos não permitidos.");
  if(/@import|url\s*\(\s*['"]?https?:/i.test(css))throw new Error("CSS gerado contém dependências externas.");
  if(/\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|importScripts|eval|Function)\s*\(/i.test(javascript))throw new Error("O JavaScript gerado usa recursos externos/não permitidos.");
  return {"index.html":html,"style.css":css,"script.js":javascript};
}
