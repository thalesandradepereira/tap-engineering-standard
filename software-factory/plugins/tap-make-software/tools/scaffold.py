#!/usr/bin/env python3
"""Create an offline-capable static demo. No network or dependencies; no overwrite."""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
import re

NAME_RE = re.compile(r"[a-z][a-z0-9-]{0,48}\Z")

CSS = r'''*{box-sizing:border-box} :root{color-scheme:dark;font-family:Inter,system-ui,-apple-system,sans-serif;background:#0c1421;color:#edf4ff}body{margin:0;min-height:100vh;background:radial-gradient(ellipse at 80% 0,#24405d 0,transparent 45%),#0c1421}.shell{max-width:1040px;margin:auto;padding:40px 22px}header{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid #33475c;padding-bottom:20px}h1{font-size:clamp(28px,5vw,44px);margin:0}h2{font-size:21px;margin:0 0 14px}.kicker{color:#72e4c7;font-size:12px;text-transform:uppercase;letter-spacing:.17em;font-weight:750}.sub{color:#a9c0d0;max-width:600px;line-height:1.65}.pill{padding:8px 12px;border:1px solid #45677c;border-radius:100px;font-size:12px;color:#c1e7ed}.panel{background:#142437;border:1px solid #30475c;padding:24px;border-radius:20px;box-shadow:0 12px 45px #0002;margin:24px 0}.entry{display:flex;flex-wrap:wrap;gap:10px}input,select,button{font:inherit;min-height:44px;border-radius:10px;border:1px solid #40576c;padding:11px 13px}input,select{background:#0a1929;color:#fff}input:focus-visible,select:focus-visible,button:focus-visible{outline:3px solid #72e4c7;outline-offset:2px}#title{flex:2;min-width:210px}button{cursor:pointer;background:#244663;color:#fff}button:hover{filter:brightness(1.17)}.primary{background:#74dec2;color:#10202a;font-weight:700;border-color:transparent}.danger{background:#382733;color:#ffd7df;border-color:#7c4e59}.toolbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}#search{flex:1;min-width:140px}#tasks{margin:0;padding:0;list-style:none}li.task{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:17px 0;border-bottom:1px solid #2b4358}li.task:last-child{border-bottom:0}.task-main{display:flex;align-items:center;gap:10px;min-width:0}.task-name{overflow-wrap:anywhere}.done .task-name{text-decoration:line-through;color:#9aafbf}.task-actions{display:flex;gap:8px;flex-wrap:wrap}.meta{display:block;font-size:12px;color:#a9c0d0;margin-top:5px}.empty{padding:30px 0;color:#a9c0d0}footer{color:#849dad;font-size:12px;text-align:center;margin:28px 0}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}@media(max-width:600px){header{align-items:flex-start;flex-direction:column}li.task{align-items:flex-start;flex-direction:column}.task-actions{align-self:flex-end}}'''
JS = r'''"use strict";
const STORAGE_KEY = "tap-make-software-demo-v1";
const $ = (id) => document.getElementById(id);
function loadTasks(){try{const value=JSON.parse(localStorage.getItem(STORAGE_KEY)||"[]");return Array.isArray(value)?value.filter(x=>x&&typeof x.id==="string"&&typeof x.title==="string"&&typeof x.done==="boolean"):[];}catch{return [];}}
let tasks = loadTasks();
function save(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(tasks));}catch{ $("status").textContent="Não foi possível gravar dados neste navegador."; }}
function normalized(s){return s.trim().toLocaleLowerCase("pt-BR");}
function render(){
 const list=$("tasks");list.replaceChildren();
 const query=normalized($("search").value);const filter=$("filter").value;
 const visible=tasks.filter(t=>normalized(t.title).includes(query)&&(filter==="all"||(filter==="done"?t.done:!t.done)));
 $("count").textContent=`${tasks.filter(t=>!t.done).length} pendentes de ${tasks.length} tarefas`;
 $("empty").hidden=visible.length>0;
 for(const task of visible){
  const li=document.createElement("li");li.className="task"+(task.done?" done":"");
  const main=document.createElement("div");main.className="task-main";
  const check=document.createElement("input");check.type="checkbox";check.checked=task.done;check.setAttribute("aria-label",`Concluir ${task.title}`);
  check.addEventListener("change",()=>{task.done=check.checked;save();render();});
  const details=document.createElement("div");
  const title=document.createElement("span");title.className="task-name";title.textContent=task.title;
  const meta=document.createElement("small");meta.className="meta";meta.textContent=task.created;
  details.append(title,meta);main.append(check,details);
  const actions=document.createElement("div");actions.className="task-actions";
  const edit=document.createElement("button");edit.type="button";edit.textContent="Editar";
  edit.setAttribute("aria-label",`Editar ${task.title}`);
  edit.addEventListener("click",()=>{const next=prompt("Edite a tarefa:",task.title);if(next===null)return;const cleaned=next.trim();if(!cleaned||cleaned.length>180){$("status").textContent="Use um título de 1 a 180 caracteres.";return;}task.title=cleaned;save();render();});
  const del=document.createElement("button");del.type="button";del.textContent="Excluir";del.className="danger";
  del.setAttribute("aria-label",`Excluir ${task.title}`);
  del.addEventListener("click",()=>{if(!confirm(`Excluir “${task.title}”?`))return;tasks=tasks.filter(t=>t.id!==task.id);save();render();});
  actions.append(edit,del);li.append(main,actions);list.append(li);
 }
}
$("new-task").addEventListener("submit", e=>{
 e.preventDefault(); const title=$("title").value.trim();
 if(!title||title.length>180){$("status").textContent="Use um título de 1 a 180 caracteres.";return;}
 tasks.unshift({id:crypto.randomUUID?crypto.randomUUID():String(Date.now())+Math.random(),title,done:false,created:new Date().toLocaleDateString("pt-BR")});
 $("title").value="";$("status").textContent="Tarefa incluída.";save();render();$("title").focus();
});
$("search").addEventListener("input",render);$("filter").addEventListener("change",render);
$("export").addEventListener("click",()=>{
 const blob=new Blob([JSON.stringify({schema_version:1,items:tasks},null,2)],{type:"application/json"});
 const url=URL.createObjectURL(blob);const link=document.createElement("a");link.href=url;link.download="tap-tarefas.json";link.click();URL.revokeObjectURL(url);
});
if("serviceWorker" in navigator && location.protocol!=="file:"){navigator.serviceWorker.register("./sw.js").catch(()=>{});}
render();'''
SW = r'''const CACHE="tap-demo-v1";const ASSETS=["./","./index.html","./style.css","./app.js","./manifest.webmanifest"];
self.addEventListener("install",event=>event.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener("activate",event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener("fetch",event=>{if(event.request.method!=="GET"||new URL(event.request.url).origin!==self.location.origin)return;event.respondWith(fetch(event.request).catch(()=>caches.match(event.request)));});'''

