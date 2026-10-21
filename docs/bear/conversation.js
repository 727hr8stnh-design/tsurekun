(() => {
 const state=document.getElementById('chat-state'),log=document.getElementById('chat-log'),input=document.getElementById('chat-message'),send=document.getElementById('chat-send'),mic=document.getElementById('chat-mic'),clear=document.getElementById('chat-clear');
 let messages=[],connected=false,busy=false,listening=false;
 const params=new URLSearchParams(location.hash.slice(1));
 let key=params.get('key')||sessionStorage.getItem('bear-chat-key')||'';
 if(params.has('key')){sessionStorage.setItem('bear-chat-key',key);history.replaceState(null,'',location.pathname+location.search);}
 const Recognition=window.SpeechRecognition||window.webkitSpeechRecognition;
 let recognition=null;
 function buttons(){send.disabled=!connected||busy||listening;mic.disabled=!connected||busy||!Recognition;clear.disabled=busy||listening;}
 function line(who,text){const item=document.createElement('p');item.textContent=who+'：'+text;log.appendChild(item);while(log.children.length>10)log.firstChild.remove();return item;}
 async function submit(){
  const text=input.value.trim();if(!text||!connected||busy)return;
  document.getElementById('quiet').click();busy=true;buttons();state.textContent='しろくまが考えているよ…';
  const request=[...messages.slice(-8),{role:'user',text}];const pending=line('あなた',text);input.value='';
  try{
   const response=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+key},body:JSON.stringify({messages:request}),signal:AbortSignal.timeout(135000)});
   const data=await response.json();
   if(!response.ok){const errors={unauthorized:'会話用の専用リンクから開き直してください。',busy:'別の返事を作っています。少し待ってから送ってね。',hourly_limit:'無料利用の上限に達しました。時間を置いて試してね。'};throw Error(errors[data.error]||'無料モデルが今は応答できません。自動再送はしていません。');}
   if(data.verified!==true||data.cost!==0||typeof data.reply!=='string')throw Error('無料の返答を確認できなかったため停止しました。');
   messages=[...request,{role:'assistant',text:data.reply}].slice(-8);line('しろくま',data.reply);
   state.textContent='返事が届いたよ。声が出ないときは下の「話して」を押してね。';
   document.dispatchEvent(new CustomEvent('bear-say',{detail:data.reply}));
  }catch(error){pending.remove();state.textContent=error.name==='TimeoutError'?'返事に時間がかかっています。自動再送はしていません。':error.message;input.value=text;}
  finally{busy=false;buttons();}
 }
 send.addEventListener('click',submit);
 clear.addEventListener('click',()=>{messages=[];log.replaceChildren();state.textContent='新しい会話を始めよう。';document.getElementById('quiet').click();});
 if(Recognition){
  recognition=new Recognition();recognition.lang='ja-JP';recognition.continuous=false;recognition.interimResults=false;
  recognition.onstart=()=>{listening=true;mic.textContent='■ 聞き取りを止める';state.textContent='聞いているよ。話し終わるまで待ってね。';buttons();};
  recognition.onresult=event=>{input.value=event.results[0][0].transcript;};
  recognition.onend=()=>{listening=false;mic.textContent='🎤 話しかける';buttons();if(input.value.trim())submit();};
  recognition.onerror=event=>{state.textContent=event.error==='not-allowed'?'マイクが許可されていません。文字でも話せます。':'聞き取れませんでした。文字でも話せます。';};
  mic.addEventListener('click',()=>{if(listening){recognition.stop();return;}document.getElementById('quiet').click();input.value='';try{recognition.start();}catch(e){state.textContent='マイクを開始できませんでした。文字でも話せます。';}});
 }else mic.textContent='マイク非対応（文字で会話）';
 fetch('/api/health').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{if(data.service!=='bear-opencode'||!key)throw Error();connected=true;state.textContent='準備できたよ。話しかけてね。';buttons();}).catch(()=>{state.textContent='会話サーバーに接続できません。Macが起動中か確認し、専用リンクから開いてください。';buttons();});
})();
