"""Optional browser regression check. Install playwright and its Chromium first."""
import json, os, subprocess, time
from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
server = subprocess.Popen([os.sys.executable, 'manage.py', 'runserver', '127.0.0.1:8017', '--noreload'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(100):
        try:
            urlopen('http://127.0.0.1:8017/'); break
        except Exception: time.sleep(.1)
    with sync_playwright() as p:
        options = {'headless': True, 'args': ['--no-sandbox']}
        if os.environ.get('CHROMIUM_PATH'): options['executable_path'] = os.environ['CHROMIUM_PATH']
        browser = p.chromium.launch(**options)
        page = browser.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('response', lambda response: errors.append(str(response.status)+' '+response.url) if response.status >= 400 else None)
        report = []
        for width in [1920,1440,1366,1280,1024,768,430,390,375,360]:
            page.set_viewport_size({'width':width,'height':844 if width<768 else 1080 if width==1920 else 768})
            page.goto('http://127.0.0.1:8017/')
            page.wait_for_load_state('networkidle')
            # Detect overflow without the safety clipping rule.
            data = page.evaluate('''() => {
                document.documentElement.style.overflowX='visible'; document.body.style.overflowX='visible';
                const result={width:innerWidth,scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth,
                escaping:[...document.querySelectorAll('main *')].filter(e=>{const r=e.getBoundingClientRect();return r.width && (r.left < -1 || r.right>innerWidth+1)}).map(e=>e.className?.baseVal??e.className)};
                document.documentElement.style.overflowX=''; document.body.style.overflowX=''; return result;
            }''')
            assert data['scroll']==data['client'],data
            assert not data['escaping'],data
            assert page.locator('.hero-person').count()==1
            screen = page.locator('#laptop-screen')
            screen.scroll_into_view_if_needed()
            page.locator('[data-screen-next]').click()
            page.wait_for_timeout(650)
            assert screen.evaluate('(e)=>e.scrollTop') > 100
            page.locator('#screen-reset').click()
            page.wait_for_timeout(650)
            assert screen.evaluate('(e)=>e.scrollTop') < 2
            for key in ['team','expense','blinkit']:
                page.locator('#tab-'+key).click()
                assert page.locator('#preview-'+key).is_visible()
                assert screen.evaluate('(e)=>e.scrollWidth === e.clientWidth')
                screen.hover()
                before = page.evaluate('scrollY')
                page.mouse.wheel(0,180)
                page.wait_for_timeout(180)
                assert screen.evaluate('(e)=>e.scrollTop') > 0
                assert abs(page.evaluate('scrollY') - before) < 2
            page.locator('#tab-overview').click()
            page.locator('#tab-overview').focus()
            page.keyboard.press('ArrowRight')
            assert page.locator('#tab-team').get_attribute('aria-selected')=='true'
            page.keyboard.press('Home')
            assert page.locator('#tab-overview').get_attribute('aria-selected')=='true'
            assert screen.evaluate('(e)=>e.scrollTop') == 0
            if width < 1280:
                page.locator('#menu-toggle').click()
                assert page.locator('#main-nav').is_visible()
                page.locator('#main-nav a[href="#education"]').click()
                assert page.locator('#menu-toggle').get_attribute('aria-expanded')=='false'
            page.locator('#theme-toggle').click()
            assert page.locator('body').get_attribute('data-theme')=='dark'
            page.reload()
            assert page.locator('body').get_attribute('data-theme')=='dark'
            page.locator('#theme-toggle').click()
            page.locator('[data-filter="data"]').click()
            assert page.locator('.case-card:visible').count()==1
            page.locator('.case-card:visible .case-link').click()
            assert page.locator('#project-dialog').is_visible()
            page.keyboard.press('Escape')
            page.locator('[data-filter="all"]').click()
            assert page.locator('.case-card:visible').count()==3
            page.mouse.move(0,0)
            if width in [1920,1366,390]:
                page.locator('.showcase').screenshot(path=f'/tmp/laptop-showcase-{width}.png')
                screen.evaluate('(e)=>e.scrollTo({top:550,behavior:"instant"})')
                page.wait_for_timeout(200)
                page.locator('.showcase').screenshot(path=f'/tmp/laptop-scrolled-{width}.png')
                screen.evaluate('(e)=>e.scrollTo({top:0,behavior:"instant"})')
            page.evaluate('scrollTo({top:0,behavior:"instant"})');page.wait_for_timeout(350)
            if width in [1920,1366,390]: page.screenshot(path=f'/tmp/laptop-hero-{width}.png')
            report.append(data)
        # Touch scrolling on a mobile viewport.
        mobile = browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        touch = mobile.new_page();touch.goto('http://127.0.0.1:8017/')
        touch.locator('#laptop-screen').scroll_into_view_if_needed()
        rect = touch.locator('#laptop-screen').bounding_box()
        client = mobile.new_cdp_session(touch)
        x = rect['x']+rect['width']/2;y=rect['y']+rect['height']*.75
        client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
        for step in range(1,11):
            client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y-step*15}]})
            touch.wait_for_timeout(15)
        client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        touch.wait_for_timeout(300)
        assert touch.locator('#laptop-screen').evaluate('(e)=>e.scrollTop') > 0
        mobile.close()
        # Reduced-motion behavior.
        page.emulate_media(reduced_motion='reduce')
        page.goto('http://127.0.0.1:8017/')
        assert page.locator('#laptop-screen').evaluate('(e)=>getComputedStyle(e).scrollBehavior')=='auto'
        assert page.locator('#laptop').evaluate('(e)=>getComputedStyle(e).transform')=='none'
        assert not errors,errors
        print(json.dumps({'viewports':report,'browser_errors':errors,'interactions':'menu, theme persistence, filters, dialogs, preview tabs, arrow-key navigation, internal wheel scrolling, screen reset, touch swipe and reduced motion passed'},indent=2))
        browser.close()
finally:
    server.terminate();server.wait()
