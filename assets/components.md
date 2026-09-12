# 컴포넌트 레퍼런스

슬라이드 하나 = `<section class="slide">` 하나. 표지·부 구분·마무리는 `class="slide cover"`
(세로 가운데 정렬 + 부 경계 판정을 겸한다).

## 무엇을 쓸지 먼저 고른다

내용의 성격이 컴포넌트를 정한다. 취향으로 고르면 같은 덱 안에서 위계가 흔들린다.

| 담을 내용 | 컴포넌트 | 절 |
|---|---|---|
| 표지 · 부 구분 · 마무리 | `cover` | §1 |
| 목차 | `agenda` | §2 |
| 두 개념 대비 | `duo` (2단 패널) | §3 |
| 3~4개 병렬 항목 | `cards` | §4 |
| 순서 3단계 | `flow` | §5 |
| 순서 4~5단계 | `map` (가로 로드맵) | §6 |
| 용어 정의 5~6개 | `wide` + `deflist` | §7 |
| 한 문장 결론 | `banner` | §8 |
| **숫자를 표·그래프로** | **`exhibits.md` 로 간다** | 별도 |

**본문 한 장의 핵심 요점은 2~4개.** 그보다 많으면 나눈다.
같은 성격의 내용은 같은 컴포넌트로 간다. 설계 단계에서 매핑을 정하고 끝까지 지킨다.

## 공통 규칙

### 캔버스

- **1280×720 고정.** 내용이 넘치면 **슬라이드를 쪼갠다.** 폰트 축소로 욱여넣지 않는다
- 본문 슬라이드의 그림 칸은 약 **1088 × 340**. 전시물 SVG 는 **가로 1080 기준 높이 330~360**
  으로 그린다. 비율이 어긋나면 `meet` 로 축소되어 **글자만 작아진다.** 넘침 검사에는 안 걸린다
- 세 패널을 한 장에 욱여넣지 말고 두 장으로 나눈다

### 색

한 슬라이드 안 여러 요소는 `a1 → a2 → a3` 순환. 경고·리스크는 `risk`.
컴포넌트마다 받는 변수 이름이 다르다.

| 컴포넌트 | 변수 |
|---|---|
| 카드 · 단계 | `--c`(막대) + `--ct`(글자) |
| 패널 | `--pc` + `--pct` (+ 배경 콜아웃 `--pbg`) |
| role | `--rc` + `--rcT` + `--g`(광채) |
| agenda | `--ac` + `--act` |

**한 요소의 색은 한 곳에서만 드러낸다.** 장의 색은 고스트 번호가 진다.
제목에 밑줄을, 카드에 막대를 겹치지 않는다.

### 글자

- 제목 안 강조는 `<span class="mark">`(단색). 본문 강조는 `<b>`(잉크색)
- 흐릿한 부가정보는 `style="color:var(--faint)"`, 명령어는 `<span class="mono">/clear</span>`
- **이모지 미사용.** 라벨은 텍스트로
- **줄바꿈**: `word-break:keep-all` 이 걸려 있어 한글은 어절 단위로만 끊긴다.
  두 줄이 필요한 제목은 `<br>` 로 자리를 지정한다. 브라우저에 맡기면 `것입니 / 다` 가 나온다.
  숫자와 단위(`420억`), 배수(`7.9배`)는 사이에 공백을 넣지 않는다

### 등장과 손질

- 등장 순서대로 `data-anim style="--d:N"` (N 은 0,1,2…)
- **문구 손질은 브라우저에서.** 산출 HTML 을 열고 `Ctrl+Shift+E` → 글자를 눌러 고침 → `Ctrl+S`.
  SVG 라벨도 고쳐진다. **`Alt` + 도형 클릭으로 색을 돌린다**(강조를 다른 막대로 옮길 때).
  값·축 범위처럼 계산이 걸린 것만 생성기로 돌아간다

---

## 1. 표지 / 부 구분 / 마무리 (cover)

