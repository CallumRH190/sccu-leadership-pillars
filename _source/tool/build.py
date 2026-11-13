import base64
fonts=[('Comfortaa','comfortaa',w) for w in (400,600,700)]+[('Nunito Sans','nunito-sans',w) for w in (400,600,700,800)]
css=''
for fam,slug,w in fonts:
    b=base64.b64encode(open(f'node_modules/@fontsource/{slug}/files/{slug}-latin-{w}-normal.woff2','rb').read()).decode()
    css+=f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;font-display:swap;src:url(data:font/woff2;base64,{b}) format('woff2')}}\n"
s=open('src.html').read().replace('/*FONTS*/',css)
open('index.html','w').write(s); print(len(s)//1024,'KB')
