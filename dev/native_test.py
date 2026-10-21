from playwright.sync_api import sync_playwright
U='file:///tmp/claude-0/-home-claude/1e501b03-4ed6-5c40-a796-75230d689d31/scratchpad/kkeutmal-app/www/index.html'
STUB='''
window.__log=[]; window.__mode='ok'; window.__perm='granted';
window.KK_NATIVE={
  SpeechRecognition:{
    available:async()=>({available:true}),
    checkPermissions:async()=>({speechRecognition:window.__perm}),
    requestPermissions:async()=>{__log.push('requestPermissions');return {speechRecognition:window.__perm}},
    start:(o)=>{__log.push('start '+JSON.stringify(o));return new Promise((res,rej)=>{window.__finish=()=>{
       if(window.__mode==='ok') res({matches:window.__matches||['과일']});
       else rej({message:window.__mode});}; })},
    stop:()=>{__log.push('stop'); setTimeout(()=>window.__finish&&window.__finish(),10); return new Promise(()=>{})}
  },
  TextToSpeech:{ speak:async(o)=>{__log.push('speak '+o.text+' '+o.lang)}, stop:async()=>{__log.push('tts.stop')} }
};
'''
def lastapp(pg): return pg.evaluate("()=>[...document.querySelectorAll('.entry.app .tile')].pop().textContent.replace(/[●]/g,'').trim()")
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':360,'height':640},is_mobile=True,has_touch=True)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/*', lambda r: r.abort() if 'fonts.g' in r.request.url else r.continue_())
    pg.add_init_script(STUB)
    pg.goto(U); pg.wait_for_timeout(400)
    print('switch text:', pg.inner_text('#swState'))
    # pick a first word and craft a valid answer
    first=lastapp(pg); print('app first word:', first)
    ans=pg.evaluate("(f)=>{const l=WORDS.filter(x=>starters(f[f.length-1]).includes(x[0])&&x!==f);return l[0]}", first)
    print('answer:', ans)
    # 1) happy path: tap mic, plugin returns matches [wrong, right]
    pg.evaluate("(a)=>{window.__matches=['엉뚱한소리',a]}", ans)
    pg.click('#mic'); pg.wait_for_timeout(100)
    print('listening class:', pg.evaluate("document.getElementById('mic').classList.contains('on')"), '|', pg.inner_text('#status'))
    pg.evaluate("window.__finish()"); pg.wait_for_timeout(1500)
    print('after result score:', pg.inner_text('#score'), '| app word:', lastapp(pg))
    print('log:', pg.evaluate("__log"))
    # 2) stop by second tap
    pg.evaluate("__log.length=0; window.__matches=['과일']")
    pg.click('#mic'); pg.wait_for_timeout(50); pg.click('#mic'); pg.wait_for_timeout(300)
    print('stop-by-tap log:', pg.evaluate("__log"))
    # 3) errors
    for msg in ['No speech input','Network error','Insufficient permissions','RecognitionService busy']:
        pg.evaluate("(m)=>{window.__mode=m}", msg)
        pg.wait_for_timeout(1300)
        pg.click('#mic'); pg.wait_for_timeout(80); pg.evaluate("window.__finish()"); pg.wait_for_timeout(150)
        print(msg,'->',pg.inner_text('#status'))
    # 4) permission denied
    pg.evaluate("window.__perm='denied'; window.__mode='ok'")
    pg.click('#mic'); pg.wait_for_timeout(200)
    print('denied ->', pg.inner_text('#status'), '| log tail:', pg.evaluate("__log.slice(-2)"))
    print('page errors:', errs)
    b.close()
