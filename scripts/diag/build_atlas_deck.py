# -*- coding: utf-8 -*-
"""전시물 아틀라스를 kernel-html-slides 덱으로 조립한다.

양식은 assets/template.html 그대로다. 1280x720 고정 캔버스, 좌하단 부 진행바,
키보드·스와이프·딥링크, 인쇄 CSS. 팔레트만 :root 스킨 교체로 아틀라스 색을 넣는다
(theme.md 의 '스타일을 갈아끼울 때' 절차. 색 리터럴은 :root 안에만 둔다).

    python build_atlas_deck.py
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(os.path.dirname(HERE))
TPL = os.path.join(SKILL, "assets", "template.html")
OUT = os.path.join(SKILL, "reference", "재무그래프_갤러리.html")

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import json  # noqa: E402
import mkchart  # noqa: E402
import atlas_ex as A  # noqa: E402
import exhibits  # noqa: E402
import slide_ex as X  # noqa: E402
import atlas3_ex as A3  # noqa: E402
import flow  # noqa: E402

TITLE = "재무 그래프 갤러리"

# ---------------------------------------------------------------- 스킨
SKIN = """  :root{
    --bg:#FFFFFF;
    --card:#FFFFFF;
    --tint:#F3F6F8;
    --ink:#0F1E2B;
    --body:#3E5364;
    --muted:#5B7186;
    --faint:#758798;
    --line:#C6D0D8;
    --line2:#DDE3E8;
    --rule:#0F1E2B;

    --a1:#1B3A57; --a1t:#132B41; --a1b:#E4EAEF;   /* 네이비 */
    --a2:#2E6F6B; --a2t:#21514E; --a2b:#E2EDEC;   /* 틸 */
    --a3:#B3762B; --a3t:#8A5A1F; --a3b:#F6EEE2;   /* 오커 */
    --risk:#8C3B36; --riskT:#6E2E2A; --riskB:#F5E7E6;

    --h1:#E7ECF0; --h2:#D8E0E6; --h3:#C6D2DA; --h4:#A9BCC9; --h5:#8AA2B3;
    --r1:#0F2A40; --r2:#1B3A57; --r3:#456A87; --r4:#7E9BB2; --r5:#B9CAD6;

    --sh:0 1px 2px rgba(15,30,43,.05);
    --sh-sm:0 1px 2px rgba(15,30,43,.04);

    /* 전시물 SVG 가 부르는 이름. 위 토큰의 별칭이라 스킨을 갈면 함께 간다 */
    --paper:var(--bg); --panel:var(--tint); --plot:var(--card);
    --ink-2:var(--body); --ink-3:var(--faint);
    --rule-soft:var(--line2); --grid:var(--line2);
    --c-navy:var(--a1); --c-teal:var(--a2); --c-ochre:var(--a3); --c-clay:var(--risk);
    --c-slate:#7A8C9B; --c-sand:#C9B893;
  }"""

EXTRA = """
  /* ---- 아틀라스 전시물 전용 ---- */
  /* 목차가 여섯 줄이라 기본 여백으로는 18px 넘친다. 이 덱에서만 좁힌다 */
  .agenda .arow{padding-top:10px; padding-bottom:10px}
  .agenda .arow .no{font-size:27px}
  .agenda .arow .tx h3{font-size:21px}
  .exhibit{flex:1; min-height:0; display:flex; flex-direction:column}
  .exhibit svg{width:100%; flex:1; min-height:0; display:block}
  .exnote{display:flex; gap:34px; margin-top:14px; flex-wrap:nowrap}
  .exnote div{font-size:14.5px; line-height:1.5; color:var(--body); flex:1}
  .exnote b{font-weight:800}
  .exnote .q b{color:var(--a1t)}
  .exnote .w b{color:var(--riskT)}
  .head .en2{font-family:'SF Mono',ui-monospace,Consolas,monospace;
    font-size:13px; font-weight:700; letter-spacing:.06em; color:var(--faint)}
  .sutbl{flex:1; min-height:0; display:flex; flex-direction:column; justify-content:center}
  .sutbl table{width:100%; border-collapse:collapse; table-layout:fixed}
  .sutbl th{text-align:left; font-size:13px; font-weight:800; letter-spacing:.08em;
    color:var(--faint); padding:0 16px 11px; border-bottom:2px solid var(--rule)}
  .sutbl th.num,.sutbl td.num{text-align:right; font-variant-numeric:tabular-nums}
  .sutbl td{font-size:17px; color:var(--body); padding:13px 16px;
    border-bottom:1px solid var(--line2)}
  .sutbl td b{color:var(--ink); font-weight:750}
  .sutbl tr.tot td{border-top:2px solid var(--rule); border-bottom:none;
    font-size:18px; font-weight:800; color:var(--ink)}
