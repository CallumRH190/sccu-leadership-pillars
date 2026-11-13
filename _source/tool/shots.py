import asyncio, sys
from playwright.async_api import async_playwright
URL='file:///home/claude/build/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1366,'height':850})
        errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        n=[0]
        async def shot(name,full=True):
            n[0]+=1; await pg.wait_for_timeout(350); await pg.screenshot(path=f'shots/{n[0]:02d}-{name}.png',full_page=full)
        async def role(r):
            await pg.click('[data-a=menu]'); await pg.click(f'[data-a=role][data-id={r}]'); await pg.wait_for_timeout(150)
        await pg.goto(URL); await pg.wait_for_timeout(600)
        await shot('team-james')
        await pg.goto(URL+'#model'); await shot('model')
        await pg.click('[data-a=mopen][data-id=assertiveness]'); await shot('model-detail')
        # head: Elena self-score
        await role('elena'); await shot('self-intro')
        await pg.click('[data-a=ss-go][data-id="0"]'); await shot('self-empty',False)
        vals=[6,4,7,7,5,8]
        for i,v in enumerate(vals):
            sl=pg.locator('.sl').first; box=await sl.locator('.sl-track').bounding_box()
            await pg.mouse.click(box['x']+box['width']*(v-1)/9, box['y']+3)
            if i==0: await shot('self-scored-no-example',False)
            dis=await pg.locator('[data-gate=self]').is_disabled(); assert dis, 'next should be disabled without example'
            await pg.fill('textarea[data-k=ex]', f'Sample example number {i+1} for the month, something real that happened.')
            await pg.fill('input[data-k=d]','2026-11-0'+str(i+2))
            if i==1: await shot('self-step-4-between',False)
            if i==2: await shot('self-step-7',False)
            await pg.click('[data-gate=self]')
        await shot('self-review')
        await pg.click('[data-a=ss-submit]'); await shot('self-locked')
        await pg.goto(URL+'#profile'); await shot('profile-head-elena')
        await pg.goto(URL+'#summary'); await shot('summary-empty')
        await role('hannah'); await shot('hannah-first-use'); await pg.goto(URL+'#profile'); await shot('profile-empty')
        # James: Tom
        await role('james'); await pg.goto(URL+'#session'); await pg.click('[data-a=head][data-id=tom]'); await shot('session-score-empty')
        dis=await pg.locator('[data-gate=james]').is_disabled(); assert dis
        await pg.click('[data-a=j-fill]'); await shot('session-score-filled')
        await pg.click('[data-a=j-lock]'); await shot('session-reveal-pre')
        await pg.click('[data-a=review][data-id=part]')
        await pg.click('[data-a=reveal]'); await pg.wait_for_timeout(700); await pg.screenshot(path='shots/mid-reveal.png')
        await pg.wait_for_timeout(2500); await shot('session-revealed')
        order=await pg.eval_on_selector_all('.xc-h h3','e=>e.map(x=>x.textContent)'); print('gap order',order)
        agreed={'Resilience':6,'Decisiveness':7,'Ingenuity':6,'Assertiveness':6,'Communication':7,'Enthusiasm':8}
        first=True
        for name in order:
            await pg.click(f'.xc-h:has(h3:text-is("{name}"))')
            if first: await shot('session-explore-open'); first=False
            await pg.click(f'[data-a=agree][data-id="{agreed[name]}"]')
        await shot('session-all-agreed')
        await pg.click('[data-a=stage][data-id=focus]'); await shot('session-focus')
        sug=await pg.eval_on_selector('.ft:has(small:text-is("Suggested")) b','e=>e.textContent'); print('suggested',sug)
        await pg.click('.ft:has(small:text-is("Suggested"))'); await pg.click('[data-a=asg][data-id="0"]')
        assert await pg.locator('[data-gate=finish]').is_disabled()
        await pg.fill('#due','2026-12-09'); await shot('session-focus-set')
        await pg.click('[data-a=finish]'); await shot('summary-tom')
        await pg.goto(URL+'#profile'); await pg.wait_for_timeout(1500); await shot('profile-tom-james')
        await pg.goto(URL+'#team'); await shot('team-after')
        await pg.click('[data-a=sess][data-id=dev]'); await shot('session-dev-ready')
        await pg.click('[data-a=sess][data-id=elena]') if await pg.locator('[data-a=sess][data-id=elena]').count() else None
        await pg.click('[data-a=head][data-id=hannah]'); await shot('session-hannah')
        await role('priya'); await pg.goto(URL+'#summary'); await shot('summary-priya'); await pg.goto(URL+'#profile'); await pg.wait_for_timeout(1500); await shot('profile-priya')
        await role('scott'); await shot('team-scott')
        # tablet
        await pg.set_viewport_size({'width':820,'height':1100}); await role('dev'); await pg.goto(URL+'#self-score'); await shot('tablet-self-locked')
        await role('james'); await pg.goto(URL+'#session'); await pg.click('[data-a=head][data-id=dev]'); await shot('tablet-session')
        txt=await pg.content(); print('emdash in page:', '—' in txt)
        print('errors',errs)
        await b.close()
asyncio.run(main())
