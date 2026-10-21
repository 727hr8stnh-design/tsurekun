"""Start the local bridge; optionally use an already configured private HTTPS URL."""
import argparse,os,subprocess,sys,time
from runner import ROOT,RUNTIME
parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:8870');args=parser.parse_args()
from urllib.parse import urlsplit
parsed=urlsplit(args.base_url)
if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.path not in ('','/') or parsed.query or parsed.fragment or parsed.username:raise SystemExit('Invalid base URL')
if parsed.scheme=='http' and parsed.hostname not in ('127.0.0.1','localhost'):raise SystemExit('Remote endpoints require HTTPS')
RUNTIME.mkdir(parents=True,exist_ok=True,mode=0o700);RUNTIME.chmod(0o700)
pidfile=RUNTIME/'bridge.pid'
if pidfile.exists():
 try:os.kill(int(pidfile.read_text()),0)
 except (ProcessLookupError,ValueError):pass
 else:raise SystemExit('Bridge already running; reuse .runtime/chat/private-link.txt')
with (RUNTIME/'bridge.log').open('a') as stream:
 bridge=subprocess.Popen([sys.executable,str(ROOT/'chat/server.py')],cwd=ROOT,stdin=subprocess.DEVNULL,stdout=stream,stderr=stream,start_new_session=True)
pidfile.write_text(str(bridge.pid))
for _ in range(30):
 if (RUNTIME/'access-token').exists():break
 if bridge.poll() is not None:raise SystemExit('Bridge failed to start')
 time.sleep(.1)
url=args.base_url.rstrip('/')+'/bear/chat.html#key='+(RUNTIME/'access-token').read_text().strip()
(RUNTIME/'private-link.txt').write_text(url);os.chmod(RUNTIME/'private-link.txt',0o600)
print('Bridge ready. Private link saved in .runtime/chat/private-link.txt (do not publish).')
