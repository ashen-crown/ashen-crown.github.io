/* Ashen Crown: Google Analytics, loaded only after the visitor allows it.
   To turn analytics on, put the GA4 measurement ID (starts with "G-") below. Empty = no analytics, no banner. */
(function () {
  var GA_ID = "G-RY5YRW8T6X";
  var KEY = "ac-analytics";
  var lang = document.documentElement.lang === "en" ? "en" : "ko";
  var T = {
    ko: { text: "방문 통계를 보려고 구글 애널리틱스 쿠키를 써도 될까요? 어떤 화면을 많이 보는지만 알 수 있고, 누구인지는 알 수 없어요.", yes: "허용", no: "허용 안 함", more: "자세히", href: "/privacy/#analytics" },
    en: { text: "May we use Google Analytics cookies to count visits? It shows which parts of the page are viewed, not who you are.", yes: "Allow", no: "Decline", more: "Details", href: "/en/privacy/#analytics" }
  }[lang];

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  window.acTrack = function () {};

  function load() {
    if (!GA_ID || window.gtag) return;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });
    window.acTrack = function (name, params) { window.gtag("event", name, params || {}); };
  }

  function banner() {
    var box = document.createElement("div");
    box.className = "consent";
    box.setAttribute("role", "region");
    box.setAttribute("aria-live", "polite");
    box.setAttribute("aria-label", lang === "en" ? "Analytics cookies" : "분석 쿠키");
    var p = document.createElement("p");
    p.textContent = T.text + " ";
    var a = document.createElement("a");
    a.href = T.href; a.textContent = T.more;
    p.appendChild(a);
    var acts = document.createElement("div");
    acts.className = "acts";
    [["yes", "btn btn-primary"], ["no", "btn btn-ghost"]].forEach(function (b) {
      var btn = document.createElement("button");
      btn.type = "button"; btn.className = b[1]; btn.textContent = T[b[0]];
      btn.addEventListener("click", function () {
        set(b[0] === "yes" ? "granted" : "denied");
        box.remove();
        if (b[0] === "yes") load();
      });
      acts.appendChild(btn);
    });
    box.appendChild(p); box.appendChild(acts);
    document.body.appendChild(box);
  }

  // "쿠키 설정 다시 고르기" links: <a href="#" data-consent-reset>
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-consent-reset]");
    if (!t) return;
    e.preventDefault();
    try { localStorage.removeItem(KEY); } catch (err) {}
    if (GA_ID && !document.querySelector(".consent")) banner();
  });

  if (!GA_ID) return;
  var c = get();
  if (c === "granted") load();
  else if (c !== "denied") banner();
})();
