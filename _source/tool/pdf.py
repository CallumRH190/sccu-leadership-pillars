import asyncio
from playwright.async_api import async_playwright
URL='file:///home/claude/build/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1000,'height':1400})
        await pg.goto(URL); await pg.click('[data-a=menu]'); await pg.click('[data-a=role][data-id=priya]')
        await pg.goto(URL+'#summary'); await pg.wait_for_timeout(1500)
        await pg.locator('.sheet').screenshot(path='shots/sheet-priya.png')
        h=await pg.eval_on_selector('.sheet','e=>e.offsetHeight')
        await pg.emulate_media(media='print')
        await pg.pdf(path='SCCU-Leadership-Pillars-Sample-Session-Summary.pdf',width='794px',height=f'{h+2}px',margin={'top':'0','right':'0','bottom':'0','left':'0'},print_background=True)
        print('sheet h',h)
        # reveal check for Dev at mid animation
        await pg.emulate_media(media='screen'); await pg.set_viewport_size({'width':1366,'height':850})
        await pg.click('[data-a=menu]'); await pg.click('[data-a=role][data-id=james]'); await pg.goto(URL+'#session'); await pg.click('[data-a=head][data-id=dev]')
        await pg.click('[data-a=reveal]'); await pg.wait_for_timeout(3000); await pg.screenshot(path='shots/reveal-dev.png')
        await b.close()
asyncio.run(main())
