# -*- coding: utf-8 -*-
"""재무분석 뷰 갤러리 덱을 만든다.

한 회사(예시)의 재무제표를 놓고 경영컨설팅·M&A 에서 실제로 그리는 순서대로 늘어놓았다.
수익성 -> 운전자본과 현금 -> 시장에서의 자리 -> 가치평가.

    python build_finance.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TPL = os.path.join(SKILL, "assets", "template.html")
OUT = os.path.join(SKILL, "reference", "parts", "재무분석_16종.html")

sys.path.insert(0, HERE)
import mkchart  # noqa: E402

TITLE = "재무분석 뷰 갤러리"
SPECS = json.loads(io.open(os.path.join(HERE, "finance_specs.json"), encoding="utf-8").read())
C = {s["key"]: mkchart.build(s) for s in SPECS}


def head(n, eyebrow, title, sub, en=""):
    e = '<span class="en">%s</span>' % en if en else ""
    return (
        '      <div class="head" data-n="%s">\n'
        '        <div class="eyebrow" data-anim style="--d:0">%s %s</div>\n'
        '        <h2 class="title" data-anim style="--d:1">%s</h2>\n'
        '        <p class="sub" data-anim style="--d:2">%s</p>\n'
        "      </div>\n" % (n, eyebrow, e, title, sub)
    )


def cover(eyebrow, en, t1, t2, sub):
    return (
        '      <section class="slide cover">\n'
        '        <div class="eyebrow" data-anim style="--d:0"><b>%s</b><span class="en">· %s</span></div>\n'
        '        <h1 class="title" data-anim style="--d:1">%s<br><span class="mark">%s</span></h1>\n'
        '        <p class="sub" data-anim style="--d:2">%s</p>\n'
        "      </section>\n" % (eyebrow, en, t1, t2, sub)
    )


def body(n, eyebrow, title, sub, inner, en=""):
    return (
        '      <section class="slide">\n'
        + head(n, eyebrow, title, sub, en)
        + '      <div data-anim style="--d:3; display:flex; flex:1; min-height:0">\n'
        + "\n".join("  " + ln for ln in inner.splitlines())
        + "\n      </div>\n      </section>\n"
    )


def chart(n, eyebrow, title, sub, key, en=""):
    return body(n, eyebrow, title, sub, C[key], en)


S = []

S.append(cover("재무분석 뷰 갤러리", "FINANCIAL VIEWS",
               "재무제표 한 벌에서",
               "무엇을 그려야 하는가",
               "수익성 · 운전자본 · 시장에서의 자리 · 가치평가 열세 가지 뷰. 전부 예시 데이터입니다"))

S.append(
    '      <section class="slide">\n'
    + head("", "목차", "그리는 순서가 정해져 있습니다",
           "돈을 얼마나 버는가에서 시작해 그 돈이 어디에 묶여 있는지로 갑니다", "AGENDA")
    + '      <div class="agenda">\n'
    + "".join(
        '        <div class="arow" data-anim style="--d:%d; --ac:var(--%s); --act:var(--%st)">\n'
        '          <div class="no">%s</div>\n'
        '          <div class="tx"><h3>%s</h3><p>%s</p></div>\n'
        '          <div class="en">%s</div>\n'
        "        </div>\n" % (3 + i, c, c, no, t, p, en)
        for i, (no, c, t, p, en) in enumerate([
            ("01", "a1", "얼마나 버는가", "매출 브릿지 · EBITDA 워크 · 공통형 손익 · 듀폰", "PROFITABILITY"),
            ("02", "a2", "그 돈이 어디 묶여 있는가", "CCC · 운전자본 추세 · 순차입금 브릿지 · 채권 연령", "WORKING CAPITAL"),
            ("03", "a3", "동종 안에서 어디인가", "마진 벤치마킹 · 성장-수익성 · 세그먼트", "BENCHMARK"),
            ("04", "a1", "얼마짜리인가", "축구장 · 비교기업 · 민감도 · 레버리지 · 자금조달", "VALUATION"),
        ])
    )
    + "      </div>\n      </section>\n"
)

# ------------------------------------------------------------ 1부
S.append(cover("제1부 · 얼마나 버는가", "PART", "손익계산서를 요약하지 않습니다",
               "어디서 벌어졌는지를 그립니다", "표로 옮겨 적는 것은 분석이 아닙니다"))

S.append(chart("01", "1-1 · 매출 브릿지", "33억 중 27억이 단가와 믹스에서 왔습니다",
               "매출이 얼마 늘었나가 아니라 무엇이 늘렸나를 답합니다", "rev_bridge", "REVENUE BRIDGE"))
S.append(chart("02", "1-2 · EBITDA 워크", "판관비 41억 중 24억이 인건비입니다",
               "매출총이익에서 EBITDA까지 무엇이 깎아 먹는지 한 줄로 봅니다", "ebitda_walk", "MARGIN WALK"))
S.append(chart("03", "1-3 · 공통형 손익", "매출 24% 증가에 판관비는 20% 증가",
               "금액과 구성비를 한 번에 봅니다. 비율만 그리면 규모가 사라집니다", "common_size", "COMMON SIZE"))

TREE = """<div class="tree">
  <div class="nd res" style="--c:var(--rule)">
    <div class="k">ROE</div><div class="v">14.2%</div>
    <div class="d">자기자본 대비<br>얼마를 남겼나</div>
  </div>
  <div class="op">=</div>
  <div class="nd" style="--c:var(--a1); --ct:var(--a1t)">
    <div class="k">순이익률</div><div class="v">6.5%</div>
    <div class="d">순이익 / 매출<br>얼마나 남기는가</div>
  </div>
  <div class="op">×</div>
  <div class="nd" style="--c:var(--a2); --ct:var(--a2t)">
    <div class="k">자산회전율</div><div class="v">1.32</div>
    <div class="d">매출 / 총자산<br>자산을 몇 번 굴리는가</div>
  </div>
  <div class="op">×</div>
  <div class="nd" style="--c:var(--a3); --ct:var(--a3t)">
    <div class="k">재무레버리지</div><div class="v">1.66</div>
    <div class="d">총자산 / 자기자본<br>남의 돈을 얼마나 쓰는가</div>
  </div>
