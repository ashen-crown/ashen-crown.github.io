"""Build index.html (Korean) and en/index.html (English) from tools/page.template.html.

The template carries both languages as lang="ko" / lang="en" twins.
Each output keeps only its own language so search engines index clean pages.
Run: python3 tools/build.py
"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://ashen-crown.github.io/"
TEMPLATE = (ROOT / "tools/page.template.html").read_text(encoding="utf-8")

META = {
    "ko": {
        "url": BASE,
        "title": "Ashen Crown 애션 크라운 | 수집형 RPG · 외부 시험 참가 모집",
        "description": "Ashen Crown(애션 크라운)은 동료 다섯과 실시간 전투를 지휘하고, 1인칭 유물 던전을 직접 탐험하고, 동료 10명으로 레이드 보스에 도전하고, 영토를 다스리는 PC 수집형 RPG입니다. 혼자 플레이하는 게임이며 외부 시험 참가자를 모집합니다.",
        "keywords": "Ashen Crown, 애션 크라운, 에션 크라운, 에센 크라운, 수집형 RPG, 스팀 RPG, 인디 게임, 외부 시험, 베타 테스트",
        "og_title": "Ashen Crown 애션 크라운 | 수집형 RPG",
        "og_description": "직접 걸어 들어가는 1인칭 유물 던전, 동료 10명으로 맞서는 레이드, 영토 경영, 날아오는 공격을 막아 내는 전투. 외부 시험 참가자 모집 중.",
        "locale": "ko_KR", "alt_locale": "en_US",
        "ld_description": "실시간 파티 전투, 1인칭 유물 던전 탐험, 동료 10명 레이드, 영토 경영을 갖춘 싱글 플레이 수집형 RPG.",
        "nav": "메뉴", "dialog": "스크린샷",
    },
    "en": {
        "url": BASE + "en/",
        "title": "Ashen Crown | Free-to-Play Collectible RPG · Playtest Sign-ups Open",
        "description": "Ashen Crown is a single-player, free-to-play collectible RPG for PC: lead five companions in real-time battles, explore relic dungeons in first person, face raid bosses with ten companions, and rule your own lands. Coming to Steam. Playtest sign-ups are open.",
        "keywords": "Ashen Crown, collectible RPG, gacha RPG, Steam RPG, indie game, free to play, playtest, beta test",
        "og_title": "Ashen Crown | Collectible RPG",
        "og_description": "First-person relic dungeons, ten-companion raids, territory to rule, and battles where you block what comes flying. Playtest sign-ups open.",
        "locale": "en_US", "alt_locale": "ko_KR",
        "ld_description": "A single-player collectible RPG with real-time party battles, first-person relic dungeons, ten-companion raids and territory management.",
        "nav": "Menu", "dialog": "Screenshot",
    },
}

ALT_EN = {
    "3장 전투 시작 화면": "Chapter 3 battle intro screen",
    "급습 경고가 뜬 전투": "Battle with an ambush warning",
    "네임드 몬스터 전투": "Battle against a named monster",
    "대장간 화면: 대장장이 볼드린, 강화할 동료, 에픽 무기가 끼워진 장비 칸": "Forge screen: Boldrin the smith, companions to upgrade, and an equipped Epic weapon",
    "로비 화면: 안내인 미라와 다음 여정, 요일 던전, 주간 보스, 결전 레이드, 유물 던전, 투기장 메뉴": "Lobby: guide Mira, the next journey, weekday dungeons, weekly boss, raid, relic dungeon and arena",
    "보른 앞에 세운 방벽이 날아온 공격을 받아 내고, 오른쪽 위에 날아오는 기술 목록과 요격·방벽 버튼이 뜬 장면": "A barrier in front of Born absorbs an attack while the top-right panel lists incoming attacks with intercept and barrier buttons",
    "사막 모래 벌레 전투": "Battle against a desert sandworm",
    "소환 화면: 왼쪽에 큰 동료 원화, 오른쪽에 이번 픽업 목록": "Summon screen: featured companion art on the left, rate-up list on the right",
    "수호자 보른이 방패로 공격을 받아 내며 「완벽 방어!」 문구가 뜬 장면": "Guardian Born blocks an attack with his shield and a Perfect Guard! pops up",
    "장비 옵션 예시: 화염 피해 +30% 최대치, 공격력 +10%, 흡혈 +4%p 최대치": "Example affixes: Fire damage +30% (max roll), Attack +10%, Lifesteal +4%p (max roll)",
    "정예 몬스터가 섞인 전투": "Battle with elite monsters",
    "4-1 실제 전투: 방벽이 파티를 지키고, 날아오는 기술을 격추하고, 완벽 방어로 막아 내는 장면": "Stage 4-1 gameplay: a barrier protects the party, incoming attacks are shot down, and a Perfect Guard blocks the last one",
    "장비 등급": "Gear rarities",
    "1인칭 회랑의 압력판 함정과 그 너머의 고블린 궁수": "A pressure plate in a first-person corridor, with a goblin archer beyond",
    "1층 돌파 후 다음 층 입구를 고르는 화면": "Choosing the next floor's entrance after clearing floor 1",
    "Break로 보스의 대기술을 끊은 장면": "Break cancels the boss's big attack",
    "결전 레이드 선택과 10인 파티 편성 화면": "Raid select and the ten-companion party",
    "네임드 모래벌레의 공격이 날아오고, 요격과 방벽 단추가 뜬 장면": "The named sandworm's attack incoming, with intercept and barrier buttons",
    "네임드 몬스터 모래벌레가 등장한 전투": "Battle where a named sandworm appears",
    "로비 화면: 안내인 미라, 모험 이어가기, 요일 던전, 주간 보스, 결전 레이드, 영토, 유물 던전 메뉴": "Lobby: guide Mira, continue the story, weekday dungeons, weekly boss, raid, territory and relic dungeon",
    "룬 석판 수수께끼 화면: 태양·달·별 문양 중 하나를 고른다": "Rune tablet riddle: choose the sun, moon or star symbol",
    "보스의 최후의 발악 경고가 뜬 장면": "The boss's last-stand warning",
    "수호자 보른이 동료의 방패로 정예 부대의 공격을 막아 내는 장면": "Guardian Born blocks an elite squad's attack with Ally Shield",
    "영지 내정 화면: 개간·방비·민심": "Land affairs: cultivation, defenses and morale",
    "영지에 동료 두 명을 주둔시킨 화면": "Two companions stationed at a land",
    "영토 지도 화면: 영지 9곳": "Territory map with nine lands",
    "유물 던전 출발 전 보급 가방 화면": "Relic dungeon supply bag before departure",
    "1인칭 회랑에서 층 문지기와 실시간으로 싸우는 장면": "Fighting the floor's gatekeeper in real time in a first-person corridor",
    "정예 부대가 증원으로 나타난 사막 전투": "Desert battle where an elite squad arrives as reinforcements",
    "침공전 성문 방어 전투 화면": "Invasion gate-defense battle",
    "함정 해체와 강행 돌파 중 고르는 화면": "Choosing between disarming the trap and forcing through",
    "4-1 Hard 실제 전투: 정예 부대와 네임드 모래벌레의 공격을 동료가 막고 요격한 뒤 반격하는 장면": "Stage 4-1 Hard gameplay: the party blocks and intercepts attacks from an elite squad and a named sandworm, then strikes back",
    "유물 던전 실제 플레이: 1인칭 회랑을 걷고, 압력판을 해체하고, 회랑의 괴물과 층 문지기를 실시간으로 쓰러뜨린 뒤 전리품을 챙겨 귀환 포탈에 이르는 장면": "Relic dungeon gameplay: first-person corridors, a disarmed pressure plate, a corridor monster and the gatekeeper beaten in real time, then loot and the return portal",
    "결전 레이드 실제 플레이: 악룡 베일가르 등장, 필살기, Break로 대기술 차단, 최후의 발악과 승리": "Raid gameplay: Veilgar's entrance, signature skills, Break cancelling the big attack, the last stand and victory",
    "4-1 Hard 전투 영상의 첫 장면": "Opening frame of the Stage 4-1 Hard battle video",
    "유물 던전 영상의 첫 장면": "Opening frame of the relic dungeon video",
    "결전 레이드 영상의 첫 장면": "Opening frame of the raid video",
    "사이트 안내": "Site",
}

# Contact form: values that change per language
FORM = {
    "ko": {"_subject": "[Ashen Crown] 외부 시험 신청", "_next": BASE + "thanks/", "언어": "ko"},
    "en": {"_subject": "[Ashen Crown] Playtest application", "_next": BASE + "en/thanks/", "언어": "en"},
}
OG_IMAGE = {"ko": ("og.jpg", "애션 크라운 로고와 재가 내리는 성채"), "en": ("og-en.jpg", "Ashen Crown logo over an ash-covered citadel")}


def faq_ld(soup):
    items = []
    for d in soup.select("#faq details"):
        q = d.summary.get_text(" ", strip=True)
        a = " ".join(p.get_text(" ", strip=True) for p in d.find_all("p"))
        items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return {"@type": "FAQPage", "mainEntity": items}

ASSET = re.compile(r"^(img|video)/")


def build(lang):
    m = META[lang]
    other = "en" if lang == "ko" else "ko"
    soup = BeautifulSoup(TEMPLATE, "html.parser")
    html = soup.html
    html["lang"] = lang
    html["data-lang"] = lang

    for el in soup.find_all(attrs={"lang": other}):
        if el is not html:
            el.decompose()

    head = soup.head
    head.title.string = m["title"]
    def meta(attr, key, value):
        tag = head.find("meta", attrs={attr: key})
        if tag is not None:
            tag["content"] = value
    meta("name", "description", m["description"])
    meta("name", "keywords", m["keywords"])
    meta("name", "robots", "index,follow")
    meta("property", "og:title", m["og_title"])
    meta("property", "og:description", m["og_description"])
    meta("property", "og:url", m["url"])
    meta("property", "og:locale", m["locale"])
    meta("property", "og:locale:alternate", m["alt_locale"])
    head.find("link", rel="canonical")["href"] = m["url"]
    for old in head.find_all("link", rel="alternate"):
        old.decompose()
    canon = head.find("link", rel="canonical")
    for hl, href in (("x-default", BASE), ("en", BASE + "en/"), ("ko", BASE)):
        canon.insert_after(soup.new_tag("link", rel="alternate", hreflang=hl, href=href))

    img, img_alt = OG_IMAGE[lang]
    meta("property", "og:image", BASE + "img/" + img)
    meta("property", "og:image:alt", img_alt)
    meta("name", "twitter:image", BASE + "img/" + img)

    ld = head.find("script", type="application/ld+json")
    data = json.loads(ld.string)
    data.pop("@context", None)
    data["description"] = m["ld_description"]
    data["url"] = m["url"]
    data["image"] = BASE + "img/" + img
    data["inLanguage"] = ["ko", "en"]
    graph = [
        data,
        {"@type": "WebSite", "name": "Ashen Crown", "alternateName": "애션 크라운", "url": BASE, "inLanguage": lang},
        {"@type": "Organization", "name": "Ashen Crown", "url": BASE, "logo": BASE + "img/icon-512.png",
         "email": "ashencrown.support@gmail.com"},
        faq_ld(soup),
    ]
    ld.string = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)

    form = soup.find(id="applyForm")
    for name, value in FORM[lang].items():
        form.find("input", attrs={"name": name})["value"] = value

    soup.find("nav")["aria-label"] = m["nav"]
    soup.find("dialog")["aria-label"] = m["dialog"]

    # language switch: real links between the two pages
    group = soup.find(class_="lang")
    group.clear()
    for code, label, href in (("ko", "한국어", "../" if lang == "en" else "./"), ("en", "EN", "./" if lang == "en" else "en/")):
        a = soup.new_tag("a", href=href, hreflang=code)
        a.string = label
        if code == lang:
            a["aria-current"] = "page"
        group.append(a)

    if lang == "en":
        for el in soup.find_all(alt=True):
            el["alt"] = ALT_EN.get(el["alt"], el["alt"])
        for el in soup.find_all(attrs={"aria-label": True}):
            el["aria-label"] = ALT_EN.get(el["aria-label"], el["aria-label"])
        for attr in ("src", "href", "poster"):
            for el in soup.find_all(attrs={attr: ASSET}):
                el[attr] = "../" + el[attr]

    out = ROOT / ("index.html" if lang == "ko" else "en/index.html")
    out.parent.mkdir(exist_ok=True)
    out.write_text("<!doctype html>\n" + str(soup.html) + "\n", encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


for code in ("ko", "en"):
    build(code)

import datetime
import pages

pages.build_all(ROOT)

# sitemap: every page that should appear in search (thank-you and 404 pages stay out)
today = datetime.date.today().isoformat()
entries = [("", "1.0"), ("privacy/", "0.3")]
urls = []
for path, prio in entries:
    alts = (f'    <xhtml:link rel="alternate" hreflang="ko" href="{BASE}{path}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}en/{path}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{path}"/>\n')
    for loc in (BASE + path, BASE + "en/" + path):
        urls.append(f"  <url>\n    <loc>{loc}</loc>\n{alts}    <lastmod>{today}</lastmod>\n    <priority>{prio}</priority>\n  </url>")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
print("wrote sitemap.xml")

(ROOT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /thanks/\nDisallow: /en/thanks/\n"
    f"Sitemap: {BASE}sitemap.xml\n", encoding="utf-8")
print("wrote robots.txt")
