"""Small pages around the main page: privacy policy, thank-you page, 404.
Each page gets its own title, description, canonical URL, breadcrumb and footer links.
Imported by build.py.
"""
import json
from html import escape

import odds

ODDS = {
    "ko": dict(title="확률 공개표 | Ashen Crown 애션 크라운",
               description="애션 크라운의 동료 소환·장비 소환·신화 조합·장비 강화·장비 상자·봉인된 유물 확률과 천장(보장) 규칙을 게임 코드 기준으로 모두 공개합니다.",
               h1="확률 공개표"),
    "en": dict(title="Odds | Ashen Crown",
               description="Every random outcome in Ashen Crown: companion and gear summon rates, pity, mythic crafting, enhancement, gear boxes and sealed relics, generated from the game code.",
               h1="Odds and guarantees"),
}

BASE = "https://ashen-crown.github.io/"
MAIL = "ashencrown.support@gmail.com"
UPDATED = "2026-11-19"

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
main h3{font-size:16.5px;margin:24px 0 8px;font-family:var(--display)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.odds{min-width:0}
table.wide{min-width:560px}
table.wide th:first-child{position:sticky;left:0;background:var(--ash-2);z-index:1}
table.wide.one{min-width:0;width:100%}
details.fold{margin-top:12px;border:1px solid var(--rule);border-radius:10px;padding:10px 14px}
details.fold summary{cursor:pointer;font-weight:600;color:var(--ember);min-height:32px;display:flex;align-items:center}
.pick{display:flex;align-items:center;gap:8px;margin:10px 0 4px;font-size:14px;color:var(--dust)}
.pick select{font:inherit;color:var(--bone);background:var(--ash);border:1px solid #5a4c3e;border-radius:6px;padding:6px 8px;max-width:60vw}
.toc ol{display:flex;flex-wrap:wrap;gap:6px 16px;list-style:none;padding:0;margin:14px 0 0;font-size:14.5px}
.todo{background:#4a3214;color:#ffd99a;border-radius:4px;padding:0 5px;font-weight:600}
@media (max-width:480px){th,td{padding:6px 7px;font-size:13px}table:not(.wide){min-width:0;width:100%}}
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
           "foot": "모든 사진은 개발 중인 실제 게임 화면입니다.", "crumbs": "현재 위치", "store": "상품 가격", "odds": "확률 공개", "sitenav": "사이트 안내", "locale": "ko_KR"},
    "en": {"home": "Home", "skip": "Skip to content", "privacy": "Privacy policy", "faq": "FAQ", "apply": "Playtest sign-up",
           "relic": "Relic dungeons", "records": "Play records", "contact": "Contact", "reply": "reply within 2 business days",
           "foot": "All images are in-development game footage.", "crumbs": "You are here", "store": "Prices", "odds": "Odds", "sitenav": "Site", "locale": "en_US"},
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
    <li><a href="{h}store/">{u['store']}</a></li>
    <li><a href="{h}odds/">{u['odds']}</a></li>
    <li><a href="{h}privacy/">{u['privacy']}</a></li>
  </ul></nav>
  <span>{u['contact']} · <a href="mailto:{MAIL}">{MAIL}</a> · {u['reply']}</span>
  <span>© 2026 Ashen Crown · {u['foot']}</span>
</div></footer>
<script src="/js/site.js" defer></script>
</body>
</html>
"""


OPERATOR_KO = 'Ashen Crown Studio'
OPERATOR_EN = 'Ashen Crown Studio'
EFFECTIVE_KO = '2026-12-01'
EFFECTIVE_EN = 'effective 2026-12-01'
GAME_KO = "애션 크라운: 빈 왕좌의 새벽"
GAME_EN = "Ashen Crown: Dawn of the Empty Throne"

PRIVACY = {
    "ko": dict(
        title="개인정보 처리방침 | Ashen Crown 애션 크라운",
        description="애션 크라운 홈페이지와 게임 「애션 크라운: 빈 왕좌의 새벽」이 받는 정보(게임 계정, 서버 저장, 채팅, 신고·차단, 외부 시험 신청)와 보관 기간, 지우는 방법을 안내합니다.",
        h1="개인정보 처리방침",
        body=f"""<p class="lead">{OPERATOR_KO}(이하 「운영자」)는 홈페이지와 게임 「{GAME_KO}」(이하 「게임」)에서 받는 개인정보를 꼭 필요한 만큼만 받고, 목적이 끝나면 지웁니다.</p>
<p class="meta">홈페이지 부분 시행 2026-11-11 · 게임 부분 시행 {EFFECTIVE_KO} · 마지막 수정 {UPDATED}</p>

<h2>1. 받는 정보와 이유</h2>
<h3>게임</h3>
<div class="tablewrap"><table>
<tr><th>언제</th><th>받는 정보</th><th>이유</th></tr>
<tr><td>로그인 (Steam판)</td><td>Steam 계정 번호(SteamID), Steam 닉네임</td><td>내 계정 확인, 진행 저장과 복구</td></tr>
<tr><td>로그인 (웹판 구글 로그인)</td><td>구글 로그인 계정 번호(Firebase 사용자 번호). 구글 메일 주소·이름·프로필 사진은 Google의 로그인 서비스(Firebase 인증)에 보관되고, 게임 서버에는 저장하지 않습니다.</td><td>내 계정 확인, 진행 저장과 복구</td></tr>
<tr><td>서버 저장</td><td>게임 진행 기록(세이브), 세이브 복구용 사본, 게임 안 이름, 구매·지급 기록, 무료 왕관석 지급 기록, 접속 기록(접속 시각·게임 버전), 오류 기록</td><td>진행 저장과 복구, 구매 지급 확인과 환불, 부정 이용 방지, 오류 수정</td></tr>
<tr><td>채팅 (전체·기사단·1:1)</td><td>보낸 글, 채팅 이름, 공개 ID(계정을 거꾸로 찾을 수 없는 번호), 보낸 시각, 도배·금칙어 판정 기록, 채팅 금지 기록, 1:1 대화 상대 목록과 1:1 받기 설정</td><td>채팅 전달, 욕설·도배·괴롭힘 막기</td></tr>
<tr><td>신고·차단</td><td>신고한 글과 그 내용, 신고 이유, 신고한 사람·신고된 사람의 공개 ID와 이름, 내 차단 목록</td><td>신고 확인과 조치, 차단한 사람의 글 숨기기</td></tr>
<tr><td>기사단</td><td>기사단 이름·문장, 단원 명부(공개 ID·이름·역할), 가입·탈퇴 시각</td><td>기사단 운영, 기사단 채팅 방 정하기</td></tr>
<tr><td>투기장 순위표</td><td>게임 안 이름, 점수, 방어 팀</td><td>순위표와 대전 상대 찾기</td></tr>
<tr><td>설문·버그 제보</td><td>보내 주신 내용, 게임 버전과 기기 정보</td><td>게임 개선, 오류 수정</td></tr>
<tr><td>결제</td><td>주문 번호, 상품, 금액, 결제 시각, 결제 상태</td><td>구매 지급 확인, 중복 지급·환불 처리</td></tr>
</table></div>
<p>결제 카드·계좌 정보는 Valve(Steam)나 앱 마켓이 처리하며 운영자는 받지 않습니다. 실명·전화번호·주민등록번호는 받지 않습니다.</p>
<h3>홈페이지</h3>
<div class="tablewrap"><table>
<tr><th>언제</th><th>받는 정보</th><th>이유</th></tr>
<tr><td>외부 시험 신청서</td><td>필수: 닉네임, 메일 주소<br>선택: 사용하는 PC, 즐겨 하는 장르, 하고 싶은 말</td><td>시험 일정과 참가 방법 안내, 시험 환경 파악</td></tr>
<tr><td>메일 문의</td><td>메일 주소, 보내 주신 내용</td><td>문의 답변</td></tr>
<tr><td>방문 통계 (허용한 경우만)</td><td>구글 애널리틱스 쿠키, 본 화면, 대략적인 지역, 기기 종류</td><td>어떤 내용을 많이 보는지 파악해 홈페이지 개선</td></tr>
</table></div>

<h2 id="chat">2. 채팅에서 다른 사람에게 보이는 것과 신고·차단</h2>
<ul>
<li>채팅은 계정 레벨 10부터 쓸 수 있습니다. 채팅 이름과 보낸 글은 그 방에 있는 다른 플레이어에게 보입니다. 1:1 대화는 나와 상대만 봅니다.</li>
<li>보내는 글은 서버가 먼저 검사해 욕설·개인정보(전화번호 등)·광고로 보이는 글을 막습니다. 짧은 시간에 여러 번 걸리면 일정 시간 채팅이 자동으로 금지됩니다.</li>
<li>글마다 신고할 수 있고, 신고하면서 그 사람을 바로 차단할 수 있습니다. 서로 다른 세 명이 신고한 글은 운영자가 확인하기 전까지 자동으로 가려집니다.</li>
<li>운영자는 신고된 글과 그 신고 내용을 확인해 글을 가리거나 채팅을 금지할 수 있습니다. 신고가 없는 1:1 대화는 운영자가 열어 보지 않습니다.</li>
<li>차단한 사람의 글과 1:1 대화는 내 화면에 보이지 않고, 그 사람은 나에게 1:1 대화를 보낼 수 없습니다.</li>
<li>채팅에 실명, 전화번호, 주소, 다른 계정 정보 같은 개인정보를 적지 마세요.</li>
</ul>

<h2>3. 보관 기간</h2>
<div class="tablewrap"><table>
<tr><th>정보</th><th>보관 기간</th></tr>
<tr><td>게임 계정과 서버 저장 정보</td><td>계정 삭제를 요청하면 30일 안에 지웁니다.</td></tr>
<tr><td>세이브 복구용 사본</td><td>최근 7일치만 돌려 가며 보관(지난 것은 자동으로 덮어씀)</td></tr>
<tr><td>전체 채팅 글</td><td>보낸 뒤 3일이 지나면 자동으로 지움</td></tr>
<tr><td>기사단 채팅·1:1 대화 글</td><td>보낸 뒤 30일이 지나면 자동으로 지움</td></tr>
<tr><td>신고 기록</td><td>조치를 마친 뒤 1년</td></tr>
<tr><td>설문·버그 제보</td><td>1년</td></tr>
<tr><td>결제(계약·대금 지급) 기록</td><td>5년 (전자상거래법)</td></tr>
<tr><td>접속 기록</td><td>3개월 (통신비밀보호법)</td></tr>
<tr><td>외부 시험 신청 정보</td><td>해당 외부 시험이 끝난 뒤 30일 이내</td></tr>
<tr><td>문의 메일</td><td>답변을 마친 뒤 1년</td></tr>
<tr><td>홈페이지 방문 통계</td><td>구글 애널리틱스 보관 기간 설정(14개월)</td></tr>
</table></div>
<p>자동 삭제는 기간이 지난 뒤 데이터베이스가 처리하므로 하루 안팎 늦을 수 있습니다. 법에서 따로 보관을 요구하는 경우에는 그 기간 동안 보관합니다.</p>

<h2>4. 다른 곳에 주는 경우와 맡기는 일</h2>
<p>받은 개인정보를 다른 사람이나 회사에 팔거나 넘기지 않습니다. 법령에 근거가 있거나 수사기관이 법에 따른 절차로 요청한 경우만 예외입니다. 게임과 홈페이지를 운영하기 위해 아래 서비스에 일을 맡깁니다.</p>
<div class="tablewrap"><table>
<tr><th>서비스 (회사, 국가)</th><th>맡기는 일</th><th>전달되는 정보</th><th>보관 기간</th></tr>
<tr><td>Steam (Valve Corporation, 미국)</td><td>Steam판 로그인 확인, 결제, 클라우드 저장</td><td>SteamID, 결제 정보, 세이브</td><td>해당 서비스 정책에 따름</td></tr>
<tr><td>Firebase (Google LLC, 미국 · 데이터는 대한민국 서울 지역 서버에 저장)</td><td>게임 서버: 진행 저장, 채팅, 기사단, 순위표, 웹판 구글 로그인</td><td>위 1번 게임 표의 정보</td><td>위 3번 기간</td></tr>
<tr><td>원스토어 (원스토어 주식회사, 대한민국)</td><td>원스토어 웹판 실행과 결제 (결제는 열린 뒤부터)</td><td>원스토어 계정 확인 정보, 결제 정보</td><td>해당 서비스 정책에 따름</td></tr>
<tr><td>FormSubmit (Devro LABS, 미국)</td><td>시험 신청서를 운영자 메일로 전달</td><td>신청서에 적은 내용</td><td>전달 후 해당 서비스 정책에 따름</td></tr>
<tr><td>Gmail (Google LLC, 미국)</td><td>신청서와 문의 메일 보관·답장</td><td>신청서·메일 내용</td><td>위 3번 기간</td></tr>
<tr><td>Google Analytics (Google LLC, 미국)</td><td>홈페이지 방문 통계 (허용한 경우만)</td><td>쿠키, 본 화면, 기기 정보</td><td>14개월</td></tr>
<tr><td>GitHub Pages (GitHub, Inc., 미국)</td><td>홈페이지·웹판 호스팅</td><td>접속 기록 (IP 주소 등)</td><td>해당 서비스 정책에 따름</td></tr>
</table></div>
<p>정보는 게임을 하거나 신청서를 보내거나 홈페이지에 접속할 때 인터넷(암호화 연결)으로 전달됩니다. 해외로 전달되는 것을 원하지 않으면 온라인 기능(서버 저장·채팅·기사단·순위표·결제)을 쓰지 않거나, 신청서 대신 메일로 문의하거나, 방문 통계를 허용하지 않으면 됩니다. 이때 해당 기능은 쓸 수 없습니다.</p>

<h2>5. 지우는 방법</h2>
<p>전자 파일은 되살릴 수 없는 방법으로 지웁니다. 백업과 복구용 사본은 보관 기간이 지나면 자동으로 덮어씁니다. 게임 계정 삭제는 아래 7번의 메일로 요청해 주세요(게임 안 삭제 단추는 준비 중입니다).</p>

<h2 id="analytics">6. 쿠키와 이 기기에 저장하는 정보</h2>
<p>게임은 세이브와 설정을 이 기기(실행 파일 폴더 또는 브라우저 저장소)에도 저장하고, 광고·추적용 쿠키는 쓰지 않습니다. 홈페이지는 처음 방문할 때 방문 통계 쿠키를 써도 되는지 묻습니다. 「허용」을 누른 경우에만 구글 애널리틱스가 작동하고, IP 주소는 줄여서 보냅니다. 「허용 안 함」을 눌러도 홈페이지는 그대로 쓸 수 있습니다.</p>
<p><a href="#" data-consent-reset>방문 통계 허용 여부 다시 고르기</a></p>

<h2>7. 내 정보에 대한 권리</h2>
<p>내 정보를 보여 달라고, 고쳐 달라고, 지워 달라고(계정 삭제 포함), 그만 쓰라고 요청할 수 있습니다. <a href="mailto:{MAIL}">{MAIL}</a>로 게임 안 계정 코드(설정에서 볼 수 있음)와 함께 보내 주시면 10일 이내에 처리하고 결과를 알려 드립니다.</p>

<h2>8. 안전하게 지키는 방법</h2>
<ul>
<li>게임과 서버 사이의 전송은 암호화(HTTPS)합니다. 데이터베이스는 서버만 읽고 쓸 수 있고, 운영 기능은 운영자 키가 있어야 쓸 수 있습니다.</li>
<li>신청서와 메일은 운영자만 볼 수 있는 계정에 보관하고, 계정에는 2단계 인증을 씁니다.</li>
<li>목적이 끝난 정보는 위 기간 안에 지웁니다.</li>
</ul>

<h2>9. 만 14세 미만 이용자</h2>
<p>만 14세 미만은 외부 시험에 신청할 수 없습니다. 게임은 Steam·구글 계정 이용 규정에 따르며, 법정대리인의 동의 없이 미성년자가 결제한 경우 본인이나 법정대리인이 취소를 요청할 수 있습니다.</p>

<h2>10. 개인정보 보호책임자와 문의</h2>
<p>개인정보 보호책임자: {OPERATOR_KO}<br>연락처: <a href="mailto:{MAIL}">{MAIL}</a> (평일 기준 2일 이내 답장)</p>
<p>개인정보 침해 신고와 상담은 개인정보침해신고센터(privacy.kisa.or.kr, 국번 없이 118), 개인정보분쟁조정위원회(kopico.go.kr, 1833-6972), 대검찰청(국번 없이 1301), 경찰청(ecrm.police.go.kr, 국번 없이 182)에서도 받을 수 있습니다.</p>

<h2>11. 바뀌는 경우</h2>
<p>이 방침을 바꾸면 시행 7일 전(이용자에게 불리하면 30일 전)부터 이 페이지와 게임 안 공지로 바뀐 날짜와 내용을 알립니다.</p>""",
    ),
    "en": dict(
        title="Privacy Policy | Ashen Crown",
        description="What the Ashen Crown website and the game Ashen Crown: Dawn of the Empty Throne collect (game account, server saves, chat, reports and blocks, playtest sign-ups), how long it is kept and how it is deleted.",
        h1="Privacy policy",
        body=f"""<p class="lead">{OPERATOR_EN} ("we") collects only what the website and the game {GAME_EN} (the "Game") need, and deletes it when the purpose is done. If this English text and the Korean version differ, the Korean version prevails.</p>
<p class="meta">Website part effective 2026-11-11 · Game part {EFFECTIVE_EN} · Last updated {UPDATED}</p>

<h2>1. What we collect and why</h2>
<h3>The Game</h3>
<div class="tablewrap"><table>
<tr><th>When</th><th>What</th><th>Why</th></tr>
<tr><td>Sign-in (Steam)</td><td>Steam account ID (SteamID), Steam nickname</td><td>Identify your account, save and restore progress</td></tr>
<tr><td>Sign-in (web version, Google)</td><td>Your Google sign-in user ID (Firebase user ID). Your Google email, name and photo stay with Google's sign-in service (Firebase Authentication); the game server does not store them.</td><td>Identify your account, save and restore progress</td></tr>
<tr><td>Server saves</td><td>Game progress (save data), recovery copies, in-game name, purchase and delivery records, free Crown Gem records, access records (time and game version), error logs</td><td>Saving and restoring progress, purchase delivery and refunds, abuse prevention, bug fixing</td></tr>
<tr><td>Chat (world, order, direct)</td><td>Messages you send, chat name, public ID (a number that cannot be traced back to your account), time sent, filter and spam checks, chat bans, your direct-message list and DM setting</td><td>Deliver chat, stop abuse, spam and harassment</td></tr>
<tr><td>Reports and blocks</td><td>The reported message and its text, the reason, public IDs and names of the reporter and the reported player, your block list</td><td>Review reports and take action, hide blocked players</td></tr>
<tr><td>Knight orders</td><td>Order name and crest, member roster (public ID, name, role), join and leave times</td><td>Run orders and order chat</td></tr>
<tr><td>Arena ranking</td><td>In-game name, points, defense team</td><td>Rankings and matchmaking</td></tr>
<tr><td>Surveys and bug reports</td><td>What you send, game version and device info</td><td>Improve the game, fix bugs</td></tr>
<tr><td>Purchases</td><td>Order number, product, amount, time, status</td><td>Confirm delivery, prevent double delivery, handle refunds</td></tr>
</table></div>
<p>Card and bank details are handled by Valve (Steam) or the app store; we never receive them. We do not collect real names, phone numbers or national ID numbers.</p>
<h3>The website</h3>
<div class="tablewrap"><table>
<tr><th>When</th><th>What</th><th>Why</th></tr>
<tr><td>Playtest sign-up form</td><td>Required: nickname, email<br>Optional: your PC, favorite genres, message</td><td>To send test dates and instructions, and understand test hardware</td></tr>
<tr><td>Email to us</td><td>Your email address and message</td><td>To reply</td></tr>
<tr><td>Visit statistics (only if you allow)</td><td>Google Analytics cookies, pages viewed, rough location, device type</td><td>To see which content is read and improve the site</td></tr>
</table></div>

<h2 id="chat">2. What others see in chat, reports and blocks</h2>
<ul>
<li>Chat opens at account level 10. Your chat name and messages are visible to other players in that room. Direct messages are visible only to you and the other player.</li>
<li>The server checks every message first and blocks profanity, personal information (such as phone numbers) and advertising. Repeated hits lead to an automatic, temporary chat ban.</li>
<li>You can report any message and block its sender at the same time. A message reported by three different players is hidden until we review it.</li>
<li>We review reported messages and may hide them or ban chat. We do not open direct messages that have not been reported.</li>
<li>Messages from players you block are hidden from you, and they cannot send you direct messages.</li>
<li>Please do not post real names, phone numbers, addresses or other account details in chat.</li>
</ul>

<h2>3. How long we keep it</h2>
<div class="tablewrap"><table>
<tr><th>Data</th><th>Retention</th></tr>
<tr><td>Game account and server data</td><td>Deleted within 30 days of an account deletion request</td></tr>
<tr><td>Save recovery copies</td><td>Rolling 7 days (older copies are overwritten)</td></tr>
<tr><td>World chat messages</td><td>Deleted automatically 3 days after sending</td></tr>
<tr><td>Order chat and direct messages</td><td>Deleted automatically 30 days after sending</td></tr>
<tr><td>Report records</td><td>1 year after the case is closed</td></tr>
<tr><td>Surveys and bug reports</td><td>1 year</td></tr>
<tr><td>Payment records</td><td>5 years (Korean E-Commerce Act)</td></tr>
<tr><td>Access records</td><td>3 months (Korean Protection of Communications Secrets Act)</td></tr>
<tr><td>Playtest sign-ups</td><td>Within 30 days after that playtest ends</td></tr>
<tr><td>Emails</td><td>1 year after we reply</td></tr>
<tr><td>Website visit statistics</td><td>Google Analytics retention setting (14 months)</td></tr>
</table></div>
<p>Automatic deletion is carried out by the database after the period ends and may take about a day.</p>

<h2>4. Sharing and services that handle your data</h2>
<p>We never sell or hand your data to others, except where required by law or requested by investigative authorities through legal procedures. We use these services to run the Game and the website:</p>
<div class="tablewrap"><table>
<tr><th>Service (company, country)</th><th>Task</th><th>Data</th><th>Retention</th></tr>
<tr><td>Steam (Valve Corporation, USA)</td><td>Steam sign-in, payment, cloud saves</td><td>SteamID, payment info, saves</td><td>Per the service's policy</td></tr>
<tr><td>Firebase (Google LLC, USA · data stored in Seoul, Korea)</td><td>Game server: saves, chat, knight orders, rankings, web Google sign-in</td><td>The game data in section 1</td><td>As in section 3</td></tr>
<tr><td>ONE store (ONE store Co., Ltd., Korea)</td><td>Running the ONE store web version and payment (once payment opens)</td><td>ONE store account check, payment info</td><td>Per the service's policy</td></tr>
<tr><td>FormSubmit (Devro LABS, USA)</td><td>Forwards the playtest form to our inbox</td><td>What you enter in the form</td><td>Per the service's policy</td></tr>
<tr><td>Gmail (Google LLC, USA)</td><td>Stores and answers sign-ups and emails</td><td>Form and email content</td><td>As in section 3</td></tr>
<tr><td>Google Analytics (Google LLC, USA)</td><td>Website visit statistics (only if you allow)</td><td>Cookies, pages viewed, device info</td><td>14 months</td></tr>
<tr><td>GitHub Pages (GitHub, Inc., USA)</td><td>Hosts the website and web version</td><td>Access logs (such as IP address)</td><td>Per the service's policy</td></tr>
</table></div>
<p>Data is sent over an encrypted internet connection when you play, send the form or visit the site. If you do not want it sent overseas, you can skip online features (server saves, chat, orders, rankings, payment), email us instead of using the form, or decline analytics; those features will then be unavailable.</p>

<h2>5. Deletion</h2>
<p>Electronic files are deleted so they cannot be recovered. Backups and recovery copies are overwritten when their period ends. To delete your game account, email us (section 7); an in-game delete button is in preparation.</p>

<h2 id="analytics">6. Cookies and data on your device</h2>
<p>The Game also stores saves and settings on your device (the game folder or browser storage) and uses no advertising or tracking cookies. On your first visit the website asks whether we may use analytics cookies. Google Analytics runs only if you choose Allow, with IP addresses shortened. The site works the same if you decline.</p>
<p><a href="#" data-consent-reset>Change your analytics choice</a></p>

<h2>7. Your rights</h2>
<p>You can ask to see, correct or delete your data (including account deletion), or ask us to stop using it. Email <a href="mailto:{MAIL}">{MAIL}</a> with your in-game account code (shown in Settings) and we will act within 10 days.</p>

<h2>8. Keeping it safe</h2>
<ul>
<li>Traffic between the Game and the server is encrypted (HTTPS). Only the server can read or write the database, and operator functions require an operator key.</li>
<li>Sign-ups and emails are kept in an account only the operator can access, protected with two-step verification.</li>
<li>Data is deleted within the periods above.</li>
</ul>

<h2>9. Children under 14</h2>
<p>Children under 14 may not sign up for playtests. The Game follows Steam's and Google's account rules. If a minor pays without a guardian's consent, the minor or the guardian may ask for cancellation.</p>

<h2>10. Contact</h2>
<p>Privacy officer: {OPERATOR_EN}, <a href="mailto:{MAIL}">{MAIL}</a> (reply within 2 business days, Korean time).</p>

<h2>11. Changes</h2>
<p>If this policy changes, we announce the date and the changes on this page and in the Game 7 days before they take effect (30 days if unfavorable to you).</p>""",
    ),
}

PACKS = [  # data/crownGems.ts CROWN_GEM_PACKS (game PR #685, 11/19 20% price cut): gems, bonus, first-purchase bonus, price KRW
    (80, 0, 80, 990), (320, 16, 320, 3900), (640, 48, 640, 7900),
    (1280, 128, 1280, 15900), (3200, 400, 3200, 39900), (6400, 960, 6400, 79900),
]
PULL = 160  # data/gacha.ts PULL_COST (Crown Gems per companion pull)


def _pack_rows(lang):
    rows = []
    for g, b, f, p in PACKS:
        total = g + b
        per = round(p / (total / PULL))
        if lang == "ko":
            extra = f'<br><small>덤 {b:,} 포함</small>' if b else ''
            rows.append(f'<tr><td class="num">₩{p:,}</td><td class="num">{total:,}{extra}</td><td class="num">+{f:,}</td><td class="num">약 ₩{per:,}</td></tr>')
        else:
            extra = f'<br><small>incl. {b:,} bonus</small>' if b else ''
            rows.append(f'<tr><td class="num">₩{p:,}</td><td class="num">{total:,}{extra}</td><td class="num">+{f:,}</td><td class="num">≈ ₩{per:,}</td></tr>')
    return "\n".join(rows)


STORE = {
    "ko": dict(
        title="상품 가격 안내 | Ashen Crown 애션 크라운",
        description="애션 크라운의 게임 안 유료 상품(왕관석 묶음, 월간 패스 ₩5,500, 잿빛 패스 ₩11,000)의 가격과 구성, 환불 안내입니다.",
        h1="상품 가격 안내",
        body=f"""<p class="lead">「{GAME_KO}」는 무료로 플레이하고, 원하면 게임 안에서 아래 상품을 살 수 있습니다. 확률로 결과가 정해지는 것은 <a href="/odds/">확률 공개표</a>에 모두 적었습니다.</p>
<p class="meta">기준일 {UPDATED} · 원화(부가세 포함) · 지금은 출시 전이라 판매하지 않으며, 출시 때 바뀌면 이 페이지를 먼저 고칩니다.</p>

<h2>1. 왕관석 (유료 재화)</h2>
<p>왕관석으로 동료 소환(1회 160 · 10회 1,600)과 장비 소환(1회 100 · 10회 1,000)을 합니다. 무료로 받은 왕관석과 산 왕관석은 확률·천장이 같습니다.</p>
<div class="tablewrap"><table class="odds">
<thead><tr><th class="num">가격</th><th class="num">받는 왕관석</th><th class="num">첫 구매 덤</th><th class="num">소환 1회 값</th></tr></thead>
<tbody>
{_pack_rows("ko")}
</tbody></table></div>
<ul>
<li>첫 구매 덤은 묶음마다 계정당 한 번, 산 왕관석만큼 더 줍니다.</li>
<li>덤과 첫 구매 덤은 무료 왕관석으로 들어가고, 쓸 때는 무료 왕관석부터 먼저 씁니다. 환불은 산 왕관석만 대상입니다.</li>
<li>왕관석은 일일·주간 임무, 기사단 출석, 업적, 수배 의뢰로도 모을 수 있습니다.</li>
</ul>

<h2>2. 월간 패스 · ₩5,500 (30일)</h2>
<p>사면 바로 왕관석 300개, 그 뒤 30일 동안 매일 접속하면 그날 보상을 받습니다. 왕관석으로는 살 수 없습니다. 사용 중에는 순환 상점 무료 새로고침이 진열 주기마다 한 번 붙습니다.</p>
<div class="tablewrap"><table>
<tr><th>30일 합계 (매일 접속했을 때)</th><th>내용</th></tr>
<tr><td>왕관석</td><td class="num">2,100 (바로 300 + 매일 60)</td></tr>
<tr><td>봉인된 장비 상자</td><td class="num">3 (7·14·21일차, 등급은 열 때 정해짐: 레어 80% · 유니크 18% · 에픽 2%)</td></tr>
<tr><td>해방석</td><td class="num">4</td></tr>
<tr><td>장비 강화석</td><td class="num">60</td></tr>
<tr><td>축복받은 강화석 · 잿불 연마석</td><td class="num">각 3</td></tr>
<tr><td>경험치 물약</td><td class="num">15</td></tr>
<tr><td>골드 · 잿불 결정</td><td class="num">32,680 · 920</td></tr>
</table></div>
<p>하루라도 접속하지 않은 날의 보상은 그날이 지나면 받을 수 없습니다. 이미 사용 중일 때는 다시 살 수 없습니다.</p>

<h2>3. 잿빛 패스 프리미엄 · ₩11,000 (시즌 6주)</h2>
<p>시즌(42일) 동안 전투·레이드·임무·투기장으로 경험치를 모아 30단계까지 올리며, 단계마다 무료 보상에 더해 프리미엄 보상을 받습니다. 왕관석으로는 열 수 없습니다.</p>
<div class="tablewrap"><table>
<tr><th>프리미엄 보상 합계 (30단계)</th><th>내용</th></tr>
<tr><td>왕관석</td><td class="num">1,200</td></tr>
<tr><td>봉인된 장비 상자</td><td class="num">7 (레어 80% · 유니크 18% · 에픽 2%)</td></tr>
<tr><td>신화 조각</td><td class="num">20</td></tr>
<tr><td>해방석</td><td class="num">7</td></tr>
<tr><td>장비 강화석 · 경험치 물약</td><td class="num">60 · 24</td></tr>
<tr><td>축복받은 강화석 · 잿불 연마석</td><td class="num">각 6</td></tr>
<tr><td>골드 · 잿불 결정</td><td class="num">83,800 · 1,960</td></tr>
<tr><td>30단계</td><td>SSR 동료 하나 고르기</td></tr>
</table></div>
<p>무료 보상(누구나): 왕관석 150, 봉인된 장비 상자 3, 레어 장비 상자 3, 해방석 3 등. 시즌이 끝나면 받지 않은 단계 보상은 사라집니다.</p>

<h2>4. 결제와 환불</h2>
<ul>
<li>결제는 Steam판은 Steam 결제로만 합니다. 다른 나라 통화 가격은 Steam 가격표를 따릅니다.</li>
<li>산 지 7일 안에 전혀 쓰지 않은 상품은 청약철회(환불)할 수 있습니다. 이미 쓴 왕관석, 받기 시작한 패스, 연 확률형 상품은 철회할 수 없고, 구매 화면에 미리 표시합니다.</li>
<li>법정대리인 동의 없이 미성년자가 결제했다면 본인이나 법정대리인이 취소를 요청할 수 있습니다.</li>
<li>환불 문의: Steam 고객지원 또는 <a href="mailto:{MAIL}">{MAIL}</a> (구매 일시·상품명을 적어 주세요).</li>
</ul>""",
    ),
    "en": dict(
        title="Prices | Ashen Crown",
        description="Prices and contents of in-game purchases in Ashen Crown: Crown Gem packs, the Monthly Pass (₩5,500) and the Ashen Pass Premium (₩11,000), plus refunds.",
        h1="Prices",
        body=f"""<p class="lead">{GAME_EN} is free to play. These optional purchases are available in the game. Every random outcome is listed on the <a href="/en/odds/">odds page</a>.</p>
<p class="meta">As of {UPDATED} · Korean won, VAT included · Not on sale yet (pre-release). If prices change at launch, this page is updated first. Prices in other currencies follow Steam's price table.</p>

<h2>1. Crown Gems (premium currency)</h2>
<p>Crown Gems pay for companion summons (160 per pull, 1,600 for 10) and gear summons (100 per pull, 1,000 for 10). Free and purchased Crown Gems have the same odds and pity.</p>
<div class="tablewrap"><table class="odds">
<thead><tr><th class="num">Price</th><th class="num">Crown Gems</th><th class="num">First-buy bonus</th><th class="num">Per pull</th></tr></thead>
<tbody>
{_pack_rows("en")}
</tbody></table></div>
<ul>
<li>The first-buy bonus doubles the purchased gems, once per pack per account.</li>
<li>Bonuses count as free gems and free gems are spent first. Only purchased gems can be refunded.</li>
<li>Crown Gems can also be earned from daily and weekly missions, order check-ins, achievements and bounties.</li>
</ul>

<h2>2. Monthly Pass · ₩5,500 (30 days)</h2>
<p>300 Crown Gems right away, then a reward each day you log in for 30 days. Cannot be bought with Crown Gems. While active, you also get one free shop refresh per rotation.</p>
<div class="tablewrap"><table>
<tr><th>30-day total (logging in every day)</th><th>Amount</th></tr>
<tr><td>Crown Gems</td><td class="num">2,100 (300 now + 60 a day)</td></tr>
<tr><td>Sealed Gear Box</td><td class="num">3 (days 7, 14, 21; grade rolled on opening: Rare 80% · Unique 18% · Epic 2%)</td></tr>
<tr><td>Liberation Stones</td><td class="num">4</td></tr>
<tr><td>Enhancement Stones</td><td class="num">60</td></tr>
<tr><td>Blessed Enhancement Stones · Ember Hone Stones</td><td class="num">3 each</td></tr>
<tr><td>EXP Potions</td><td class="num">15</td></tr>
<tr><td>Gold · Ember Crystals</td><td class="num">32,680 · 920</td></tr>
</table></div>
<p>A day's reward expires if you don't log in that day. You can't buy it again while it is active.</p>

<h2>3. Ashen Pass Premium · ₩11,000 (6-week season)</h2>
<p>Earn pass XP from battles, raids, missions and the arena over a 42-day season to reach level 30. Premium adds a second reward track. Cannot be unlocked with Crown Gems.</p>
<div class="tablewrap"><table>
<tr><th>Premium total (30 levels)</th><th>Amount</th></tr>
<tr><td>Crown Gems</td><td class="num">1,200</td></tr>
<tr><td>Sealed Gear Box</td><td class="num">7 (Rare 80% · Unique 18% · Epic 2%)</td></tr>
<tr><td>Mythic Fragments</td><td class="num">20</td></tr>
<tr><td>Liberation Stones</td><td class="num">7</td></tr>
<tr><td>Enhancement Stones · EXP Potions</td><td class="num">60 · 24</td></tr>
<tr><td>Blessed Enhancement Stones · Ember Hone Stones</td><td class="num">6 each</td></tr>
<tr><td>Gold · Ember Crystals</td><td class="num">83,800 · 1,960</td></tr>
<tr><td>Level 30</td><td>Choose one SSR companion</td></tr>
</table></div>
<p>Free track (everyone): 150 Crown Gems, 3 Sealed Gear Boxes, 3 Rare Gear Boxes, 3 Liberation Stones and more. Unclaimed rewards expire when the season ends.</p>

<h2>4. Payment and refunds</h2>
<ul>
<li>On Steam, purchases go through Steam only.</li>
<li>Products left completely unused can be withdrawn (refunded) within 7 days. Spent gems, passes already started and opened random items cannot be withdrawn; this is shown on the purchase screen in advance.</li>
<li>If a minor paid without a guardian's consent, the minor or the guardian may request cancellation.</li>
<li>Refunds: Steam Support or <a href="mailto:{MAIL}">{MAIL}</a> with the purchase date and product name.</li>
</ul>""",
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
        st = STORE[lang]
        out.append((pre + "store/index.html", page(lang, "store", st["title"], st["description"], st["h1"], st["body"])))
        out.append((pre + "odds/index.html", page(lang, "odds", ODDS[lang]["title"], ODDS[lang]["description"], ODDS[lang]["h1"], odds.page_body(lang))))
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
