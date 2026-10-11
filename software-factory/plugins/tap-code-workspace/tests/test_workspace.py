import importlib.util, io, json, os, pathlib, subprocess, sys, tempfile, unittest
from unittest.mock import patch
SRC=pathlib.Path(__file__).resolve().parents[1]/'server'/'tap_workspace_mcp.py'
spec=importlib.util.spec_from_file_location('tap_workspace_mcp',SRC)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class TestWorkspace(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  self.root=pathlib.Path(self.temp.name)/'project';self.root.mkdir()
  (self.root/'ok.py').write_text('answer = 42\n')
  (self.root/'good.json').write_text('{"ok":true}')
  (self.root/'.env').write_text('API_KEY=dummy')
 def tearDown(self): self.temp.cleanup()
 def test_root_required(self):
  with patch.dict(os.environ,{'TAP_WORKSPACE_ROOT':''}):
   with self.assertRaises(m.WorkspaceError):m.get_root()
 def test_root_project_valid(self):
  with patch.dict(os.environ,{'TAP_WORKSPACE_ROOT':str(self.root)}):self.assertEqual(m.get_root(),self.root)
 def test_root_home_rejected(self):
  with patch.dict(os.environ,{'TAP_WORKSPACE_ROOT':str(pathlib.Path.home())}):
   with self.assertRaises(m.WorkspaceError):m.get_root()
 def test_read_text(self):self.assertEqual(m.read_text('ok.py',self.root),'answer = 42\n')
 def test_absolute_block(self):
  with self.assertRaises(m.WorkspaceError):m.read_text('/etc/passwd',self.root)
 def test_traversal_block(self):
  with self.assertRaises(m.WorkspaceError):m.read_text('../outside.py',self.root)
 def test_hidden_block(self):
  with self.assertRaises(m.WorkspaceError):m.read_text('.env',self.root)
 def test_symlink_block(self):
  (self.root/'link.py').symlink_to(self.root/'ok.py')
  with self.assertRaises(m.WorkspaceError):m.read_text('link.py',self.root)
 def test_list_excludes_secret(self):
  self.assertEqual(sorted(m.list_files(self.root)),['good.json','ok.py'])
 def test_read_size_limit(self):
  (self.root/'too.py').write_bytes(b'a'*(m.MAX_TEXT+1))
  with self.assertRaises(m.WorkspaceError):m.read_text('too.py',self.root)
 def test_write_denied_default(self):
  with patch.dict(os.environ,{'TAP_ALLOW_WRITES':'0'}):
   with self.assertRaises(m.WorkspaceError):m.write_text('a.py','x=1',False,self.root)
 def test_write_new_when_enabled(self):
  with patch.dict(os.environ,{'TAP_ALLOW_WRITES':'1'}):
   self.assertEqual(m.write_text('a.py','x=1',False,self.root)['status'],'written')
  self.assertEqual((self.root/'a.py').read_text(),'x=1')
 def test_write_existing_requires_overwrite(self):
  with patch.dict(os.environ,{'TAP_ALLOW_WRITES':'1'}):
   with self.assertRaises(m.WorkspaceError):m.write_text('ok.py','x=2',False,self.root)
   m.write_text('ok.py','x=2',True,self.root)
  self.assertEqual(m.read_text('ok.py',self.root),'x=2')
 def test_write_missing_parent_rejected(self):
  with patch.dict(os.environ,{'TAP_ALLOW_WRITES':'1'}):
   with self.assertRaises(m.WorkspaceError):m.write_text('missing/new.py','hi',False,self.root)
 def test_write_symlink_parent_rejected(self):
  (self.root/'linkdir').symlink_to(self.root, target_is_directory=True)
  with patch.dict(os.environ,{'TAP_ALLOW_WRITES':'1'}):
   with self.assertRaises(m.WorkspaceError):m.write_text('linkdir/new.py','hi',False,self.root)
 def test_python_syntax_parse(self):self.assertTrue(m.check_syntax('ok.py',self.root)['valid'])
 def test_json_parse(self):self.assertTrue(m.check_syntax('good.json',self.root)['valid'])
 def test_invalid_python(self):
  (self.root/'bad.py').write_text('def :-')
  with self.assertRaises(SyntaxError):m.check_syntax('bad.py',self.root)
 def test_unsupported_check_language(self):
  (self.root/'bad.js').write_text('const x =')
  with self.assertRaises(m.WorkspaceError):m.check_syntax('bad.js',self.root)
 def test_rpc_initialize(self):
  x=m.rpc({'jsonrpc':'2.0','id':1,'method':'initialize','params':{}})
  self.assertEqual(x['result']['serverInfo']['name'],'tap-code-workspace')
 def test_rpc_tools(self):
  self.assertEqual(len(m.rpc({'jsonrpc':'2.0','id':2,'method':'tools/list'})['result']['tools']),5)
 def test_rpc_rejected_action(self):
  with patch.dict(os.environ,{'TAP_WORKSPACE_ROOT':str(self.root),'TAP_ALLOW_WRITES':'0'}):
   x=m.rpc({'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'tap_write_text','arguments':{'path':'x.py','content':'no'}}})
  self.assertTrue(x['result']['isError'])
 def test_mcp_end_to_end_stdio(self):
  msgs=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{}}, {'jsonrpc':'2.0','id':2,'method':'tools/list'}, {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'tap_read_text','arguments':{'path':'ok.py'}}}]
  env={**os.environ,'TAP_WORKSPACE_ROOT':str(self.root),'TAP_ALLOW_WRITES':'0'}
  run=subprocess.run([sys.executable,str(SRC)],input='\n'.join(json.dumps(x) for x in msgs)+'\n',text=True,capture_output=True,timeout=5,env=env)
  self.assertEqual(run.returncode,0,run.stderr)
  out=[json.loads(x) for x in run.stdout.splitlines()]
  self.assertEqual([x['id'] for x in out],[1,2,3])
  self.assertFalse(out[2]['result']['isError'])
if __name__=='__main__': unittest.main()
