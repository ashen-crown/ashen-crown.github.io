"""Small pages around the main page: privacy policy, thank-you page, 404.
Each page gets its own title, description, canonical URL, breadcrumb and footer links.
Imported by build.py.
"""
import json
from html import escape

BASE = "https://ashen-crown.github.io/"
MAIL = "ashencrown.support@gmail.com"
UPDATED = "2026-11-11"

CSS = """
:root{--ash:#14110f;--ash-2:#1d1915;--bone:#ece4d6;--dust:#a89c8a;--ember:#e0a24e;--ember-hot:#f0b965;--rule:#3a322a;
--display:"Gowun Batang","Nanum Myeongjo",serif;--body:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;--latin:"Cinzel","Times New Roman",serif;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;word-break:keep-all;overflow-wrap:break-word;background:var(--ash);color:var(--bone);font:16px/1.75 var(--body)}
a{color:var(--ember)}
a:focus-visible,button:focus-visible{outline:2px solid var(--ember-hot);outline-offset:3px}
h1,h2{font-family:var(--display);font-weight:700;margin:0;text-wrap:balance}
.wrap{max-width:820px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.skip{position:absolute;left:12px;top:-60px;background:var(--ember);color:#1a1209;padding:10px 14px;border-radius:6px;font-weight:600;text-decoration:none}
.skip:focus{top:12px}
.nav{border-bottom:1px solid var(--rule)}
.nav .wrap{display:flex;align-items:center;gap:16px;height:56px;max-width:1080px}
.brand{font-family:var(--latin);font-weight:700;letter-spacing:.14em;color:var(--bone);text-decoration:none;font-size:15px}
.brand span{color:var(--ember)}
.lang{margin-left:auto;display:flex;border:1px solid var(--rule);border-radius:999px;overflow:hidden}
.lang a{color:var(--dust);font:600 12px/1 var(--body);padding:7px 10px;text-decoration:none}
.lang a[aria-current="page"]{background:var(--ember);color:#1a1209}
.crumbs ol{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0;padding:20px 0 0;font-size:13.5px;color:var(--dust)}
.crumbs li+li::before{content:"›";margin-right:6px;color:#6b5f50}
.crumbs a{color:var(--dust)}
.crumbs [aria-current]{color:var(--bone)}
main{padding-block:28px 24px}
main h1{font-size:clamp(26px,4vw,36px);line-height:1.3;margin-bottom:10px}
.lead{color:#d6ccbc;max-width:62ch}
main h2{font-size:20px;margin:36px 0 10px}
main p,main li{max-width:68ch}
main p+p{margin-top:10px}
main ul,main ol{padding-left:20px}
.meta{color:var(--dust);font-size:14px;margin-top:6px}
.tablewrap{overflow-x:auto;margin-top:8px}
table{border-collapse:collapse;font-size:14px;min-width:560px}
th,td{border:1px solid var(--rule);padding:8px 10px;text-align:left;vertical-align:top}
th{background:var(--ash-2);font-weight:600}
.box{background:var(--ash-2);border:1px solid var(--rule);border-radius:10px;padding:18px 20px;margin-top:22px}
.actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.btn{display:inline-flex;align-items:center;padding:12px 20px;border-radius:6px;font-weight:600;font-size:15px;text-decoration:none;border:1px solid transparent}
.btn-primary{background:var(--ember);color:#1a1209}
.btn-primary:hover{background:var(--ember-hot)}
.btn-ghost{border-color:#5a4c3e;color:var(--bone)}
.consent{position:fixed;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:25;max-width:560px;margin:0 auto;background:var(--ash-2);border:1px solid #5a4630;border-radius:10px;padding:16px;display:grid;gap:10px;box-shadow:0 16px 48px rgba(0,0,0,.5);font-size:14px}
.consent .acts{display:flex;flex-wrap:wrap;gap:8px}
.consent .btn{padding:9px 14px;font-size:14px;cursor:pointer;font-family:var(--body)}
footer{margin-top:64px;border-top:1px solid var(--rule);padding-block:24px 40px;color:var(--dust);font-size:13.5px}
footer .wrap{display:grid;gap:10px;max-width:1080px}
.foot-links{display:flex;flex-wrap:wrap;gap:6px 18px;list-style:none;margin:0;padding:0}
.foot-links a{color:var(--dust);text-decoration:none}
.foot-links a:hover{color:var(--bone);text-decoration:underline}
"""

