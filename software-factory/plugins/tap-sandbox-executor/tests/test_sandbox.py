import importlib.util
import os
from pathlib import Path
import tempfile
from unittest import TestCase, mock

modfile=Path(__file__).resolve().parents[1]/"server"/"sandbox_mcp.py"
spec=importlib.util.spec_from_file_location("sandbox_mcp",modfile)
sandbox=importlib.util.module_from_spec(spec)
spec.loader.exec_module(sandbox)

class TestSandbox(TestCase):
    def test_disabled(self):
        with mock.patch.dict(os.environ,{},clear=True):
            with self.assertRaises(sandbox.SandboxError): sandbox.run_tests()
    def test_mount_option_injection(self):
        with mock.patch.dict(os.environ,{"TAP_SANDBOX_PROJECT_ROOT":"/tmp/root,readonly=false","TAP_SANDBOX_IMAGE":"python@sha256:"+"a"*64},clear=True):
            with self.assertRaises(sandbox.SandboxError): sandbox.config()
    def test_require_image_digest(self):
        with tempfile.TemporaryDirectory() as root:
            with mock.patch.dict(os.environ,{"TAP_SANDBOX_PROJECT_ROOT":root,"TAP_SANDBOX_IMAGE":"python:latest"},clear=True):
                with self.assertRaises(sandbox.SandboxError): sandbox.config()
    def test_valid_digest(self):
        with tempfile.TemporaryDirectory() as root:
            with mock.patch.dict(os.environ,{"TAP_SANDBOX_PROJECT_ROOT":root,"TAP_SANDBOX_IMAGE":"python@sha256:"+"a"*64},clear=True):
                p,image=sandbox.config(); self.assertEqual(p,Path(root))
    def test_no_tests(self):
        with tempfile.TemporaryDirectory() as root:
            e={"TAP_SANDBOX_PROJECT_ROOT":root,"TAP_SANDBOX_IMAGE":"python@sha256:"+"a"*64,"TAP_SANDBOX_ALLOW_RUN":"1"}
            with mock.patch.dict(os.environ,e,clear=True):
                with self.assertRaises(sandbox.SandboxError): sandbox.run_tests()
    def test_fixed_command(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root)/"tests").mkdir()
            e={"TAP_SANDBOX_PROJECT_ROOT":root,"TAP_SANDBOX_IMAGE":"python@sha256:"+"a"*64,"TAP_SANDBOX_ALLOW_RUN":"1"}
            with mock.patch.dict(os.environ,e,clear=True),mock.patch.object(sandbox.subprocess,"run",return_value=mock.Mock(returncode=0,stdout="ok",stderr="")) as mocked:
                result=sandbox.run_tests(); self.assertTrue(result["passed"])
                argv=mocked.call_args.args[0]
                for token in ("--network=none","--read-only","--cap-drop=ALL","--pull=never"):
                    self.assertIn(token,argv)
                self.assertNotIn("-c",argv)
    def test_rpc_tools(self):
        r=sandbox.rpc({"jsonrpc":"2.0","id":1,"method":"tools/list"})
        self.assertEqual(len(r["result"]["tools"]),2)
    def test_rpc_refuse_unknown(self):
        r=sandbox.rpc({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"exec","arguments":{}}})
        self.assertTrue(r["result"]["isError"])
