import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

from fastapi.testclient import TestClient

HERE = Path(__file__).resolve().parents[1] / 'server' / 'studio.py'
spec = importlib.util.spec_from_file_location('tap_studio', HERE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class StudioTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.app = mod.create_app(db_path=str(Path(self.tmp.name) / 'test.db'), bootstrap_user='admin', bootstrap_password='this-is-a-long-local-testing-password')
        self.client = TestClient(self.app)
        self.assertEqual(self.client.get('/health').status_code, 200)

    def tearDown(self):
        self.client.close()
        self.tmp.cleanup()

    def login(self, user='admin', password='this-is-a-long-local-testing-password'):
        r = self.client.post('/api/login',json={'username':user,'password':password})
        self.assertEqual(r.status_code, 200, r.text)
        self.token = r.json()['access_token']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def create(self):
        self.login()
        r=self.client.post('/api/projects',json={'name':'Meu App de Academia','description':'Avaliação física para uma academia'},headers=self.headers)
        self.assertEqual(r.status_code, 201,r.text)
        return r.json()['id']

    def test_health_no_credentials(self):
        res = self.client.get('/health')
        self.assertNotIn('token',res.text.lower())

    def test_denies_anonymous_api_access(self):
        self.assertEqual(self.client.get('/api/projects').status_code,401)
        self.assertEqual(self.client.post('/mcp',json={'jsonrpc':'2.0','id':1,'method':'tools/list'}).status_code,401)

    def test_login_wrong_password(self):
        self.assertEqual(self.client.post('/api/login',json={'username':'admin','password':'wrong'}).status_code,401)

    def test_project_create_and_list_and_read_files(self):
        project_id=self.create()
        listings=self.client.get('/api/projects',headers=self.headers).json()
        self.assertEqual(len(listings),1)
        r=self.client.get(f'/api/projects/{project_id}/files',headers=self.headers)
        self.assertEqual(r.status_code,200)
        self.assertTrue({'index.html','style.css','app.js','README.md'}.issubset(set(r.json())))
        self.assertIn('Meu App de Academia',r.json()['index.html'])

    def test_rejects_path_traversal_and_secrets(self):
        p=self.create()
        for path in ('../private.txt','.env','./index.html','file/../../a.js','id_rsa'):
            r=self.client.put(f'/api/projects/{p}/files',headers=self.headers,json={'path':path,'content':'attack'})
            self.assertEqual(r.status_code,400,(path,r.text))

    def test_export_zip_is_valid(self):
        import io,zipfile
        p=self.create()
        r=self.client.get(f'/api/projects/{p}/export',headers=self.headers)
        self.assertEqual(r.status_code,200)
        with zipfile.ZipFile(io.BytesIO(r.content)) as archive:
            self.assertIn('index.html',archive.namelist())
            self.assertIn('style.css',archive.namelist())

    def test_file_update_and_size_limit(self):
        p=self.create()
        r=self.client.put(f'/api/projects/{p}/files',headers=self.headers,json={'path':'index.html','content':'<h1>OK</h1>'})
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(self.client.get(f'/api/projects/{p}/files',headers=self.headers).json()['index.html'],'<h1>OK</h1>')
        r=self.client.put(f'/api/projects/{p}/files',headers=self.headers,json={'path':'x.css','content':'x'*205000})
        self.assertIn(r.status_code,(400,413,422))

    def test_cross_user_isolation(self):
        p=self.create()
        self.app.state.store.create_user('another','a-second-long-local-testing-password')
        other=self.client.post('/api/login',json={'username':'another','password':'a-second-long-local-testing-password'}).json()['access_token']
        hdr={'Authorization':f'Bearer {other}'}
        self.assertEqual(self.client.get(f'/api/projects/{p}/files',headers=hdr).status_code,404)
        self.assertEqual(self.client.put(f'/api/projects/{p}/files',headers=hdr,json={'path':'app.js','content':'hack'}).status_code,404)

    def test_session_revocation(self):
        self.login()
        self.assertEqual(self.client.post('/api/logout',headers=self.headers).status_code,200)
        self.assertEqual(self.client.get('/api/projects',headers=self.headers).status_code,401)

    def test_mcp_request_tool_calls(self):
        self.login()
        r=self.client.post('/mcp',headers={**self.headers,'Accept':'application/json, text/event-stream'},json={'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'test','version':'1'}}})
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(r.json()['result']['serverInfo']['name'],'tap-studio-runtime')
        r=self.client.post('/mcp',headers=self.headers,json={'jsonrpc':'2.0','id':2,'method':'tools/list'})
        self.assertEqual(r.status_code,200,r.text)
        names=[x['name'] for x in r.json()['result']['tools']]
        self.assertIn('tap_create_project',names)
        r=self.client.post('/mcp',headers=self.headers,json={'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'tap_create_project','arguments':{'name':'Projeto Estúdio','description':'Tela principal'}}})
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(r.json()['result']['isError'],False)

    def test_ai_generation_requires_consent_and_config(self):
        self.login()
        request={'name':'Academia TAP','description':'Quero um sistema para academias','consent_external_model':False}
        r=self.client.post('/api/projects/ai-generate',headers=self.headers,json=request)
        self.assertEqual(r.status_code,400,r.text)
        request['consent_external_model']=True
        r=self.client.post('/api/projects/ai-generate',headers=self.headers,json=request)
        self.assertEqual(r.status_code,503,r.text)

    def test_ai_generated_files_are_validated_before_storage(self):
        import asyncio
        bad={'index.html':'<h1>OK</h1>','.env':'SECRET=123','style.css':'a{}','app.js':'alert(1)'}
        with self.assertRaises(ValueError):
            mod.validate_ai_files(bad)
        good=mod.validate_ai_files({'index.html':'<!doctype html><h1>OK</h1>','style.css':'a{}','app.js':'alert(1)'})
        self.assertEqual(set(good),{'index.html','style.css','app.js'})

    def test_ai_mocked_provider_persists_only_validated_files(self):
        from unittest.mock import AsyncMock, patch
        self.login()
        settings = {
            'TAP_STUDIO_MODEL_ENDPOINT':'https://models.example.org/v1/chat/completions',
            'TAP_STUDIO_ALLOWED_MODEL_HOSTS':'models.example.org',
            'TAP_STUDIO_MODEL_KEY':'TEST-ONLY-NOT-REAL-KEY',
            'TAP_STUDIO_MODEL_NAME':'mock-test-model',
        }
        files={'index.html':'<!doctype html><h1>Protótipo</h1>', 'style.css':'body{color:black}', 'app.js':'console.log("local")'}
        with patch.dict(os.environ,settings), patch.object(mod,'call_model',new=AsyncMock(return_value=files)) as model:
            r=self.client.post('/api/projects/ai-generate',headers=self.headers,json={
                'name':'Projeto IA Simulado','description':'Teste sem rede','consent_external_model':True})
            self.assertEqual(r.status_code,201,r.text)
            self.assertTrue(r.json()['ai_generated'])
            self.assertFalse(r.json()['deployed'])
            self.assertEqual(self.client.get(f"/api/projects/{r.json()['id']}/files",headers=self.headers).json()['app.js'],files['app.js'])
            model.assert_awaited_once()

    def test_no_auto_publication_or_commands(self):
        self.login()
        r=self.client.post('/mcp',headers=self.headers,json={'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'run_shell','arguments':{'command':'rm -rf /'}}})
        self.assertTrue(r.json()['result']['isError'])
        self.assertNotIn('run_shell',[x['name'] for x in mod.MCP_TOOLS])

    def test_preview_security_headers(self):
        r=self.client.get('/')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.headers['X-Content-Type-Options'],'nosniff')
        self.assertIn('Content-Security-Policy',r.headers)

if __name__ == '__main__':unittest.main()
