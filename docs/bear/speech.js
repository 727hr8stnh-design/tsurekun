(() => {
 const viewer=document.getElementById('viewer'),speak=document.getElementById('speak'),quiet=document.getElementById('quiet'),words=document.getElementById('words'),status=document.getElementById('speech-status');
 const supported='speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
 let active=null,previous=null,timer=null;
 const style=document.getElementById('voice-style');
 const styles={soft:{rate:.88,pitch:1.45},bright:{rate:1.02,pitch:1.6},calm:{rate:.9,pitch:1.05}};
 if(style){try{const saved=localStorage.getItem('bear-voice-style');if(styles[saved])style.value=saved;}catch(e){}
 style.addEventListener('change',()=>{stop();try{localStorage.setItem('bear-voice-style',style.value);}catch(e){}status.textContent='声の雰囲気を変えたよ。「話して」で聞いてみてね。';});}
 const controls=['groove','breakbeat','toggle'].map(id=>document.getElementById(id));
 function enable(){speak.disabled=!supported; if(!supported)status.textContent='このブラウザでは音声読み上げを利用できません。Safariで開いてください。';}
 viewer.addEventListener('load',enable);
 if(document.getElementById('scene').classList.contains('loaded'))enable();
 function finish(message){
  clearTimeout(timer);active=null;quiet.disabled=true;speak.disabled=false;
  if(previous){viewer.animationName=previous.name;viewer.currentTime=0;if(previous.paused)viewer.pause();else viewer.play();previous=null;}
  controls.forEach(b=>b.disabled=false);status.textContent=message;document.dispatchEvent(new Event('bear-speech-finished'));
 }
 function stop(){if(!supported)return;const wasActive=!!active;active=null;window.speechSynthesis.cancel();if(wasActive)finish('声を止めました');}
 speak.addEventListener('click',()=>{
  const text=words.value.trim();if(!text){status.textContent='話してほしいセリフを入力してください。';words.focus();return;}
  if(active)stop();
  const utterance=new SpeechSynthesisUtterance(text);active=utterance;
  const tone=styles[style?.value]||styles.soft;
  utterance.lang='ja-JP';utterance.rate=tone.rate;utterance.pitch=tone.pitch;utterance.volume=1;
  const voice=window.speechSynthesis.getVoices().find(v=>v.lang.toLowerCase().startsWith('ja'));if(voice)utterance.voice=voice;
  previous={name:viewer.animationName,paused:viewer.paused};
  speak.disabled=true;quiet.disabled=false;controls.forEach(b=>b.disabled=true);status.textContent='声を準備しています…';
  utterance.onstart=()=>{if(active!==utterance)return;clearTimeout(timer);viewer.animationName='03_Talk_4s';viewer.currentTime=0;viewer.play();status.textContent='おしゃべり中…';timer=setTimeout(stop,45000);};
  utterance.onend=()=>{if(active===utterance)finish('話し終わったよ。セリフを変えて、また話しかけてね。');};
  utterance.onerror=()=>{if(active===utterance)finish('声を再生できませんでした。音量を確認して、もう一度「話して」を押してください。');};
  timer=setTimeout(()=>{if(active===utterance){stop();status.textContent='声が始まりませんでした。音量と音声設定を確認して再度押してください。';}},15000);
  try{window.speechSynthesis.speak(utterance);}catch(e){finish('声を再生できませんでした。もう一度お試しください。');}
 });
 quiet.addEventListener('click',stop);
 document.addEventListener('bear-stop',stop);
 document.addEventListener('bear-say',event=>{if(!speak.disabled){words.value=event.detail; speak.click();}});
 window.addEventListener('pagehide',()=>{if(supported)stop();});
 document.addEventListener('visibilitychange',()=>{if(document.hidden&&supported)stop();});
})();