"""


def tw(t):
    """글자 폭을 한글 한 자를 1 로 놓고 센다. 숫자·영문·빈칸은 절반으로 본다."""
    return sum(1.0 if ord(c) > 0x2000 else 0.5 for c in t)


def sbr(t, w, pre=0.0):
    """어차피 두 줄로 흐를 글을 문장 경계에서 끊는다.

    문장 중간에서 접히면 읽다가 걸린다. 줄 수가 늘지 않는 자리만 고른다.
    폭은 글자 폭으로 어림하고, 실측은 assets/slidecheck.ps1 의 '문장 줄바꿈' 검사가 한다.
    pre 는 <b>답하는 질문.</b> 처럼 앞에 먼저 붙는 글자의 폭.
    """
    if "<br>" in t or tw(t) + pre <= w:
        return t
    # 문장으로 잘라 폭이 차는 데까지 담는다. 한 문장이 한 줄보다 길면 그 줄은 그냥 흐르게 둔다
    parts, at = [], 0
    for m in re.finditer(r"\. ", t):
        parts.append(t[at:m.end() - 1])
        at = m.end()
    parts.append(t[at:])
    if len(parts) < 2:
        return t
    lines, cur, head = [], "", pre
    for sen in parts:
        cand = sen if not cur else cur + " " + sen
        if cur and head + tw(cand) > w:
            lines.append(cur)
            cur, head = sen, 0.0
        else:
            cur = cand
    lines.append(cur)
    return "<br>".join(lines)


def cover(eyebrow, en, t1, t2, sub):
    sub = sbr(sub, 40)   # 표지 받침글 940px 에서 한 줄 최대 38 폭(실측)
    return ('      <section class="slide cover">\n'
            '        <div class="eyebrow" data-anim style="--d:0"><b>%s</b>'
            '<span class="en">· %s</span></div>\n'
            '        <h1 class="title" data-anim style="--d:1">%s<br>'
            '<span class="mark">%s</span></h1>\n'
            '        <p class="sub" data-anim style="--d:2">%s</p>\n'
            "      </section>\n" % (eyebrow, en, t1, t2, sub))


# 번호는 손으로 적지 않는다. 부를 끼워 넣으면 전부 밀려 틀리기 때문이다
_N = {"ex": 0, "part": 0, "sub": 0}


def part_cover(name, en, t1, t2, sub):
    """부 표지. 부 번호는 세어서 붙인다."""
    _N["part"] += 1
    _N["sub"] = 0
    return cover("제%d부 · %s" % (_N["part"], name), en, t1, t2, sub)


def exhibit(name, en, title, svg, q, warn):
    """전시물 한 장. 제목은 유형명이 아니라 발견한 사실."""
    # (2/2) 는 앞 장의 이어짐이라 번호를 새로 따지 않는다
    cont = name.endswith("(2/2)")
    if not cont:
        _N["ex"] += 1
        _N["sub"] += 1
    n = "%02d" % _N["ex"]
    eyebrow = "%d-%d · %s" % (_N["part"], _N["sub"], name)
    # 각주 칸 527px 에서 한 줄에 들어간 최대가 40.5 폭이었다(실측). 그 아래로는 건드리지 않는다
    q, warn = sbr(q, 41, pre=tw("답하는 질문. ")), sbr(warn, 41, pre=tw("함정. "))
    return (
        '      <section class="slide">\n'
        '        <div class="head" data-n="%s">\n'
        '          <div class="eyebrow" data-anim style="--d:0">%s '
        '<span class="en">%s</span></div>\n'
        '          <h2 class="title" data-anim style="--d:1">%s</h2>\n'
        "        </div>\n"
        '        <div class="exhibit" data-anim style="--d:2">\n%s\n        </div>\n'
        '        <div class="exnote" data-anim style="--d:3">\n'
        '          <div class="q"><b>답하는 질문.</b> %s</div>\n'
        '          <div class="w"><b>함정.</b> %s</div>\n'
        "        </div>\n      </section>\n" % (n, eyebrow, en, title, svg, q, warn))


SU = """<div class="sutbl">
  <table>
    <colgroup><col style="width:29%"><col style="width:17%"><col style="width:8%">
              <col style="width:29%"><col style="width:17%"></colgroup>
    <thead><tr><th>조달</th><th class="num">금액 (억원)</th><th></th>
      <th>사용</th><th class="num">금액 (억원)</th></tr></thead>
    <tbody>
      <tr><td><b>인수금융</b> · EBITDA의 4.4배</td><td class="num">210</td><td></td>
          <td><b>지분 인수대금</b></td><td class="num">380</td></tr>
      <tr><td><b>우선주</b></td><td class="num">90</td><td></td>
          <td><b>거래 비용</b></td><td class="num">18</td></tr>
      <tr><td><b>보통주</b></td><td class="num">120</td><td></td>
          <td><b>운전자금</b></td><td class="num">22</td></tr>
      <tr class="tot"><td>합계</td><td class="num">420</td><td></td>
          <td>합계</td><td class="num">420</td></tr>
    </tbody>
  </table>
