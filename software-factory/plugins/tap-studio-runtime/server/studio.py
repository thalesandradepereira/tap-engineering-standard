"""TAP Studio Runtime: self-hostable single-host software workspace.

Limits: private beta, SQLite persistent volume, password login, HTTP MCP prototype.
Not a cloud agent executor or a ChatGPT OAuth integration until configured.
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
import hmac
import html
import io
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import threading
import time
from typing import Any
import zipfile
from urllib.parse import urlsplit
import ipaddress
import httpx

from fastapi import FastAPI, Header, HTTPException, Request, Response, Depends
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

HERE = Path(__file__).resolve().parent.parent
WEB = HERE / 'web'
NAME_RE = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._/-]{0,119}$')
LOGIN_RE = re.compile(r'^[a-zA-Z0-9_-]{3,40}$')
ALLOWED = {'.html', '.css', '.js', '.json', '.md', '.txt', '.svg'}
MAX_FILE_BYTES = 100_000
MAX_FILES = 30
SESSION_SECONDS = 8 * 60 * 60

class LoginIn(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    password: str = Field(min_length=1, max_length=256)

class ProjectIn(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    description: str = Field(default='', max_length=2000)

class AIIn(ProjectIn):
    consent_external_model: bool = False

class FileIn(BaseModel):
    path: str = Field(min_length=1, max_length=120)
    content: str = Field(max_length=100_000)


def check_path(path: str) -> str:
    if (not NAME_RE.fullmatch(path) or path.startswith('.') or '//' in path
        or any(s in {'.', '..'} or s.startswith('.') for s in path.split('/'))
        or path.split('/')[-1] in {'id_rsa', 'credentials.json'}
        or Path(path).suffix.lower() not in ALLOWED):
        raise ValueError('invalid or sensitive file path')
    return path


def validate_ai_files(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or not {'index.html','style.css','app.js'}.issubset(value) or len(value) > MAX_FILES:
        raise ValueError('AI output must include index.html, style.css and app.js')
    result={}
    for path,content in value.items():
        check_path(path)
        if not isinstance(content,str) or len(content.encode('utf-8')) > MAX_FILE_BYTES:
            raise ValueError('Invalid AI file content or oversized file')
        result[path]=content
    return result


def model_config():
    endpoint=os.environ.get('TAP_STUDIO_MODEL_ENDPOINT','')
    secret=os.environ.get('TAP_STUDIO_MODEL_KEY','')
    name=os.environ.get('TAP_STUDIO_MODEL_NAME','')
    allowed=os.environ.get('TAP_STUDIO_ALLOWED_MODEL_HOSTS','')
    if not all((endpoint,secret,name,allowed)):
        return None
    u=urlsplit(endpoint)
    hosts={x.strip().lower() for x in allowed.split(',') if x.strip()}
    if u.scheme!='https' or u.port not in (None,443) or u.username or u.password or u.query or u.fragment:
        raise ValueError('AI model endpoint must be an approved HTTPS URL')
    host=(u.hostname or '').lower()
    if host not in hosts or host in {'localhost','metadata.google.internal'} or not u.path.endswith('/chat/completions'):
        raise ValueError('AI model endpoint must match an explicitly allowed host and path')
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError('IP literal model endpoints are forbidden')
    return {'endpoint':endpoint,'secret':secret,'model':name}


async def call_model(settings: dict, name: str, description: str) -> dict[str,str]:
    system = ('Generate a small, accessible static web prototype. Reply ONLY with JSON '
              '{"files":{"index.html":"...","style.css":"...","app.js":"..."}}. '
              'No external dependencies, secret keys, network calls, credentials or telemetry. '
              'Never claim backend or deployment exists. This code requires human review.')
    async with httpx.AsyncClient(timeout=35.0, follow_redirects=False) as client:
        resp=await client.post(settings['endpoint'],headers={'Authorization':'Bearer '+settings['secret']},json={
            'model':settings['model'],
            'messages':[{'role':'system','content':system},{'role':'user','content':'Name: '+name+'\nRequirements: '+description}],
            'response_format':{'type':'json_object'},'max_tokens':2500,'temperature':0.2
        })
        resp.raise_for_status()
        if len(resp.content)>500000:raise ValueError('Model response too large')
        data=resp.json()
    answer=data['choices'][0]['message']['content']
    files=json.loads(answer)['files']
    return validate_ai_files(files)


def password_hash(pw: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', pw.encode('utf-8'), salt, 310_000)
    return salt.hex() + ':' + digest.hex()


def password_matches(pw: str, encoded: str) -> bool:
    try:
        salt_hex, expected = encoded.split(':', 1)
        actual = password_hash(pw, bytes.fromhex(salt_hex)).split(':')[1]
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


class Store:
    def __init__(self, path: str):
        if path == ':memory:':
            raise ValueError('sqlite database must have a durable path')
        self.path = path
        self.setup()

    @contextmanager
    def connect(self):
        con = sqlite3.connect(self.path, timeout=5)
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA foreign_keys=ON')
        con.execute('PRAGMA busy_timeout=5000')
        try:
            with con:
                yield con
        finally:
            con.close()

    def setup(self):
        with self.connect() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS sessions (
                    token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL,
                    expires_at INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
                CREATE TABLE IF NOT EXISTS projects (
                    id TEXT PRIMARY KEY, user_id INTEGER NOT NULL, name TEXT NOT NULL,
                    description TEXT NOT NULL, created_at INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
                CREATE TABLE IF NOT EXISTS files (
                    project_id TEXT NOT NULL, path TEXT NOT NULL, content TEXT NOT NULL,
                    PRIMARY KEY(project_id,path),
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE);
            ''')

    def create_user(self, username: str, password: str):
        if not LOGIN_RE.fullmatch(username) or len(password) < 12:
            raise ValueError('invalid username or password length')
        with self.connect() as db:
            db.execute('INSERT INTO users (username,password_hash) VALUES (?,?)',
                       (username, password_hash(password)))

    def ensure_admin(self, username: str, password: str):
        with self.connect() as db:
            result = db.execute('SELECT id FROM users LIMIT 1').fetchone()
        if not result:
            self.create_user(username,password)

    def login(self, user: str, password: str) -> str | None:
        with self.connect() as db:
            row = db.execute('SELECT * FROM users WHERE username=?', (user,)).fetchone()
            if not row or not password_matches(password,row['password_hash']):
                return None
            token = secrets.token_urlsafe(32)
            db.execute('INSERT INTO sessions VALUES (?,?,?)',
                       (hashlib.sha256(token.encode()).hexdigest(),row['id'],int(time.time())+SESSION_SECONDS))
            return token

    def user_id(self, token: str) -> int | None:
        if len(token) > 256 or len(token) < 30:
            return None
        digest = hashlib.sha256(token.encode()).hexdigest()
        with self.connect() as db:
            row = db.execute('SELECT user_id FROM sessions WHERE token_hash=? AND expires_at > ?',
                             (digest, int(time.time()))).fetchone()
            return row['user_id'] if row else None

    def logout(self, token: str):
        with self.connect() as db:
            db.execute('DELETE FROM sessions WHERE token_hash=?', (hashlib.sha256(token.encode()).hexdigest(),))

    def projects(self, user_id: int):
        with self.connect() as db:
            return [dict(row) for row in db.execute(
                'SELECT id,name,description,created_at FROM projects WHERE user_id=? ORDER BY created_at DESC',
                (user_id,)).fetchall()]

    def owned(self, user_id: int, project_id: str) -> bool:
        with self.connect() as db:
            return bool(db.execute('SELECT 1 FROM projects WHERE id=? AND user_id=?',(project_id,user_id)).fetchone())

    def create_project(self, user_id: int, name: str, description: str, ai_files: dict | None = None):
        project_id = secrets.token_hex(12)
        hname=html.escape(name.strip())
        hdesc=html.escape(description.strip())
        files = {
            'index.html': '<!doctype html>\n<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+hname+'</title></head><body><main class="app"><span class="eyebrow">TAP Creative Lab</span><h1>'+hname+'</h1><p>'+hdesc+'</p><button id="start">Começar</button><p id="result" aria-live="polite"></p></main></body></html>\n',
            'style.css': '*,*::before,*::after{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;background:#081a21;color:#f3f2ea;font:16px system-ui,sans-serif}.app{max-width:640px;padding:44px}.eyebrow{color:#d7b878;letter-spacing:.24em;text-transform:uppercase;font-size:12px}h1{font-size:clamp(30px,6vw,64px);line-height:1.06}p{line-height:1.65;color:#bbccd0}button{background:#d7b878;border:0;border-radius:9px;padding:14px 24px;cursor:pointer;font-weight:700}\n',
            'app.js': 'document.querySelector("#start").addEventListener("click",()=>{document.querySelector("#result").textContent="Seu projeto está pronto para evoluir!";});\n',
            'README.md': '# '+name.strip()+'\n\n'+description.strip()+'\n\nProtótipo web estático. Ainda não inclui backend, login nem modelo de IA.\n',
        }
        if ai_files is not None:
            files=validate_ai_files(ai_files)
        with self.connect() as db:
            db.execute('INSERT INTO projects VALUES (?,?,?,?,?)',
                       (project_id,user_id,name.strip(),description.strip(),int(time.time())))
            db.executemany('INSERT INTO files VALUES (?,?,?)',
                           [(project_id,p,content) for p,content in files.items()])
        return project_id

    def files(self, user_id: int, pid: str) -> dict[str,str] | None:
        with self.connect() as db:
            row=db.execute('SELECT id FROM projects WHERE id=? AND user_id=?',(pid,user_id)).fetchone()
            if not row:return None
            return {r['path']:r['content'] for r in db.execute('SELECT path,content FROM files WHERE project_id=? ORDER BY path',(pid,))}

    def write(self, user_id: int, pid: str, path: str, content: str) -> bool:
        check_path(path)
        if len(content.encode('utf-8')) > MAX_FILE_BYTES:
            raise ValueError('file too large')
        with self.connect() as db:
            if not db.execute('SELECT 1 FROM projects WHERE id=? AND user_id=?',(pid,user_id)).fetchone():
                return False
            count=db.execute('SELECT count(*) AS n FROM files WHERE project_id=?',(pid,)).fetchone()['n']
            exists=db.execute('SELECT 1 FROM files WHERE project_id=? AND path=?',(pid,path)).fetchone()
            if count >= MAX_FILES and not exists:
                raise ValueError('project file limit reached')
            db.execute('INSERT INTO files VALUES (?,?,?) ON CONFLICT(project_id,path) DO UPDATE SET content=excluded.content',
                       (pid,path,content))
        return True


MCP_TOOLS = [
    {'name':'tap_list_projects','description':'List projects owned by the authenticated account.',
     'inputSchema':{'type':'object','properties':{},'additionalProperties':False}},
    {'name':'tap_create_project','description':'Create a deterministic starter web application, no AI call or deployment.',
     'inputSchema':{'type':'object','properties':{'name':{'type':'string'},'description':{'type':'string'}},'required':['name'],'additionalProperties':False}},
    {'name':'tap_read_project_files','description':'Read project files for the authenticated account.',
     'inputSchema':{'type':'object','properties':{'project_id':{'type':'string'}},'required':['project_id'],'additionalProperties':False}},
    {'name':'tap_write_project_file','description':'Update text file in an owned project; does not execute or publish it.',
     'inputSchema':{'type':'object','properties':{'project_id':{'type':'string'},'path':{'type':'string'},'content':{'type':'string'}},'required':['project_id','path','content'],'additionalProperties':False}},
]


def create_app(db_path: str, bootstrap_user: str | None = None,
               bootstrap_password: str | None = None) -> FastAPI:
    app=FastAPI(title='TAP Studio Runtime',docs_url=None,redoc_url=None,openapi_url=None)
    store=Store(db_path)
    app.state.store=store
    if bootstrap_user and bootstrap_password:
        store.ensure_admin(bootstrap_user,bootstrap_password)
    limiter:dict[str,list[float]]={}
    ai_limiter:dict[int,list[float]]={}
    limiter_lock=threading.Lock()

    @app.middleware('http')
    async def secure_headers(request:Request, call_next):
        resp=await call_next(request)
        resp.headers['X-Content-Type-Options']='nosniff'
        resp.headers['Referrer-Policy']='no-referrer'
        resp.headers['X-Frame-Options']='DENY'
        resp.headers['Cache-Control']='no-store'
        resp.headers['Content-Security-Policy']="default-src 'none'; connect-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'self'; frame-src 'self'"
        return resp

    def auth(authorization: str | None = Header(default=None)) -> tuple[int,str]:
        if not authorization or not authorization.startswith('Bearer '):
            raise HTTPException(401,'Authentication required',headers={'WWW-Authenticate':'Bearer'})
        token=authorization[7:]
        uid=store.user_id(token)
        if uid is None:
            raise HTTPException(401,'Invalid or expired session',headers={'WWW-Authenticate':'Bearer'})
        return uid,token

    def files_or_404(uid,pid):
        result=store.files(uid,pid)
        if result is None:raise HTTPException(404,'Project not found')
        return result

    @app.get('/health')
    def health():return {'status':'ok','service':'tap-studio-runtime','runtime':'self-hosted'}

    @app.get('/')
    def index():return FileResponse(WEB / 'index.html',media_type='text/html')

    @app.get('/studio.css')
    def css():return FileResponse(WEB / 'studio.css',media_type='text/css')

    @app.get('/studio.js')
    def js():return FileResponse(WEB / 'studio.js',media_type='text/javascript')

    @app.post('/api/login')
    def login(item:LoginIn,request:Request):
        ip=request.client.host if request.client else 'unknown'
        now=time.monotonic()
        with limiter_lock:
            attempts=[x for x in limiter.get(ip,[]) if now-x < 60]
            if len(attempts)>=10:raise HTTPException(429,'Too many login attempts')
            attempts.append(now);limiter[ip]=attempts
        token=store.login(item.username,item.password)
        if token is None:raise HTTPException(401,'Invalid login')
        with limiter_lock:limiter.pop(ip,None)
        return {'access_token':token,'token_type':'bearer','expires_in':SESSION_SECONDS}

    @app.post('/api/logout')
    def logout(user=Depends(auth)):
        store.logout(user[1]);return {'ok':True}

    @app.get('/api/projects')
    def list_projects(user=Depends(auth)):return store.projects(user[0])

    @app.post('/api/projects',status_code=201)
    def create_project(p:ProjectIn,user=Depends(auth)):
        if not p.name.strip():raise HTTPException(400,'Project name is required')
        if len(store.projects(user[0])) >= 100:raise HTTPException(409,'Project limit reached')
        pid=store.create_project(user[0],p.name,p.description)
        return {'id':pid,'status':'scaffolded','ai_generated':False,'deployed':False}

    @app.post('/api/projects/ai-generate',status_code=201)
    async def ai_generate(item:AIIn,user=Depends(auth)):
        if not item.consent_external_model:
            raise HTTPException(400,'Explicit consent is required to send this description to an external AI model')
        settings=model_config()
        if settings is None:
            raise HTTPException(503,'AI model provider not configured; deterministic scaffolding is available')
        if len(store.projects(user[0])) >= 100:
            raise HTTPException(409,'Project limit reached')
        now=time.monotonic()
        with limiter_lock:
            attempts=[x for x in ai_limiter.get(user[0],[]) if now-x<60]
            if len(attempts)>=2:raise HTTPException(429,'AI limit: two requests per minute')
            attempts.append(now);ai_limiter[user[0]]=attempts
        try:
            files=await call_model(settings,item.name,item.description)
            pid=store.create_project(user[0],item.name,item.description,ai_files=files)
        except (httpx.HTTPError,ValueError,KeyError,IndexError,TypeError,json.JSONDecodeError):
            raise HTTPException(502,'AI provider did not return a valid project') from None
        return {'id':pid,'status':'generated','ai_generated':True,'deployed':False,'review_required':True}

    @app.get('/api/projects/{project_id}/files')
    def list_files(project_id:str,user=Depends(auth)):return files_or_404(user[0],project_id)

    @app.put('/api/projects/{project_id}/files')
    def write_file(project_id:str,p:FileIn,user=Depends(auth)):
        try:
            ok=store.write(user[0],project_id,p.path,p.content)
        except ValueError as e:raise HTTPException(400,str(e)) from e
        if not ok:raise HTTPException(404,'Project not found')
        return {'ok':True,'path':p.path,'executed':False,'deployed':False}

    @app.get('/api/projects/{project_id}/export')
    def export_project(project_id:str,user=Depends(auth)):
        files=files_or_404(user[0],project_id)
        mem=io.BytesIO()
        with zipfile.ZipFile(mem,'w',compression=zipfile.ZIP_DEFLATED) as archive:
            for path,content in files.items():archive.writestr(path,content)
        mem.seek(0)
        return StreamingResponse(mem,media_type='application/zip',headers={'Content-Disposition':f'attachment; filename="tap-project-{project_id}.zip"'})

    @app.post('/mcp')
    async def mcp(request:Request,user=Depends(auth)):
        if (request.headers.get('content-length') and int(request.headers['content-length'])>150000):
            raise HTTPException(413,'Request too large')
        try:data=await request.json()
        except Exception as e:raise HTTPException(400,'Invalid JSON') from e
        if not isinstance(data,dict):raise HTTPException(400,'Expected MCP JSON-RPC object')
        method=data.get('method')
        if 'id' not in data:
            if method=='notifications/initialized':return Response(status_code=202)
            raise HTTPException(400,'Unsupported notification')
        rid=data['id']
        if method=='initialize':
            result={'protocolVersion':'2025-11-25','capabilities':{'tools':{}},'serverInfo':{'name':'tap-studio-runtime','version':'0.1.0'}}
        elif method=='ping':result={}
        elif method=='tools/list':result={'tools':MCP_TOOLS}
        elif method=='tools/call':
            params=data.get('params') or {}
            name=params.get('name');args=params.get('arguments') or {}
            value=None;error=False
            try:
                if not isinstance(args,dict):raise ValueError('Invalid arguments')
                if name=='tap_list_projects' and not args:
                    value=store.projects(user[0])
                elif name=='tap_create_project' and set(args)<={'name','description'}:
                    p=ProjectIn.model_validate(args)
                    pid=store.create_project(user[0],p.name,p.description)
                    value={'id':pid,'ai_generated':False,'deployed':False}
                elif name=='tap_read_project_files' and set(args)=={'project_id'}:
                    value=files_or_404(user[0],args['project_id'])
                elif name=='tap_write_project_file' and set(args)=={'project_id','path','content'}:
                    p=FileIn.model_validate(args)
                    if not store.write(user[0],args['project_id'],p.path,p.content):raise ValueError('Project not found')
                    value={'saved':True,'deployed':False}
                else:raise ValueError('Unknown tool or incorrect arguments')
            except Exception:
                error=True;value={'error':'Tool rejected: check authorization and validated input'}
            result={'content':[{'type':'text','text':json.dumps(value,ensure_ascii=False)}],'isError':error}
        else:
            return {'jsonrpc':'2.0','id':rid,'error':{'code':-32601,'message':'Method not found'}}
        return {'jsonrpc':'2.0','id':rid,'result':result}

    return app


def main():
    import uvicorn
    db_path=os.environ.get('TAP_STUDIO_DB_PATH')
    if not db_path or not Path(db_path).is_absolute():
        raise RuntimeError('TAP_STUDIO_DB_PATH must be an absolute path on durable storage')
    Path(db_path).parent.mkdir(parents=True,exist_ok=True)
    user=os.environ.get('TAP_STUDIO_ADMIN_USER')
    password=os.environ.get('TAP_STUDIO_ADMIN_PASSWORD')
    if bool(user)!=bool(password):raise RuntimeError('Both bootstrap credentials are required together')
    app=create_app(db_path,bootstrap_user=user,bootstrap_password=password)
    uvicorn.run(app,host='0.0.0.0',port=int(os.environ.get('PORT','8080')),proxy_headers=False)

if __name__=='__main__':main()
