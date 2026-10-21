# usage: python3 ui_test.py <끝말잇기.html path> <screenshot out dir>
import sys, os
from playwright.sync_api import sync_playwright
html, out = os.path.abspath(sys.argv[1]), sys.argv[2]
os.makedirs(out, exist_ok=True)
def ok(c, m): print(('ok   ' if c else 'FAIL ') + m); return c
res = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (w, h) in {'phone': (360, 640), 'small': (360, 520)}.items():
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=2, is_mobile=True, has_touch=True)
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/*', lambda r: r.abort() if 'fonts.g' in r.request.url else r.continue_())
        pg.clock.install()
        pg.goto('file://' + html); pg.clock.run_for(300)
        res.append(ok(not pg.is_checked('#timeSw'), f'{name}: 시간제한 기본 꺼짐'))
        res.append(ok(pg.is_hidden('#timebar'), f'{name}: 꺼짐일 때 막대 숨김'))
        pg.click('label.sw:has(#timeSw)'); pg.clock.run_for(200)
        res.append(ok(pg.is_checked('#timeSw') and pg.is_visible('#timebar'), f'{name}: 켜면 막대 표시'))
        pg.clock.run_for(10000)
        w10 = pg.evaluate("parseFloat(document.getElementById('timefill').style.width)")
        res.append(ok(40 < w10 < 60, f'{name}: 10초 경과 시 막대 약 50% ({w10:.0f}%)'))
        pg.clock.run_for(7000)
        res.append(ok(pg.evaluate("document.getElementById('timebar').classList.contains('low')"), f'{name}: 마지막 5초 경고색'))
        # rejected input must not reset the clock
        pg.fill('#word', '나는 밥을 먹었다'); pg.keyboard.press('Enter'); pg.clock.run_for(100)
        res.append(ok('한 단어만' in pg.inner_text('#status'), f'{name}: 공백 문장 거절 메시지'))
        pg.screenshot(path=f'{out}/{name}_timer_low.png')
        pg.clock.run_for(4000)
        txt = pg.inner_text('#stage')
        res.append(ok('시간 초과' in txt and pg.is_disabled('#word'), f'{name}: 20초 초과 시 패배·입력 잠금'))
        res.append(ok(pg.is_hidden('#timebar'), f'{name}: 종료 후 막대 숨김'))
        pg.screenshot(path=f'{out}/{name}_timeup.png')
        # persistence
        pg.reload(); pg.clock.run_for(300)
        res.append(ok(pg.is_checked('#timeSw'), f'{name}: 새로고침 후 설정 유지'))
        # new game restarts, correct answer stops bar
        sc = pg.evaluate("({sh:document.documentElement.scrollHeight, ch:document.documentElement.clientHeight})")
        res.append(ok(sc['sh'] <= sc['ch'], f'{name}: 스크롤 없음 {sc}'))
        pg.screenshot(path=f'{out}/{name}_main.png')
        pg.fill('#word', '가나다라'); pg.keyboard.press('Enter'); pg.clock.run_for(100)
        res.append(ok('표준국어대사전에 없는' in pg.inner_text('#status'), f'{name}: 사전에 없는 단어 거절 메시지'))
        pg.click('#infoBtn'); pg.clock.run_for(100)
        t = pg.inner_text('#infoDlg')
        res.append(ok(pg.is_visible('#infoDlg') and 'CC BY-SA 2.0 KR' in t and '표준국어대사전' in t, f'{name}: 출처 창에 라이선스 표시'))
        pg.screenshot(path=f'{out}/{name}_info.png')
        pg.click('#infoClose'); pg.clock.run_for(100)
        res.append(ok(not pg.is_visible('#infoDlg'), f'{name}: 출처 창 닫힘'))
        res.append(ok(not errs, f'{name}: 페이지 오류 없음 {errs}'))
        pg.close()
    b.close()
print('RESULT', 'ALL PASS' if all(res) else 'HAS FAIL')