```html
<section class="slide cover">
  <div class="eyebrow" data-anim style="--d:0"><span class="dot"></span><b>주제 라벨</b><span class="en">· ORIENTATION</span></div>
  <h1 class="title" data-anim style="--d:1">큰 제목 1줄<br><span class="mark">강조 제목 2줄</span></h1>
  <p class="sub" data-anim style="--d:2">부제 · 키워드 나열<br>한 줄 요약</p>
</section>
```
- 부 구분(divider)도 같은 구조. eyebrow를 `<b>제1부 · 부 제목</b><span class="en">· PART</span>`로.
- 마무리엔 하단에 `<div class="legend" data-anim style="--d:3"><span class="pill human"><i></i>질문 · Q&amp;A</span></div>` 추가 가능.

## 2. 목차 (agenda)

```html
<section class="slide">
  <div class="head">
    <div class="eyebrow" data-anim style="--d:0"><span class="dot"></span>목차 <span class="en">AGENDA</span></div>
    <h2 class="title" data-anim style="--d:1">오늘 함께 볼 <span class="mark">다섯 갈래</span></h2>
    <p class="sub" data-anim style="--d:2">한 줄 소개</p>
  </div>
  <div class="agenda">
    <div class="arow" data-anim style="--d:3; --ac:var(--a1); --act:var(--a1t)">
      <div class="no">01</div>
      <div class="tx"><h3>항목명</h3><p>세부 키워드</p></div>
      <div class="en">SECTION</div>
    </div>
    <!-- 02(a2), 03(a3), 04(a1)… 색 순환, --d 증가 -->
  </div>
</section>
```

## 3. 2단 대비 (duo) — 가장 자주 쓰는 본문 레이아웃

```html
<section class="slide">
  <div class="head">
    <div class="eyebrow" data-anim style="--d:0"><span class="dot"></span>2-1 · 소주제 <span class="en">TALK / WORK</span></div>
    <h2 class="title" data-anim style="--d:1">개념 A vs <span class="mark">개념 B</span></h2>
    <p class="sub" data-anim style="--d:2">대비의 핵심</p>
  </div>
  <div class="duo">
    <div class="panel" data-anim style="--d:3; --pc:var(--a1); --pct:var(--a1t); --pbg:var(--a1b)">
      <div class="pk">좌측 라벨</div>
      <h3>좌측 제목</h3>
      <ul class="pts" style="flex:0 0 auto; margin-top:44px">
        <li>요점 — <b>강조</b></li>
        <li><b>키워드</b> — 설명</li>
      </ul>
      <!-- 하단 콜아웃(선택) -->
      <div class="usage">
        <div class="ut">라벨</div>
        <ul class="uw"><li>내용</li></ul>
      </div>
    </div>
    <div class="panel" data-anim style="--d:4; --pc:var(--a3); --pct:var(--a3t); --pbg:var(--a3b)">
      <div class="pk">우측 라벨</div>
      <h3>우측 제목</h3>
      <ul class="pts" style="flex:0 0 auto; margin-top:44px">
        <li>요점</li>
      </ul>
    </div>
  </div>
</section>
```
- `pts`에 요점이 3개 이하면 `style="flex:0 0 auto; margin-top:44px"`로 위쪽 정렬. 많으면 style 빼서 세로 중앙 정렬.
- `.usage` 안 `<li class="off">`는 비활성(흐림) 항목 표기.

## 4. 3단(또는 2단) 카드 (cards)

```html
<div class="cards">   <!-- 2단은 class="cards two" -->
  <div class="card" data-anim style="--d:3; --c:var(--a1); --ct:var(--a1t)">
    <div class="idx">01</div><h3>카드 제목</h3>
    <p>설명 문장. <b>강조</b></p>
  </div>
  <!-- 02(a2), 03(a3) -->
</div>
```
- 카드 안에 항목 리스트를 넣으려면 `<p>` 대신 `svc` 리스트:
```html
<ul class="svc">
  <li><span class="k">대화</span> ChatGPT</li>
  <li><span class="k">작업</span> Codex</li>
  <li class="ext"><span class="k">부가</span> Sora·이미지</li>  <!-- ext=점선 구분 보조행 -->
</ul>
```
- 카드 아래 배너를 덧붙이려면 `.cards`에 `style="margin-bottom:22px"` 주고 뒤에 `.banner` 배치.

## 5. 흐름 3단계 (flow: role ×3 + banner)

