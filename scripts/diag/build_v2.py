# -*- coding: utf-8 -*-
"""서린푸드 머니플로우 진단 v2 — 손익흐름이 척추인 판.

구성: 흐름(현재) -> 새는 자리 3곳 확대 -> 흐름(개입 후) -> 가치 환산 -> 요약.

    python build_v2.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from draw import G, sc, fmt  # noqa: E402
import flow  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "reference", "서린푸드_머니플로우.html")

# ---------------------------------------------------------------- 데이터
BEFORE = {
    "rev": 320, "cogs": 231, "sga": 60, "op": 29, "dep": 19, "ebitda": 48,
    "outs": [("운전자본 증가", 14, "leak"), ("설비투자", 11, "mid"),
             ("이자", 4, "mid"), ("법인세", 5, "mid"), ("잉여현금", 14, "final")],
    "final_sub": "전환율 29%",
}
AFTER = {
    "rev": 320, "cogs": 223.6, "sga": 58.2, "op": 38.2, "dep": 19, "ebitda": 57.2,
    "dec": 1,
    "outs": [("운전자본 증가", 5.0, "mid"), ("설비투자", 11.0, "mid"),
             ("이자", 3.0, "mid"), ("법인세", 7.0, "mid"), ("잉여현금", 31.2, "final")],
    "final_sub": "전환율 55%",
}
AFTER_D = {
    "cogs": "▼7.4  외주 재협상 4.9 + 가공 믹스 2.6",
    "sga": "▼1.8  온라인 정상화",
    "op": "▲9.2",
    "out4": "▲17억",
}


# ---------------------------------------------------------------- 흐름 1 · 현재
def hero():
    g, pos = flow.sankey(BEFORE, "a", H=560)
    x1, yc, hc = pos["cogs"]
    flow._tag(g, x1 + 26, yc + hc / 2 + 28, "① 외주 역마진 6.8억이 이 안에 있다")
    xs, ys, hs = pos["sga"]
    flow._tag(g, xs + 26, ys + hs / 2 + 32, "③ 온라인 영업적자 0.4억")
    xw, yw, hw = pos["outs"][0]
    flow._tag(g, 706, yw - 46, "② 이익 증가분 7억을 재고가 삼켰다")
    g.txt(70, 36, "띠의 두께가 곧 금액입니다. 왼쪽에서 320억이 들어와 오른쪽 아래로 14억이 나옵니다.",
          "l", fill="var(--ink-2)", size=13.5)
    return g.done()


# ---------------------------------------------------------------- 흐름 2 · 개입 후
def hero_after():
    g, pos = flow.sankey(AFTER, "b", deltas=AFTER_D, H=560)
    xw, yw, hw = pos["outs"][0]
    g.note(700, yw - 92, ["재고 정상 궤도로 운전자본 ▼9.0",
                          "차입 상환으로 이자 ▼1.0 · 법인세 ▲2.0"], 292)
    g.txt(70, 36, "같은 매출 320억에 세 가지 개입만 반영한 흐름입니다. 초록 숫자가 바뀐 자리입니다.",
          "l", fill="var(--ink-2)", size=13.5)
    return g.done()


# ---------------------------------------------------------------- 확대 카드 3장
def card_cogs():
    g = G(360, 220, "공장별 단위원가와 판가")
    rows = [("1공장", 1180, False), ("2공장", 1340, False), ("3공장", 1520, False), ("외주", 1880, True)]
    for i, (n, c, bad) in enumerate(rows):
        y = 30 + i * 40
        w = sc(c, 0, 2000, 0, 250)
        g.rect(64, y, w, 22, "var(--c-clay)" if bad else "var(--c-navy)", 2, o=.85 if bad else .75)
        g.txt(58, y + 15, n, "l", "end", fill="var(--ink)", weight=650, size=12)
        g.txt(64 + w + 6, y + 15, fmt(c), "f", size=11.5, weight=700,
              fill="var(--c-clay)" if bad else "var(--ink-2)")
    px = 64 + sc(1620, 0, 2000, 0, 250)
    g.line(px, 22, px, 192, "var(--c-ochre)", 1.8, "5 3")
    g.txt(px, 208, "판가 1,620원", "ls", "middle", fill="var(--c-ochre)", weight=800)
    return g.done()


def card_wc():
    g = G(360, 220, "현금전환주기 미니 타임라인")
    def dx(d):
        return sc(d, 0, 115, 70, 340)
    rows = [("재고", 0, 68, "var(--c-navy)", "55 → 68일"),
            ("채권", 68, 41, "var(--c-teal)", "41일"),
            ("채무", 0, 52, None, "52일"),
            ("내 돈", 52, 57, "var(--ink)", "57일 = 46억")]
    for i, (n, s, ln, c, lab) in enumerate(rows):
        y = 30 + i * 40
        if c is None:
            g.rect(dx(s), y, dx(s + ln) - dx(s), 22, "var(--plot)", 2,
                   stroke="var(--c-ochre)", sw=1.4, dash="4 3")
        else:
            g.rect(dx(s), y, dx(s + ln) - dx(s), 22, c, 2, o=.85)
        g.txt(64, y + 15, n, "l", "end", fill="var(--ink)", weight=650, size=12)
        g.txt(dx(s + ln) + 6 if s + ln < 100 else dx(s) - 6, y + 15, lab, "f",
              "start" if s + ln < 100 else "end", size=11.5, weight=700,
              fill="var(--c-clay)" if i == 0 else "var(--ink-2)")
    g.txt(70, 208, "재고만 13일 늘었다 · 동종 중앙값 45.5일", "ls")
    return g.done()


def card_online():
    g = G(360, 220, "사업부 이익률 미니 풀")
    segs = [("급식", 148, 6.8), ("유통", 84, 13.6), ("온라인", 28, -1.6), ("가공", 60, 13.3)]
    zero = sc(0, -5, 16, 180, 26)
    x = 46
    for n, rv, m in segs:
        w = 292 * rv / 320
        y = sc(m, -5, 16, 180, 26)
        bad = m < 0
        if bad:
            g.rect(x + 1, zero, w - 2, y - zero, "var(--c-clay)", 0, o=.9)
            g.txt(x + w / 2, y + 16, n, "l", "middle", fill="var(--c-clay)", weight=800, size=11.5)
            g.txt(x + w / 2, y + 31, "%.1f%%" % m, "f", "middle", fill="var(--c-clay)", size=11)
        else:
            g.rect(x + 1, y, w - 2, zero - y, "var(--c-navy)", 0, o=.72)
            g.txt(x + w / 2, y - 18, n, "l", "middle", fill="var(--ink)", weight=650, size=11.5)
            g.txt(x + w / 2, y - 5, "%.1f%%" % m, "f", "middle", size=11)
        x += w
    g.line(46, zero, 338, zero, "var(--rule)", 1.2)
    g.txt(46, 208, "폭 = 매출 · 높이 = 이익률 · 온라인만 WACC 아래", "ls")
    return g.done()


# ---------------------------------------------------------------- 가치 스트립
def value_strip():
    g = G(1080, 150, "기업가치 381에서 455로 가는 구간 스트립")
    def px(v):
        return sc(v, 0, 470, 40, 1040)
    y, h = 52, 40
    g.rect(px(0), y, px(381) - px(0), h, "var(--ink)", 3)
    g.txt(px(190), y + h / 2 + 6, "현재 기업가치  381억", "fw", "middle")
    segs = [("외주 재협상", 39), ("온라인", 14), ("가공 믹스", 21)]
    x = 381
    for i, (n, v) in enumerate(segs):
        g.rect(px(x) + 2, y, px(x + v) - px(x) - 3, h, "var(--c-teal)", 3, o=.6 + i * .14)
        g.txt(px(x + v / 2), y - 10, "+" + fmt(v), "f", "middle",
              fill="var(--c-teal)", weight=800, size=13)
        g.txt(px(x + v / 2), y + h + (18 if i % 2 == 0 else 36), n, "ls", "middle")
        x += v
    g.txt(px(455) + 10, y + 18, "455억", "f", fill="var(--c-teal)", size=21, weight=800)
    g.txt(px(455) + 10, y + 38, "+19%", "f", fill="var(--ink-2)", size=12.5, weight=700)
    g.line(px(381), y - 26, px(381), y + h + 6, "var(--ink-3)", 1, "3 3")
    g.txt(px(381), y - 34, "EV/EBITDA 7.9배 유지 · 배수 확대 없이", "ls", "middle")
    return g.done()


# ---------------------------------------------------------------- HTML
CSS = """
:root{
  --paper:#EDF0F3; --panel:#F7F8FA; --plot:#FFFFFF;
  --ink:#0F1E2B; --ink-2:#3E5364; --ink-3:#758798;
  --rule:#C6D0D8; --rule-soft:#DDE3E8; --grid:#DCE3E8;
  --c-navy:#1B3A57; --c-ochre:#B3762B; --c-teal:#2E6F6B; --c-clay:#8C3B36;
  --c-slate:#7A8C9B; --c-sand:#C9B893; --maxw:1150px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);
  font-family:'Pretendard Variable',Pretendard,-apple-system,'Malgun Gothic',sans-serif;
  font-size:15.5px;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 34px}