</div>"""
S.append(body("04", "1-4 · 듀폰 분해", "ROE 14.2%는 마진이 아니라 회전율이 만들었습니다",
              "동종 평균 순이익률은 7.1%로 더 높습니다. 서린푸드는 자산을 더 빨리 굴립니다",
              TREE, "DUPONT"))

# ------------------------------------------------------------ 2부
S.append(cover("제2부 · 그 돈이 어디 묶여 있는가", "PART", "이익이 났는데 현금이 없다면",
               "답은 여기 있습니다", "운전자본이 손익과 현금을 가르는 자리입니다"))

S.append(chart("05", "2-1 · 현금 회전일 (CCC)", "매입에서 수금까지 109일, 그중 57일이 내 돈입니다",
               "재고에 묶인 68일 + 채권에 묶인 41일 - 공급사가 대준 52일", "ccc", "CASH CONVERSION CYCLE"))
S.append(chart("06", "2-2 · 운전자본 추세", "매출채권은 잡았고 재고는 못 잡았습니다",
               "세 지표를 한 화면에 놓아야 어디가 늘었는지 보입니다", "wc_trend", "DSO / DIO / DPO"))
S.append(chart("07", "2-3 · 순차입금 브릿지", "EBITDA 48억을 벌고 차입금은 14억 줄었습니다",
               "번 돈과 갚은 돈 사이에 무엇이 끼어 있는지 답합니다", "netdebt", "NET DEBT BRIDGE"))
S.append(chart("08", "2-4 · 매출채권 연령", "잔액은 줄었는데 90일 초과는 2억에서 5억",
               "총액만 보면 좋아진 것으로 읽힙니다. 나눠야 보입니다", "ar_aging", "AR AGING"))

# ------------------------------------------------------------ 3부
S.append(cover("제3부 · 동종 안에서 어디인가", "PART", "좋다 나쁘다를 말하려면",
               "옆에 누구를 세울지부터 정합니다", "비교군을 못 정하면 어떤 숫자도 판정이 안 됩니다"))

S.append(chart("09", "3-1 · 마진 벤치마킹", "동종 5개사 중 3위, 중앙값과 같습니다",
               "자사만 색을 남기고 나머지는 눕힙니다", "peer_margin", "BENCHMARK"))
S.append(chart("10", "3-2 · 성장-수익성", "성장은 중앙값 위, 마진은 선에 걸쳐 있습니다",
               "가로는 성장, 세로는 마진, 원 크기는 매출입니다. 점선은 동종 중앙값입니다",
               "growth_margin", "MATRIX"))
S.append(chart("11", "3-3 · 세그먼트", "매출은 급식이 크고 이익률은 가공이 높습니다",
               "폭이 규모, 높이가 구성비입니다. 둘을 한 그림에 겹칩니다", "segment", "MARIMEKKO"))

# ------------------------------------------------------------ 4부
S.append(cover("제4부 · 얼마짜리인가", "PART", "값은 하나로 나오지 않습니다",
               "범위로 나오고 겹치는 데가 답입니다", "한 숫자를 내놓는 순간 방어할 수 없게 됩니다"))

S.append(chart("12", "4-1 · 축구장", "제시가 380억은 네 방법 중 셋의 범위 안입니다",
               "방법마다 나온 범위를 한 축에 겹칩니다. LBO만 밖에 있습니다", "football", "FOOTBALL FIELD"))

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
      <tr class="total"><td>중앙값</td><td class="num off">445</td><td class="num hi">1.15x</td>
          <td class="num hi">7.7x</td><td class="num hi">12.2x</td></tr>
    </tbody>
  </table>
  <div class="cap">중앙값을 쓰고 평균을 쓰지 않습니다. 한 곳이 튀면 평균이 통째로 끌려갑니다. 예시 데이터</div>
</div>"""
S.append(body("13", "4-2 · 비교기업", "평균이 아니라 중앙값을 씁니다",
              "네 곳 중 명진식품이 매출 1,250억으로 셋보다 큽니다. 평균을 쓰면 그 회사 배수가 됩니다",
              COMPS, "TRADING COMPS"))

