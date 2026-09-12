# -*- coding: utf-8 -*-
"""전시물 갤러리 덱을 만든다.

template.html 의 껍데기(CSS·JS·좌하단 표시)를 그대로 쓰고 슬라이드만 갈아 끼운다.
차트 조각은 mkchart.py 가 숫자에서 뽑는다. 문구를 고치면 다시 돌린다.

    python build_gallery.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TPL = os.path.join(SKILL, "assets", "template.html")
OUT = os.path.join(SKILL, "reference", "전시물_갤러리.html")

sys.path.insert(0, HERE)
import mkchart  # noqa: E402

TITLE = "전시물 갤러리"

SPECS = json.loads(io.open(os.path.join(HERE, "gallery_specs.json"), encoding="utf-8").read())
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


def cover(eyebrow, en, t1, t2, sub, part=False):
    return (
        '      <section class="slide cover">\n'
        '        <div class="eyebrow" data-anim style="--d:0"><b>%s</b><span class="en">· %s</span></div>\n'
        '        <h1 class="title" data-anim style="--d:1">%s<br><span class="mark">%s</span></h1>\n'
        '        <p class="sub" data-anim style="--d:2">%s</p>\n'
        "      </section>\n" % (eyebrow, en, t1, t2, sub)
    )


def chart_slide(n, eyebrow, title, sub, key, en=""):
    return (
        '      <section class="slide">\n'
        + head(n, eyebrow, title, sub, en)
        + '      <div data-anim style="--d:3; display:flex; flex:1; min-height:0">\n'
        + "\n".join("  " + ln for ln in C[key].splitlines())
        + "\n      </div>\n      </section>\n"
    )


S = []

# ---------------------------------------------------------------- 표지·목차
S.append(cover("전시물 갤러리", "EXHIBITS", "고를 것은 디자인이 아니라",
               "무엇을 비교하는가입니다",
               "표 3종 · 그래프 7종 · 도표 주의사항 · 전부 이 스킬의 토큰으로만 그렸습니다"))

S.append(
    '      <section class="slide">\n'
    + head("", "목차", "세 가지를 정하면 나머지는 정해집니다", "메시지를 먼저 쓰고, 형태는 그 다음에 고릅니다", "AGENDA")
    + '      <div class="agenda">\n'
    + "".join(
        '        <div class="arow" data-anim style="--d:%d; --ac:var(--%s); --act:var(--%st)">\n'
        '          <div class="no">%s</div>\n'
        '          <div class="tx"><h3>%s</h3><p>%s</p></div>\n'
        '          <div class="en">%s</div>\n'
        "        </div>\n" % (3 + i, c, c, no, t, p, en)
        for i, (no, c, t, p, en) in enumerate([
            ("01", "a1", "형태를 고르는 순서", "메시지 · 비교 유형 다섯 · 형태", "CHOOSE"),
            ("02", "a2", "표", "비교표 · 평가 매트릭스 · 강조표", "TABLE"),
            ("03", "a3", "그래프", "항목 · 구성비 · 시계열 · 워터폴 · 상관", "CHART"),
            ("04", "a1", "도표와 단계", "한 장에 뜻 하나. 부호를 겹치지 않습니다", "DIAGRAM"),
        ])
    )
    + "      </div>\n      </section>\n"
)

# ---------------------------------------------------------------- 1부
S.append(cover("제1부 · 형태를 고르는 순서", "PART", "데이터가 형태를 정하지 않습니다",
               "메시지가 정합니다", "Zelazny 의 세 걸음을 그대로 씁니다"))

S.append(
    '      <section class="slide">\n'
    + head("01", "1-1 · 비교 유형", "말에 이미 형태가 들어 있습니다",
           "메시지를 한 문장으로 쓰고, 그 안의 낱말을 봅니다", "COMPARISON")
    + '      <div class="wide" data-anim style="--d:3">\n'
    '        <div class="panel" style="--pc:var(--a1); --pct:var(--a1t); --pbg:var(--a1b)">\n'
    '          <div class="deflist">\n'
    + "".join(
        '            <div class="row"><div class="cw"><span class="c">%s</span></div>'
        '<div class="k">%s</div><div class="d">%s</div></div>\n' % (k, t, d)
        for k, t, d in [
            ("구성비", "누적 막대", "비중 · 몫 · 퍼센트. 항목이 다섯을 넘으면 나머지로 묶습니다"),
            ("항목", "가로 막대", "가장 큰 · 상위 · 대비. 큰 것부터 내려 정렬합니다"),
            ("시계열", "세로 막대", "늘었다 · 줄었다. 달·분기가 여섯을 넘으면 꺾은선으로 바꿉니다"),
            ("빈도", "세로 막대", "분포 · 구간별. 구간을 같은 폭으로 자릅니다"),
            ("상관", "점", "따라 움직인다 · 관계. 점이 스무 개 미만이면 표가 낫습니다"),
        ]
    )
    + "          </div>\n        </div>\n      </div>\n      </section>\n"
)

S.append(
    '      <section class="slide">\n'
    + head("02", "1-2 · 고르기 전에", "형태보다 먼저 정할 것이 있습니다",
           "이 두 가지가 안 정해지면 어떤 형태로 그려도 안 읽힙니다", "BEFORE")
    + '      <div class="duo">\n'
    '        <div class="panel" data-anim style="--d:3; --pc:var(--a1); --pct:var(--a1t); --pbg:var(--a1b)">\n'
    '          <div class="pk">먼저 정한다</div><h3>제목이 곧 결론입니다</h3>\n'
    '          <ul class="pts">\n'
    "            <li>그림을 손으로 가리고 제목만 읽었을 때 <b>할 말이 남아야</b> 합니다</li>\n"
    "            <li>제목에 숫자가 들어갑니다. <b>44%</b> 처럼 그림에서 읽히는 그 숫자입니다</li>\n"
    "            <li>한 장에 뜻은 하나입니다. 둘이면 장을 나눕니다</li>\n"
    "            <li>출처와 기간을 아래 한 줄로 답니다</li>\n"
    "          </ul>\n"
    "        </div>\n"
    '        <div class="panel" data-anim style="--d:4; --pc:var(--risk); --pct:var(--riskT); --pbg:var(--riskB)">\n'
    '          <div class="pk">하지 않는다</div><h3>이 넷은 매번 사고를 냅니다</h3>\n'
    '          <ul class="pts">\n'
    "            <li><b>파이 차트.</b> 각도는 사람이 못 읽습니다. 구성비는 100% 누적 막대로 갑니다</li>\n"
    "            <li><b>0 이 아닌 축.</b> 막대에서 축을 자르면 차이가 부풀어 보입니다</li>\n"
    "            <li><b>모든 점에 라벨.</b> 처음 · 끝 · 꺾이는 곳만 답니다</li>\n"
    "            <li><b>색 여섯 가지.</b> 강조는 하나입니다. 나머지는 회색으로 눕힙니다</li>\n"
    "          </ul>\n"
    "        </div>\n      </div>\n      </section>\n"
)

# ---------------------------------------------------------------- 2부 표
S.append(cover("제2부 · 표", "PART", "표는 읽는 것이 아니라",
               "찾아보는 것입니다", "그래서 정렬과 단위가 형태보다 먼저입니다"))

S.append(
    '      <section class="slide">\n'
    + head("03", "2-1 · 비교표", "글자는 왼쪽, 숫자는 오른쪽입니다",
           "단위는 칸마다 붙이지 않고 머리행에 한 번만 적습니다", "TABLE")
    + '      <div class="tbl" data-anim style="--d:3">\n'
    "        <table>\n"
    '          <colgroup><col style="width:30%"><col style="width:22%">'
    '<col style="width:24%"><col style="width:24%"></colgroup>\n'
    "          <thead><tr><th>업무</th><th>담당</th>"
    '<th class="num">월 처리 건수</th><th class="num">월 비용 (만원)</th></tr></thead>\n'
    "          <tbody>\n"
    + "".join(
        '            <tr><td><b>%s</b></td><td>%s</td>'
        '<td class="num">%s</td><td class="num">%s</td></tr>\n' % r
        for r in [
            ("기장 · 전표", "담당 회계사", "1,240", "180"),
            ("부가세 · 원천세", "담당 회계사", "26", "60"),
            ("결산 · 세무조정", "파트너 검토", "4", "140"),
            ("월간 보고", "파트너", "12", "70"),
        ]
    )
    + '            <tr class="total"><td>합계</td><td class="off">4개 업무</td>'
    '<td class="num">1,282</td><td class="num">450</td></tr>\n'
    "          </tbody>\n        </table>\n"
    '        <div class="cap">예시 데이터 · 12개월 평균. 합계 행은 맨 아래에 두고 위에 굵은 선을 긋습니다.</div>\n'
    "      </div>\n      </section>\n"
)

S.append(
    '      <section class="slide">\n'
    + head("04", "2-2 · 평가 매트릭스", "정도는 다섯 칸으로만 나눕니다",
           "일곱 칸으로 나누면 채우는 사람도 읽는 사람도 근거를 못 댑니다", "MATRIX")
    + '      <div class="tbl" data-anim style="--d:3">\n'
    "        <table>\n"
    '          <colgroup><col style="width:28%"><col style="width:18%"><col style="width:18%">'
    '<col style="width:18%"><col style="width:18%"></colgroup>\n'
    "          <thead><tr><th>대안</th><th>도입 기간</th><th>초기 비용</th>"
    "<th>내부 인력 부담</th><th>되돌리기</th></tr></thead>\n"
    "          <tbody>\n"
    + "".join(
        '            <tr><td><b>%s</b></td>%s</tr>\n'
        % (name, "".join('<td><span class="hb%s">%s</span></td>'
                         % ("" if v >= 4 else " off", "●" * v + "○" * (5 - v)) for v in vals))
        for name, vals in [
            ("전부 내부에서", [2, 4, 1, 5]),
            ("전부 외부에 맡김", [4, 2, 5, 2]),
            ("입력만 맡기고 판단은 내부", [4, 4, 4, 4]),
        ]
    )
    + "          </tbody>\n        </table>\n"
    '        <div class="cap">채운 동그라미가 많을수록 유리합니다. 세 대안의 축이 같아야 비교가 됩니다.</div>\n'
    "      </div>\n      </section>\n"
)

S.append(
    '      <section class="slide">\n'
    + head("05", "2-3 · 강조표", "칸에 색을 칠하면 그 칸만 읽힙니다",
           "그래서 한 표에 강조는 한 종류입니다. 둘을 섞으면 둘 다 안 보입니다", "HIGHLIGHT")
    + '      <div class="tbl" data-anim style="--d:3">\n'
    "        <table>\n"
    '          <colgroup><col style="width:28%"><col style="width:18%"><col style="width:18%">'
    '<col style="width:18%"><col style="width:18%"></colgroup>\n'
    "          <thead><tr><th>지표</th>"
    '<th class="num">1분기</th><th class="num">2분기</th>'
    '<th class="num">3분기</th><th class="num">4분기</th></tr></thead>\n'
    "          <tbody>\n"
    '            <tr><td><b>마감 소요일</b></td><td class="num">13</td><td class="num">11</td>'
    '<td class="num">7</td><td class="num hi">5</td></tr>\n'
    '            <tr><td><b>수정 전표 건수</b></td><td class="num">418</td><td class="num">301</td>'
    '<td class="num">190</td><td class="num">122</td></tr>\n'
    '            <tr><td><b>미확정 거래처</b></td><td class="num">96</td><td class="num">88</td>'
    '<td class="num">91</td><td class="num warn">104</td></tr>\n'
    '            <tr><td><b>월 비용 (만원)</b></td><td class="num">450</td><td class="num">450</td>'
    '<td class="num">450</td><td class="num">450</td></tr>\n'
    "          </tbody>\n        </table>\n"
    '        <div class="cap">파란 칸은 목표 달성, 붉은 칸은 유일하게 나빠진 곳입니다. '
    "예시 데이터.</div>\n"
    "      </div>\n      </section>\n"
)

# ---------------------------------------------------------------- 3부 그래프
S.append(cover("제3부 · 그래프", "PART", "일곱 가지면 실무는",
               "거의 다 덮입니다", "숫자를 넣으면 스크립트가 좌표를 뽑습니다"))

S.append(chart_slide("06", "3-1 · 항목 비교", "422건 중 184건이 한 가지 사유입니다",
                     "큰 것부터 내려 정렬하고, 강조는 맨 위 하나만 남깁니다", "bars", "BAR"))
S.append(chart_slide("07", "3-2 · 구성비", "경리팀은 시간의 62%를 입력에 씁니다",
                     "구성비는 파이가 아니라 100% 누적 가로 막대로 그립니다", "sbar", "STACKED"))
S.append(chart_slide("08", "3-3 · 시계열 (기간이 짧을 때)", "마감이 13일에서 5일이 됐습니다",
                     "달·분기가 여섯 이하면 세로 막대가 낫습니다. 축은 0에서 시작합니다", "cols", "COLUMN"))
S.append(chart_slide("09", "3-4 · 구성비 x 시간", "매출은 21% 늘고 자문은 4배가 됐습니다",
                     "누적 세로 막대는 총량과 안쪽 구성을 한 번에 집니다", "stack", "STACKED COLUMN"))
S.append(chart_slide("10", "3-5 · 워터폴", "여덟 밤이 어디서 줄었는지 답합니다",
                     "A에서 B로 간 이유를 물으면 이 형태입니다. 늘어난 항목은 붉게 둡니다", "wf", "WATERFALL"))
S.append(chart_slide("11", "3-6 · 시계열 (계열이 둘 이상)", "4월에 동종 평균을 앞질렀습니다",
                     "비교 계열은 회색으로 눕히고 라벨은 처음·끝·꼭짓점에만 답니다", "line", "LINE"))
S.append(chart_slide("12", "3-7 · 상관", "규모가 커지면 지연도 늘어납니다",
                     "그런데 서린푸드는 그 선 위에 있습니다. 규모 탓이 아닙니다", "dot", "SCATTER"))

# ---------------------------------------------------------------- 4부 도표
S.append(cover("제4부 · 도표와 단계", "PART", "도표가 어려워지는 이유는",
               "부호를 겹쳐 쓰기 때문입니다", "화살표 · 색 · 위치 · 매달린 상자를 한 장에 다 넣은 경우"))

S.append(
    '      <section class="slide">\n'
    + head("13", "4-1 · 부호 세기", "한 장이 지는 부호는 둘까지입니다",
           "세 번째 부호가 들어오는 순간 아래에 범례가 붙고, 범례가 붙으면 이미 진 것입니다", "SIGNS")
    + '      <div class="duo">\n'
    '        <div class="panel" data-anim style="--d:3; --pc:var(--risk); --pct:var(--riskT); --pbg:var(--riskB)">\n'
    '          <div class="pk">어려워진 도표</div><h3>부호 넷을 한 장에 넣었습니다</h3>\n'
    '          <ul class="pts">\n'
    "            <li><b>화살표</b>가 순서를 집니다</li>\n"
    "            <li><b>테두리 색</b>이 입력 여부를 집니다</li>\n"
    "            <li><b>아래 매달린 상자</b>가 하위 화면을 집니다</li>\n"
    "            <li>그래서 아래에 설명 줄이 <b>세 줄</b> 붙었습니다</li>\n"
    "          </ul>\n"
    '          <div class="usage"><div class="ut">증상</div><ul class="uw">\n'
    "            <li>제목은 순서라고 하는데 그림은 순서가 아닙니다</li>\n"
    "          </ul></div>\n"
    "        </div>\n"
    '        <div class="panel" data-anim style="--d:4; --pc:var(--a1); --pct:var(--a1t); --pbg:var(--a1b)">\n'
    '          <div class="pk">고친 뒤</div><h3>장을 둘로 가릅니다</h3>\n'
    '          <ul class="pts">\n'
    "            <li>첫 장은 <b>순서만</b>. 상자 여섯 개를 한 줄로 세우고 화살표만 남깁니다</li>\n"
    "            <li>둘째 장은 <b>표로</b>. 화면 이름 · 주인 · 읽기/쓰기를 열로 세웁니다</li>\n"
    "            <li>범례가 사라집니다. <b>범례가 필요하면 형태가 틀린 것입니다</b></li>\n"
    "          </ul>\n"
    '          <div class="usage"><div class="ut">판정</div><ul class="uw">\n'
    "            <li>그림 아래 설명 줄이 두 줄을 넘으면 장을 나눕니다</li>\n"
    "          </ul></div>\n"
    "        </div>\n      </div>\n      </section>\n"
)

S.append(
    '      <section class="slide">\n'
    + head("14", "4-2 · 단계", "단계는 다섯을 넘기지 않습니다",
           "여섯 번째가 생기면 두 개를 묶거나 장을 나눕니다", "STEPS")
    + '      <div class="map" data-anim style="--d:3">\n'
    + '<div class="marw">→</div>'.join(
        '        <div class="step" style="--sc:var(--%s); --sct:var(--%st)">'
        '<div class="n">%s</div><h3>%s</h3><p>%s</p></div>\n' % (c, c, n, t, d)
        for c, n, t, d in [
            ("a1", "STEP 1", "메시지를 쓴다", "한 문장. 숫자가 들어간다"),
            ("a2", "STEP 2", "비교 유형을 고른다", "구성비·항목·시계열·빈도·상관"),
            ("a3", "STEP 3", "형태를 고른다", "유형이 형태를 정한다"),
            ("a1", "STEP 4", "강조를 하나 남긴다", "나머지는 회색"),
            ("a2", "STEP 5", "잰다", "slidecheck 로 넘침 확인"),
        ]
    )
    + '      </div>\n      <div class="rail" data-anim style="--d:4">\n'
    '        <div class="msg">순서를 뒤집으면 <b>데이터가 형태를 정하게</b> 됩니다</div>\n'
    '        <div class="tools"><span class="tool"><i></i>mkchart.py</span>'
    '<span class="tool"><i></i>slidecheck.ps1</span></div>\n'
    "      </div>\n      </section>\n"
)

S.append(cover("마무리", "CLOSING", "고를 것은 열 가지가 아니라",
               "다섯 가지 비교 유형입니다",
               "표 3종 · 그래프 7종 · 도표 규칙 2개. 나머지는 스킬이 집니다"))

# ---------------------------------------------------------------- 조립
tpl = io.open(TPL, encoding="utf-8").read()
open_tag = '<div class="deck" id="deck">'
close = "\n    </div>\n  </div>\n\n  <div class=\"brandbar\""
a = tpl.index(open_tag) + len(open_tag)
b = tpl.index(close)
out = tpl[:a] + "\n\n" + "\n".join(S) + tpl[b:]
out = out.replace("{{DECK_TITLE}}", TITLE)
out = out.replace('<section class="slide cover">', '<section class="slide cover active">', 1)
io.open(OUT, "w", encoding="utf-8").write(out)
print("wrote", OUT, "slides =", out.count('<section class="slide'))