```html
<div class="flow">
  <div class="role" data-anim style="--d:3; --rc:var(--a1); --rcT:var(--a1t); --g:var(--a1)">
    <div class="lab"><i></i>STEP 01</div>
    <h3>단계명</h3>
    <div class="items">내용<br>보조</div>
    <div class="note">각주</div>
  </div>
  <div class="arrow" data-anim style="--d:4">→</div>
  <!-- STEP 02(a2), arrow, STEP 03(a3) -->
</div>
<div class="banner" data-anim style="--d:8">핵심 한 문장 — <b>강조</b></div>
```

## 6. 로드맵 (map: step ×N + rail)

```html
<div class="map">
  <div class="step" data-anim style="--d:3; --sc:var(--a1); --sct:var(--a1t)">
    <div class="n">STEP 01</div><h3>단계</h3><p>설명</p>
  </div>
  <div class="marw" data-anim style="--d:4">→</div>
  <!-- step/marw 반복. 4~6단계까지 가로로 -->
</div>
<div class="rail" data-anim style="--d:9">
  <div class="msg"><b>핵심</b> 메시지</div>
  <div class="tools">
    <span class="tool"><i></i><span class="mono">/명령</span> 설명</span>
  </div>
</div>
```

## 7. 넓은 정의 목록 (wide + deflist) — 용어 5~6개 한 화면

```html
<div class="wide" data-anim style="--d:3">
  <div class="panel" style="--pc:var(--a1); --pct:var(--a1t)">
    <div class="deflist">
      <div class="row">
        <div class="cw"><span class="c">용어</span></div>
        <div class="k">짧은 정의</div>
        <div class="d">긴 설명</div>
      </div>
      <!-- row 반복 -->
    </div>
  </div>
</div>
```
**칸 폭이 고정돼 있다 — 글자를 칸에 맞춘다.**

| 자리 | 폭 | 넣을 수 있는 분량 |
|---|---|---|
| `.cw .c` (배지) | 128px 칸 · 15px 볼드 | **한글 5자 내외** |
| `.k` (짧은 정의) | **116px 고정** · 18px 볼드 | **한글 6자 내외** — 넘으면 소리 없이 두 줄이 된다 |
| `.d` (설명) | 나머지 전부 | 길어도 된다. 넘치는 말은 전부 여기로 |

`.k` 에 `무엇을 놓고 하나`(8자)를 넣으면 두 줄이 되고, `.slide` 가 `overflow:hidden` 이라 아래가 잘린다.
**칸을 넓히지 말고 글자를 줄인다** — `무엇을 놓고` 로 줄이고 나머지는 `.d` 로 내린다.
`slidecheck.ps1` 이 이 줄바꿈을 잡아 준다.

- 한 컬럼 세로 나열형 glossary가 필요하면 `.wide` 없이 `.deflist`만 패널 안에 두고 `.row`에 `.t`/`.d` 구조 사용.

## 8. 강조 배너 (banner) — 단독으로도 사용

```html
<div class="banner" data-anim style="--d:6">평범한 문장 — <b>결정적 한마디</b></div>
```

---

## 표 · 그래프

이 파일에는 없다. **`exhibits.md` 가 정본이다** — `tbl`(표 3종), `chart`(그래프 7종), 그리고 도표 부호 규칙.
그래프 조각은 `scripts/mkchart.py` 가 숫자에서 뽑는다.

---

## 슬라이드 개수·분량 감각

- 본문 슬라이드 하나엔 **핵심 요점 2~4개**. 그 이상이면 나눈다.
- duo 패널의 `pts` 항목은 한쪽당 **2~4개, 각 1~2줄**.
- 카드 설명 `<p>`는 **2~3줄** 이내.
- 제목(`head .title`)은 **한 줄**, 부제(`head .sub`)는 **한 줄** 권장.

---

## 쓰지 말 것 (전 컴포넌트 공통)

인쇄와 실측을 동시에 깨뜨리는 것들이다. 화면에서는 멀쩡해 보이므로 발견이 늦다.

