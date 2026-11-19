"""Probability disclosure page (/odds/) from the game's own table.

Source: tools/data/probability-disclosure.md, a copy of docs/release/PROBABILITY_DISCLOSURE.md in the game
repository. The game builds that file from its code (scripts/probability-disclosure.mjs, checked by a test),
so the numbers here are the game's numbers. To update: copy the file again, set SOURCE_COMMIT, run build.py.
"""
import re
from html import escape
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "data/probability-disclosure.md"
# Game repository commit the copy came from (checked with `probability-disclosure.mjs --check`).
SOURCE_COMMIT = "873d6b6"
SOURCE_DATE = "2026-11-18"

# Long tables fold away so the page stays readable on a phone.
FOLD = {"동료별 확률 (배너별)": "배너별 동료 확률 전체 보기", "장비별 확률": "장비별 확률 전체 보기"}


def inline(s):
    s = escape(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(rows, wide=False):
    head, align, body = cells(rows[0]), cells(rows[1]), [cells(r) for r in rows[2:]]
    right = [a.endswith(":") for a in align]
    def td(tag, i, v):
        cls = ' class="num"' if right[i] else ""
        return f"<{tag}{cls}>{inline(v)}</{tag}>"
    out = ['<div class="tablewrap"><table class="odds' + (" wide" if wide else "") + '">',
           "<thead><tr>" + "".join(td("th", i, v) for i, v in enumerate(head)) + "</tr></thead><tbody>"]
    for r in body:
        out.append("<tr>" + "".join(td("th" if i == 0 and wide else "td", i, v) for i, v in enumerate(r)) + "</tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


def render_ko():
    """Korean body: the disclosure as HTML (title line dropped; page has its own h1)."""
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    out, i, fold_open, last_heading = [], 0, False, ""
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("# "):
            i += 1
            continue
        if line.startswith("## ") or line.startswith("### "):
            if fold_open:
                out.append("</details>")
                fold_open = False
            level = 2 if line.startswith("## ") else 3
            text = line[level + 1:]
            last_heading = text
            out.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < n and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            wide = len(cells(rows[0])) > 6
            big = len(rows) > 40
            if big:
                label = FOLD.get(last_heading, FOLD["장비별 확률"] if "장비" in rows[0] else "전체 표 보기")
                out.append(f'<details class="fold"{" data-banner-table" if wide else ""}><summary>{escape(label)} ({len(rows) - 2}줄)</summary>')
                out.append(table(rows, wide))
                out.append("</details>")
            else:
                out.append(table(rows, wide))
            continue
        if line.startswith("- "):
            items = []
            while i < n and lines[i].startswith("- "):
                items.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if line.strip():
            out.append(f"<p>{inline(line)}</p>")
        i += 1
    if fold_open:
        out.append("</details>")
    return "\n".join(out)


def rarity_rows():
    """(rarity, base rate, pool) rows from section 1 for the English summary."""
    text = SOURCE.read_text(encoding="utf-8")
    sec = text.split("## 1.")[1].split("###")[0]
    rows = []
    for m in re.finditer(r"^\| (UR|SSR|SR|R|N) \| ([\d.]+%) \| 동료 (\d+)명 중 1명 \|$", sec, re.M):
        rows.append((m.group(1), m.group(2), m.group(3)))
    return rows


def table_after(heading, first_col_filter=None):
    """Rows (as lists) of the first table under a heading."""
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("#") and heading in l)
    i = start + 1
    while not lines[i].startswith("|"):
        i += 1
    rows = []
    while i < len(lines) and lines[i].startswith("|"):
        rows.append(cells(lines[i]))
        i += 1
    return rows[2:]


EN_GRADE = {"신화": "Mythic", "에픽": "Epic", "유니크": "Unique", "레어": "Rare", "매직": "Magic"}


def render_en():
    """English body: every rate and rule; per-companion / per-item lists point to the Korean page."""
    r = rarity_rows()
    rar = "".join(f"<tr><td>{k}</td><td class=\"num\">{v}</td><td>1 of {p} companions, equal odds</td></tr>" for k, v, p in r)
    pity = "".join(f"<tr><td class=\"num\">{escape(a.replace('회 뒤 다음 1회', ''))}</td><td class=\"num\">{b}</td><td class=\"num\">{c}</td></tr>"
                   for a, b, c in table_after("천장(보장 규칙)"))
    eq = "".join(f"<tr><td>{EN_GRADE[g]}</td><td class=\"num\">{v}</td></tr>" for g, v in table_after("## 2."))
    craft = "".join(f"<tr><td class=\"num\">{escape(a.replace('번째', ''))}</td><td class=\"num\">{b}</td></tr>" for a, b in table_after("## 3."))
    enh = "".join(f"<tr><td class=\"num\">{a}</td><td class=\"num\">{b}</td><td class=\"num\">{c}</td></tr>" for a, b, c in table_after("## 4."))
    boxes = table_after("## 5.")
    box_name = {"레어 장비 상자": "Rare Gear Box", "유니크 장비 상자": "Unique Gear Box", "에픽 장비 상자": "Epic Gear Box"}
    box = "".join("<tr><td>" + box_name.get(row[0], row[0]) + "</td>" +
                  "".join(f"<td class=\"num\">{escape(c.replace('종 · 각 ', ' items, each '))}</td>" for c in row[1:]) + "</tr>" for row in boxes)
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    sealed_row = next(cells(l) for l in lines if l.startswith("| 봉인된 장비 상자 |"))
    relic = "".join(f"<tr><td lang=\"ko\">{escape(row[0])}</td><td class=\"num\">{row[1]}</td><td class=\"num\">{row[2]}</td><td class=\"num\">{row[3]}</td></tr>" for row in table_after("## 6."))
    return f"""<p class="lead">Every random item in the game, with the odds the game itself uses. The numbers below are generated from the game code and match the in-game "Odds &amp; Guarantees" window.</p>
<p class="meta">Source: game build {SOURCE_COMMIT} ({SOURCE_DATE}) · Rates are for the next single pull with no pity progress.</p>
<div class="box"><p>Companion and gear summons cost Crown Gems. Free and purchased Crown Gems have exactly the same odds and pity. Ember Crystals (earned in play) cannot be used to summon.</p>
<p>The per-companion table for every banner and the per-item gear table are long and use Korean item names, so they are on the <a href="/odds/" hreflang="ko">Korean page</a>.</p></div>

<h2>1. Companion summon</h2>
<p>Price: 160 Crown Gems per pull, 1,600 for 10. A 10-pull is the same as ten single pulls, except that your account's first 10-pull guarantees at least one SSR or better.</p>
<div class="tablewrap"><table class="odds"><thead><tr><th>Rarity</th><th class="num">Base rate</th><th>Result</th></tr></thead><tbody>{rar}</tbody></table></div>
<h3>Pity (guarantees)</h3>
<ul>
<li>After 70 pulls without SSR or better, SSR and UR rates rise with each pull (table below). Getting SSR or better resets the count.</li>
<li>The 100th pull without SSR or better is a guaranteed SSR.</li>
<li>The 180th pull without UR is a guaranteed UR.</li>
<li>First 10-pull (once per account): if the first nine give no SSR or better, the last is a guaranteed SSR.</li>
</ul>
<div class="tablewrap"><table class="odds"><thead><tr><th class="num">Pulls without SSR+</th><th class="num">SSR</th><th class="num">UR</th></tr></thead><tbody>{pity}</tbody></table></div>
<h3>Rate-up banners</h3>
<ul>
<li>When a UR appears, it is the banner's featured UR 50% of the time; otherwise one of the other URs with equal odds.</li>
<li>If you get a non-featured UR, your next UR is the featured one. This carries over between banners, so the featured UR takes at most 360 pulls.</li>
<li>When an SSR appears, it is the banner's featured SSR 18.75% of the time; otherwise one of the other SSRs with equal odds. Rarity rates do not change.</li>
<li>On every banner: featured UR 0.4% (0.8% when guaranteed), featured SSR 1.725%.</li>
</ul>

<h2>2. Gear summon</h2>
<p>Price: 100 Crown Gems per pull, 1,000 for 10. Normal gear never appears.</p>
<div class="tablewrap"><table class="odds"><thead><tr><th>Grade</th><th class="num">Base rate</th></tr></thead><tbody>{eq}</tbody></table></div>
<ul>
<li>In a 10-pull, if the first nine give nothing Unique or better, the last is Unique or better (keeping the Unique/Epic/Mythic ratio).</li>
<li>The 40th pull without Epic or better is a guaranteed Epic or better. Getting Epic or Mythic resets the count.</li>
<li>A Mythic is the featured Mythic 50% of the time. The 200th pull without the featured Mythic guarantees it.</li>
<li>Each gear pull gives 1 gear exchange point; 120 points can be exchanged for the current featured Mythic.</li>
<li>Gear pity and points are counted separately from companion summons.</li>
</ul>

<h2>3. Mythic crafting</h2>
<p>Success starts at 30% and rises by 10 percentage points for that Mythic after each failure. The 8th try always succeeds; crafting resets the count. On failure, Primal Embers and gold are lost and 50% of Mythic fragments and story materials are returned.</p>
<div class="tablewrap"><table class="odds"><thead><tr><th class="num">Try</th><th class="num">Success</th></tr></thead><tbody>{craft}</tbody></table></div>

<h2>4. Gear enhancement</h2>
<p>+1 to +7 always succeed. A Blessed Enhancement Stone adds 15 percentage points. Each failure builds "momentum"; at 100% the next attempt always succeeds.</p>
<div class="tablewrap"><table class="odds"><thead><tr><th class="num">Target</th><th class="num">Success</th><th class="num">With Blessed Stone</th></tr></thead><tbody>{enh}</tbody></table></div>

<h2>5. Gear boxes</h2>
<p>Opening a box gives one piece of gear of that grade from your current story chapter, each with equal odds. These boxes only come from limited rewards (weekly missions, chapter star goals, exchanges).</p>
<div class="tablewrap"><table class="odds wide"><thead><tr><th>Box</th>{''.join(f'<th class="num">Ch. {c}</th>' for c in range(1, 9))}</tr></thead><tbody>{box}</tbody></table></div>
<p>The Sealed Gear Box (from the Monthly Pass and the Ashen Pass) first rolls a grade, then gives one item of that grade as above.</p>
<div class="tablewrap"><table class="odds"><thead><tr><th>Box</th><th class="num">Rare</th><th class="num">Unique</th><th class="num">Epic</th></tr></thead><tbody><tr><td>Sealed Gear Box</td><td class="num">{sealed_row[1]}</td><td class="num">{sealed_row[2]}</td><td class="num">{sealed_row[3]}</td></tr></tbody></table></div>

<h2>6. Sealed relics</h2>
<p>Found only in relic dungeons. Opening one gives a relic-slot item of its line, with the grade odds below (one item per grade per line).</p>
<div class="tablewrap"><table class="odds"><thead><tr><th>Relic (Korean name)</th><th class="num">Rare</th><th class="num">Unique</th><th class="num">Epic</th></tr></thead><tbody>{relic}</tbody></table></div>"""


KO_INTRO = f"""<p class="lead">게임 안에서 확률로 결과가 정해지는 모든 것과 그 확률입니다.</p>
<p class="meta">기준: 게임 빌드 {SOURCE_COMMIT} ({SOURCE_DATE}) · 확률이 바뀌면 이 페이지를 먼저 고치고 바뀐 날짜를 적습니다.</p>
<nav class="toc" aria-label="목차"><ol>
<li><a href="#s1">동료 소환</a></li><li><a href="#s2">장비 소환</a></li><li><a href="#s3">신화 조합</a></li>
<li><a href="#s4">장비 강화</a></li><li><a href="#s5">장비 상자</a></li><li><a href="#s6">봉인된 유물</a></li></ol></nav>"""


def page_body(lang):
    if lang == "en":
        body = render_en()
    else:
        body = KO_INTRO + render_ko()
    # anchors for the table of contents
    for n in range(1, 7):
        body = re.sub(rf"<h2>{n}\. ", f'<h2 id="s{n}">{n}. ', body, count=1)
    return body + BANNER_SCRIPT


# On phones the 21-banner table is too wide: let the reader pick one banner and show only that column.
BANNER_SCRIPT = """
<script>
document.querySelectorAll("[data-banner-table]").forEach(function (box) {
  var t = box.querySelector("table"); if (!t) return;
  var heads = t.tHead.rows[0].cells; if (heads.length < 4) return;
  var label = document.createElement("label"); label.className = "pick";
  label.appendChild(document.createTextNode("배너 고르기 "));
  var sel = document.createElement("select");
  var all = document.createElement("option"); all.value = ""; all.textContent = "모든 배너"; sel.appendChild(all);
  for (var i = 2; i < heads.length; i++) { var o = document.createElement("option"); o.value = i; o.textContent = heads[i].textContent; sel.appendChild(o); }
  label.appendChild(sel);
  box.insertBefore(label, box.querySelector(".tablewrap"));
  sel.addEventListener("change", function () {
    var pick = sel.value ? +sel.value : 0;
    for (var r = 0; r < t.rows.length; r++) for (var c = 2; c < t.rows[r].cells.length; c++)
      t.rows[r].cells[c].hidden = pick ? c !== pick : false;
    t.classList.toggle("one", !!pick);
  });
});
</script>"""