</div>"""

sank, _ = flow.sankey({"rev": 320, "cogs": 231, "sga": 60, "op": 29, "dep": 19, "ebitda": 48,
                       "outs": [("운전자본 증가", 14, "leak"), ("설비투자", 11, "mid"),
                                ("이자", 4, "mid"), ("법인세", 5, "mid"), ("잉여현금", 14, "final")],
                       "final_sub": "전환율 29%"}, "dk", H=360, k=0.62)

# ---------------------------------------------------------------- 기본 재무 뷰
# 재무분석 갤러리(build_finance.py)와 같은 사양을 읽어 같은 그림을 쓴다.
# 겹치는 뷰(매출 브릿지·CCC·축구장·민감도)는 뒤 부에 이미 있어 빼놓았다
_SPECS = {d["key"]: d for d in json.loads(
    io.open(os.path.join(SKILL, "scripts", "finance_specs.json"), encoding="utf-8").read())}
CH = {k: mkchart.build(_SPECS[k]) for k in
      ("ebitda_walk", "common_size", "wc_trend", "netdebt", "ar_aging",
       "peer_margin", "growth_margin", "leverage")}

COMPS = """<div class="tbl">
  <table>
    <colgroup><col style="width:30%"><col style="width:16%"><col style="width:18%">
              <col style="width:18%"><col style="width:18%"></colgroup>
    <thead><tr><th>회사</th><th class="num">매출 (억원)</th><th class="num">EV / 매출</th>
      <th class="num">EV / EBITDA</th><th class="num">PER</th></tr></thead>
    <tbody>
      <tr><td><b>대한푸드시스템</b></td><td class="num">880</td><td class="num">1.6x</td>
          <td class="num">8.8x</td><td class="num">14.2x</td></tr>
      <tr><td><b>한울에프앤비</b></td><td class="num">410</td><td class="num">1.3x</td>
          <td class="num">7.9x</td><td class="num">12.6x</td></tr>
      <tr><td><b>명진식품</b></td><td class="num">1,250</td><td class="num">1.0x</td>
          <td class="num">7.4x</td><td class="num">11.8x</td></tr>
      <tr><td><b>가온에프씨</b></td><td class="num">190</td><td class="num">0.8x</td>
          <td class="num">6.5x</td><td class="num">10.4x</td></tr>
      <tr class="tot"><td>중앙값</td><td class="num">445</td><td class="num hi">1.15x</td>
          <td class="num hi">7.7x</td><td class="num hi">12.2x</td></tr>
    </tbody>
  </table>
