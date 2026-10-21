const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const nodes={},listeners={},spoken=[];let cancelled=0;
function element(id){return nodes[id]??={disabled:false,textContent:'',value:id==='voice-style'?'soft':id==='words'?'こんにちは':'',events:{},addEventListener(n,f){this.events[n]=f;},click(){if(!this.disabled)this.events.click?.();},classList:{contains:()=>true},play(){},pause(){}};}
const document={hidden:false,getElementById:element,addEventListener(n,f){listeners[n]=f;},dispatchEvent(){}};
const speechSynthesis={getVoices:()=>[{lang:'ja-JP',name:'test voice'}],speak:u=>spoken.push(u),cancel:()=>cancelled++};
vm.runInNewContext(fs.readFileSync('docs/bear/speech.js','utf8'),{document,window:{speechSynthesis,SpeechSynthesisUtterance:class{},addEventListener(){}},SpeechSynthesisUtterance:class{},localStorage:{getItem(){},setItem(){}},Event:class{},setTimeout:()=>1,clearTimeout(){}});
element('speak').click();assert.equal(spoken[0].pitch,1.45);assert.equal(spoken[0].rate,.72);spoken[0].onend();
element('voice-style').value='bright';element('voice-style').events.change();element('speak').click();assert.equal(spoken[1].pitch,1.6);assert.equal(spoken[1].rate,.85);spoken[1].onend();
element('voice-style').value='calm';element('voice-style').events.change();element('speak').click();assert.equal(spoken[2].pitch,1.05);spoken[2].onend();
listeners['bear-stop']();assert.ok(cancelled>=3);assert.equal(element('speak').disabled,false);
console.log('PASS: soft default, bright/calm presets, idle speech cancellation');
