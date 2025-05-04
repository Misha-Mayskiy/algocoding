import asyncio
from collections import defaultdict
from PIL import Image, UnidentifiedImageError


async def process_image(fname):
    print(f'Start {fname}')
    try:
        img = Image.open(fname).convert('RGB')
    except (FileNotFoundError, UnidentifiedImageError):
        print(f'Done {fname}, percent 0')
        print(f'Done {fname}, amount 0')
        print(f'Done {fname}, quarter I')
        return fname, 0, 0, 'I'

    w, h = img.size
    total = w * h
    px = img.load()

    s = sum(sum(px[x, y]) for y in range(h) for x in range(w))
    await asyncio.sleep(0.1)
    avg = s / total

    bright = 0
    freq = defaultdict(int)
    quad = {'I': 0, 'II': 0, 'III': 0, 'IV': 0}
    mx, my = w / 2, h / 2

    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            br = r + g + b
            if br > avg:
                bright += 1
                freq[br] += 1
                if x >= mx and y < my:
                    quad['I'] += 1
                elif x < mx and y < my:
                    quad['II'] += 1
                elif x < mx and y >= my:
                    quad['III'] += 1
                else:
                    quad['IV'] += 1

    percent = (max(freq.values()) * 1000) // bright if bright else 0
    print(f'Done {fname}, percent {percent}')

    amount = (bright * 100) // total if total else 0
    print(f'Done {fname}, amount {amount}')

    quarter = min(('I', 'II', 'III', 'IV'), key=lambda q: (-quad[q], q))
    print(f'Done {fname}, quarter {quarter}')

    return fname, percent, amount, quarter


async def asteroids(*files):
    results = await asyncio.gather(*(process_image(f) for f in files))
    for f in files:
        print(f'Ready {f}')
    return results
