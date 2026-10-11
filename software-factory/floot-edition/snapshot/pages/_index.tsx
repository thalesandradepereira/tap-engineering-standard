import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { Layers3, Github, Network, ShieldCheck, Cloud, Plus, Code2, Monitor, Download, ExternalLink, FileCode2, Check, X, ArrowRight, TerminalSquare, CircleDot, Save, LogOut, Trash2 } from "lucide-react";
import { Button } from "../components/Button";
import { Input } from "../components/Input";
import { Textarea } from "../components/Textarea";
import { useAuth } from "../helpers/useAuth";
import { studioTemplates } from "../helpers/studioTemplates";
import { getStudioProjects } from "../endpoints/studio/projects_GET.schema";
import { postStudioCreate } from "../endpoints/studio/create_POST.schema";
import { postStudioSave } from "../endpoints/studio/save_POST.schema";
import { postStudioDelete } from "../endpoints/studio/delete_POST.schema";
import {StudioAiPanel} from "../components/StudioAiPanel";
import type {GeneratedFiles} from "../endpoints/studio/ai_generate_POST.schema";
import styles from "./_index.module.css";

type FileName = "index.html" | "style.css" | "script.js";
type Project = Awaited<ReturnType<typeof getStudioProjects>>["projects"][number];
const source = "https://github.com/thalesandradepereira/tap-engineering-standard";