.mast{padding:52px 0 0}
.mast .kick{display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;
  font-size:12px;letter-spacing:.12em;color:var(--ink-3);border-bottom:2px solid var(--ink);
  padding-bottom:14px}
.mast h1{font-family:'Noto Serif KR',serif;font-weight:900;font-size:46px;line-height:1.3;
  margin-top:34px;letter-spacing:-.01em}
.mast h1 em{font-style:normal;color:var(--c-teal)}
.mast h1 .x{color:var(--c-clay)}
.mast .sub{margin-top:16px;font-size:17px;color:var(--ink-2);max-width:46em}

.stage{margin-top:44px;background:var(--plot);border:1px solid var(--rule)}
.stage-head{display:flex;align-items:baseline;gap:16px;padding:22px 30px 16px;
  border-bottom:1px solid var(--rule-soft)}
.stage-head .no{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:700;
  letter-spacing:.1em;color:var(--plot);background:var(--ink);padding:3px 10px;border-radius:2px}
.stage-head h2{font-family:'Noto Serif KR',serif;font-weight:700;font-size:23px;flex:1}
.stage-head .tag{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--ink-3)}
.stage-body{padding:18px 24px 10px}
.stage-body svg{width:100%;height:auto;display:block}
.stage-foot{padding:12px 30px 18px;border-top:1px solid var(--rule-soft);
  font-size:13.5px;color:var(--ink-2);display:flex;gap:36px;flex-wrap:wrap}