def generate(name: str, output: Path, template: str = "static-pwa") -> Path:
    if not NAME_RE.fullmatch(name) or "--" in name or name.endswith("-"):
        raise ValueError("Nome deve ser kebab-case seguro: a-z, 0-9, hífen, começando por letra.")
    if template != "static-pwa":
        raise ValueError("Template não implementado; disponíveis: static-pwa.")
    target = output / name
    # Refuse overwrite, including symlink targets. No deletes or network calls.
    target.mkdir(parents=True, exist_ok=False)
    label = html.escape(name.replace("-", " ").title())
    page = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0c1421"><meta name="description" content="Demonstração local de tarefas do TAP Make Software"><link rel="manifest" href="./manifest.webmanifest"><link rel="stylesheet" href="./style.css"><title>{label} · TAP Make Software</title></head><body><main class="shell"><header><div><p class="kicker">TAP Creative Lab · Software Factory</p><h1>{label}</h1><p class="sub">Organize as suas tarefas com uma interface responsiva. Os dados ficam apenas neste navegador. Sem login ou sincronização entre aparelhos.</p></div><span class="pill">DEMO · Offline</span></header><section class="panel" aria-labelledby="add-heading"><h2 id="add-heading">Nova tarefa</h2><form id="new-task" class="entry"><label class="sr-only" for="title">Descrição da tarefa</label><input id="title" name="title" placeholder="O que precisa ser feito?" maxlength="180" required autocomplete="off"><button class="primary" type="submit">Adicionar</button></form><p id="status" role="status" aria-live="polite"></p></section><section class="panel" aria-labelledby="list-heading"><h2 id="list-heading">Suas tarefas</h2><div class="toolbar"><label class="sr-only" for="search">Buscar tarefas</label><input id="search" type="search" placeholder="Buscar..." aria-label="Buscar tarefas"><label class="sr-only" for="filter">Filtrar tarefas</label><select id="filter" aria-label="Filtrar tarefas"><option value="all">Todas</option><option value="open">Pendentes</option><option value="done">Concluídas</option></select><button id="export" type="button">Exportar JSON</button></div><p id="count" class="sub"></p><ul id="tasks" aria-label="Lista de tarefas"></ul><p id="empty" class="empty" hidden>Nenhuma tarefa para este filtro.</p></section><footer>Made by TAP · Exemplo de protótipo sem autenticação ou banco cloud.</footer></main><script defer src="./app.js"></script></body></html>'''
    files = {
        "index.html": page,
        "style.css": CSS,
        "app.js": JS,
        "sw.js": SW,
        "manifest.webmanifest": json.dumps({"name": name.replace("-", " ").title(), "short_name": name[:18], "start_url": "./", "display": "standalone", "background_color": "#0c1421", "theme_color": "#0c1421"}, ensure_ascii=False, indent=2),
        "README.md": f"# {label}\n\nProtótipo demonstrativo gerado pelo TAP Make Software. Abra `index.html` em um navegador moderno para testar tarefas. Para testar Service Worker/offline, hospede em localhost via `python3 -m http.server 8000` na pasta do app. Dados em `localStorage`: não há banco, autenticação, backup remoto nem sincronização. Não armazene dados sensíveis. Pode publicar como site estático mediante autorização.\n",
    }
    for fname, body in files.items():
        (target / fname).write_text(body + "\n", encoding="utf-8")
    return target

def main():
    parser = argparse.ArgumentParser(description="TAP Make Software — scaffolder local offline")
    parser.add_argument("command", choices=["new"])
    parser.add_argument("name", help="Nome seguro em kebab-case")
    parser.add_argument("--template", default="static-pwa", choices=["static-pwa"])
    parser.add_argument("--output", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        print(generate(args.name, args.output, args.template))
    except (ValueError, FileExistsError, OSError) as exc:
        parser.exit(2, f"Erro: {exc}\n")

if __name__ == "__main__":
    main()