UI = {
    "ko": {"home": "홈", "skip": "본문 바로가기", "privacy": "개인정보 처리방침", "faq": "자주 묻는 질문", "apply": "외부 시험 신청",
           "relic": "유물 던전", "records": "실제 플레이", "contact": "문의", "reply": "평일 기준 2일 이내 답장",
           "foot": "모든 사진은 개발 중인 실제 게임 화면입니다.", "crumbs": "현재 위치", "sitenav": "사이트 안내", "locale": "ko_KR"},
    "en": {"home": "Home", "skip": "Skip to content", "privacy": "Privacy policy", "faq": "FAQ", "apply": "Playtest sign-up",
           "relic": "Relic dungeons", "records": "Play records", "contact": "Contact", "reply": "reply within 2 business days",
           "foot": "All images are in-development game footage.", "crumbs": "You are here", "sitenav": "Site", "locale": "en_US"},
}


def home(lang):
    return "/" if lang == "ko" else "/en/"


def page(lang, slug, title, description, h1, body, *, index=True, crumbs=True, other_href=None):
    u = UI[lang]
    url = BASE + ("" if lang == "ko" else "en/") + (slug + "/" if slug else "")
    h = home(lang)
    other = "en" if lang == "ko" else "ko"
    other_href = other_href or (home(other) + (slug + "/" if slug else ""))
    self_href = h + (slug + "/" if slug else "")
    ko_href = self_href if lang == "ko" else other_href
    en_href = self_href if lang == "en" else other_href

    ld = []
    if crumbs:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": u["home"], "item": BASE + h.lstrip("/")},
            {"@type": "ListItem", "position": 2, "name": h1, "item": url}]})
    head_extra = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    alt_links = "" if not index else (
        f'<link rel="alternate" hreflang="ko" href="{BASE}{slug}/">\n'
        f'<link rel="alternate" hreflang="en" href="{BASE}en/{slug}/">\n'
        f'<link rel="alternate" hreflang="x-default" href="{BASE}{slug}/">\n')
    crumb_html = "" if not crumbs else (
        f'<nav class="crumbs" aria-label="{u["crumbs"]}"><ol><li><a href="{h}">{u["home"]}</a></li>'
        f'<li><span aria-current="page">{escape(h1)}</span></li></ol></nav>')

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="{'index,follow' if index else 'noindex,follow'}">
{'' if not crumbs else f'<link rel="canonical" href="{url}">'}
{alt_links}<meta property="og:site_name" content="Ashen Crown">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:image" content="{BASE}img/{'og.jpg' if lang == 'ko' else 'og-en.jpg'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{u['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14110f">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Cinzel:wght@600;700&display=swap">
{head_extra}<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main">{u['skip']}</a>
<header class="nav"><div class="wrap">
  <a class="brand" href="{h}" translate="no">ASHEN <span>CROWN</span></a>
  <div class="lang" role="group" aria-label="Language"><a href="{ko_href}" hreflang="ko"{' aria-current="page"' if lang == 'ko' else ''}>한국어</a><a href="{en_href}" hreflang="en"{' aria-current="page"' if lang == 'en' else ''}>EN</a></div>
</div></header>
<div class="wrap">{crumb_html}</div>
<main id="main" tabindex="-1"><div class="wrap">
<h1>{escape(h1)}</h1>
{body}
</div></main>
<footer><div class="wrap">
  <nav aria-label="{u['sitenav']}"><ul class="foot-links">
    <li><a href="{h}">{u['home']}</a></li>
    <li><a href="{h}#records">{u['records']}</a></li>
    <li><a href="{h}#relic">{u['relic']}</a></li>
    <li><a href="{h}#apply">{u['apply']}</a></li>
    <li><a href="{h}#faq">{u['faq']}</a></li>
    <li><a href="{h}privacy/">{u['privacy']}</a></li>
  </ul></nav>
  <span>{u['contact']} · <a href="mailto:{MAIL}">{MAIL}</a> · {u['reply']}</span>
  <span>© 2026 Ashen Crown · {u['foot']}</span>
</div></footer>
<script src="/js/site.js" defer></script>
</body>
</html>
"""


PRIVACY = {
    "ko": dict(
        title="개인정보 처리방침 | Ashen Crown 애션 크라운",
        description="애션 크라운 홈페이지가 외부 시험 신청과 문의, 방문 통계를 위해 어떤 정보를 받고, 얼마나 보관하며, 어떻게 지우는지 안내합니다.",
        h1="개인정보 처리방침",
        body=f"""<p class="lead">애션 크라운(Ashen Crown, 이하 「운영자」)은 홈페이지에서 받는 개인정보를 꼭 필요한 만큼만 받고, 목적이 끝나면 지웁니다.</p>
<p class="meta">시행일 {UPDATED}</p>

<h2>1. 받는 정보와 이유</h2>
<div class="tablewrap"><table>
<tr><th>언제</th><th>받는 정보</th><th>이유</th></tr>
<tr><td>외부 시험 신청서</td><td>필수: 닉네임, 메일 주소<br>선택: 사용하는 PC, 즐겨 하는 장르, 하고 싶은 말</td><td>시험 일정과 참가 방법 안내, 시험 환경 파악</td></tr>
<tr><td>메일 문의</td><td>메일 주소, 보내 주신 내용</td><td>문의 답변</td></tr>
<tr><td>방문 통계 (허용한 경우만)</td><td>구글 애널리틱스 쿠키, 본 화면, 대략적인 지역, 기기 종류</td><td>어떤 내용을 많이 보는지 파악해 홈페이지 개선</td></tr>
</table></div>
<p>만 14세 미만은 외부 시험에 신청할 수 없습니다.</p>

<h2>2. 보관 기간</h2>
<ul>
<li>외부 시험 신청 정보: 해당 외부 시험이 끝난 뒤 30일 이내에 지웁니다.</li>
<li>문의 메일: 답변을 마친 뒤 1년 동안 보관하고 지웁니다.</li>
<li>방문 통계: 구글 애널리틱스 보관 기간 설정(14개월)에 따릅니다.</li>
</ul>
<p>법에서 따로 보관을 요구하는 경우에는 그 기간 동안 보관합니다.</p>

<h2>3. 다른 곳에 주는 경우</h2>
<p>받은 개인정보를 다른 사람이나 회사에 팔거나 넘기지 않습니다. 다만 홈페이지와 메일을 운영하기 위해 아래 해외 서비스를 씁니다.</p>
<div class="tablewrap"><table>
<tr><th>서비스 (회사, 국가)</th><th>맡기는 일</th><th>전달되는 정보</th><th>보관 기간</th></tr>
<tr><td>FormSubmit (Devro LABS, 미국)</td><td>신청서를 운영자 메일로 전달</td><td>신청서에 적은 내용</td><td>전달 후 해당 서비스 정책에 따름</td></tr>
<tr><td>Gmail (Google LLC, 미국)</td><td>신청서와 문의 메일 보관·답장</td><td>신청서·메일 내용</td><td>위 2번 기간</td></tr>
<tr><td>Google Analytics (Google LLC, 미국)</td><td>방문 통계 (허용한 경우만)</td><td>쿠키, 본 화면, 기기 정보</td><td>14개월</td></tr>
<tr><td>GitHub Pages (GitHub, Inc., 미국)</td><td>홈페이지 호스팅</td><td>접속 기록 (IP 주소 등)</td><td>해당 서비스 정책에 따름</td></tr>
</table></div>
<p>정보는 신청서를 보내거나 홈페이지에 접속할 때 인터넷으로 전달됩니다. 해외로 전달되는 것을 원하지 않으면 신청서 대신 메일로 문의하거나, 방문 통계를 허용하지 않으면 됩니다.</p>

<h2 id="analytics">4. 쿠키와 방문 통계</h2>
<p>처음 방문하면 방문 통계 쿠키를 써도 되는지 묻습니다. 「허용」을 누른 경우에만 구글 애널리틱스가 작동하고, IP 주소는 줄여서 보냅니다. 「허용 안 함」을 눌러도 홈페이지는 그대로 쓸 수 있습니다.</p>
<p><a href="#" data-consent-reset>방문 통계 허용 여부 다시 고르기</a></p>

<h2>5. 내 정보에 대한 권리</h2>
<p>내 정보를 보여 달라고, 고쳐 달라고, 지워 달라고, 그만 쓰라고 요청할 수 있습니다. <a href="mailto:{MAIL}">{MAIL}</a>로 보내 주시면 10일 이내에 처리하고 결과를 알려 드립니다.</p>

<h2>6. 안전하게 지키는 방법</h2>
<ul>
<li>신청서와 메일은 운영자만 볼 수 있는 계정에 보관하고, 계정에는 2단계 인증을 씁니다.</li>
<li>목적이 끝난 정보는 위 기간 안에 지웁니다.</li>
</ul>

<h2>7. 개인정보 보호책임자와 문의</h2>
<p>개인정보 보호책임자: 애션 크라운 운영자<br>연락처: <a href="mailto:{MAIL}">{MAIL}</a> (평일 기준 2일 이내 답장)</p>
<p>개인정보 침해 신고와 상담은 개인정보침해신고센터(privacy.kisa.or.kr, 국번 없이 118)나 개인정보분쟁조정위원회(kopico.go.kr, 1833-6972)에서도 받을 수 있습니다.</p>

<h2>8. 바뀌는 경우</h2>
<p>이 방침을 바꾸면 이 페이지에 바뀐 날짜와 내용을 적어 알립니다.</p>""",
    ),
    "en": dict(
        title="Privacy Policy | Ashen Crown",
        description="What the Ashen Crown website collects for playtest sign-ups, contact and visit statistics, how long it is kept, and how it is deleted.",
        h1="Privacy policy",
        body=f"""<p class="lead">Ashen Crown ("we") collects only what the website needs and deletes it when the purpose is done.</p>
<p class="meta">Effective {UPDATED}</p>

<h2>1. What we collect and why</h2>
<div class="tablewrap"><table>
<tr><th>When</th><th>What</th><th>Why</th></tr>
<tr><td>Playtest sign-up form</td><td>Required: nickname, email<br>Optional: your PC, favorite genres, message</td><td>To send test dates and instructions, and understand test hardware</td></tr>
<tr><td>Email to us</td><td>Your email address and message</td><td>To reply</td></tr>
<tr><td>Visit statistics (only if you allow)</td><td>Google Analytics cookies, pages viewed, rough location, device type</td><td>To see which content is read and improve the site</td></tr>
</table></div>
<p>Children under 14 may not sign up for playtests.</p>

<h2>2. How long we keep it</h2>
<ul>
<li>Playtest sign-ups: deleted within 30 days after that playtest ends.</li>
<li>Emails: kept for one year after we reply, then deleted.</li>
<li>Visit statistics: Google Analytics retention setting (14 months).</li>
</ul>

<h2>3. Services that handle your data</h2>
<p>We never sell or hand your data to others. We use these overseas services to run the site and email:</p>
<div class="tablewrap"><table>
<tr><th>Service (company, country)</th><th>Task</th><th>Data</th><th>Retention</th></tr>
<tr><td>FormSubmit (Devro LABS, USA)</td><td>Forwards the form to our inbox</td><td>What you enter in the form</td><td>Per the service's policy</td></tr>
<tr><td>Gmail (Google LLC, USA)</td><td>Stores and answers sign-ups and emails</td><td>Form and email content</td><td>As in section 2</td></tr>
<tr><td>Google Analytics (Google LLC, USA)</td><td>Visit statistics (only if you allow)</td><td>Cookies, pages viewed, device info</td><td>14 months</td></tr>
<tr><td>GitHub Pages (GitHub, Inc., USA)</td><td>Hosts the website</td><td>Access logs (such as IP address)</td><td>Per the service's policy</td></tr>
</table></div>

<h2 id="analytics">4. Cookies and visit statistics</h2>
<p>On your first visit we ask whether we may use analytics cookies. Google Analytics runs only if you choose Allow, with IP addresses shortened. The site works the same if you decline.</p>
<p><a href="#" data-consent-reset>Change your analytics choice</a></p>

<h2>5. Your rights</h2>
<p>You can ask to see, correct or delete your data, or ask us to stop using it. Email <a href="mailto:{MAIL}">{MAIL}</a> and we will act within 10 days.</p>

<h2>6. Keeping it safe</h2>
<ul>
<li>Sign-ups and emails are kept in an account only the operator can access, protected with two-step verification.</li>
<li>Data is deleted within the periods above.</li>
</ul>

<h2>7. Contact</h2>
<p>Privacy contact: Ashen Crown operator, <a href="mailto:{MAIL}">{MAIL}</a> (reply within 2 business days, Korean time).</p>

<h2>8. Changes</h2>
<p>If this policy changes, we will post the date and what changed on this page.</p>""",
    ),
}

THANKS = {
    "ko": dict(
        title="신청 완료 | Ashen Crown 애션 크라운 외부 시험",
        description="애션 크라운 외부 시험 신청이 접수되었습니다. 시험 일정이 정해지면 메일로 안내드립니다.",
        h1="신청해 주셔서 고마워요",
        body="""<p class="lead">외부 시험 신청이 접수되었어요. 시험 일정이 정해지면 적어 주신 메일로 신청 순서대로 안내드릴게요.</p>
<div class="box">
<p><b>다음 순서</b></p>
<ol>
<li>평일 기준 2일 이내에 접수 확인 메일을 보내 드려요.</li>
<li>시험 일정이 정해지면 게임을 받는 방법을 메일로 알려 드려요.</li>
<li>플레이한 뒤 짧은 설문이나 메일로 느낀 점을 들려주세요.</li>
</ol>
<p>메일이 오지 않으면 스팸함을 확인하시거나 <a href="mailto:ashencrown.support@gmail.com">ashencrown.support@gmail.com</a>으로 알려 주세요.</p>
</div>
<div class="actions"><a class="btn btn-primary" href="/#relic">유물 던전 영상 보기</a><a class="btn btn-ghost" href="/#faq">자주 묻는 질문</a><a class="btn btn-ghost" href="/">홈으로</a></div>""",
    ),
    "en": dict(
        title="Thank you | Ashen Crown Playtest",
        description="Your Ashen Crown playtest sign-up was received. We'll email you once a test date is set.",
        h1="Thanks for signing up",
        body="""<p class="lead">We received your playtest sign-up. Once a test date is set, we'll email you in order of sign-up.</p>
<div class="box">
<p><b>What happens next</b></p>
<ol>
<li>Within 2 business days (Korean time) we'll confirm by email.</li>
<li>When a test date is set, we'll email you how to get the build.</li>
<li>After playing, tell us what you thought in a short survey or email.</li>
</ol>
<p>No email? Check your spam folder or write to <a href="mailto:ashencrown.support@gmail.com">ashencrown.support@gmail.com</a>.</p>
</div>
<div class="actions"><a class="btn btn-primary" href="/en/#relic">Watch the relic dungeon run</a><a class="btn btn-ghost" href="/en/#faq">FAQ</a><a class="btn btn-ghost" href="/en/">Home</a></div>""",
    ),
}

NOT_FOUND_BODY = """<p class="lead">주소가 바뀌었거나 없는 페이지예요. 아래에서 찾으시는 곳으로 가 보세요.</p>
<p class="lead" lang="en">This page doesn't exist or has moved. Try one of these instead.</p>
<div class="actions">
<a class="btn btn-primary" href="/">애션 크라운 홈</a>
<a class="btn btn-ghost" href="/#apply">외부 시험 신청</a>
<a class="btn btn-ghost" href="/#faq">자주 묻는 질문</a>
<a class="btn btn-ghost" href="/en/" hreflang="en" lang="en">English home</a>
</div>"""


def build_all(root):
    out = []
    for lang in ("ko", "en"):
        pre = "" if lang == "ko" else "en/"
        p = PRIVACY[lang]
        out.append((pre + "privacy/index.html", page(lang, "privacy", p["title"], p["description"], p["h1"], p["body"])))
        t = THANKS[lang]
        out.append((pre + "thanks/index.html", page(lang, "thanks", t["title"], t["description"], t["h1"], t["body"], index=False)))
    out.append(("404.html", page("ko", "", "페이지를 찾을 수 없어요 | Ashen Crown 애션 크라운",
                                 "요청한 페이지를 찾을 수 없습니다. 애션 크라운 홈으로 돌아가세요.",
                                 "페이지를 찾을 수 없어요", NOT_FOUND_BODY, index=False, crumbs=False, other_href="/en/")))
    for rel, html in out:
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(html, encoding="utf-8")
        print("wrote", rel)
    return [rel for rel, _ in out]
