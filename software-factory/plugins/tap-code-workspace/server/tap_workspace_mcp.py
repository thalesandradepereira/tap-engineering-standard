"""TAP local workspace MCP, stdio. Safe-by-default *file* tools, not a sandbox.

Python 3.11+, no third-party packages. All user-owned project source is
untrusted: this server NEVER executes it. Never use in a multi-tenant service.
"""
from __future__ import annotations
import ast
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

MAX_TEXT = 128 * 1024
EXTS = {'.py','.json','.js','.jsx','.ts','.tsx','.css','.html','.sql','.md','.txt','.yml','.yaml','.toml','.svg','.xml'}
BLOCK = {'node_modules','__pycache__','dist','build','venv','.git','.env','secrets','credentials','private'}

class WorkspaceError(Exception):
    pass

def get_root() -> Path:
    configured = os.environ.get('TAP_WORKSPACE_ROOT', '')
    if not configured or not Path(configured).is_absolute():
        raise WorkspaceError('TAP_WORKSPACE_ROOT must be an explicit absolute directory')
    root = Path(configured).resolve(strict=True)
    if not root.is_dir() or root == Path('/') or root == Path.home().resolve():
        raise WorkspaceError('Workspace root is not a dedicated project directory')
    return root

def resolve_project_file(relative: str, root: Path, *, create: bool = False) -> Path:
    if not isinstance(relative, str) or not relative or len(relative)>400 or '\\' in relative or '\x00' in relative:
        raise WorkspaceError('Invalid relative file path')
    rel = Path(relative)
    if rel.is_absolute() or any(part in ('','..','.') or part.startswith('.') or part.lower() in BLOCK for part in rel.parts):
        raise WorkspaceError('Disallowed path')
    if rel.suffix.lower() not in EXTS:
        raise WorkspaceError('File extension not permitted')
    cur = root
    for part in rel.parts:
        cur = cur/part
        if cur.is_symlink():
            raise WorkspaceError('Symbolic links not permitted')
    # Strict containment after parent-resolving to guard path escape.
    target = root/rel
    if not target.resolve(strict=False).is_relative_to(root):
        raise WorkspaceError('Path escapes workspace')
    if target.exists() and not target.is_file():
        raise WorkspaceError('Not a regular file')
    if not create and not target.is_file():
        raise WorkspaceError('File not found')
    return target

def read_text(relative: str, root: Path) -> str:
    p = resolve_project_file(relative, root)
    if p.stat().st_size > MAX_TEXT:
        raise WorkspaceError('File exceeds text size limit')
    # Open read-only with NOFOLLOW where supported to reduce symlink race.
    fd = os.open(p, os.O_RDONLY | getattr(os,'O_NOFOLLOW',0))
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise WorkspaceError('Not a regular file')
        data = os.read(fd, MAX_TEXT + 1)
    finally:
        os.close(fd)
    if len(data)>MAX_TEXT:
        raise WorkspaceError('File exceeds text size limit')
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise WorkspaceError('Not UTF-8 text') from exc

def write_text(relative: str, content: str, overwrite: bool, root: Path) -> dict:
    if os.environ.get('TAP_ALLOW_WRITES') != '1':
        raise WorkspaceError('Write disabled; host must opt in via TAP_ALLOW_WRITES=1')
    if not isinstance(content,str) or len(content.encode('utf-8'))>MAX_TEXT:
        raise WorkspaceError('Content must be UTF-8 string <= 128 KiB')
    p=resolve_project_file(relative,root,create=True)
    if p.exists() and overwrite is not True:
        raise WorkspaceError('Existing file requires explicit overwrite=true')
    if not p.parent.is_dir():
        raise WorkspaceError('Parent directory must already exist')
    # Temp write + atomic replace reduces half-written files; not multi-user secure.
    fd,tmp = tempfile.mkstemp(prefix='tap-write-',dir=p.parent)
    try:
        with os.fdopen(fd,'wb') as out:
            out.write(content.encode('utf-8'))
            out.flush()
            os.fsync(out.fileno())
        os.chmod(tmp,0o600)
        os.replace(tmp,p)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return {'path':relative,'bytes':len(content.encode('utf-8')),'status':'written'}

