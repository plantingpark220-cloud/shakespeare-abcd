"""產生 26 張印象派筆觸風格油畫 (images/*.jpg)。需要: pip install pillow numpy
執行: python gen_images.py   ——想要新構圖可改下方 SCENES 或換 seed"""
import json, random, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter
W, H = 1200, 800
src = open('data.js', encoding='utf8').read()
WORDS = json.loads(src[src.index('['):src.rindex(']') + 1])
h = lambda x: tuple(int(x[i:i+2], 16) for i in (1, 3, 5))
mix = lambda a, b, t: tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
# 天空上/下, 地面上/下, 地平線高度, 太陽或月亮(x,y,半徑,色), 地形, 元素
SCENES = {
'A': ('#6fa8d6','#f8e8c6','#2f6f9e','#a5cbd9',.55,(.75,.3,48,'#fff3c4'),'water','boats hills'),
'B': ('#2c2f5a','#8a6f9c','#1c2b4a','#4a557e',.5,(.3,.25,36,'#e8e4d0'),'water','hills stars'),
'C': ('#b8c4bc','#e4e6dc','#5f7a5a','#9fb09a',.52,None,'path','trees'),
'D': ('#e8a3a8','#f8d9b8','#4d6b45','#7a9a5a',.5,(.7,.22,34,'#fff6e0'),'field','trees flowers:#f4f0ea'),
'E': ('#2d2a63','#f09a54','#3b3f6e','#c9786a',.55,(.5,.55,40,'#ffd69a'),'water','hills'),
'F': ('#8fb4d0','#f2e2b4','#b08a3c','#d9b25e',.5,None,'path','trees hills'),
'G': ('#cfe6ee','#fdf6e2','#9cc59a','#e4efc6',.55,(.8,.2,60,'#fffbe8'),'field','flowers:#ffffff flowers:#f6e3f0'),
'H': ('#7fc0e0','#fbe7b0','#3a86b5','#bfe1e4',.52,(.5,.35,55,'#fff1b0'),'water','boats'),
'I': ('#7b1e2e','#f2703c','#7a2236','#d4503a',.55,(.5,.5,70,'#ffd27a'),'water','hills'),
'J': ('#f2a8b6','#fff0c0','#6c9a5c','#b6c878',.55,(.5,.55,44,'#fff6c8'),'field','hills flowers:#f6c84a'),
'K': ('#3e4a6e','#a9a8b8','#2e3a4a','#62687e',.55,None,'path','trees stars'),
'L': ('#0f1e4a','#3a5a9a','#10224e','#35569a',.58,(.65,.2,26,'#fffbe0'),'water','stars'),
'M': ('#8e78b8','#f6c6a4','#6b9a5e','#c9c27a',.55,(.35,.56,46,'#ffe3a0'),'field','flowers:#e8d85a hills'),
'N': ('#5cc0d8','#fdf0cc','#1f9aa8','#8fdac8',.5,(.78,.25,50,'#fff4c0'),'water','hills trees flowers:#e8506a'),
'O': ('#1e2b5a','#5a6aa0','#1c2c52','#4c5f96',.52,(.28,.22,34,'#f6f2da'),'water','trees'),
'P': ('#141a4a','#6a4f9a','#171f55','#5b4f94',.5,(.72,.28,30,'#f2eed8'),'water','stars'),
'Q': ('#c8a46a','#f6e2a8','#8a6a3a','#cfae6a',.55,(.5,.3,70,'#fff6d0'),'field','hills'),
'R': ('#a8d4e8','#f2f0d0','#4e8a4a','#9cc058',.35,(.85,.15,40,'#fff8d0'),'field','flowers:#e8d24a flowers:#7a9a3a flowers:#ffffff'),
'S': ('#a8c4d8','#f6dcaa','#c0782a','#e8b43e',.5,(.78,.28,40,'#fff0c0'),'field','trees hills flowers:#c0502a'),
'T': ('#4a5568','#a2adb4','#2a3a4e','#6a7e90',.5,None,'water','boats hills'),
'U': ('#5a5a9a','#f0b890','#3a4a7a','#c88a8a',.6,(.5,.58,30,'#ffe0b0'),'water','hills'),
'V': ('#c4d4ec','#f8ecdc','#7aa4c4','#d4e4ec',.55,(.3,.25,30,'#ffffff'),'water','trees flowers:#ffffff'),
'W': ('#4a3a6a','#e69a92','#3a5a42','#7a9a62',.5,(.78,.2,32,'#f8f0d8'),'field','trees flowers:#e8506a flowers:#f4a0b0'),
'X': ('#a82a1e','#f6a038','#6a3a2a','#d0602a',.5,(.25,.3,46,'#ffe19a'),'field','hills flowers:#d62a1e'),
'Y': ('#5fb4e0','#f4f0dc','#2c78b2','#9cd0e0',.55,(.8,.18,40,'#fffbe0'),'water','ship'),
'Z': ('#1f6fc2','#9fd4f0','#1f78b4','#6cc4e0',.55,(.5,.1,60,'#fffde6'),'water','boats'),
}
def guide(S):
    sk, sb, ga, gb, hz, sun, kind, ex = S
    hz = int(H * hz); g = Image.new('RGB', (W, H)); d = ImageDraw.Draw(g)
    for y in range(H):
        c = mix(h(sk), h(sb), y / hz) if y < hz else mix(h(ga), h(gb), (y - hz) / (H - hz))
        d.line([(0, y), (W, y)], fill=tuple(int(v) for v in c))
    tok = ex.split()
    if 'stars' in tok:
        for _ in range(90): x, y = random.randrange(W), random.randrange(int(hz * .8)); d.ellipse((x, y, x + 3, y + 3), fill=(255, 250, 220))
    if sun:
        x, y, r, c = sun; x *= W; y *= H
        for k in range(10, 0, -1):
            rr = r * (1 + k * .45); d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=tuple(int(v) for v in mix(h(sb), h(c), 1 - k / 10)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=h(c))
        if kind == 'water':
            for _ in range(160):
                yy = random.randrange(hz + 6, H); w = 8 + (yy - hz) * .12
                xx = x + random.gauss(0, 30 + (yy - hz) * .1); d.line([(xx - w, yy), (xx + w, yy)], fill=h(c), width=3)
    if 'hills' in tok:
        col = tuple(int(v) for v in mix(h(sb), h(ga), .55)); pts = [(0, hz)]
        for x in range(0, W + 20, 20): pts.append((x, hz - 40 - 30 * math.sin(x / 170 + random.random()) - 20 * math.sin(x / 63)))
        d.polygon(pts + [(W, hz), (0, hz)], fill=col)
    if kind == 'path':
        d.polygon([(W * .46, hz), (W * .54, hz), (W * .85, H), (W * .15, H)], fill=tuple(int(v) for v in mix(h(gb), (255, 245, 215), .45)))
    for t in tok:
        if t.startswith('flowers'):
            col = h(t.split(':')[1])
            for _ in range(700):
                x = random.randrange(W); y = random.randrange(hz + 10, H); s = 2 + (y - hz) / 60
                d.ellipse((x, y, x + s * 2, y + s * 2), fill=col)
    if 'trees' in tok:
        for x0 in (.08, .2, .9, .78):
            x = x0 * W; b = hz + 60 * random.random() + 20; th = random.randint(220, 330); d.line([(x, b), (x, b - th * .55)], fill=(70, 50, 40), width=14)
            for _ in range(26):
                a, rr = random.uniform(0, 6.28), random.uniform(0, 70)
                cx, cy = x + math.cos(a) * rr, b - th * .65 + math.sin(a) * rr * .8
                d.ellipse((cx - 46, cy - 38, cx + 46, cy + 38), fill=tuple(int(v) for v in mix(h(ga), (20, 40, 30), random.uniform(.15, .55))))
    def boat(x, y, s):
        d.ellipse((x - 40 * s, y - 6 * s, x + 40 * s, y + 12 * s), fill=(60, 45, 40))
        d.polygon([(x - 4 * s, y - 4 * s), (x - 4 * s, y - 70 * s), (x - 36 * s, y - 8 * s)], fill=(250, 244, 230))
        d.polygon([(x + 4 * s, y - 4 * s), (x + 4 * s, y - 85 * s), (x + 40 * s, y - 8 * s)], fill=(240, 224, 200))
    if 'boats' in tok:
        for _ in range(4): boat(random.randint(100, W - 100), hz + random.randint(10, 90), random.uniform(.6, 1.2))
    if 'ship' in tok:
        boat(430, hz + 150, 3.2); boat(900, hz + 40, 1.2)
    return g
