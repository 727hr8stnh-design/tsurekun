"""Stop only this project's bridge and tunnel after verifying process identity."""
import os,signal,subprocess
from runner import ROOT,RUNTIME
for name,marker in [('tunnel','cloudflared tunnel --url http://127.0.0.1:8870'),('bridge',str(ROOT/'chat/server.py'))]:
 p=RUNTIME/(name+'.pid')
 if not p.exists():continue
 pid=int(p.read_text())
 result=subprocess.run(['/bin/ps','-p',str(pid),'-o','command='],capture_output=True,text=True)
 if result.returncode:print(name,'already stopped');continue
 if marker not in result.stdout:raise SystemExit('PID identity mismatch: '+name)
 os.kill(pid,signal.SIGTERM);print(name,'stopped')