| 쓰지 말 것 | 무슨 일이 일어나는가 | 대신 |
|---|---|---|
| 보고서용 SVG(세로로 긴 것)를 슬라이드에 그대로 넣기 | viewBox 비율이 안 맞아 축소된다. 12.5px 글자가 7px 로 렌더되는데 넘침 검사는 통과한다 | 높이 330~360 의 슬라이드 판을 따로 그린다 |
| `word-break` 를 지우거나 `break-all` 로 바꾸기 | 한글이 어절 중간에서 끊긴다. 제목이 `것입니 / 다` 로 갈라져도 넘침 검사는 통과한다 | `keep-all` 을 그대로 두고 `<br>` 로 끊을 자리를 지정한다 |
| `opacity` (등장 애니메이션 제외) | 인쇄 시 **합성 레이어**가 생겨 그 글자가 독립 텍스트 스트림이 된다. `printcheck.ps1`의 '스트림 하나 = 페이지 하나' 가정이 깨져 **페이지 0쪽으로 보고**된다 | 옅은 단색(`--a1b` 등)으로 채운다 |
| `background-clip:text` 그라데이션 글자 | 인쇄에서 글자가 **통째로 사라진다** | `.mark` 처럼 단색 |
| `color:transparent` + `-webkit-text-stroke` | 위와 같다 | 옅은 단색 채움 |
| `mix-blend-mode` · `filter` | 래스터화되어 텍스트가 이미지가 된다 | 쓰지 않는다 |
| 색 리터럴(`#2E6BFF`) | 테마 교체가 불가능해진다 | 토큰(`var(--a1)`)만 |
| `inline-flex` + `border-radius` 배지 | 별도 페인트 레이어가 생겨 위와 같은 사고를 낸다 | `inline-block` |
| 글자 위 `box-shadow: inset` 형광 밑줄 | 인쇄에서 **취소선처럼** 읽힌다 | 굵기(`<b>`)로만 강조 |
| `.wide`·`.cards`·`.duo` 뒤에 `.banner` 를 그냥 붙이기 | 셋 다 `flex:1` 이라 남은 높이를 먼저 다 먹는다. 배너가 그 위로 앉아 **패널 마지막 줄이 잘린다.** `.slide` 가 `overflow:hidden` 이라 넘침 검사도 통과한다(2026-09-10 삼일PwC 덱에서 deflist 5행이 잘림) | 컨테이너에 `flex:0 0 auto; margin-bottom:22px` 를 같이 준다. `0 1 auto` 는 여전히 줄어들어 잘린다. `.flow` 는 `margin-bottom:24px` 가 이미 있어 그대로 써도 된다 |

`[data-anim]`의 `opacity`·`transform`은 예외다 — 인쇄 CSS가 이미 무력화한다. 다만 **화면 측정 도구는 그 시작 위치를 실제 위치로 오인**하므로, 재기 전에 중화해야 한다(`slidecheck.ps1`이 그렇게 한다).

---

## 이 스킨에서 달라진 것 (원본 html-slides 대비)

| | 내용 |
|---|---|
| 본문 슬라이드 머리 | `<div class="head" data-n="01">` — 왼쪽 여백에 큰 고스트 번호가 깔린다. 표지·구분 슬라이드에는 주지 않는다 |
| 라벨 | `.eyebrow`는 배지다. 표지처럼 **flex 직계 자식**으로 놓일 때는 `align-self:flex-start`가 걸려 있어야 폭이 늘어나지 않는다(템플릿에 포함) |
| 카드·패널·단계 | 상단 그라데이션 막대 대신 **액센트 규칙선**(`border-top`) |
| 배너 | 잉크 채움 + 흰 글자 |
| 내비게이션 | **화면 위 조작부가 없다.** 좌하단 `.brandbar` 가 현재 부·부 진행바·전체 페이지를 읽어주고, **부 진행바의 칸이 곧 이동 버튼이다.** 그 밖에는 키보드·스와이프 |
| 이동 | `←/→`와 `↑/↓` 둘 다 받는다. 터치는 가로·세로 스와이프 모두 |

**검증은 눈이 아니라 `slidecheck.ps1`이 한다.** `.slide`는 `overflow:hidden`이라 넘친 줄은 그냥 안 보인다 — 한 줄이 잘려도 화면은 멀쩡하다.
