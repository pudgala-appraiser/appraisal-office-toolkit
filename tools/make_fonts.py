"""본명조 300·500을 인트로에 나오는 글자만 추려 woff2로 만든다.
문안을 고친 뒤 다시 돌린다.  쓰기: python tools/make_fonts.py   (저장소 맨 위에서)
원본 글꼴: Noto Serif CJK KR Light·Medium (SIL OFL 1.1)
"""
import re, os, html
from fontTools.ttLib import TTCollection
from fontTools import subset

SRC = '/usr/share/fonts/opentype/noto/NotoSerifCJK-%s.ttc'
PAGES = ['index.html', 'open-appraisal.html']
OUT = 'fonts'
os.makedirs(OUT, exist_ok=True)

def visible(s):
    s = re.sub(r'<(script|style)\b.*?</\1>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', s))

src = [open(p, encoding='utf-8').read() for p in PAGES]
ascii_ = {chr(c) for c in range(0x20, 0x7f)}
# 500: 화면에 보이는 글자 전부 + 인장·탁본 한자 (탁본은 스크립트가 그리므로 따로 적는다)
t500 = set(''.join(visible(s) for s in src)) | set('審査鑑規雁陣鷹眼') | ascii_
t500 = {c for c in t500 if c >= ' '}
# 300: data-thin을 붙인 요소(화면 이름, 목록의 한자)의 글자만
thin = ''.join(m for s in src for m in
               re.findall(r'<(?:h1|div|p|span)[^>]*\bdata-thin\b[^>]*>(.*?)</(?:h1|div|p|span)>', s, re.S))
t300 = set(visible(thin)) | {' '}

def kr_index(path):
    for i, f in enumerate(TTCollection(path).fonts):
        if (f['name'].getDebugName(16) or f['name'].getDebugName(1)) == 'Noto Serif CJK KR': return i
    raise SystemExit('KR face not found in ' + path)

def build(weight_name, text, dest):
    path = SRC % weight_name
    opt = subset.Options(); opt.flavor = 'woff2'; opt.font_number = kr_index(path)
    opt.layout_features = ['kern', 'locl']; opt.name_IDs = [1, 2]; opt.notdef_outline = True
    opt.desubroutinize = True
    font = subset.load_font(path, opt)
    sub = subset.Subsetter(opt); sub.populate(text=''.join(sorted(text))); sub.subset(font)
    subset.save_font(font, dest, opt)
    cm = font.getBestCmap()
    miss = ''.join(sorted(c for c in text if ord(c) not in cm))
    print(dest, os.path.getsize(dest), 'bytes,', len(cm), 'glyphs', '| 빠진 글자:', miss or '없음')

build('Light', t300, os.path.join(OUT, 'dasot-serif-300.woff2'))
build('Medium', t500, os.path.join(OUT, 'dasot-serif-500.woff2'))
print('thin:', ''.join(sorted(t300)))