.stage-foot b{color:var(--ink)}
.stage-foot .src{color:var(--ink-3);font-size:11.5px;flex-basis:100%}

.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px}
.card{background:var(--plot);border:1px solid var(--rule)}
.card .ch{padding:16px 22px 12px;border-bottom:1px solid var(--rule-soft)}
.card .ch .no{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:11px;
  font-weight:700;color:var(--c-clay);border:1.3px solid var(--c-clay);border-radius:50%;
  width:22px;height:22px;text-align:center;line-height:19px;margin-right:8px}
.card .ch h3{display:inline;font-family:'Noto Serif KR',serif;font-size:17.5px;font-weight:700}
.card .amt{float:right;font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:800;
  color:var(--c-clay)}
.card svg{width:100%;height:auto;display:block;padding:10px 8px 0}
.card .fix{padding:12px 22px 18px;font-size:13px;color:var(--ink-2);border-top:1px dashed var(--rule-soft)}
.card .fix b{color:var(--c-teal)}

.sect-title{margin:64px 0 0;display:grid;grid-template-columns:110px 1fr;gap:24px;
  border-top:2px solid var(--ink);padding-top:20px}
.sect-title .num{font-family:'IBM Plex Mono',monospace;font-size:13px;color:var(--ink-3);padding-top:7px}
.sect-title h2{font-family:'Noto Serif KR',serif;font-weight:700;font-size:28px}
.sect-title p{margin-top:10px;color:var(--ink-2);max-width:60em}

