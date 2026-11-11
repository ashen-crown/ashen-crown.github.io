"""Make the share thumbnails (img/og.jpg, img/og-en.jpg) and site icons from existing art.
Run once after the key art or logo changes: python tools/make_images.py [path-to-app-icon.png]
The app icon defaults to the game's own icon in work/CURRENT/public/ui/title/app-icon.png.
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
ICON_SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "CURRENT/public/ui/title/app-icon.png"


def cover(im, w, h, fx=0.62, fy=0.45):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx)
    y = round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def og(logo_name, out_name):
    W, H = 1200, 630
    bg = cover(Image.open(IMG / "hero-bg.webp").convert("RGB"), W, H)
    shade = Image.new("L", (W, H))
    d = ImageDraw.Draw(shade)
    for x in range(W):  # dark on the left where the logo sits, fading to the right
        d.line([(x, 0), (x, H)], fill=round(215 * max(0.0, 1 - x / (W * 0.78))))
    dark = Image.new("RGB", (W, H), (20, 17, 15))
    bg = Image.composite(dark, bg, shade)
    logo = Image.open(IMG / logo_name).convert("RGBA")
    lw = 560
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    bg.paste(logo, (64, (H - logo.height) // 2), logo)
    bg.save(IMG / out_name, "JPEG", quality=86, optimize=True, progressive=True)
    print("wrote img/" + out_name, bg.size)


def icons():
    src = Image.open(ICON_SRC).convert("RGBA")
    side = min(src.size)
    src = src.crop(((src.width - side) // 2, (src.height - side) // 2, (src.width + side) // 2, (src.height + side) // 2))
    for size, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
        im = src.resize((size, size), Image.LANCZOS)
        if name == "apple-touch-icon.png":  # iOS shows transparency as black; flatten on the page color
            flat = Image.new("RGB", im.size, (20, 17, 15))
            flat.paste(im, (0, 0), im)
            im = flat
        im.save(IMG / name, optimize=True)
        print("wrote img/" + name)
    src.resize((64, 64), Image.LANCZOS).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote favicon.ico")
    manifest = {
        "name": "Ashen Crown 애션 크라운", "short_name": "Ashen Crown", "start_url": "/", "display": "browser",
        "background_color": "#14110f", "theme_color": "#14110f",
        "icons": [{"src": "/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/img/icon-512.png", "sizes": "512x512", "type": "image/png"}],
    }
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote site.webmanifest")


og("logo-ko.webp", "og.jpg")
og("logo-en.webp", "og-en.jpg")
icons()
