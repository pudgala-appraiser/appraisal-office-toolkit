"""홈 화면 아이콘 세 종을 만든다 — 흰 바탕에 네 도구의 인장(審 흑 · 査 대추 · 鑑 하늘빛 · 規 치자).
도구의 벌이 바뀌면 SEALS의 색을 고치고 다시 돌린다.  쓰기: python tools/make_icons.py   (저장소 맨 위에서)
필요: playwright, 크롬, Noto Serif CJK KR Medium
"""
from playwright.sync_api import sync_playwright

SEALS = [('審', '#000000', '#ece9e2'), ('査', '#8a1c1c', '#ffffff'),
         ('鑑', '#8fcbf7', '#0e2233'), ('規', '#f0c544', '#17140a')]
OUT = [('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180)]

def svg(px):
    m, g = 64, 32                      # 512 기준 바깥 여백, 인장 사이
    s = (512 - 2 * m - g) / 2          # 인장 한 변
    cells = ''
    for i, (ch, bg, fg) in enumerate(SEALS):
        x, y = m + (i % 2) * (s + g), m + (i // 2) * (s + g)
        cells += (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{bg}"/>'
                  f'<text x="{x + s / 2}" y="{y + s * 46 / 64}" font-size="{s * 38 / 64}" fill="{fg}" '
                  f'text-anchor="middle" font-family="Noto Serif CJK KR" font-weight="500">{ch}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 512 512">'
            f'<rect width="512" height="512" fill="#ffffff"/>{cells}</svg>')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for name, px in OUT:
        pg = b.new_page(viewport={'width': px, 'height': px})
        pg.set_content(f'<body style="margin:0">{svg(px)}</body>')
        pg.wait_for_timeout(200)
        pg.screenshot(path=name, clip={'x': 0, 'y': 0, 'width': px, 'height': px})
        print(name, px)
    b.close()