def paint(g, kind, hz):
    a = np.array(g.filter(ImageFilter.GaussianBlur(2)), dtype=float); hz = int(H * hz)
    img = Image.new('RGB', (W, H), (210, 196, 170)); d = ImageDraw.Draw(img)
    for size, cnt in ((30, 2500), (16, 9000), (9, 20000), (5, 34000)):
        for _ in range(cnt):
            x, y = random.randrange(W), random.randrange(H)
            c = a[y, x] + np.random.normal(0, 9, 3)
            if random.random() < .08: c = c * .75 + np.array([255, 205, 130]) * .25
            ang = random.gauss(-.1, .25) if y < hz else (random.gauss(0, .08) if kind == 'water' else random.gauss(1.57, .5))
            L = size * random.uniform(.8, 1.8); dx, dy = math.cos(ang) * L, math.sin(ang) * L
            d.line((x - dx, y - dy, x + dx, y + dy), fill=tuple(int(max(0, min(255, v))) for v in c), width=max(2, int(size * .55)))
    arr = np.array(img, dtype=float) + np.random.normal(0, 4, (H, W, 1))
    return Image.fromarray(np.clip(arr, 0, 255).astype('uint8'))
for e in WORDS:
    random.seed(ord(e['l'])); np.random.seed(ord(e['l']))
    S = SCENES[e['l']]; img = paint(guide(S), S[6], S[4])
    img.save(f"images/{e['l'].lower()}_{e['s']}.jpg", quality=90); print(e['l'], e['s'])
