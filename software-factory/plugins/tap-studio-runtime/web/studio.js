'use strict';
const $ = (id) => document.getElementById(id);
let token = '', projects = [], activeId = null, activeFiles = {}, selectedFile = null;
async function api(path, options = {}) {
  const headers = {...(options.headers || {}), ...(token ? {Authorization:'Bearer '+token} : {})};
  if (options.body && typeof options.body === 'object' && !(options.body instanceof Blob)) {
    headers['Content-Type'] = 'application/json'; options.body = JSON.stringify(options.body);
  }
  const resp = await fetch(path,{...options, headers, cache:'no-store'});
  if (!resp.ok) { let error; try {error = (await resp.json()).detail;} catch {error = `Erro HTTP ${resp.status}`;} throw Error(typeof error === 'string' ? error : 'Falha na solicitação'); }
  return resp;
}
function alertText(msg) { $('toast').textContent = msg; }
function display(el, yes) { el.classList.toggle('hidden',!yes); }
function showProject(p) { activeId = p.id; $('projectTitle').textContent=p.name; $('projectDescription').textContent=p.description||'Projeto web'; display($('emptyState'),false); display($('editorShell'),true);display($('previewShell'),false);$('download').disabled=false;$('showPreview').disabled=false; document.querySelectorAll('.project-item').forEach(el=>el.classList.toggle('active',el.dataset.id===p.id)); loadFiles(); }
async function loadProjects() {
  projects = await (await api('/api/projects')).json(); const list=$('projectsList'); list.replaceChildren();
  for(const p of projects) {const btn=document.createElement('button'); btn.className='project-item'; btn.dataset.id=p.id; const strong=document.createElement('strong');strong.textContent=p.name;const small=document.createElement('small');small.textContent=new Date(p.created_at*1000).toLocaleDateString('pt-BR');btn.append(strong,small);btn.addEventListener('click',()=>showProject(p));list.append(btn);}
  if(activeId){const current=projects.find(p=>p.id===activeId);if(current){document.querySelectorAll('.project-item').forEach(el=>el.classList.toggle('active',el.dataset.id===activeId));}else activeId=null;}
}
async function loadFiles() {
  if(!activeId)return;activeFiles=await (await api(`/api/projects/${activeId}/files`)).json();selectedFile=Object.hasOwn(activeFiles,selectedFile)?selectedFile:Object.keys(activeFiles)[0]; const div=$('fileList');div.replaceChildren();
  for(const name of Object.keys(activeFiles)){let btn=document.createElement('button');btn.textContent=name;btn.className='file-item'+(name===selectedFile?' active':'');btn.onclick=()=>selectFile(name);div.append(btn);}
  selectFile(selectedFile);
}
function selectFile(name){selectedFile=name;$('fileName').textContent=name;$('codeEditor').value=activeFiles[name]||'';document.querySelectorAll('.file-item').forEach(el=>el.classList.toggle('active',el.textContent===name));}
function previewDoc(files) {
  let doc=files['index.html']||'<!doctype html><html><body><h1>Prévia vazia</h1></body></html>';
  const prefix=`<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; connect-src 'none'">`;
  const escapedStyle=(files['style.css']||'').replace(/<\/style/gi,'<\\/style');
  const escapedScript=(files['app.js']||'').replace(/<\/script/gi,'<\\/script');
  if (/<head[^>]*>/i.test(doc)) doc=doc.replace(/(<head[^>]*>)/i,`$1${prefix}<style>${escapedStyle}</style>`); else doc=`<head>${prefix}<style>${escapedStyle}</style></head>`+doc;
  doc=doc.replace(/<\/body>/i,`<script>${escapedScript}<\/script></body>`);
  return doc;
}
$('loginForm').addEventListener('submit',async(ev)=>{ev.preventDefault();$('loginError').textContent='';try{const response=await api('/api/login',{method:'POST',body:{username:$('username').value,password:$('password').value}});token=(await response.json()).access_token;$('password').value='';display($('loginScreen'),false);display($('studioScreen'),true);await loadProjects();}catch(e){$('loginError').textContent=e.message;}});
function openNew(){$('newDialog').showModal();$('newName').focus();}
$('newProject').onclick=openNew;$('emptyCreate').onclick=openNew;$('cancelCreate').onclick=()=>$('newDialog').close();
$('createForm').addEventListener('submit',async(ev)=>{ev.preventDefault();try{const response=await api('/api/projects',{method:'POST',body:{name:$('newName').value,description:$('newDescription').value}});const {id}=await response.json();$('newDialog').close();$('createForm').reset();await loadProjects();showProject(projects.find(p=>p.id===id));alertText('Projeto criado. Estrutura inicial pronta.');}catch(e){alertText(e.message);}});
$('saveFile').onclick=async()=>{if(!activeId||!selectedFile)return;try{await api(`/api/projects/${activeId}/files`,{method:'PUT',body:{path:selectedFile,content:$('codeEditor').value}});activeFiles[selectedFile]=$('codeEditor').value;alertText('Arquivo salvo.');}catch(e){alertText(e.message);}};
$('showPreview').onclick=()=>{if(!activeId)return;display($('editorShell'),false);display($('previewShell'),true);$('previewFrame').srcdoc=previewDoc(activeFiles);alertText('Prévia em iframe isolado; alterações não salvas não aparecem.');};
$('closePreview').onclick=()=>{display($('previewShell'),false);display($('editorShell'),true);};
$('download').onclick=async()=>{if(!activeId)return;try{const r=await api(`/api/projects/${activeId}/export`);const blob=await r.blob();const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`tap-project-${activeId}.zip`;a.click();URL.revokeObjectURL(url);alertText('Exportação concluída.');}catch(e){alertText(e.message);}};
$('logout').onclick=async()=>{try{await api('/api/logout',{method:'POST'});}catch{}token='';activeId=null;projects=[];activeFiles={};display($('studioScreen'),false);display($('loginScreen'),true);alertText('');};

$('generateWithAI').onclick=async()=>{if(!$('allowExternalModel').checked){alertText('Marque o consentimento explícito antes de usar IA externa.');return;}const name=$('newName').value.trim();if(name.length<3){alertText('Informe um nome com ao menos três caracteres.');return;}const button=$('generateWithAI');button.disabled=true;try{const resp=await api('/api/projects/ai-generate',{method:'POST',body:{name,description:$('newDescription').value,consent_external_model:true}});const {id}=await resp.json();$('newDialog').close();$('createForm').reset();await loadProjects();showProject(projects.find(p=>p.id===id));alertText('IA gerou uma estrutura inicial. Revise o código antes de publicar.');}catch(e){alertText(e.message);}finally{button.disabled=false;}};
