"""Full run-through of the trial version: James on a laptop, the head on a phone."""
import asyncio, os, json, datetime
from playwright.async_api import async_playwright
URL = 'file:///home/claude/build/trial.html'
OUT = 'trial_shots'; os.makedirs(OUT, exist_ok=True)
TODAY = datetime.date.today(); D = lambda n: (TODAY - datetime.timedelta(days=n)).isoformat()
HEAD_EX = ['Kept the open day running when two staff were off sick and nobody outside the team noticed.',
           'Chose the new booking supplier the same day the quotes came in and told the team why.',
           'Rebuilt the induction as two short calls when the room booking fell through.',
           'Told a team member the same afternoon that the report was late and when I needed it.',
           'Rang each employer about the date change and asked them to say it back to me.',
           'Picked up the careers stand nobody owned and had it staffed by Friday.']
HEAD_SC = [7, 8, 6, 5, 8, 9]
J_EX = ['Stayed level in the Monday meeting the morning the two absences landed.', 'Supplier decision made and closed inside the week.',
        'The two-call induction was a neat fix, but it came from the team, not from them.', 'The late report was raised the same day. Clear and direct.',
        'Employers knew the new date before I did.', 'Careers stand picked up without being asked.']
J_SC = [7, 8, 5, 7, 7, 8]
errs = []; n = [0]

async def shot(pg, name, full=True):
    n[0] += 1; await pg.wait_for_timeout(300); await pg.screenshot(path=f'{OUT}/{n[0]:02d}-{name}.png', full_page=full)

