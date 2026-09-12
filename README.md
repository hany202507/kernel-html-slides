# kernel-html-slides

대본·마크다운·노트를 **1280×720 고정 캔버스의 단일 파일 HTML 슬라이드**로 만드는 Claude Code 스킬입니다.

디자인을 매번 새로 정하지 않습니다. 색·간격·컴포넌트가 `assets/template.html` 에 박제돼 있고,
클로드는 그 안에서 내용만 채웁니다. 넘쳤는지는 눈으로 보지 않고 `slidecheck.ps1` 로 잽니다.

## 설치

스킬 폴더에 그대로 넣습니다.

```bash
git clone https://github.com/hany202507/kernel-html-slides.git ~/.claude/skills/kernel-html-slides
```

윈도우 파워셸이면 이렇습니다.

```powershell
git clone https://github.com/hany202507/kernel-html-slides.git "$env:USERPROFILE\.claude\skills\kernel-html-slides"
```

클로드 코드를 다시 열면 스킬 목록에 잡힙니다. 「이 문서로 슬라이드 만들어줘」 라고 하면 트리거됩니다.

## 쓰는 법

변환할 문서를 주고 슬라이드를 만들어 달라고 합니다. 클로드가 `SKILL.md` 의 절차대로 구조를 설계하고,
템플릿을 복사해 채우고, 넘침을 실측하고, 문체를 점검합니다.

산출물은 HTML 한 개입니다. 브라우저에서 열면 방향키로 넘어가고 `F` 로 전체화면이 됩니다.
`Ctrl+Shift+E` 로 손질 모드를 켜면 화면에서 글자를 고치고 `Ctrl+S` 로 저장할 수 있습니다.

## 무엇이 들었나

| 폴더 | 무엇 |
|---|---|
| `SKILL.md` | 절차와 절대 원칙. 클로드가 읽는 본문 |
| `assets/template.html` | 디자인 정본. 색·간격·컴포넌트가 여기 박혀 있다 |
| `assets/theme.md` · `components.md` | 색 토큰과 컴포넌트 마크업 |
| `assets/tone.md` | **문체 정본.** 제목·부제·배너에 무엇을 담는지 자리마다 정해 뒀다 |
| `assets/exhibits.md` | 표 3종 · 그래프 13종. 숫자를 그릴 때 형태 고르는 순서 |
| `assets/finance-views.md` | 재무제표 분석 16뷰. CCC · 브릿지 · 듀폰 · 축구장 · 민감도 |
| `assets/advanced-views.md` | 막대로 답이 안 되는 질문용 13뷰. 토네이도 · 산키 · 팬 · 코호트 |
| `assets/slidecheck.ps1` | **넘침 실측기.** 1280×720 에서 일곱 가지를 잰다 |
| `scripts/` | 그래프 좌표 생성기와 갤러리 빌더 |
| `reference/` | 완성본 예시. 사람이 눈으로 보는 것이고 클로드는 읽지 않는다 |

## 넘침 검사

슬라이드는 `overflow:hidden` 이라 **넘친 줄이 그냥 안 보입니다.** 한 줄이 잘려 나가도 화면은 멀쩡합니다.
그래서 눈으로 판정하지 않고 잽니다.

```powershell
powershell -ExecutionPolicy Bypass -File assets/slidecheck.ps1 "C:\절대\경로\슬라이드.html"
```

일곱 가지를 봅니다. 캔버스를 넘쳤는가, 고정폭 라벨이 두 줄로 접혔는가, 제목이 어설프게 끊겼는가,
그림이 축소됐는가, 표지 제목이 가로로 넘쳤는가, 문장 중간에서 접혔는가, 그림이 viewBox 밖으로 나갔는가.

**넘치면 폰트를 줄이지 않고 슬라이드를 나눕니다.** 그것이 이 스킬의 첫 번째 원칙입니다.

크롬이나 엣지가 있어야 돌아갑니다. 맥·리눅스에는 파워셸이 없어 이 검사기가 안 돕니다.

## 예시

`reference/` 의 HTML 을 브라우저에서 열어 보십시오.

| 파일 | 무엇 |
|---|---|
| `스킬사용법.html` | 이 스킬로 만든 사용 설명서 |
| `기준_슬라이드.html` | 컴포넌트 기준 덱 |
| `전시물_갤러리.html` · `재무그래프_갤러리.html` | 표와 그래프 형태 목록 |
| `재무진단_서린푸드.html` · `서린푸드_머니플로우.html` | 재무 분석 덱 예시 |
| `전시물_아틀라스_독본.html` | 고급 전시물 아틀라스 |

**서린푸드는 가칭입니다.** 실존 기업이 아니고 숫자도 예시입니다.

## 자매 스킬

읽는 보고서 문서가 필요하면 `kernel-html-reports` 를 씁니다. 색 토큰(`assets/theme.md`)은 둘이 같습니다.

## 만든 사람

박상정 공인회계사. 문체 정본은 `assets/tone.md` 에 있습니다.
