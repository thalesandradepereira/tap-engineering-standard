"""TAP sandbox MCP (local stdio). Docker only, explicit opt-in, no arbitrary commands.

This is a reduced-risk test runner, NOT a multi-tenant security boundary.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import subprocess
import sys

IMAGE_RE = re.compile(r"^[a-z0-9][a-z0-9./:_-]*@sha256:[0-9a-f]{64}$")

class SandboxError(Exception):
    pass

def config():
    raw = os.environ.get("TAP_SANDBOX_PROJECT_ROOT", "")
    if not raw or not Path(raw).is_absolute():
        raise SandboxError("project root must be an explicit absolute path")
    # Reject path-string characters that could become Docker --mount option separators.
    if any(ch in raw for ch in (",", chr(10), chr(13), chr(0))) or Path(raw).is_symlink():
        raise SandboxError("unsafe project root path")
    p = Path(raw).resolve(strict=True)
    if not p.is_dir() or p == Path("/") or p == Path.home().resolve():
        raise SandboxError("use a dedicated project directory")
    if p.is_symlink():
        raise SandboxError("symlink root refused")
    image = os.environ.get("TAP_SANDBOX_IMAGE", "")
    if not IMAGE_RE.fullmatch(image):
        raise SandboxError("use reviewed immutable Docker image by sha256 digest")
    return p, image

def run_tests():
    if os.environ.get("TAP_SANDBOX_ALLOW_RUN") != "1":
        raise SandboxError("execution disabled; explicit opt-in required")
    root, image = config()
    if not (root / "tests").is_dir() or (root / "tests").is_symlink():
        raise SandboxError("tests directory missing or symlinked")
    argv = ["docker", "run", "--rm", "--pull=never", "--network=none", "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=64", "--memory=256m", "--cpus=1", "--user=65534:65534", "--tmpfs=/tmp:rw,nosuid,noexec,size=16m", "--mount", "type=bind,src=" + str(root) + ",dst=/work,readonly", "--workdir=/work", image, "python", "-B", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=75, check=False, stdin=subprocess.DEVNULL)
    except FileNotFoundError as exc:
        raise SandboxError("Docker executable not available") from exc
    except subprocess.TimeoutExpired as exc:
        raise SandboxError("Test run timed out") from exc
    return {"exit_code": proc.returncode, "passed": proc.returncode == 0, "stdout":proc.stdout[-6000:], "stderr":proc.stderr[-6000:], "profile":"python-unittest", "isolated_docker":True, "cloud":False}

TOOLS = [
  {"name":"tap_sandbox_status","description":"Read sandbox configuration status without running code.","inputSchema":{"type":"object","properties":{},"additionalProperties":False}},
  {"name":"tap_run_python_unittests","description":"Run fixed Python unittest discovery in restricted local Docker; explicit opt-in required.","inputSchema":{"type":"object","properties":{},"additionalProperties":False}}
]

def rpc(data):
    if not isinstance(data,dict) or "id" not in data:
        return None
    mid=data.get("id"); method=data.get("method"); params=data.get("params") or {}
    try:
        if method=="initialize": result={"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"tap-sandbox-executor","version":"1.0.0"}}
        elif method=="tools/list": result={"tools":TOOLS}
        elif method=="ping": result={}
        elif method=="tools/call":
            try:
                args=params.get("arguments") or {}
                if args or params.get("name") not in [x["name"] for x in TOOLS]:
                    raise SandboxError("Unknown tool or arguments")
                if params["name"]=="tap_sandbox_status":
                    val={"run_enabled":os.environ.get("TAP_SANDBOX_ALLOW_RUN")=="1", "image_configured":bool(os.environ.get("TAP_SANDBOX_IMAGE")), "project_configured":bool(os.environ.get("TAP_SANDBOX_PROJECT_ROOT")), "cloud":False}
                else: val=run_tests()
                result={"content":[{"type":"text","text":json.dumps(val,ensure_ascii=False)}],"isError":False}
            except (SandboxError,KeyError,TypeError) as err:
                result={"content":[{"type":"text","text":"Rejected: "+str(err)}],"isError":True}
        else:
            return {"jsonrpc":"2.0","id":mid,"error":{"code":-32601,"message":"Method not found"}}
        return {"jsonrpc":"2.0","id":mid,"result":result}
    except (KeyError,TypeError,ValueError):
        return {"jsonrpc":"2.0","id":mid,"error":{"code":-32602,"message":"Invalid params"}}

def main():
    for line in sys.stdin:
        if len(line)>50000: continue
        try:
            r=rpc(json.loads(line))
            if r is not None: print(json.dumps(r,ensure_ascii=False),flush=True)
        except (TypeError,ValueError,json.JSONDecodeError): continue

if __name__=="__main__": main()
