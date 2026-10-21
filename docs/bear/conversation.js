(() => {
 const state=document.getElementById('chat-state'),log=document.getElementById('chat-log'),input=document.getElementById('chat-message'),send=document.getElementById('chat-send'),mic=document.getElementById('chat-mic'),clear=document.getElementById('chat-clear'),recover=document.getElementById('chat-recover');
 let messages=[],connected=false,busy=false,listening=false,activeRecognition=null,controller=null,requestVersion=0;
 const params=new URLSearchParams(location.hash.slice(1));
 let key=params.get('key')||sessionStorage.getItem('bear-chat-key')||'';
 if(params.has('key')){sessionStorage.setItem('bear-chat-key',key);history.replaceState(null,'',location.pathname+location.search);}
 const Recognition=window.SpeechRecognition||window.webkitSpeechRecognition;
 function buttons(){send.disabled=!connected||busy||listening;mic.disabled=!connected||busy||!Recognition;clear.disabled=busy||listening;mic.textContent=listening?'■ 聞き取りを止める':Recognition?'🎤 話しかける':'マイク非対応（文字で会話）';}
 function line(who,text){const item=document.createElement('p');item.textContent=who+'：'+text;log.appendChild(item);while(log.children.length>10)log.firstChild.remove();return item;}
 function endListening(message){
  const active=activeRecognition;activeRecognition=null;listening=false;
  if(active){clearTimeout(active.timer);clearTimeout(active.startTimer);active.recognition.onend=active.recognition.onerror=active.recognition.onresult=active.recognition.onstart=null;try{active.recognition.abort();}catch(e){}}
  if(message)state.textContent=message;buttons();
 }
 function resetActivity(message){
  requestVersion++;if(controller)controller.abort();controller=null;busy=false;
  endListening();document.dispatchEvent(new Event('bear-stop'));state.textContent=message;buttons();
 }
 async function submit(){
  const text=input.value.trim();if(!text||!connected||busy||listening)return;
  document.dispatchEvent(new Event('bear-stop'));busy=true;buttons();state.textContent='しろくまが考えているよ…（最大約50秒）';
  const version=++requestVersion,request=[...messages.slice(-8),{role:'user',text}],pending=line('あなた',text);input.value='';
  const abort=new AbortController();controller=abort;const timeout=setTimeout(()=>abort.abort(),60000);
  try{
   const response=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+key},body:JSON.stringify({messages:request}),signal:abort.signal});
   const data=await response.json();if(version!==requestVersion){pending.remove();return;}
   if(!response.ok){const errors={unauthorized:'会話用の専用リンクから開き直してください。',busy:'前の返事を終了しています。最大50秒ほど待ってから送ってね。',hourly_limit:'無料利用の上限に達しました。時間を置いて試してね。',timeout_no_retry:'返事に時間がかかったので止めました。もう一度話しかけられます。'};throw Error(errors[data.error]||'無料モデルが今は応答できません。自動再送はしていません。');}
   if(data.verified!==true||data.cost!==0||typeof data.reply!=='string')throw Error('無料の返答を確認できなかったため停止しました。');
   messages=[...request,{role:'assistant',text:data.reply}].slice(-8);line('しろくま',data.reply);
   state.textContent='返事が届いたよ。声が出ないときは下の「話して」を押してね。';document.dispatchEvent(new CustomEvent('bear-say',{detail:data.reply}));
  }catch(error){pending.remove();if(version!==requestVersion&&!input.value)input.value=text;if(version===requestVersion){state.textContent=error.name==='AbortError'?'返事の待機を止めました。もう一度話しかけられます。':error.message;input.value=text;}}
  finally{clearTimeout(timeout);if(version===requestVersion){busy=false;controller=null;buttons();}}
 }
 send.addEventListener('click',submit);
 clear.addEventListener('click',()=>{resetActivity('新しい会話を始めよう。');messages=[];log.replaceChildren();});
 recover.addEventListener('click',()=>resetActivity('音声と待機を止めました。もう一度話しかけてね。'));
 mic.addEventListener('click',()=>{
  if(listening){const active=activeRecognition;if(active){try{active.recognition.stop();}catch(e){}clearTimeout(active.timer);active.timer=setTimeout(()=>endListening('聞き取りを止めました。文字でも話せます。'),1500);}return;}
  if(!Recognition||busy)return;
  document.dispatchEvent(new Event('bear-stop'));input.value='';
  const recognition=new Recognition(),active={recognition,timer:null,startTimer:null};activeRecognition=active;listening=true;buttons();state.textContent='マイクを準備しています…';
  recognition.lang='ja-JP';recognition.continuous=false;recognition.interimResults=false;
  recognition.onstart=()=>{if(activeRecognition===active)state.textContent='聞いているよ。20秒以内で話してね。';};
  recognition.onresult=event=>{if(activeRecognition!==active)return;const text=event.results[0][0].transcript;input.value=text;endListening();submit();};
  recognition.onend=()=>{if(activeRecognition===active)endListening('聞き取れませんでした。もう一度押すか、文字で話してね。');};
  recognition.onerror=event=>{if(activeRecognition===active)endListening(event.error==='not-allowed'?'マイクが許可されていません。文字でも話せます。':'聞き取りを終了しました。もう一度押すか、文字で話してね。');};
  active.timer=setTimeout(()=>{if(activeRecognition===active)endListening('聞き取りを一度止めました。もう一度押すか、文字で話してね。');},20000);
  // Allow iOS to release speech playback before acquiring the microphone.
  active.startTimer=setTimeout(()=>{if(activeRecognition!==active)return;try{recognition.start();}catch(e){endListening('マイクを開始できませんでした。文字でも話せます。');}},300);
 });
 function connect(){const abort=new AbortController(),timeout=setTimeout(()=>abort.abort(),8000);fetch('/api/health',{signal:abort.signal}).then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{if(data.service!=='bear-opencode'||!key)throw Error();connected=true;if(!busy&&!listening)state.textContent='準備できたよ。話しかけてね。';buttons();}).catch(()=>{connected=false;if(!busy&&!listening)state.textContent='会話サーバーに接続できません。MacとTailscaleの接続を確認してください。';buttons();}).finally(()=>clearTimeout(timeout));}
 document.addEventListener('visibilitychange',()=>{if(document.hidden)resetActivity('画面を離れたので音声を止めました。');else connect();});
 window.addEventListener('pagehide',()=>resetActivity('停止しました。'));connect();
})();
