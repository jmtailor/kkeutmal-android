import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    try:
        b = p.chromium.launch()
    except Exception as e:
        print('launch failed', str(e)[:300]); sys.exit(0)
    for name,(w,h) in {'phone':(360,640),'small':(360,520)}.items():
        pg = b.new_page(viewport={'width':w,'height':h}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg.route('**/*', lambda r: r.abort() if 'fonts.g' in r.request.url else r.continue_())
        pg.goto('file:///tmp/claude-0/-home-claude/1e501b03-4ed6-5c40-a796-75230d689d31/scratchpad/%EB%81%9D%EB%A7%90%EC%9E%87%EA%B8%B0.html')
        pg.wait_for_timeout(500)
        # play a couple of turns
        for wd in ['과일','이슬']:
            st = pg.inner_text('#status')
            last = pg.evaluate("state => 0", None) if False else None
        info = pg.evaluate("({sh:document.documentElement.scrollHeight, ch:document.documentElement.clientHeight, sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth})")
        print(name, info)
        pg.screenshot(path=f'shot_{name}.png')
    b.close()