S.append(chart("14", "4-3 · 민감도", "WACC 1%p에 기업가치가 40억 넘게 움직입니다",
               "가정 두 개만 흔듭니다. 셋을 흔들면 표를 읽을 수 없습니다", "sens", "SENSITIVITY"))
S.append(chart("15", "4-4 · 레버리지와 커버리지", "2.8배에서 1.4배, 이자보상배율은 6.8배",
               "막대는 배수, 선은 배율입니다. 축이 둘이면 범례에 단위를 함께 적습니다", "leverage", "LEVERAGE"))

SU = """<div class="tbl">
  <table>
    <colgroup><col style="width:28%"><col style="width:22%">
              <col style="width:28%"><col style="width:22%"></colgroup>
    <thead><tr><th>조달</th><th class="num">금액 (억원)</th>
      <th>사용</th><th class="num">금액 (억원)</th></tr></thead>
    <tbody>
      <tr><td><b>인수금융</b></td><td class="num">210</td>
          <td><b>지분 인수대금</b></td><td class="num">380</td></tr>
      <tr><td><b>우선주</b></td><td class="num">90</td>
          <td><b>거래 비용</b></td><td class="num">18</td></tr>
      <tr><td><b>보통주</b></td><td class="num">120</td>
          <td><b>운전자금</b></td><td class="num">22</td></tr>
      <tr class="total"><td>합계</td><td class="num">420</td>
          <td>합계</td><td class="num">420</td></tr>
    </tbody>
  </table>
  <div class="cap">양쪽 합계가 반드시 같습니다. 다르면 표가 아니라 계산이 틀린 것입니다. 예시 데이터</div>
</div>"""
S.append(body("16", "4-5 · 자금조달", "양쪽 합계가 같지 않으면 표가 아닙니다",
              "인수금융 210억은 EBITDA 48억의 4.4배입니다. 레버리지 여력을 여기서 확인합니다",
              SU, "SOURCES & USES"))

S.append(cover("마무리", "CLOSING", "열여섯 장 전부",
               "숫자 하나만 바꾸면 다시 그려집니다",
               "형태는 스킬이 집니다. 사람이 정할 것은 어느 뷰를 쓸지 하나입니다"))

# ------------------------------------------------------------ 조립
tpl = io.open(TPL, encoding="utf-8").read()
open_tag = '<div class="deck" id="deck">'
close = '\n    </div>\n  </div>\n\n  <div class="brandbar"'
a = tpl.index(open_tag) + len(open_tag)
b = tpl.index(close)
out = tpl[:a] + "\n\n" + "\n".join(S) + tpl[b:]
out = out.replace("{{DECK_TITLE}}", TITLE)
out = out.replace('<section class="slide cover">', '<section class="slide cover active">', 1)
io.open(OUT, "w", encoding="utf-8").write(out)
print("wrote", OUT, "slides =", out.count('<section class="slide'))
