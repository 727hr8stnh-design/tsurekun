import unittest,sys,subprocess,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import runner
from server import validate
class ChatSafety(unittest.TestCase):
 def test_zero_cost(self):runner.check_free({'cost':{'input':0,'output':0,'cache':{'read':0,'write':0}}})
 def test_paid_unknown_boolean_rejected(self):
  for value in [None,True,-1,.01,'0']:
   with self.subTest(value=value),self.assertRaises(runner.GateError):runner.check_free({'cost':{'input':value,'output':0}})
 def test_attestation_requires_exact_model_and_zero(self):
  row={'role':'assistant','providerID':'opencode','modelID':runner.MODEL.split('/')[1],'cost':0,'finish':'stop','time':{'completed':1}}
  self.assertEqual(runner.attest([row])['cost'],0)
  for patch in [{'cost':None},{'cost':.1},{'modelID':'paid-model'},{'finish':'tool-calls'},{'time':{}}]:
   with self.subTest(patch=patch),self.assertRaises(runner.GateError):runner.attest([dict(row,**patch)])
 def test_request_validation(self):
  self.assertEqual(validate({'messages':[{'role':'user','text':'こんにちは'}]})[0]['text'],'こんにちは')
  for data in [None,{}, {'messages':[]},{'messages':[{'role':'system','text':'x'}]},{'messages':[{'role':'user','text':'x'*501}]}]:
   with self.subTest(data=str(data)[:60]),self.assertRaises(ValueError):validate(data)
 def test_http_auth_origin_and_json_boundary(self):
  import threading,urllib.request,urllib.error
  import server
  http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
  thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
  base='http://127.0.0.1:'+str(http.server_port)
  try:
   cases=[({},401),({'Authorization':'Bearer '+server.TOKEN,'Origin':'https://untrusted.example'},403),({'Authorization':'Bearer '+server.TOKEN,'Content-Type':'text/plain'},415)]
   for headers,expected in cases:
    request=urllib.request.Request(base+'/api/chat',data=b'{}',headers=headers)
    with self.subTest(expected=expected),self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(request)
    self.assertEqual(error.exception.code,expected);error.exception.close()
  finally:http.shutdown();http.server_close();thread.join()
 def test_sandbox_blocks_checkout_read_and_write(self):
  canary=runner.ROOT/'verification/chat-canary';canary.write_text('dummy')
  code='import pathlib; p=pathlib.Path('+repr(str(canary))+');\nfor op in (p.read_text, lambda:p.write_text("modified")):\n try:op()\n except PermissionError:pass\n else:raise SystemExit(2)\n'
  python=Path(sys.executable).resolve()
  launcher=Path(sys.base_prefix)/'Resources/Python.app/Contents/MacOS/Python'
  profile=runner.sandbox()+'(allow process-exec (literal '+json.dumps(str(python))+') (literal '+json.dumps(str(launcher.resolve()))+'))'
  p=subprocess.run(['/usr/bin/sandbox-exec','-p',profile,str(python),'-I','-c',code],env=runner.environment(),cwd=runner.RUNTIME,capture_output=True)
  self.assertEqual(p.returncode,0,p.stderr.decode());self.assertEqual(canary.read_text(),'dummy')
if __name__=='__main__':unittest.main()