</div>"""

# ---------------------------------------------------------------- 슬라이드
S = []
S.append(cover("재무 그래프 갤러리", "FINANCE EXHIBITS",
               "재무제표와 딜의 전시물 45종을",
               "한 회사의 숫자로 그렸습니다",
               "매출 320억 식품회사 서린푸드(가칭) 한 곳의 숫자로 전부 그렸습니다. "
               "묻고 싶은 것을 먼저 정하고 그 질문에 답하는 장을 찾아 쓰십시오. "
               "전부 예시 데이터입니다."))

S.append(
    '      <section class="slide">\n'
    '        <div class="head">\n'
    '          <div class="eyebrow" data-anim style="--d:0">목차 <span class="en">AGENDA</span></div>\n'
    '          <h2 class="title" data-anim style="--d:1">일곱 부, 마흔다섯 장</h2>\n'
    '          <p class="sub" data-anim style="--d:2">좌하단 진행바를 누르면 그 부로 바로 갑니다</p>\n'
    "        </div>\n"
    '        <div class="agenda">\n'
    + "".join(
        '          <div class="arow" data-anim style="--d:%d; --ac:var(--%s); --act:var(--%st)">\n'
        '            <div class="no">%s</div>\n'
        '            <div class="tx"><h3>%s</h3><p>%s</p></div>\n'
        '            <div class="en">%s</div>\n'
        "          </div>\n" % (3 + i, c, c, no, t, p, en)
        for i, (no, c, t, p, en) in enumerate([
            ("01", "a1", "재무제표 읽기", "EBITDA 워크 · 운전자본 · 채권 연령 · 비교기업", "BASICS"),
            ("02", "a2", "가치평가", "축구장 · 회귀 · 몬테카를로 · 토네이도", "VALUATION"),
            ("03", "a3", "딜 구조", "조달과 사용 · 수익 원천 · 만기 분포", "DEAL"),
            ("04", "a1", "실적·현금 분해", "손익 생키 · CCC · 듀폰 · 원가곡선", "PERFORMANCE"),
            ("05", "a2", "시장·경쟁", "이익 풀 · 기울기 · 상자 · 덤벨", "MARKET"),
            ("06", "a3", "고객·실행", "고래곡선 · 코호트 · 볼링 · 팬차트", "CUSTOMER"),
            ("07", "a1", "컨설팅 펌과 IR", "파워커브 · 세 지평선 · Rule of 40 · 계약잔고", "FIRM & IR"),
        ]))
    + "        </div>\n      </section>\n")

# ---- 제1부 · 재무제표 읽기
S.append(part_cover("재무제표 읽기", "PART", "요약해 옮겨 적는 것은",
                    "분석이 아닙니다",
                    "재무제표 한 벌에서 먼저 그리는 아홉 가지입니다. 여기까지가 기본이고 다음 부부터가 딜입니다"))
S.append(exhibit("EBITDA 워크", "MARGIN WALK",
                 "판관비 41억 중 24억이 인건비입니다", CH["ebitda_walk"],
                 "매출총이익에서 EBITDA 까지 무엇이 얼마를 깎는가.",
                 "감가상각을 어디서 뺐는지 밝힙니다. 매출원가에 섞여 있으면 EBITDA 가 달라집니다."))
S.append(exhibit("공통형 손익", "COMMON SIZE",
                 "매출 24% 증가에 판관비는 20% 증가", CH["common_size"],
                 "금액이 늘었나 구성비가 늘었나. 둘은 다른 이야기다.",
                 "비율만 그리면 규모가 사라집니다. 금액을 같이 적습니다."))
S.append(exhibit("운전자본 추세", "DSO / DIO / DPO",
                 "매출채권은 잡았고 재고는 못 잡았습니다", CH["wc_trend"],
                 "묶인 돈이 어디서 늘었는가.",
                 "DSO 는 매출로, DIO 와 DPO 는 매출원가로 나눕니다. 셋 다 매출로 나누면 틀립니다."))
S.append(exhibit("순차입금 브릿지", "NET DEBT BRIDGE",
                 "EBITDA 48억을 벌고 차입금은 14억 줄었습니다", CH["netdebt"],
                 "번 돈과 갚은 돈 사이에 무엇이 끼어 있는가.",
                 "리스부채를 넣었는지에 따라 결론이 뒤집힙니다. 각주로 못 박습니다."))
S.append(exhibit("매출채권 연령", "AR AGING",
                 "잔액은 줄었는데 90일 초과는 2억에서 5억", CH["ar_aging"],
                 "받을 돈이 얼마나 늙었는가.",
                 "총액만 보면 좋아진 것으로 읽힙니다. 나이대로 갈라야 보입니다."))
S.append(exhibit("마진 벤치마킹", "BENCHMARK",
                 "동종 5개사 중 3위, 중앙값과 같습니다", CH["peer_margin"],
                 "동종 안에서 우리 마진이 어디인가.",
                 "평균이 아니라 중앙값을 씁니다. 한 곳이 튀면 평균이 끌려갑니다."))
S.append(exhibit("성장-수익성", "MATRIX",
                 "성장은 중앙값 위, 마진은 선에 걸쳐 있습니다", CH["growth_margin"],
                 "빨리 크는 곳인가 잘 남기는 곳인가.",
                 "원 크기까지 세 번째 변수로 쓰면 눈이 크기를 못 잽니다. 매출처럼 익숙한 값만 씁니다."))
S.append(exhibit("비교기업", "TRADING COMPS",
                 "평균이 아니라 중앙값을 씁니다", COMPS,
                 "동종은 우리를 몇 배로 쳐주고 있는가.",
                 "네 곳 중 명진식품이 매출 1,250억으로 셋보다 큽니다. 평균을 쓰면 그 회사 배수가 됩니다."))
S.append(exhibit("레버리지와 커버리지", "LEVERAGE",
                 "2.8배에서 1.4배, 이자보상배율은 6.8배", CH["leverage"],
                 "빚을 갚을 수 있는가, 얼마나 여유가 있는가.",
                 "축이 둘입니다. 막대는 배수, 선은 배율이라고 범례에 함께 적습니다."))

# ---- 제1부
S.append(part_cover("가치평가", "PART", "값은 하나로 나오지 않습니다",
               "범위로 나오고 겹치는 데가 답입니다",
               "범위와 분포를 먼저 내고, 가정이 흔들릴 때 값이 얼마나 움직이는지, "
                    "그 범위가 동종보다 싼지까지 봅니다"))
S.append(exhibit("축구장", "FOOTBALL FIELD",
                 "제시가 380억은 다섯 방법 중 셋의 범위 안입니다", A.football(),
                 "방법마다 나온 가치 범위가 어디서 겹치는가.",
                 "방법 이름 옆에 가정을 함께 적습니다. EV인지 지분가치인지 섞이면 그림이 통째로 틀립니다."))
S.append(exhibit("EV-Equity", "BRIDGE",
                 "EV 381억이 주주 손에 오면 305억입니다", A.evbridge(),
                 "기업가치와 지분가치 사이에서 누가 얼마를 먼저 가져가는가.",
                 "순차입금에 리스부채·우선주를 넣었는지가 협상 단골 분쟁입니다. 각주로 못 박습니다."))
S.append(exhibit("배수 회귀", "REGRESSION",
                 "성장 대비 0.4배 싸게 평가받고 있습니다", A.regression(),
                 "우리 배수가 싼 것인가, 성장이 느려서 그 배수인 것인가.",
                 "점 다섯 개로 회귀선을 긋는 건 장식입니다. R²와 표본 수를 함께 적고, 낮으면 선을 지웁니다."))
S.append(exhibit("확률분포", "MONTE CARLO",
                 "열 번 중 한 번은 318억 아래입니다", A.montecarlo(),
                 "이 가치가 나올 확률이 얼마나 되는가.",
                 "분포는 가정의 결과지 사실이 아닙니다. 어떤 분포를 몇 회 돌렸는지 출처에 적습니다."))
S.append(exhibit("토네이도", "TORNADO",
                 "WACC 하나가 137억을 흔듭니다", A.tornado(),
                 "협상에서 어느 가정부터 다퉈야 하는가. 위 두 줄이면 끝납니다.",
                 "일변량입니다. 흔든 폭을 라벨에 적지 않으면 항목 간 비교가 성립하지 않습니다."))
S.append(exhibit("증감 격자", "ACCRETION",
                 "현금 인수라면 420억까지 이익이 늘어납니다", A.accretion(),
                 "인수가와 대금 구성 중 어느 조합까지 주당이익이 버티는가.",
                 "첫해 회계 효과일 뿐 가치 판단이 아닙니다. 증가한다고 싼 것도 아닙니다."))

# ---- 제2부
S.append(part_cover("딜 구조", "PART", "돈이 어디서 와서",
               "누구에게 가는가",
               "대주단과 투자자가 돈을 넣기 전에 실제로 따지는 것들입니다"))
S.append(exhibit("조달과 사용", "SOURCES & USES",
                 "조달과 사용은 420억에서 반드시 만납니다", SU,
                 "인수 자금이 어디서 와서 어디로 가는가.",
                 "합계 행이 없는 조달·사용 표는 검증 불가능합니다. 인수금융 배수를 함께 적습니다."))
S.append(exhibit("수익 원천", "ATTRIBUTION",
                 "수익의 47%가 EBITDA 성장에서 나왔습니다", A.attribution(),
                 "돈을 번 원천이 실력(이익 성장)인가 시장(배수)인가 레버리지인가.",
                 "네 조각의 합이 지분가치 증가분과 정확히 맞아야 합니다. 잔차를 만들지 않습니다."))
S.append(exhibit("회수 배분", "PAYOFF",
                 "회수 300억 아래서는 보통주 몫이 없습니다", A.payoff(),
                 "회수금액별로 각 증권이 얼마를 받는가. 우선순위의 실감.",
                 "참가부·전환권이 붙으면 꺾임 위치가 달라집니다. 권리 조건을 선 옆에 적습니다."))
S.append(exhibit("만기 분포", "MATURITY PROFILE",
                 "2028년에 58억이 한꺼번에 돌아옵니다", A.ladder(),
                 "총 차입금이 아니라, 언제 얼마가 몰려 돌아오는가.",
                 "유동성 선이 없으면 이 그림은 반쪽입니다. 리볼빙은 만기와 성격이 다릅니다."))

# ---- 제3부
S.append(part_cover("실적·현금 분해", "PART", "요약하지 않고",
               "분해합니다",
               "매출이 어디서 늘었고, 그 돈이 현금까지 얼마나 오고, 어디에 묶여 있는지를 나눠 봅니다"))
S.append(exhibit("매출 브릿지", "PRICE-VOLUME-MIX",
                 "33억 증가분 중 27억이 단가와 믹스입니다", A.pvm(),
                 "매출이 얼마 늘었나가 아니라 무엇이 늘렸나.",
                 "요인 합이 증가분과 안 맞으면 기타로 메우지 않습니다. 못 나눈 것은 못 나눴다고 적습니다."))
S.append(exhibit("손익 흐름도", "P&L SANKEY",
                 "320억이 들어와서 14억이 남습니다", sank.done(),
                 "1,000원이 들어와 얼마가 남고 나머지는 어디로 갔는가. 손익에서 끊지 않고 현금까지 잇습니다.",
                 "화려해서 남용됩니다. 분기·합류가 실제로 없으면 그냥 폭포가 낫습니다."))
S.append(exhibit("현금전환주기 (1/2)", "CASH CONVERSION CYCLE",
                 "매입에서 수금까지 109일,<br>그중 57일이 회사 돈입니다", X.ccc_timeline(),
                 "영업 한 바퀴에 며칠이 걸리고, 그중 며칠을 내 돈으로 버티는가.",
                 "DSO는 매출, DIO·DPO는 매출원가로 나눕니다. 평잔인지 기말인지 밝힙니다."))
S.append(exhibit("현금전환주기 (2/2)", "TREND & PEER",
                 "채권은 잡았고 재고만 13일 늘었습니다", X.ccc_trend(),
                 "몇 년째 그런지, 동종 안에서는 어디인지.",
                 "회전일 하나만 그리면 원인이 안 보입니다. 세 지표를 같이 놓아야 어디가 움직였는지 보입니다."))
S.append(exhibit("듀폰 격차 분해", "DUPONT GAP",
                 "회전율 +2.7%p가 마진 열세 −1.3%p를 덮었습니다", X.dupont_gap(),
                 "동종보다 ROE가 높은 이유가 마진인가 회전율인가 레버리지인가.",
                 "한 항씩 갈아 끼운 순서에 따라 기여가 조금 달라집니다. 순서를 각주에 밝힙니다."))
S.append(exhibit("경험 곡선", "EXPERIENCE CURVE",
                 "누적 생산 두 배마다 단가가 12% 내렸습니다", A.experience(),
                 "원가 하락이 우연인가 규모의 학습인가. 다음 두 배의 원가를 예측할 수 있는가.",
                 "로그축임을 크게 적습니다. 선형으로 읽으면 하락이 멈춘 것처럼 보입니다."))
S.append(exhibit("원가 곡선", "COST CURVE",
                 "외주 26천 톤은 판가보다 260원 비싸게 만듭니다", X.costcurve(),
                 "어느 생산 구간이 판가를 밑도는가.",
                 "고정비 배부 포함인지에 따라 결론이 뒤집힙니다. 이 그림 하나로 계약 해지를 결정하지 않습니다."))

# ---- 제4부
S.append(part_cover("시장·경쟁", "PART", "순위는 비교군이 바뀌면 뒤집힙니다",
               "분포는 안 뒤집힙니다",
               "동종 분포의 어디에 있고 어느 쪽으로 가고 있는지, 규모와 수익성을 같이 놓고 봅니다"))
S.append(exhibit("이익 풀", "PROFIT POOL",
                 "유통은 급식보다 매출이 작고 이익은 큽니다", X.profit_pool(),
                 "매출이 아니라 이익이 어디서 나오는가. 면적이 곧 영업이익입니다.",
                 "100% 누적으로 그리면 정작 볼 이익이 바닥의 얇은 띠가 됩니다. 높이를 이익률로 둡니다."))
S.append(exhibit("ROIC 스프레드", "SPREAD vs GROWTH",
                 "온라인만 스프레드가 음수인데 성장은 가장 빠릅니다", A.spread_bubble(),
                 "성장이 가치를 만드는 사업인가 태우는 사업인가.",
                 "스프레드가 음수인 사업의 성장은 축하가 아니라 경보입니다. 네 번째 변수는 얹지 않습니다."))
S.append(exhibit("기울기", "SLOPE GRAPH",
                 "2년 사이 서린푸드가 두 곳을 제쳤습니다", A.slope(),
                 "순위가 어떻게 바뀌었는가. 시계열 다섯 개를 겹치는 것보다 두 시점이 명확할 때.",
                 "중간 연도의 궤적은 지워집니다. 중간에 반전이 있었다면 이 형식이 그걸 숨깁니다."))
S.append(exhibit("소형 다중", "SMALL MULTIPLES",
                 "온라인만 여섯 분기 연속 내리막입니다", A.smallmult(),
                 "네 사업부의 궤적을 겹치지 않고 나란히.",
                 "모든 패널의 축과 기간을 동일하게 잡습니다. 다르면 이 형식은 거짓말이 됩니다."))
S.append(exhibit("사분위 상자", "BOX PLOT",
                 "5년에 걸쳐 1분위 밖에서 중앙값까지 왔습니다", A.box(),
                 "순위가 아니라 분포의 어디에 있는가, 그리고 어느 방향으로 움직였는가.",
                 "표본이 열둘이면 사분위가 성립하는 하한선입니다. 다섯 곳으로 상자를 그리지 않습니다."))
S.append(exhibit("격차 막대", "DUMBBELL",
                 "가공은 2.9%p 앞서고 온라인은 5.5%p 뒤집니다", A.dumbbell(),
                 "자사와 기준값이 항목별로 얼마나 벌어져 있는가.",
                 "행끼리 단위가 같아야 합니다. 마진과 회전일을 한 그림에 놓으면 축이 무너집니다."))

# ---- 제5부
S.append(part_cover("고객·실행", "PART", "남는 고객,",
               "굴러가는 과제",
               "이익은 어느 고객에게서 오는가, 약속한 개선이 실제로 실현되고 있는가"))
S.append(exhibit("고래 곡선", "WHALE CURVE",
                 "상위 여덟 곳이 이익의 128%를 법니다", A.whale(),
                 "이익이 어느 고객에게서 오고, 어느 고객이 도로 깎아 가는가.",
                 "고객별 이익 배부(물류·영업비)가 절반의 싸움입니다. 기준이 바뀌면 꼬리 명단이 바뀝니다."))
S.append(exhibit("코호트", "COHORT + PARETO",
                 "2023년에 받은 거래처가 다릅니다", X.cohort_pareto(),
                 "언제 들어온 고객이 얼마나 남고, 매출은 몇 곳에 몰려 있는가.",
                 "코호트 표에서 비어 있는 곳은 아직 그 기간을 안 지난 것입니다. 0으로 채우면 거짓말이 됩니다."))
S.append(exhibit("실현 곡선", "SYNERGY PHASING",
                 "3분기째, 실현은 계획의 70%입니다", A.synergy(),
                 "약속한 개선 이익이 계획 곡선 위에 있는가.",
                 "계획선을 나중에 다시 그리면 이 그림은 무의미해집니다. 착수 시점 계획선을 박제합니다."))
S.append(exhibit("볼링 차트", "BOWLING CHART",
                 "여덟 과제 중 하나가 궤도를 벗어났습니다", A.bowling(),
                 "과제별로 어느 분기에 무엇이 밀렸는가. 경영회의 한 장 요약.",
                 "상태 색은 규칙으로 정합니다. 자기 신고에 맡기면 전부 초록이 됩니다."))
S.append(exhibit("팬 차트", "FAN CHART",
                 "2028년 매출은 352억에서 468억 사이입니다", A.fan(),
                 "전망이 얼마나 넓게 벌어지는가. 실행 계획의 결과 범위를 정직하게.",
                 "실적 구간에 띠를 씌우지 않습니다. 밴드는 둘까지, 셋이면 농담이 안 갈립니다."))

# ---- 제6부 · 컨설팅 펌과 IR
S.append(part_cover("컨설팅 펌과 IR", "PART", "업계 안에서 어디에 서 있고",
               "성장이 어디서 오는가",
               "전략 컨설팅과 상장사 IR 이 실제로 쓰는 도표입니다"))
S.append(exhibit("파워 커브", "POWER CURVE",
                 "가운데 일곱 곳은 자본비용을 겨우 맞춥니다", A3.power_curve(),
                 "업계의 경제적 이익이 어떻게 갈라져 있는가. 평균은 아무도 살지 않는 값이다.",
                 "순위가 아니라 분포다. 가운데가 납작하다는 것이 요점이므로 자사만 강조하고 나머지는 눕힌다."))
S.append(exhibit("전략적 통제 지도", "CONTROL MAP",
                 "같은 시가총액 곡선 위에서 어디로 갈 것인가", A3.control_map(),
                 "장부를 키울 것인가 배율을 올릴 것인가. 두 길이 다른 일이라는 것을 보여준다.",
                 "배율은 시장이 정한다. 이 지도는 목표가 아니라 현재 위치를 읽는 데 쓴다."))
S.append(exhibit("세 지평선", "THREE HORIZONS",
                 "급식 비중 69%가 25%로 내려갑니다", A3.horizons(),
                 "기존 사업이 꺼지는 속도보다 새 사업이 뜨는 속도가 빠른가.",
                 "전망 구간을 실적과 같은 색으로 칠하지 않는다. 경계선을 반드시 긋는다."))
S.append(exhibit("성장 원천 분해", "GROWTH DECOMPOSITION",
                 "순증 33억 중 기존이 26억, 이탈이 12억을 되가져갔습니다", A3.growth_decomp(),
                 "성장이 기존 거래처에서 왔나 신규에서 왔나, 이탈이 얼마를 깎았나.",
                 "신규만 세면 이탈이 안 보인다. 셋을 같이 놓아야 유지율이 드러난다."))
S.append(exhibit("Rule of 40", "GROWTH + FCF MARGIN",
                 "성장은 동종 2위인데 합은 15.9로 20도 못 넘습니다", A3.rule40(),
                 "성장과 현금 마진을 더한 하나의 숫자로 볼 때 어디에 있는가.",
                 "40 은 SaaS 에서 나온 기준이다. 업종이 다르면 선을 그대로 옮겨 쓰지 않는다."))
S.append(exhibit("코호트 레이어케이크", "LAYER CAKE",
                 "새로 딴 거래처가 이탈을 덮고도 남습니다", A3.layer_cake(),
                 "매출이 어느 해에 딴 거래처에서 나오고 있는가.",
                 "코호트가 여섯을 넘으면 색이 안 갈린다. 오래된 것은 묶고 묶었다고 밝힌다."))
S.append(exhibit("획득비 회수", "CAC PAYBACK",
                 "최근 코호트일수록 회수가 빨라지고 있습니다", A3.cac_payback(),
                 "새 거래처를 따는 데 쓴 돈을 몇 달 만에 돌려받나.",
                 "획득비에 무엇을 넣었는지 밝힌다. 영업 인건비를 빼면 회수가 두 배 빨라 보인다."))
S.append(exhibit("설비투자와 잉여현금", "CAPEX vs FCF",
                 "잉여현금이 멈춘 것은 투자가 아니라 운전자본 탓입니다", A3.capex_fcf(),
                 "설비투자를 늘려서 현금이 준 것인가, 다른 이유인가.",
                 "축이 둘이다. 막대와 선의 단위를 범례에 함께 적지 않으면 오독을 부른다."))
S.append(exhibit("계약 잔고", "BACKLOG COVERAGE",
                 "다음 해 매출의 절반은 이미 계약으로 잡혀 있습니다", A3.backlog(),
                 "앞으로 인식할 계약이 얼마나 쌓여 있고 다음 해 매출을 얼마나 덮는가.",
                 "잔고는 계약이지 매출이 아니다. 해지 조항과 인식 시점을 각주에 밝힌다."))
S.append(cover("마무리", "CLOSING", "그림부터 고르면 헤맵니다",
               "질문을 먼저 적으십시오",
               "묻고 싶은 것을 한 문장으로 적고, 그 문장에 막대가 답하면 막대를 씁니다. "
               "나머지 마흔넷은 막대로 안 되는 질문에 씁니다. "
               "숫자만 바꾸면 마흔다섯 장이 그대로 다시 그려집니다."))

# ---------------------------------------------------------------- 조립
tpl = io.open(TPL, encoding="utf-8").read()
tpl = re.sub(r"  :root\{.*?\n  \}", SKIN, tpl, count=1, flags=re.S)
tpl = tpl.replace("  /* =================== chrome (fixed UI) =================== */",
                  EXTRA + "\n  /* =================== chrome (fixed UI) =================== */", 1)
open_tag = '<div class="deck" id="deck">'
close = '\n    </div>\n  </div>\n\n  <div class="brandbar"'
a = tpl.index(open_tag) + len(open_tag)
b = tpl.index(close)
out = tpl[:a] + "\n\n" + "\n".join(S) + tpl[b:]
out = out.replace("{{DECK_TITLE}}", TITLE)
out = out.replace('<section class="slide cover">', '<section class="slide cover active">', 1)
io.open(OUT, "w", encoding="utf-8").write(out)
print("wrote", OUT, "slides =", out.count('<section class="slide'))
