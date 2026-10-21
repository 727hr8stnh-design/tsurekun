"""Private token-protected conversation bridge; never expose OpenCode itself."""
import hmac,json,os,secrets,threading,time
from collections import deque
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from runner import ROOT,RUNTIME,MODEL,reply,GateError
TOKEN_FILE=RUNTIME/'access-token'
LOCK=threading.Lock();REQUESTS=deque()

def token():
    RUNTIME.mkdir(parents=True,exist_ok=True,mode=0o700)
    if not TOKEN_FILE.exists():
        fd=os.open(TOKEN_FILE,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:f.write(secrets.token_urlsafe(32))
    return TOKEN_FILE.read_text().strip()
TOKEN=token()

def validate(payload):
    messages=payload.get('messages') if isinstance(payload,dict) else None
    if not isinstance(messages,list) or not 1<=len(messages)<=9:raise ValueError('invalid_messages')
    result=[]
    for m in messages:
        if not isinstance(m,dict) or m.get('role') not in ('user','assistant') or not isinstance(m.get('text'),str) or not 1<=len(m['text'].strip())<=1000:raise ValueError('invalid_message')
        result.append({'role':m['role'],'text':m['text'].strip()})
    if result[-1]['role']!='user' or len(result[-1]['text'])>500:raise ValueError('invalid_last_message')
    return result

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT/'docs'),**kw)
    def log_message(self,*a):pass # no URL, transcript or token logging
    def end_headers(self):
        self.send_header('Referrer-Policy','no-referrer');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cache-Control','no-store');super().end_headers()
    def send_json(self,status,data):
        body=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        path=urlsplit(self.path).path
        if path=='/api/health':return self.send_json(200,{'service':'bear-opencode','model':MODEL,'free_only':True})
        if path.startswith('/api/'):return self.send_json(404,{'error':'not_found'})
        return super().do_GET()
    def do_POST(self):
        if urlsplit(self.path).path!='/api/chat':return self.send_json(404,{'error':'not_found'})
        if not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+TOKEN):return self.send_json(401,{'error':'unauthorized'})
        origin=self.headers.get('Origin')
        if origin and urlsplit(origin).netloc!=self.headers.get('Host'):return self.send_json(403,{'error':'origin_rejected'})
        if self.headers.get_content_type()!='application/json':return self.send_json(415,{'error':'json_required'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=20000:raise ValueError('body_size')
            messages=validate(json.loads(self.rfile.read(length)))
        except (ValueError,UnicodeError):return self.send_json(400,{'error':'invalid_request'})
        if not LOCK.acquire(False):return self.send_json(429,{'error':'busy'})
        try:
            now=time.monotonic()
            while REQUESTS and now-REQUESTS[0]>3600:REQUESTS.popleft()
            if len(REQUESTS)>=30:return self.send_json(429,{'error':'hourly_limit'})
            REQUESTS.append(now)
            try:self.send_json(200,reply(messages))
            except GateError as e:self.send_json(503,{'error':str(e),'retry':False})
            except Exception:self.send_json(503,{'error':'bridge_unavailable','retry':False})
        finally:LOCK.release()

if __name__=='__main__':
    print('Bear bridge listening on 127.0.0.1:8870; free model only',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8870),Handler).serve_forever()
