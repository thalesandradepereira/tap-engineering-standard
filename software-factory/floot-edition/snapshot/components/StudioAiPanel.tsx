import React, {useState} from "react";
import {Sparkles, WandSparkles, ShieldCheck, Coins, CheckCircle2, X, Eye, Code2} from "lucide-react";
import {Button} from "./Button";
import {Textarea} from "./Textarea";
import {postAiGenerate, type GeneratedFiles} from "../endpoints/studio/ai_generate_POST.schema";
import {studioTemplates} from "../helpers/studioTemplates";
import styles from "./StudioAiPanel.module.css";

type Props={projectId:string,projectName:string,dirty:boolean,onApply:(files:GeneratedFiles)=>void};
export function StudioAiPanel({projectId,projectName,dirty,onApply}:Props){
 const [prompt,setPrompt]=useState("");
 const [loading,setLoading]=useState(false);
 const [candidate,setCandidate]=useState<GeneratedFiles|null>(null);
 const [error,setError]=useState("");
 const [consent,setConsent]=useState(false);
 const [credits,setCredits]=useState<number|null>(null);
 const [remaining,setRemaining]=useState<number|null>(null);
 const [showPreview,setShowPreview]=useState(true);
 async function generate(){
  if(!consent||loading||prompt.trim().length<12)return;
  const confirmed=window.confirm("A geração usará GPT-6 Luna e poderá consumir créditos Floot. Limite: 3 tentativas por dia na conta autorizada. O seu código será mantido até você clicar em Aplicar e Salvar. Deseja continuar?");
  if(!confirmed)return;
  setLoading(true);setError("");setCandidate(null);
  try{
   const result=await postAiGenerate({projectId,prompt:prompt.trim(),consentToCredits:true});
   setCandidate(result.candidate);setCredits(result.creditsConsumed);setRemaining(result.remainingToday);setShowPreview(true);
  }catch(err){
   const ex=err as Error&{code?:string};
   if(ex.code==="OUT_OF_CREDITS"){setError("Créditos Floot indisponíveis. Consulte os créditos da plataforma.");}
   else setError((ex.message||"A geração falhou.")+(typeof (ex as Error&{creditsConsumed?:number}).creditsConsumed==="number"?" Créditos dessa tentativa: "+(ex as Error&{creditsConsumed?:number}).creditsConsumed+".":"")+" Nenhuma repetição será feita automaticamente.");
  }finally{setLoading(false);}
 }
 function apply(){
  if(!candidate)return;
  if(dirty&&!window.confirm("Há alterações não salvas neste projeto. Aplicar o novo código irá substituí-las no editor. Continuar?"))return;
  onApply(candidate);setCandidate(null);
 }
 const preview=candidate?studioTemplates.makePreview(candidate["index.html"],candidate["style.css"],candidate["script.js"],true):"";
 return <section className={styles.panel} aria-label="TAP AI Studio">
  <div className={styles.heading}><div className={styles.icon}><Sparkles size={20}/></div><div><div className={styles.eyebrow}>TAP AI BUILDER · BETA</div><h2>Crie por descrição</h2><p>Descreva a página que deseja gerar em português. A IA cria HTML, CSS e JavaScript para revisão antes de salvar.</p></div><span className={styles.model}>GPT-6 LUNA</span></div>
  <Textarea className={styles.prompt} rows={3} maxLength={1500} placeholder="Ex.: Crie um dashboard automotivo premium com 3 cartões de indicadores, gráfico ilustrativo e menu lateral, responsivo para MacBook..." value={prompt} onChange={e=>{setPrompt(e.target.value);setCandidate(null);}} aria-label="Descrição da página a gerar"/>
  <div className={styles.controls}><label className={styles.consent}><input type="checkbox" checked={consent} onChange={e=>setConsent(e.target.checked)}/><span>Autorizo esta solicitação de geração com consumo de créditos Floot.</span></label><Button onClick={generate} disabled={loading||!consent||prompt.trim().length<12}><WandSparkles size={16}/>{loading?"Gerando…":"Gerar com IA"}</Button></div>
  <div className={styles.disclaimer}><ShieldCheck size={14}/> A IA não recebe o código atual, não altera o banco automaticamente e não publica aplicativos. Limite de 3 solicitações/dia, restrito à conta autorizada.</div>
  {error&&<div role="alert" className={styles.error}>{error}</div>}
  {candidate&&<div className={styles.result}><div className={styles.resultHeader}><div><CheckCircle2 size={18}/><strong>Proposta gerada para {projectName}</strong></div><div className={styles.resultActions}><button onClick={()=>setShowPreview(v=>!v)}><Eye size={14}/>{showPreview?"Ocultar prévia":"Mostrar prévia"}</button><button className={styles.discard} onClick={()=>setCandidate(null)}><X size={14}/>Descartar</button></div></div>
   {showPreview?<iframe title="Prévia isolada da proposta IA" srcDoc={preview} sandbox="allow-scripts" className={styles.preview}/>:<div className={styles.codeSummary}><Code2 size={18}/> 3 arquivos gerados: index.html · style.css · script.js</div>}
   <div className={styles.resultFoot}><span><Coins size={14}/> Créditos desta geração: <strong>{credits??"—"}</strong> {remaining!==null?"· Restantes hoje: "+remaining:""}</span><Button onClick={apply}><CheckCircle2 size={16}/>Aplicar no editor</Button></div>
   <small className={styles.note}>Após aplicar, confira a página no Preview e clique em <b>Salvar</b>. Nada é salvo ou publicado automaticamente.</small>
  </div>}
 </section>;
}