export default function Index() {
 const {authState,logout}=useAuth();
 const [projects,setProjects]=useState<Project[]>([]);
 const [selected,setSelected]=useState<string|null>(null);
 const [file,setFile]=useState<FileName>("index.html");
 const [tab,setTab]=useState<"code"|"preview">("preview");
 const [showCreate,setShowCreate]=useState(false);
 const [projectName,setProjectName]=useState("");
 const [view,setView]=useState<"studio"|"about">("studio");
 const [notice,setNotice]=useState("");
 const [error,setError]=useState("");
 const [loading,setLoading]=useState(true);
 const [busy,setBusy]=useState(false);
 const [dirtyIds,setDirtyIds]=useState<string[]>([]);
 useEffect(()=>{
   if(authState.type!=="authenticated")return;
   let active=true;
   getStudioProjects().then(data=>{
     if(!active)return;
     setProjects(data.projects);
     setSelected(prev=>prev??data.projects[0]?.id??null);
     setLoading(false);
   }).catch(err=>{
     if(active){setError(err instanceof Error?err.message:"Falha ao carregar projetos");setLoading(false);}
   });
   return ()=>{active=false};
 },[authState.type]);
 const project=projects.find(p=>p.id===selected);
 function applyGenerated(files:GeneratedFiles){
   if(!selected)return;
   setProjects(prev=>prev.map(p=>p.id===selected?{...p,files:{...files}}:p));
   setDirtyIds(ids=>ids.includes(selected)?ids:[...ids,selected]);
   setTab("preview");
   setNotice("Código da IA aplicado ao editor. Revise e clique em Salvar para persistir.");
 }
 const dirty=Boolean(selected&&dirtyIds.includes(selected));
 const modify=(v:string)=>{
   setProjects(prev=>prev.map(p=>p.id===selected?{...p,files:{...p.files,[file]:v}}:p));
   if(selected)setDirtyIds(ids=>ids.includes(selected)?ids:[...ids,selected]);
 };
 const preview=project?studioTemplates.makePreview(project.files["index.html"],project.files["style.css"],project.files["script.js"],true):"";
 async function create(){
   const name=projectName.trim();
   if(name.length<2)return;
   setBusy(true);setError("");
   try{
     const result=await postStudioCreate({name,description:"Novo projeto TAP"});
     setProjects(p=>[result.project,...p]);
     setSelected(result.project.id);setProjectName("");setShowCreate(false);setTab("code");
     setNotice("Projeto criado e persistido no Floot.");
   }catch(err){setError(err instanceof Error?err.message:"Falha ao criar");}
   finally{setBusy(false);}
 }
 async function save(){
   if(!project)return;setBusy(true);setError("");
   try{
     const response=await postStudioSave({id:project.id,files:project.files});
     setProjects(p=>p.map(x=>x.id===response.project.id?response.project:x));
     setDirtyIds(ids=>ids.filter(x=>x!==project.id));setNotice("Arquivos salvos no banco de dados.");
   }catch(err){setError(err instanceof Error?err.message:"Falha ao salvar");}
   finally{setBusy(false);}
 }
 async function remove(){
   if(!project || !window.confirm("Excluir permanentemente este projeto? Esta operação não tem desfazer."))return;
   setBusy(true);setError("");
   try{await postStudioDelete({id:project.id});
     const rest=projects.filter(x=>x.id!==project.id);
     setProjects(rest);setSelected(rest[0]?.id??null);setDirtyIds(ids=>ids.filter(x=>x!==project.id));setNotice("Projeto excluído.");
   }catch(err){setError(err instanceof Error?err.message:"Falha ao excluir");}
   finally{setBusy(false);}
 }
 function download(){
   if(!project)return;
   const text=studioTemplates.makePreview(project.files["index.html"],project.files["style.css"],project.files["script.js"]);
   const blob=new Blob([text],{type:"text/html;charset=utf-8"});
   const url=URL.createObjectURL(blob);
   const a=document.createElement("a");
   a.href=url;a.download=project.name.toLowerCase().replace(/[^a-z0-9-]+/g,"-").slice(0,45)+"-tap.html";a.click();
   setTimeout(()=>URL.revokeObjectURL(url),1000);
 }
 if(authState.type==="loading")return <div style={{padding:50,color:"#e5f4ea",background:"#0d1819",minHeight:"100vh"}}>Verificando sessão...</div>;
 if(authState.type==="unauthenticated")return <Navigate to="/login" replace/>;
 return <div className={styles.app}>
  <aside className={styles.sidebar}>
   <div className={styles.brand}><div className={styles.brandIcon}><Layers3 size={23}/></div><div><b>TAP <span>STUDIO</span></b><small>SOFTWARE FACTORY</small></div></div>
   <div className={styles.sideGroup}><span className={styles.sideCaption}>WORKSPACE</span><button className={view==="studio"?styles.navActive:styles.nav} onClick={()=>setView("studio")}><Code2 size={17}/> Editor <span className={styles.navMeta}>01</span></button><button className={view==="about"?styles.navActive:styles.nav} onClick={()=>setView("about")}><Network size={17}/> Arquitetura</button></div>
   <div className={styles.sideGroup}><span className={styles.sideCaption}>INTEGRAÇÕES</span><a className={styles.nav} href={source} target="_blank" rel="noopener noreferrer"><Github size={17}/> GitHub <ExternalLink size={13}/></a><a className={styles.nav} href={source+"/tree/main/software-factory/plugins/tap-graphify"} target="_blank" rel="noopener noreferrer"><Network size={17}/> Graphify <ExternalLink size={13}/></a></div>
   <div className={styles.sideBottom}><div className={styles.statusDot}></div><div><b>Floot · PostgreSQL</b><span>Projetos com sessão autenticada</span></div></div>
  </aside>
  <main className={styles.main}>
   <header className={styles.header}><div className={styles.breadcrumb}>WORKSPACE <span>/</span> {view==="studio"?"EDITOR":"ARQUITETURA"}</div><div className={styles.headerRight}><span className={styles.env}>● FLOOT HOSTED EDITION</span><span className={styles.avatar}>{authState.user.displayName?.slice(0,1)||"T"}</span><Button variant="ghost" size="sm" onClick={()=>logout()} title="Sair"><LogOut size={15}/></Button></div></header>
   <div className={styles.content}>
    <div className={styles.hero}><div><div className={styles.kicker}><span className={styles.kickerLine}></span> TAP ENGINEERING LAB</div><h1>{view==="studio"?"Crie. Teste. Evolua.":"Projetado para evoluir."}</h1><p>{view==="studio"?"Seu espaço para transformar ideias em aplicações, com código acessível e controle de versão.":"Código-fonte versionado no GitHub. Serviços isolados. Integrações verificáveis e sem promessas de produção."}</p></div><div className={styles.version}><span>EDIÇÃO FLOOT</span><strong>v0.1 beta</strong><small>Preview separado do Python Studio</small></div></div>
    {view==="studio"?<>
    <div className={styles.metrics}><div className={styles.metric}><span>PROJETOS</span><strong>{String(projects.length).padStart(2,"0")}</strong><small>Seu workspace privado</small></div><div className={styles.metric}><span>FRAMEWORK</span><strong>WEB</strong><small>HTML · CSS · JavaScript</small></div><div className={styles.metric}><span>VERSÃO TAP</span><strong>4.1.0</strong><small>Release do código GitHub</small></div><div className={styles.metric}><span>BACKEND</span><strong>FLOOT</strong><small>PostgreSQL e autenticação</small></div></div>
    {project&&<StudioAiPanel key={project.id} projectId={project.id} projectName={project.name} dirty={dirty} onApply={applyGenerated}/>}
    <div className={styles.sectionTop}><div><h2>Seus projetos</h2><p>Projetos editáveis. Salve o trabalho à medida que evolui.</p></div><Button onClick={()=>setShowCreate(true)}><Plus size={16}/> Novo projeto</Button></div>
    {error&&<div role="alert" style={{padding:12,marginBottom:10,border:"1px solid #a55e56",borderRadius:8,color:"#ffc3bd"}}>{error}</div>}
    <div className={styles.workgrid}><div className={styles.projList}>{loading?<p style={{padding:14}}>Carregando projetos...</p>:projects.length===0?<p style={{padding:14,color:"#a9b8b3"}}>Nenhum projeto ainda. Use <strong>Novo projeto</strong> para começar.</p>:projects.map(p=><button key={p.id} className={p.id===selected?styles.projActive:styles.proj} onClick={()=>{setSelected(p.id);setFile("index.html");}}><div className={styles.projIcon}><FileCode2 size={21}/></div><div className={styles.projBody}><b>{p.name}</b><span>{p.description}</span><small>Atualizado {new Date(p.updated_at).toLocaleDateString("pt-BR")}</small></div><ArrowRight size={16}/></button>)}<div className={styles.projFooter}><ShieldCheck size={14}/> Cada conta acessa seus próprios projetos · TAP</div></div>
     <div className={styles.editor}><div className={styles.editorHeader}><div className={styles.editorLabel}><TerminalSquare size={17}/><strong>{project?.name||"Selecione ou crie um projeto"}</strong></div><div className={styles.toolBtns}><button onClick={()=>setTab("code")} className={tab==="code"?styles.toolActive:styles.tool}><Code2 size={14}/> Código</button><button onClick={()=>setTab("preview")} className={tab==="preview"?styles.toolActive:styles.tool}><Monitor size={14}/> Preview</button></div></div><div className={styles.tabstrip}>{(["index.html","style.css","script.js"] as FileName[]).map(t=><button key={t} className={file===t?styles.fileActive:styles.file} onClick={()=>{setFile(t);setTab("code")}}><CircleDot size={11}/>{t}</button>)}</div>{tab==="code"?<Textarea aria-label="Editor de código" className={styles.codearea} value={project?.files[file]||""} disabled={!project||busy} onChange={e=>modify(e.target.value)} rows={15}/>:<iframe title="Preview isolado do código do projeto" className={styles.preview} srcDoc={preview} sandbox="allow-scripts"/>}<div className={styles.editorFoot}><span><Check size={13}/>{dirty?"Alterações não salvas":"Sincronizado com Floot PostgreSQL"}</span><div style={{display:"flex",gap:7}}><Button variant="ghost" size="sm" onClick={remove} disabled={!project||busy}><Trash2 size={14}/></Button><Button variant="outline" size="sm" onClick={download} disabled={!project}><Download size={14}/> HTML</Button><Button size="sm" onClick={save} disabled={!project||busy||!dirty}><Save size={14}/> {busy?"Salvando...":"Salvar"}</Button></div></div></div>
    </div>
    </>:<div className={styles.arch}><div><ShieldCheck size={27}/><h2>Engenharia auditável</h2><p>Atualizações controladas por Pull Requests, testes de regressão e revisão de segurança.</p></div><div><Github size={27}/><h2>GitHub como fonte</h2><p>10 plugins, 11 Skills e os releases versionados ficam no repositório oficial.</p></div><div><Cloud size={27}/><h2>Floot como hospedagem</h2><p>Esta edição web usa infraestrutura Floot; não executa o backend Python original.</p></div></div>}
    <div className={styles.footer}><span>TAP CREATIVE LAB • MADE BY TAP</span><a href={source+"/releases/tag/software-factory-v4.1.0"} target="_blank" rel="noopener noreferrer">Release oficial no GitHub ↗</a></div>
   </div>
  </main>
  {showCreate&&<div className={styles.overlay}><div className={styles.modal}><div className={styles.modalTitle}><h2>Novo projeto</h2><button onClick={()=>setShowCreate(false)} aria-label="Fechar"><X size={20}/></button></div><p>Crie uma base HTML, CSS e JavaScript para o seu aplicativo no banco Floot.</p><Input autoFocus placeholder="Nome do aplicativo" value={projectName} onChange={e=>setProjectName(e.target.value)} onKeyDown={e=>{if(e.key==="Enter")create();}}/><div className={styles.modalActions}><Button variant="outline" onClick={()=>setShowCreate(false)}>Cancelar</Button><Button onClick={create} disabled={projectName.trim().length<2||busy}>{busy?"Criando...":"Criar projeto"}</Button></div></div></div>}
  {notice&&<div className={styles.toast} role="status" onClick={()=>setNotice("")}>{notice} <X size={14}/></div>}
 </div>;
}