.tblw{margin:26px 0 0;border:1px solid var(--rule);background:var(--plot)}
table{border-collapse:collapse;width:100%;font-size:13.5px;table-layout:fixed}
th,td{text-align:left;padding:12px 16px;border-bottom:1px solid var(--rule-soft);
  vertical-align:top;word-break:keep-all}
th{font-size:12px;color:var(--ink-3);font-weight:600;background:var(--panel);white-space:nowrap}
td.num{font-family:'IBM Plex Mono',monospace;text-align:right;white-space:nowrap}
th.num{text-align:right}
tr.tot td{border-top:2px solid var(--ink);font-weight:700;border-bottom:0}

.method{margin:54px 0 0;padding:24px 0 0;border-top:1px solid var(--rule);
  font-size:13px;color:var(--ink-3);max-width:74em}
footer{margin:46px 0 0;padding:20px 0 66px;border-top:2px solid var(--ink);
  display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;
  font-size:11.5px;color:var(--ink-3);letter-spacing:.08em}
@media print{body{background:#fff}.stage,.card,.tblw{break-inside:avoid}}
"""

B = ["""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>서린푸드 머니플로우 · 돈이 새는 자리</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@700;900&family=IBM+Plex+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>""" + CSS + """</style></head><body><div class="wrap">

<header class="mast">
  <div class="kick"><span>PROJECT SEORIN · MONEY FLOW</span><span>2026.09 · 예시 데이터</span></div>
  <h1>320억이 들어와서<br><em>14억</em>이 남습니다. <span class="x">34억</span>은 길에서 샙니다.</h1>
  <p class="sub">손익계산서와 현금흐름표를 한 장의 흐름으로 이었습니다. 띠의 두께가 금액입니다. 새는 자리 세 곳을 확대해 보고, 고친 뒤의 흐름을 같은 그림으로 다시 그렸습니다.</p>
</header>
"""]

B.append('<div class="stage"><div class="stage-head"><span class="no">FLOW 1</span>'
         '<h2>지금의 흐름 · 2025년</h2><span class="tag">단위 억원 · 띠 두께 = 금액</span></div>'
         '<div class="stage-body">' + hero() + '</div>'
         '<div class="stage-foot">'
         '<span>영업이익률 <b>9.1%</b>로 준수합니다</span>'
         '<span>그런데 EBITDA 48억 중 잉여현금은 <b>14억, 전환율 29%</b></span>'
         '<span>재고·설비·금융비용이 번 돈의 3분의 2를 도로 가져갑니다</span>'
         '<span class="src">예시 데이터 · 감가상각은 비현금 비용이므로 EBITDA에 합류하는 것으로 표시</span>'
         '</div></div>')

B.append("""
<div class="sect-title"><div class="num">ZOOM</div><div>
  <h2>새는 자리 세 곳</h2>
  <p>흐름도에 표식을 단 세 지점입니다. 셋 다 전사 평균에 가려져 있었고, 셋 다 열여덟 달 안에 움직일 수 있습니다.</p>
</div></div>
<div class="cards">
""")
B.append('<div class="card"><div class="ch"><span class="no">1</span><h3>원가 231억 안의 역마진</h3>'
         '<span class="amt">연 6.8억</span></div>' + card_cogs() +
         '<div class="fix">외주 26천 톤을 판가보다 260원 비싸게 만들고 있습니다. '
         '<b>재협상 목표 190원, 연 4.9억 회복.</b> 잔여는 3공장 증설 검토와 묶어 판단합니다.</div></div>')
B.append('<div class="card"><div class="ch"><span class="no">2</span><h3>운전자본이 삼킨 14억</h3>'
         '<span class="amt">재고 +13일</span></div>' + card_wc() +
         '<div class="fix">6분기 동안 채권은 잡혔고 재고만 55일에서 68일이 됐습니다. '
         '<b>12일 단축이면 일회성 현금 7.6억.</b> S&amp;OP 도입과 SKU 하위 20% 정리로 갑니다.</div></div>')
B.append('<div class="card"><div class="ch"><span class="no">3</span><h3>판관비 속 온라인 적자</h3>'
         '<span class="amt">연 0.4억 + α</span></div>' + card_online() +
         '<div class="fix">온라인 28억은 ROIC 3.1%로 자본비용을 밑돕니다. '
         '<b>가격·믹스 재설계와 물류 3PL 통합으로 연 1.8억 정상화.</b> 안 되면 축소가 답입니다.</div></div>')
B.append('</div>')

B.append('<div class="sect-title"><div class="num">FLOW 2</div><div>'
         '<h2>고친 뒤의 흐름</h2>'
         '<p>같은 매출 320억에 세 가지 개입만 반영해 같은 그림을 다시 그렸습니다. '
         '흐름의 모양 자체가 달라집니다. 오른쪽 아래 띠가 두 배가 넘게 굵어집니다.</p></div></div>')
B.append('<div class="stage"><div class="stage-head"><span class="no">FLOW 2</span>'
         '<h2>개입 반영 후 · 정상화 연도 기준</h2><span class="tag">단위 억원 · 초록 = 바뀐 자리</span></div>'
         '<div class="stage-body">' + hero_after() + '</div>'
         '<div class="stage-foot">'
         '<span>잉여현금 <b>14억 → 31억</b></span>'
         '<span>전환율 <b>29% → 55%</b>, 동종 상위권 진입</span>'
         '<span>여기에 재고 단축의 일회성 현금 <b>7.6억</b>이 첫해에 별도로 붙습니다</span>'
         '<span class="src">예시 데이터 · 성장 효과 제외, 개입 효과만 반영한 비교용 흐름</span>'
         '</div></div>')

B.append('<div class="sect-title"><div class="num">VALUE</div><div>'
         '<h2>가치로 환산하면</h2>'
         '<p>배수를 올려 잡지 않았습니다. EV/EBITDA 7.9배 그대로, 이익 개선분만 곱했습니다.</p></div></div>')
B.append('<div class="stage"><div class="stage-body">' + value_strip() + '</div></div>')

B.append("""
<div class="tblw"><table>
<thead><tr><th style="width:24%">개입</th><th style="width:13%" class="num">연간 손익</th>
<th style="width:13%" class="num">기업가치</th><th style="width:10%">시한</th><th>먼저 확인할 것</th></tr></thead>
<tbody>
<tr><td><b>외주 단가 재협상</b></td><td class="num">+4.9억</td><td class="num">+39억</td>
    <td>6개월</td><td>외주사 원가 구조, 대체 공급선</td></tr>
<tr><td><b>재고 12일 단축</b></td><td class="num">이자 0.4억</td><td class="num">현금 +7.6억</td>
    <td>12개월</td><td>안전재고 약정의 해지 조항</td></tr>
<tr><td><b>온라인 손익 정상화</b></td><td class="num">+1.8억</td><td class="num">+14억</td>
    <td>12개월</td><td>채널별 배송비 실측</td></tr>
<tr><td><b>가공 믹스 확대</b></td><td class="num">+2.6억</td><td class="num">+21억</td>
    <td>18개월</td><td>3공장 잔여 캐파 실사</td></tr>
<tr class="tot"><td>합계</td><td class="num">+9.3억</td><td class="num">+74억 (+19%)</td>
    <td colspan="2"></td></tr>
</tbody></table></div>

<div class="method">
  <p><b>방법과 한계.</b> 회사와 숫자는 전부 예시입니다. 두 흐름도는 같은 축척이라 띠 두께를 직접 비교할 수 있습니다. 개입 후 흐름은 성장 효과를 뺀 비교용이며, 감가상각·설비투자는 현행 유지로 두었습니다. 기업가치는 EV/EBITDA 7.9배 고정입니다.</p>
</div>

<footer><span>PROJECT SEORIN · MONEY FLOW · 2026.09</span><span>예시 데이터 · 배포 전 검토 필요</span></footer>
</div></body></html>""")

io.open(OUT, "w", encoding="utf-8").write("\n".join(B))
print("wrote", OUT, os.path.getsize(OUT), "bytes")
