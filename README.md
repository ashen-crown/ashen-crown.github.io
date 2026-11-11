# Ashen Crown

Ashen Crown(애션 크라운) 게임 소개 홈페이지입니다. GitHub Pages로 공개됩니다.

- 주소: https://ashen-crown.github.io/ (영어: https://ashen-crown.github.io/en/)
- 문의: ashencrown.support@gmail.com

이 저장소의 그림과 글은 Ashen Crown의 것이며, 허락 없이 다른 곳에 쓸 수 없습니다.
All images and text © 2026 Ashen Crown. All rights reserved.

## 처음 한 번 해야 하는 설정
- **구글 애널리틱스**: GA4 측정 ID(`G-`로 시작)를 `js/site.js` 맨 위 `GA_ID = ""` 따옴표 안에 넣습니다. 비워 두면 통계도, 동의 배너도 나오지 않습니다.
- **신청서(FormSubmit)**: 공개 후 첫 신청이 들어가면 FormSubmit이 ashencrown.support@gmail.com으로 확인 메일을 보냅니다. 그 메일의 버튼을 눌러야 그다음부터 신청서가 메일로 옵니다.

## 페이지 구성
- `index.html`, `en/index.html`: 본 페이지 (`tools/page.template.html`에서 만들어짐)
- `privacy/`, `thanks/`, `404.html` (+ `en/` 아래 영어판): `tools/pages.py`에서 만들어짐
- `sitemap.xml`, `robots.txt`: `tools/build.py`가 함께 만듦
- 공유 썸네일 `img/og.jpg`·`img/og-en.jpg`, 아이콘, `site.webmanifest`: `python tools/make_images.py` (그림이 바뀔 때만)

## 고치는 방법
문구는 `tools/page.template.html` 한 파일에 한국어(`lang="ko"`)·영어(`lang="en"`)가 함께 들어 있습니다.
고친 뒤 `python3 tools/build.py`를 실행하면 `index.html`(한국어)과 `en/index.html`(영어)이 만들어집니다.
