# -*- coding: utf-8 -*-
"""고급 재무분석 전시물 갤러리.

M&A · 경영컨설팅에서 쓰는 전시물 열세 가지. 막대와 선으로는 안 되는 것들만 모았다.

    python build_advanced.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TPL = os.path.join(SKILL, "assets", "template.html")
OUT = os.path.join(SKILL, "reference", "parts", "고급차트_13종.html")

sys.path.insert(0, HERE)
import mkchart  # noqa: E402

TITLE = "고급 재무분석 전시물"
SPECS = json.loads(io.open(os.path.join(HERE, "advanced_specs.json"), encoding="utf-8").read())
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


def chart(n, eyebrow, title, sub, key, en=""):
    return (
        '      <section class="slide">\n'
        + head(n, eyebrow, title, sub, en)
        + '      <div data-anim style="--d:3; display:flex; flex:1; min-height:0">\n'
        + "\n".join("  " + ln for ln in C[key].splitlines())
        + "\n      </div>\n      </section>\n"
    )


S = []

S.append(cover("고급 재무분석 전시물", "ADVANCED EXHIBITS",
               "막대와 선으로는",
               "말할 수 없는 것들",
               "불확실성 · 가치의 원천 · 동종과의 거리 · 구조. 열세 가지 전부 예시 데이터입니다"))

S.append(
    '      <section class="slide">\n'
    + head("", "목차", "질문이 어려워지면 형태도 달라집니다",
           "막대로 답할 수 있는 질문은 이미 앞 갤러리에서 끝났습니다", "AGENDA")
    + '      <div class="agenda">\n'
    + "".join(
        '        <div class="arow" data-anim style="--d:%d; --ac:var(--%s); --act:var(--%st)">\n'
        '          <div class="no">%s</div>\n'
        '          <div class="tx"><h3>%s</h3><p>%s</p></div>\n'
        '          <div class="en">%s</div>\n'
        "        </div>\n" % (3 + i, c, c, no, t, p, en)
        for i, (no, c, t, p, en) in enumerate([
            ("01", "a1", "불확실성을 그린다", "토네이도 · 확률분포 · 팬 차트", "UNCERTAINTY"),
            ("02", "a2", "가치의 원천을 쪼갠다", "EV-Equity 브릿지 · 수익 원천 · 2단 분해", "ATTRIBUTION"),
            ("03", "a3", "동종과의 거리를 잰다", "사분위 상자 · 격차 막대 · 궤적", "DISTANCE"),
            ("04", "a1", "구조를 본다", "원가 곡선 · 흐름도 · 만기 사다리 · 코호트", "STRUCTURE"),
        ])
    )
    + "      </div>\n      </section>\n"
)

# ------------------------------------------------------------ 1부
S.append(cover("제1부 · 불확실성을 그린다", "PART", "값 하나를 내놓는 순간",
               "방어할 수 없게 됩니다", "얼마인가가 아니라 얼마나 흔들리는가를 그립니다"))

S.append(chart("01", "1-1 · 토네이도", "WACC 하나가 137억을 흔듭니다",
               "가정을 하나씩 흔들어 보고 많이 흔드는 것부터 위에 세웁니다", "tornado", "TORNADO"))
S.append(chart("02", "1-2 · 확률분포", "열 번 중 한 번은 318억 아래입니다",
               "시뮬레이션 1만 회의 분포와 누적확률을 겹칩니다", "mc", "MONTE CARLO"))
S.append(chart("03", "1-3 · 팬 차트", "2028년 매출은 352억에서 468억 사이입니다",
               "전망은 선이 아니라 띠입니다. 멀어질수록 넓어집니다", "fan", "FAN CHART"))

# ------------------------------------------------------------ 2부
S.append(cover("제2부 · 가치의 원천을 쪼갠다", "PART", "얼마를 벌었나가 아니라",
               "어디서 벌었나를 답합니다", "합계는 이미 알고 있습니다. 협상은 분해에서 벌어집니다"))

S.append(chart("04", "2-1 · EV-Equity 브릿지", "EV 381억이 주주 손에 오면 305억입니다",
               "기업가치와 주주가치를 섞어 말하면 거래가 통째로 어긋납니다", "evbridge", "EV TO EQUITY"))
S.append(chart("05", "2-2 · 수익 원천 분해", "수익의 47%가 EBITDA 성장에서 나왔습니다",
               "배수 확대가 14%뿐이라 시장에 기댄 거래가 아닙니다", "irr", "VALUE CREATION"))
S.append(chart("06", "2-3 · 2단 분해", "회전율이 만든 ROE입니다",
               "한 층만 쪼개면 어디를 건드릴지 안 나옵니다. 두 층까지 내려갑니다", "tree2", "DUPONT"))

# ------------------------------------------------------------ 3부
S.append(cover("제3부 · 동종과의 거리를 잰다", "PART", "1위인지 3위인지가 아니라",
               "분포의 어디에 있는지입니다", "순위는 비교군이 바뀌면 뒤집힙니다. 분포는 안 뒤집힙니다"))

S.append(chart("07", "3-1 · 사분위 상자", "5년에 걸쳐 1분위 아래에서 중앙값까지 왔습니다",
               "동종 12개사의 분포를 상자로 그리고 자사를 마름모로 얹습니다", "box", "BOX PLOT"))
S.append(chart("08", "3-2 · 격차 막대", "가공은 2.9%p 앞서고 온라인은 5.5%p 뒤집니다",
               "전사 평균 하나로는 이 두 사실이 다 지워집니다", "dumbbell", "DUMBBELL"))
S.append(chart("09", "3-3 · 궤적", "점이 아니라 5년치 움직임입니다",
               "지금 어디 있느냐보다 어느 쪽으로 가고 있느냐가 답인 경우가 많습니다", "trail", "TRAJECTORY"))

# ------------------------------------------------------------ 4부
S.append(cover("제4부 · 구조를 본다", "PART", "평균은 구조를 지웁니다",
               "쪼개면 그 자리가 드러납니다", "전사 숫자 하나로는 어디를 손댈지 정해지지 않습니다"))

S.append(chart("10", "4-1 · 원가 곡선", "외주 26천 톤은 판가보다 비싸게 만듭니다",
               "가로가 누적 물량, 세로가 단가입니다. 폭이 곧 규모입니다", "costcurve", "COST CURVE"))
S.append(chart("11", "4-2 · 흐름도", "매출 320억 중 손에 남는 것은 29억입니다",
               "띠 두께가 그대로 금액입니다. 어디서 새는지가 보입니다", "sankey", "SANKEY"))
S.append(chart("12", "4-3 · 만기 사다리", "2028년에 58억이 한꺼번에 돌아옵니다",
               "총 차입금이 아니라 언제 돌아오는지가 위험입니다", "ladder", "MATURITY LADDER"))
S.append(chart("13", "4-4 · 코호트", "3년차에 2023년 수주만 80%로 주저앉았습니다",
               "행이 갈수록 짧아집니다. 아직 그 기간을 안 지났기 때문입니다", "cohort", "COHORT"))

S.append(cover("마무리", "CLOSING", "형태를 늘린 것이 아니라",
               "답할 수 있는 질문을 늘린 것입니다",
               "열세 가지 전부 숫자만 바꾸면 다시 그려집니다"))

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
