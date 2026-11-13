"""Checks for the faults the independent tester found in the trial version."""
import asyncio, os, json, datetime, subprocess
from playwright.async_api import async_playwright
URL = 'file:///home/claude/build/trial.html'
TODAY = datetime.date.today(); D = lambda n: (TODAY - datetime.timedelta(days=n)).isoformat()
EX = ['Kept the open day running when two staff were off sick, see https://example.com/a-very-long-address/that-goes-on-and-on-and-on-without-any-spaces-at-all-for-a-long-time',
      'Chose the new booking supplier the same day the quotes came in and told the team why.', 'Rebuilt the induction as two short calls when the room booking fell through.',
      'Told a team member the same afternoon that the report was late and when I needed it.', 'Rang each employer about the date change and asked them to say it back to me.',
      'Picked up the careers stand nobody owned and had it staffed by Friday. ' * 4]
PIDS = ['resilience', 'decisiveness', 'ingenuity', 'assertiveness', 'communication', 'enthusiasm']
errs = []; res = {}

async def head_scores(hp, name, scores):
    await hp.fill('#hn', name); await hp.tap('[data-a=ss-go][data-id="0"]')
    for i in range(6):
        box = await hp.locator('.sl').first.locator('.sl-track').bounding_box()
        await hp.touchscreen.tap(box['x'] + box['width'] * (scores[i] - 1) / 9, box['y'] + box['height'] / 2)
        await hp.fill('textarea[data-k=ex]', EX[i]); await hp.fill('input[data-k=d]', D(i + 1)); await hp.tap('[data-gate=self]')
    res.setdefault('phone review sideways scroll', await hp.evaluate('document.documentElement.scrollWidth>innerWidth+1'))
    await hp.tap('[data-a=ss-submit]'); return await hp.input_value('#sendlink')

