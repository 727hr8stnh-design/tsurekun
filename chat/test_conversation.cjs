const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
(async()=>{
 const nodes={},timers=new Map(),listeners={},recognizers=[];let sequence=0,chatAbort=false;
 function element(id){return nodes[id]??=( {disabled:false,textContent:'',value:'',children:[],events:{},addEventListener(name,fn){this.events[name]=fn;},click(){if(!this.disabled)this.events.click?.();},appendChild(item){this.children.push(item);item.remove=()=>{this.children=this.children.filter(x=>x!==item);};},get firstChild(){return this.children[0];},replaceChildren(){this.children=[];}});}
 class Recognition{constructor(){recognizers.push(this);}start(){}stop(){}abort(){this.aborted=true;}}
 const document={hidden:false,getElementById:element,createElement:()=>element('line'+(++sequence)),addEventListener:(n,f)=>listeners[n]=f,dispatchEvent(){}};
 const context={document,window:{SpeechRecognition:Recognition,addEventListener(){}},location:{hash:'#key=dummy',pathname:'/bear/chat.html',search:''},history:{replaceState(){}},sessionStorage:{getItem(){return null;},setItem(){}},URLSearchParams,AbortController,Event:class{},CustomEvent:class{},
  setTimeout(fn,ms){const id=++sequence;timers.set(id,{fn,ms});return id;},clearTimeout(id){timers.delete(id);},fetch:(url,options)=>url==='/api/health'?Promise.resolve({ok:true,json:async()=>({service:'bear-opencode'})}):new Promise((resolve,reject)=>{options.signal.addEventListener('abort',()=>{chatAbort=true;reject(Object.assign(new Error(),{name:'AbortError'}));});})};
 vm.runInNewContext(fs.readFileSync('docs/bear/conversation.js','utf8'),context);
 const flush=()=>new Promise(resolve=>setImmediate(resolve));await flush();
 assert.equal(element('chat-mic').disabled,false);
 element('chat-mic').click();assert.equal(element('chat-send').disabled,true);
 const first=recognizers[0],staleResult=first.onresult;
 [...timers.values()].find(x=>x.ms===20000).fn();
 assert.equal(element('chat-send').disabled,false);assert.equal(first.aborted,true);
 staleResult({results:[[{transcript:'stale'}]]});assert.equal(element('chat-message').value,'');
 element('chat-message').value='こんにちは';element('chat-send').click();assert.equal(element('chat-send').disabled,true);
 element('chat-recover').click();await flush();assert.equal(chatAbort,true);assert.equal(element('chat-send').disabled,false);assert.equal(element('chat-message').value,'こんにちは');
 element('chat-mic').click();assert.equal(element('chat-send').disabled,true);
 document.hidden=true;listeners.visibilitychange();assert.equal(element('chat-send').disabled,false);assert.equal(recognizers[1].aborted,true);
 console.log('PASS: missing microphone end, stale callback, request cancellation, background recovery');
})().catch(error=>{console.error(error);process.exitCode=1;});
