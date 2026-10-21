const fs = require('fs');
const html = fs.readFileSync(process.argv[2], 'utf8');
const m = html.match(/<script id="logic">([\s\S]*?)<\/script>/);
const ui = html.match(/<script id="ui">([\s\S]*?)<\/script>/);
new Function(ui[1]); // syntax check of UI script
const api = new Function(m[1] + '; return {WORDS, BY_START, starters, dueum, check, pick, candidates, continuations};')();
const {WORDS, BY_START, starters, check, pick, candidates, continuations} = api;
console.log('words', WORDS.length, 'start syllables', BY_START.size);
const eq = (a,b,l)=>{const ok=JSON.stringify(a)===JSON.stringify(b);console.log(ok?'ok  ':'FAIL',l,JSON.stringify(a));};
eq(starters('리'),['리','이'],'리');
eq(starters('라'),['라','나'],'라');
eq(starters('녀'),['녀','여'],'녀');
eq(starters('로'),['로','노'],'로');
eq(starters('류'),['류','유'],'류');
eq(starters('냥'),['냥','양'],'냥');
eq(starters('기'),['기'],'기');
eq(starters('락'),['락','낙'],'락');
const used = new Set(['사과']);
eq(check('과일','사과',used).ok,true,'사과→과일');
eq(check('과자','사과',new Set(['사과','과자'])).reason,'used','중복');
eq(check('나무','사과',used).reason,'chain','체인오류');
eq(check('a','사과',used).reason,'hangul','한글아님');
eq(check('과','사과',used).reason,'short','1글자');
eq(check('이슬','바다 ' .trim()+'리'.repeat(0)||'기리',used).ok,false,'(기리 뒤 이슬은 불가: 리→이 가능 아님? 확인)');
eq(check('이슬','기리',used).ok,true,'기리→이슬 두음');
// dead ends and playability
let dead=[]; for (const w of WORDS){ if(continuations(w,new Set())===0) dead.push(w);} console.log('dead-end words', dead.length, dead.join(' '));
// simulate random games app vs app, check no crash and chain validity
for (const level of ['easy','normal','hard']) {
  let totalLen=0;
  for (let g=0; g<200; g++){
    const u=new Set(); let prev=pick(null,u,level); u.add(prev); let n=1;
    for(;;){ const w=pick(prev,u,level); if(!w) break; if(!check(w,prev,u).ok) throw new Error('invalid '+prev+'→'+w); u.add(w); prev=w; n++; }
    totalLen+=n;
  }
  console.log(level,'avg chain', (totalLen/200).toFixed(1));
}