async def james_scores(jp):
    for i, pid in enumerate(PIDS):
        await jp.locator(f'.sl[data-p={pid}]').scroll_into_view_if_needed()
        box = await jp.locator(f'.sl[data-p={pid}]').locator('.sl-track').bounding_box()
        await jp.mouse.click(box['x'] + box['width'] * 6 / 9, box['y'] + box['height'] / 2)
        await jp.fill(f'#jex-{pid}', 'A real thing I saw this month, written out in a sentence or two.'); await jp.fill(f'#jd-{pid}', D(i + 1))
    await jp.click('[data-a=j-lock]')

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        mk_phone = lambda: b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        # head A (Jordan) submits, then changes an answer: two links, old and new
        hc = await mk_phone(); hp = await hc.new_page(); hp.on('pageerror', lambda e: errs.append('H ' + str(e)))
        await hp.goto(URL + '?who=head'); link_old = await head_scores(hp, 'Jordan', [7, 8, 6, 5, 8, 9])
        res['phone send sideways scroll'] = await hp.evaluate('document.documentElement.scrollWidth>innerWidth+1')
        await hp.wait_for_timeout(30); await hp.tap('[data-a=unlock]'); await hp.tap('[data-a=ss-submit]'); link_new = await hp.input_value('#sendlink')
        res['resubmit wording'] = 'replaces the one you sent before' in await hp.inner_text('body'); assert link_new != link_old
        # head B types a name that matches nobody
        h2 = await mk_phone(); h2p = await h2.new_page(); await h2p.goto(URL + '?who=head'); link_jo = await head_scores(h2p, 'Jo', [6, 6, 6, 6, 6, 6])
        # James: tab A open, link opens in tab B
        jc = await b.new_context(viewport={'width': 1366, 'height': 850}, accept_downloads=True)
        A = await jc.new_page(); A.on('pageerror', lambda e: errs.append('A ' + str(e)))
        await A.goto(URL); await A.fill('#nh-n', 'Jordan Lee'); await A.click('[data-a=add-head]')
        B = await jc.new_page(); B.on('pageerror', lambda e: errs.append('B ' + str(e))); await B.goto(link_new); await B.wait_for_timeout(300)
        res['new tab loaded'] = 'stay hidden' in await B.inner_text('body')
        await A.bring_to_front(); await A.wait_for_timeout(300); await A.click('[data-a=menu]'); await A.click('[data-a=menu]')
        st = await A.evaluate("JSON.parse(localStorage.getItem('sccu-pillars-trial-v1'))")
        hd = list(st['heads'].values())[0]['cur']; res['old tab did not wipe'] = bool(hd['selfAt'] and hd.get('sealed'))
        res['old tab shows loaded'] = 'scores are loaded' in await A.inner_text('body')
        await B.close()
        # older link refused
        await A.goto(link_old); await A.wait_for_timeout(300); res['older link refused'] = 'older set' in await A.inner_text('body')
        # backup before the reveal holds no readable scores
        async with A.expect_download() as dl:
            await A.click('[data-a=menu]'); await A.click('[data-a=backup]')
        d = await dl.value; await d.save_as('/tmp/pre.json'); raw = open('/tmp/pre.json').read()
        res['pre-reveal backup hides examples'] = not any(e[:40] in raw for e in EX) and '"sealed"' in raw
        # James scores, unlocks, relocks
        await james_scores(A); res['ready after lock'] = 'Reveal both sets' in await A.inner_text('body')
        await A.click('[data-a=j-unlock]'); res['james can unlock'] = await A.locator('[data-a=j-lock]').count() == 1
        await A.click('[data-a=j-lock]')
        txt = await A.inner_text('body'); res['nothing leaks before reveal'] = not any(e[:40] in txt for e in EX)
        await A.click('[data-a=reveal]'); await A.wait_for_timeout(2600)
        await A.click('.xc-h >> nth=0'); txt = await A.inner_text('body'); res['examples appear after reveal'] = any(e[:40] in txt for e in EX)
        # link after reveal gives a visible message
        await A.goto(link_new); await A.wait_for_timeout(300); res['link after reveal message'] = 'already been revealed' in await A.inner_text('body')
        # finish and print
        await A.goto(URL + '#session'); order = await A.eval_on_selector_all('.xc-h h3', 'e=>e.map(x=>x.textContent)')
        for name in order:
            if await A.locator(f'.xc-h:has(h3:text-is("{name}"))[aria-expanded=true]').count() == 0: await A.click(f'.xc-h:has(h3:text-is("{name}"))')
            await A.click('[data-a=agree][data-id="7"]')
        await A.click('[data-a=stage][data-id=focus]'); await A.click('.ft:has(small:text-is("Suggested"))'); await A.click('[data-a=asg][data-id="0"]')
        await A.fill('#due', (TODAY + datetime.timedelta(days=28)).isoformat()); await A.click('[data-a=finish]'); await A.wait_for_timeout(400)
        await A.emulate_media(media='print'); await A.evaluate('fitPrint()')
        await A.pdf(path='/tmp/sum.pdf', prefer_css_page_size=True, print_background=True)
        out = subprocess.run(['pdfinfo', '/tmp/sum.pdf'], capture_output=True, text=True).stdout
        res['summary pdf pages'] = [l for l in out.splitlines() if l.startswith('Pages')][0]
        subprocess.run(['pdftoppm', '-r', '60', '-png', '/tmp/sum.pdf', '/tmp/sumprint'])
        res['picker hidden in print'] = not await A.locator('.hpick').is_visible(); await A.emulate_media(media='screen')
        # second head, unmatched name: James is asked whose it is
        await A.goto(URL + '#team'); await A.click('[data-a=new-head]'); await A.fill('#nh-n', 'Robin Shaw'); await A.click('[data-a=add-head]')
        await A.goto(URL + '#team'); await A.click('[data-a=new-head]'); await A.fill('#nh-n', 'Casey Ward'); await A.click('[data-a=add-head]')
        await A.goto(link_jo); await A.wait_for_timeout(300); txt = await A.inner_text('body'); res['unmatched name asks'] = 'Whose session are they for' in txt
        st = await A.evaluate("Object.values(S.heads).map(h=>[h.name,!!h.cur.selfAt])"); res['nothing loaded before choice'] = st[1][1] is False and st[2][1] is False
        await A.click('[data-a=assign] >> text=Robin Shaw'); st = await A.evaluate("Object.values(S.heads).map(h=>[h.name,!!h.cur.selfAt])"); res['assigned to chosen head'] = st[1][1] is True and st[2][1] is False
        await A.screenshot(path='/tmp/t2_assigned.png')
        # wrong backup file
        open('/tmp/wrong.json', 'w').write('{"hello":1}'); await A.set_input_files('#rf', '/tmp/wrong.json'); await A.wait_for_timeout(300)
        res['wrong backup message'] = "isn't a Leadership Pillars backup" in await A.inner_text('body')
        await A.set_input_files('#rf', '/tmp/pre.json'); await A.wait_for_timeout(300); res['restore message'] = 'Backup restored' in await A.inner_text('body')
        res['short example hint'] = 'example of a few words' in open('/home/claude/build/src.html').read()
        for k, v in res.items(): print(('OK  ' if v not in (False,) and not (k.endswith('sideways scroll') and v) else 'BAD ') + k + ': ' + str(v))
        print('errors', errs); await b.close()
asyncio.run(main())
