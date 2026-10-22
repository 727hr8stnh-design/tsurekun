(() => {
 const viewer=document.getElementById('viewer'),status=document.getElementById('outfit-status'),buttons=[...document.querySelectorAll('[data-outfit]')];
 const outfits={vest:{src:'model.glb?v=7',name:'茶色のベスト'},sweater:{src:'sweater.glb?v=2',name:'セーター'},shirt:{src:'shirt.glb?v=2',name:'Tシャツ'},bare:{src:'bare.glb?v=1',name:'服なし'}};
 let current='vest',pending=null,timer=null,restore=null;
 const animated=['groove','breakbeat','toggle','speak'].map(id=>document.getElementById(id));
 function lock(value){buttons.forEach(b=>b.disabled=value);animated.forEach(b=>b.disabled=value);}
 function selected(){buttons.forEach(b=>{const on=b.dataset.outfit===current;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});}
 viewer.addEventListener('load',()=>{
  if(!pending)return;clearTimeout(timer);current=pending;pending=null;lock(false);selected();
  if(restore){viewer.animationName=restore.animation;viewer.currentTime=0;if(restore.paused)viewer.pause();else viewer.play();restore=null;}
  status.textContent=outfits[current].name+(current==='bare'?'にしたよ。':'に着替えたよ。');
 });
 function failed(){if(!pending)return;clearTimeout(timer);pending=null;buttons.forEach(b=>b.disabled=false);status.textContent='服を読み込めませんでした。もう一度服を選んでね。';}
 viewer.addEventListener('error',failed);
 buttons.forEach(button=>button.addEventListener('click',()=>{
  const next=button.dataset.outfit;if(pending||!outfits[next])return;
  document.getElementById('chat-recover')?.click();document.dispatchEvent(new Event('bear-stop'));
  restore={animation:viewer.animationName==='03_Talk_4s'?'01_Sway_4s':viewer.animationName,paused:viewer.paused};
  pending=next;lock(true);status.textContent='着替えているよ…';
  // A failed previous load may need the same selection again.
  if(viewer.getAttribute('src')===outfits[next].src)viewer.removeAttribute('src');
  viewer.setAttribute('src',outfits[next].src);timer=setTimeout(failed,20000);
 }));selected();
})();