async def set_slider(pg, sel, v):
    box = await pg.locator(sel).locator('.sl-track').bounding_box()
    await pg.mouse.click(box['x'] + box['width'] * (v - 1) / 9, box['y'] + box['height'] / 2)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        # ---------- James, laptop
        jc = await b.new_context(viewport={'width': 1366, 'height': 850}, accept_downloads=True); jp = await jc.new_page()
        jp.on('pageerror', lambda e: errs.append('J ' + str(e))); jp.on('console', lambda m: errs.append('J ' + m.text) if m.type == 'error' else None)
        await jp.goto(URL); await shot(jp, 'j-setup')
        assert await jp.locator('[data-gate=newhead]').is_disabled()
        await jp.fill('#nh-n', 'Jordan Lee'); await jp.fill('#nh-d', 'Futures'); await jp.click('[data-a=add-head]'); await shot(jp, 'j-session-invite')
        link = await jp.input_value('#inv'); print('head link', link); assert link.endswith('trial.html?who=head')
        # ---------- the head, phone
        hc = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True); hp = await hc.new_page()
        hp.on('pageerror', lambda e: errs.append('H ' + str(e))); hp.on('console', lambda m: errs.append('H ' + m.text) if m.type == 'error' else None)
        await hp.goto(link); await shot(hp, 'h-intro')
        assert await hp.locator('[data-gate=hname]').is_disabled(), 'start should need a name'
        await hp.fill('#hn', 'Jordan'); await hp.tap('[data-a=ss-go][data-id="0"]'); await shot(hp, 'h-pillar-empty')
        for i in range(6):
            sl = hp.locator('.sl').first; box = await sl.locator('.sl-track').bounding_box()
            await hp.touchscreen.tap(box['x'] + box['width'] * (HEAD_SC[i] - 1) / 9, box['y'] + box['height'] / 2)
            assert await hp.locator('[data-gate=self]').is_disabled()
            await hp.fill('textarea[data-k=ex]', HEAD_EX[i]); await hp.fill('input[data-k=d]', D(i + 1))
            if i in (0, 3): await shot(hp, f'h-pillar-{i+1}')
            await hp.tap('[data-gate=self]')
        await shot(hp, 'h-review'); await hp.tap('[data-a=ss-submit]'); await shot(hp, 'h-send')
        send_link = await hp.input_value('#sendlink'); code = await hp.input_value('#sendcode')
        print('code length', len(code), 'link length', len(send_link)); assert code.startswith('LP1.') and '#code=LP1.' in send_link
        over = await hp.evaluate('document.documentElement.scrollWidth>innerWidth+1'); print('phone sideways scroll:', over)
        await hp.tap('[data-a=share]'); await shot(hp, 'h-send-copied', False)
        # the head reloads and still has the link
        await hp.reload(); assert (await hp.input_value('#sendcode')) == code
        # ---------- James scores blind
        for i, pid in enumerate(['resilience', 'decisiveness', 'ingenuity', 'assertiveness', 'communication', 'enthusiasm']):
            await jp.locator(f'.sl[data-p={pid}]').scroll_into_view_if_needed(); await set_slider(jp, f'.sl[data-p={pid}]', J_SC[i])
            await jp.fill(f'#jex-{pid}', J_EX[i]); await jp.fill(f'#jd-{pid}', D(i + 1))
        await jp.click('[data-a=j-lock]'); await shot(jp, 'j-wait')
        txt = await jp.inner_text('body'); assert not any(e in txt for e in HEAD_EX), 'head examples visible before load'
        # ---------- the link arrives
        await jp.goto(send_link); await jp.wait_for_timeout(400); await shot(jp, 'j-loaded-ready')
        txt = await jp.inner_text('body'); assert 'stay hidden' in txt and not any(e in txt for e in HEAD_EX), 'examples leaked before reveal'
        assert '#code' not in jp.url, jp.url
        await jp.click('[data-a=reveal]'); await jp.wait_for_timeout(3000); await shot(jp, 'j-revealed')
        order = await jp.eval_on_selector_all('.xc-h h3', 'e=>e.map(x=>x.textContent)'); print('gap order', order)
        first = True
        for name in order:
            await jp.click(f'.xc-h:has(h3:text-is("{name}"))')
            if first: await shot(jp, 'j-explore'); first = False
            await jp.click('[data-a=agree][data-id="7"]')
        await jp.click('[data-a=stage][data-id=focus]'); await jp.click('.ft:has(small:text-is("Suggested"))'); await jp.click('[data-a=asg][data-id="0"]')
        await jp.fill('#due', (TODAY + datetime.timedelta(days=28)).isoformat()); await jp.click('[data-a=finish]'); await shot(jp, 'j-summary')
        txt = await jp.inner_text('body'); assert 'Integrity' not in txt, 'integrity placeholder shown in trial'
        async with jp.expect_download() as dl:
            await jp.click('[data-a=backup]')
        d = await dl.value; await d.save_as('/tmp/trial-backup.json'); bk = json.load(open('/tmp/trial-backup.json')); print('backup heads', [h['name'] for h in bk['heads'].values()], d.suggested_filename)
        await jp.goto(URL + '#profile'); await jp.wait_for_timeout(1300); await shot(jp, 'j-profile')
        txt = await jp.inner_text('body'); assert '94%' not in txt and 'Integrity' not in txt, 'placeholder results shown in trial'
        await jp.goto(URL + '#team'); await shot(jp, 'j-team')
        await jp.click('[data-a=menu]'); await shot(jp, 'j-menu', False); await jp.click('[data-a=role][data-id=scott]'); await shot(jp, 's-team')
        # ---------- second head: link arrives before the head exists, then paste route
        await jp.click('[data-a=menu]'); await jp.click('[data-a=role][data-id=james]')
        await jp.click('[data-a=menu]'); await jp.click('[data-a=new-head]'); await shot(jp, 'j-add-another')
        await jp.fill('#nh-n', 'Robin Shaw'); await jp.click('[data-a=add-head]')
        await jp.fill('#code', 'not a code'); await jp.click('[data-a=load-code]'); assert "doesn't look like" in await jp.inner_text('body')
        code2 = await hp.evaluate("(()=>{const s=JSON.parse(localStorage.getItem('sccu-pillars-trial-head-v1'));s.heads.me.name='Robin';localStorage.setItem('sccu-pillars-trial-head-v1',JSON.stringify(s));return true})()")
        await hp.reload(); code_robin = await hp.input_value('#sendcode')
        await jp.fill('#code', code_robin); await jp.click('[data-a=load-code]'); await shot(jp, 'j-pasted')
        st = await jp.evaluate("Object.values(S.heads).map(h=>[h.name,!!h.cur.selfAt,h.cur.done])"); print('heads now', st)
        assert st[1][1] is True
        # ---------- fresh browser: link first, then set up, then restore
        fc = await b.new_context(viewport={'width': 1366, 'height': 850}); fp = await fc.new_page(); fp.on('pageerror', lambda e: errs.append('F ' + str(e)))
        await fp.goto(send_link); await fp.wait_for_timeout(300); await shot(fp, 'f-link-before-setup')
        assert 'have arrived' in await fp.inner_text('body')
        await fp.fill('#nh-n', 'Jordan Lee'); await fp.click('[data-a=add-head]'); assert 'stay hidden' in await fp.inner_text('body')
        await fp.set_input_files('#rf', '/tmp/trial-backup.json'); await fp.wait_for_timeout(400)
        st = await fp.evaluate("Object.values(S.heads).map(h=>[h.name,h.cur.done])"); print('after restore', st); assert st == [['Jordan Lee', True]]
        await fp.click('[data-a=menu]'); await fp.click('[data-a=clear]'); assert 'Click again' in await fp.inner_text('body'); await fp.click('[data-a=clear]')
        assert await fp.evaluate("Object.keys(S.heads).length") == 0
        # ---------- head changes their mind, and starts again
        await hp.tap('[data-a=unlock]'); await shot(hp, 'h-unlocked'); await hp.tap('[data-a=ss-submit]')
        await hp.tap('[data-a=menu]'); await hp.tap('[data-a=clear]'); await hp.tap('[data-a=clear]'); await shot(hp, 'h-cleared')
        assert await hp.locator('#hn').count() == 1
        # ---------- the head on a laptop, and the demo is untouched
        lc = await b.new_context(viewport={'width': 1366, 'height': 850}); lp = await lc.new_page(); await lp.goto(link); await shot(lp, 'h-intro-laptop')
        for pg, nm in ((jp, 'manager'), (hp, 'head')):
            html = await pg.content(); print(nm, 'em-dash', '—' in html)
        demo = await b.new_context(); dp = await demo.new_page(); await dp.goto('file:///home/claude/build/index.html'); await dp.wait_for_timeout(300)
        print('demo heads', await dp.evaluate("Object.keys(S.heads).length"), 'demo pill', await dp.inner_text('.pill'))
        print('errors', errs); await b.close()
asyncio.run(main())
