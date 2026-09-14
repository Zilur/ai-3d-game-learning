"""Optional browser test. Requires playwright and an installed Chromium.
Uses set_content so it does not depend on local file:// browser policy.
Run: python tools/test_web.py
No screenshots or personal data are committed.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import math,json
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=__import__('shutil').which('chromium'),headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1180,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((ROOT/'web/space-lab.html').read_text(encoding='utf-8'))
 assert page.evaluate('labMath.state().world') == [4,0,0]
 page.locator('#parentYaw').fill('90');page.locator('#parentYaw').dispatch_event('input')
 before=page.evaluate('labMath.state().world')
 page.locator('#parentStep').click()
 after=page.evaluate('labMath.state().world')
 assert abs(after[0]-before[0])<1e-8 and abs(after[2]-before[2]+1)<1e-8
 before=after;page.locator('#worldStep').click();after=page.evaluate('labMath.state().world')
 assert abs(after[0]-before[0]-1)<1e-8 and abs(after[2]-before[2])<1e-8
 before=after;page.locator('#selfStep').click();after=page.evaluate('labMath.state().world')
 assert abs(after[0]-before[0]+math.sqrt(.5))<1e-8
 page.locator('#explain').click();assert '先写' in page.locator('#feedback').inner_text()
 page.locator('#prediction').fill('沿自身轴要考虑父节点和自身旋转。');page.locator('#explain').click()
 assert 'position在父空间' in page.locator('#feedback').inner_text()
 page.locator('#doorTab').click();page.locator('#doorAngle').fill('90');page.locator('#doorAngle').dispatch_event('input')
 assert '左下角世界位置 = (0.00, 0.00, 0.00)' in page.locator('#readout').inner_text()
 page.locator('#pivot').select_option('center')
 assert '左下角世界位置 = (1.00, 0.00, 1.00)' in page.locator('#readout').inner_text()
 page.locator('#reset').click();assert '角度 0°' in page.locator('#readout').inner_text()
 page.set_viewport_size({'width':390,'height':844})
 assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
 assert not errors,errors
 print('PASS browser: initial transform, parent/self/world displacement, prediction gate, hinge/centre pivot, reset, mobile width, no JS errors.')
 b.close()