def list_files(root:Path, limit:int=100)->list[str]:
    if not isinstance(limit,int) or isinstance(limit,bool) or limit<1 or limit>200:
        raise WorkspaceError('Limit must be 1..200')
    paths=[]
    for dirpath,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if not d.startswith('.') and d.lower() not in BLOCK and not (Path(dirpath)/d).is_symlink())
        for name in sorted(files):
            p=Path(dirpath)/name
            if name.startswith('.') or p.is_symlink() or p.suffix.lower() not in EXTS:
                continue
            paths.append(p.relative_to(root).as_posix())
            if len(paths)>=limit:
                return paths
    return paths

def check_syntax(relative:str,root:Path)->dict:
    text=read_text(relative,root)
    suffix=Path(relative).suffix.lower()
    if suffix == '.py':
        ast.parse(text,filename=relative)
        return {'path':relative,'language':'python','valid':True,'executed':False}
    if suffix == '.json':
        json.loads(text)
        return {'path':relative,'language':'json','valid':True,'executed':False}
    raise WorkspaceError('Only Python AST and JSON parsing are supported; no code execution')

TOOL_SPECS=[
 {'name':'tap_workspace_status','description':'Show authorized project root and read/write status; never execute code.','inputSchema':{'type':'object','properties':{},'additionalProperties':False}},
 {'name':'tap_list_files','description':'List text source files under authorized project root.','inputSchema':{'type':'object','properties':{'limit':{'type':'integer','minimum':1,'maximum':200}},'additionalProperties':False}},
 {'name':'tap_read_text','description':'Read bounded UTF-8 project text, no hidden files or symlinks.','inputSchema':{'type':'object','properties':{'path':{'type':'string'}},'required':['path'],'additionalProperties':False}},
 {'name':'tap_write_text','description':'Write project text; requires TAP_ALLOW_WRITES=1, explicit overwrite for existing files.','inputSchema':{'type':'object','properties':{'path':{'type':'string'},'content':{'type':'string'},'overwrite':{'type':'boolean'}},'required':['path','content'],'additionalProperties':False}},
 {'name':'tap_check_syntax','description':'Parse Python or JSON syntax without running project code.','inputSchema':{'type':'object','properties':{'path':{'type':'string'}},'required':['path'],'additionalProperties':False}}
]

def tool_call(name:str,args:dict)->dict:
    root=get_root()
    if not isinstance(args,dict):
        raise WorkspaceError('arguments must be object')
    if name == 'tap_workspace_status':
        val={'workspace':str(root),'writes_enabled':os.environ.get('TAP_ALLOW_WRITES')=='1','code_execution':False,'mode':'local stdio only'}
    elif name == 'tap_list_files': val={'files':list_files(root,args.get('limit',100))}
    elif name == 'tap_read_text': val={'path':args['path'],'content':read_text(args['path'],root)}
    elif name == 'tap_write_text': val=write_text(args['path'],args['content'],args.get('overwrite',False),root)
    elif name == 'tap_check_syntax': val=check_syntax(args['path'],root)
    else: raise WorkspaceError('Unknown tool')
    return {'content':[{'type':'text','text':json.dumps(val,ensure_ascii=False)}],'isError':False}

def rpc(message:dict)->dict|None:
    request_id=message.get('id')
    method=message.get('method')
    if request_id is None:
        return None # notifications are not answered
    try:
        if method=='initialize':
            result={'protocolVersion':'2025-11-25','capabilities':{'tools':{'listChanged':False}},'serverInfo':{'name':'tap-code-workspace','version':'1.0.0'}}
        elif method=='ping': result={}
        elif method=='tools/list': result={'tools':TOOL_SPECS}
        elif method=='tools/call':
            params=message.get('params') or {}
            try: result=tool_call(params.get('name',''), params.get('arguments') or {})
            except (WorkspaceError,KeyError,ValueError,SyntaxError,json.JSONDecodeError) as err:
                result={'content':[{'type':'text','text':'Rejected: '+str(err)}],'isError':True}
        else: return {'jsonrpc':'2.0','id':request_id,'error':{'code':-32601,'message':'Method not found'}}
        return {'jsonrpc':'2.0','id':request_id,'result':result}
    except (TypeError,ValueError,KeyError) as err:
        return {'jsonrpc':'2.0','id':request_id,'error':{'code':-32602,'message':'Invalid params'}}

def main():
    for line in sys.stdin:
        if len(line)>300_000:
            continue
        try:
            data=json.loads(line)
            if not isinstance(data,dict):
                continue
            reply=rpc(data)
            if reply is not None:
                sys.stdout.write(json.dumps(reply,ensure_ascii=False,separators=(',',':'))+'\n')
                sys.stdout.flush()
        except (json.JSONDecodeError,TypeError,ValueError):
            continue

if __name__ == '__main__': main()
