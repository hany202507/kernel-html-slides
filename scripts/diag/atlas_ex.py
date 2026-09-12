# -*- coding: utf-8 -*-
"""고급 전시물 아틀라스 — 서린푸드 판.

두 아틀라스(사용자 제공 27종)와 기존 13종을 합친 세트에서, 재무진단·머니플로우가
이미 그린 것은 그 함수를 재사용하고 나머지를 여기서 그린다. 전부 draw.py 문법.
숫자는 data.py 의 서린푸드 예시와 이어진다.
"""
import math

import data as D
from draw import G, sc, fmt

NAVY, OCHRE, TEAL, CLAY = "var(--c-navy)", "var(--c-ochre)", "var(--c-teal)", "var(--c-clay)"
SLATE, SAND = "var(--c-slate)", "var(--c-sand)"
INK, INK2, INK3 = "var(--ink)", "var(--ink-2)", "var(--ink-3)"


# ================================================================ 가치평가
def football():
    rows = [("52주 주가 범위", 240, 330, SLATE, .55),
            ("상장사 배수  EV/EBITDA 6.5~9.0x", 312, 432, NAVY, .95),
            ("유사거래  7.2~10.1x", 346, 485, NAVY, .7),
            ("현금흐름할인  WACC 9.5~11.5%", 268, 412, TEAL, .9),
            ("차입매수 여력  IRR 20~25%", 240, 330, OCHRE, .85)]
    g = G(1080, 330, "다섯 가지 방법의 가치 범위와 제시가")
    ml, mr, mt, mb = 300, 84, 40, 30
    lo, hi = 210, 510
    def px(v): return sc(v, lo, hi, ml, mr and 1080 - mr)
    for v in (250, 300, 350, 400, 450, 500):
        g.line(px(v), mt - 6, px(v), 330 - mb, "var(--grid)", 1)
        g.txt(px(v), 330 - mb + 18, fmt(v), "f", "middle", fill=INK3, size=11)
    band = (330 - mt - mb) / len(rows)
    for i, (lab, a, b, c, o) in enumerate(rows):
        y = mt + band * i + band / 2
        g.rect(px(a), y - 10, px(b) - px(a), 20, c, 3, o=o)
        g.txt(ml - 16, y + 4, lab, "l", "end", fill=INK, weight=650, size=12.5)
        g.txt(px(a) - 8, y + 4, fmt(a), "f", "end", fill=INK3, size=11.5)
        g.txt(px(b) + 8, y + 4, fmt(b), "f", "start", fill=INK2, size=11.5, weight=700)
    g.rect(px(380) - 3, mt - 14, 6, 330 - mb - mt + 14, OCHRE, 0, o=.15)
    g.line(px(380), mt - 14, px(380), 330 - mb, OCHRE, 1.6)
    g.txt(px(380), mt - 20, "제시가 380억", "f", "middle", fill="var(--c-ochre)", weight=800, size=12.5)
    return g.done()


def evbridge():
    items = [("기업가치 EV", 381, "tot"), ("순차입금", -82, "dn"), ("소수주주지분", -12, "dn"),
             ("비영업자산", 18, "up"), ("지분가치", 305, "tot")]
    g = G(1080, 340, "기업가치에서 지분가치로 가는 다리")
    pl, pr, pt, pb = 60, 1020, 46, 280
    def py(v): return sc(v, 0, 420, pb, pt)
    stepw = (pr - pl) / len(items)
    run = 0.0
    for i, (lab, v, kind) in enumerate(items):
        cx = pl + stepw * i + stepw / 2
        if kind == "tot":
            g.rect(cx - 52, py(v), 104, pb - py(v), NAVY if i == 0 else INK, 2)
            g.txt(cx, py(v) - 10, fmt(v), "f", "middle", weight=800, size=15)
            run = v
        else:
            y1, y0 = py(run), py(run + v)
            g.rect(cx - 42, min(y0, y1), 84, abs(y0 - y1), CLAY if v < 0 else TEAL, 2, o=.85)
            g.txt(cx, min(y0, y1) - 8, ("" if v < 0 else "+") + fmt(v), "f", "middle",
                  fill="var(--c-clay)" if v < 0 else "var(--c-teal)", weight=700, size=13)
            run += v
        if i < len(items) - 1:
            g.line(cx + (52 if kind == "tot" else 42), py(run),
                   cx + stepw - (52 if items[i + 1][2] == "tot" else 42), py(run),
                   INK3, 1, "3 3", .7)
        g.txt(cx, pb + 20, lab, "l", "middle", fill=INK, weight=600, size=12.5)
    g.line(pl, pb, pr, pb, "var(--rule)", 1)
    g.txt(pl, pb + 46, "순차입금 정의(리스부채·우선주 포함 여부)를 각주로 못 박습니다. 여기서 분쟁이 납니다.", "ls")
    return g.done()


def regression():
    peers = [("명진", 2.1, 6.4, 1250), ("대한", 4.2, 8.8, 880), ("세일", 6.0, 7.3, 540),
             ("한울", 9.8, 8.3, 410), ("가온", 14.6, 8.6, 190)]
    slope, icept = 0.17, 6.32          # 최소제곱 근사
    g = G(1080, 360, "성장률과 EV/EBITDA 배수의 회귀 산점도")
    ml, mr, mt, mb = 70, 60, 34, 44
    def PX(x): return sc(x, 0, 17, ml, 1080 - mr)
    def PY(y): return sc(y, 5, 10.5, 360 - mb, mt)
    for v in (6, 8, 10):
        g.line(ml, PY(v), 1080 - mr, PY(v), "var(--grid)", 1)
        g.txt(ml - 8, PY(v) + 4, "%dx" % v, "f", "end", fill=INK3, size=11)
    g.line(ml, 360 - mb, 1080 - mr, 360 - mb, "var(--rule)", 1)
    g.line(PX(0), PY(icept), PX(17), PY(icept + slope * 17), SLATE, 2, "7 5")
    g.txt(PX(0.6), PY(icept + slope * 0.6) - 12, "회귀선 · R² 0.62 · 표본 5", "ls", "start",
          fill=INK2, weight=700)
    rmax = 1250
    for n, x, y, r in peers:
        rr = 8 + 20 * (r / rmax) ** .5
        g.circle(PX(x), PY(y), rr, SLATE)
        g.txt(PX(x), PY(y) - rr - 8, n, "l", "middle", fill=INK2, weight=650, size=12)
    sx, sy = 11.5, 7.9
    fair = icept + slope * sx
    g.circle(PX(sx), PY(sy), 13, NAVY)
    g.txt(PX(sx), PY(sy) - 24, "서린푸드 7.9x", "f", "middle", fill=INK, weight=800, size=13)
    g.line(PX(sx), PY(sy) - 8, PX(sx), PY(fair) + 4, OCHRE, 1.6, "3 3")
    g.txt(PX(sx), PY(sy) + 30, "회귀선 대비 0.4x 할인", "f", "middle",
          fill="var(--c-ochre)", weight=700, size=12)
    g.txt(1080 - mr, 360 - mb + 28, "매출 성장률 (%)", "lb", "end", fill=INK, weight=700)
    g.txt(ml, mt - 10, "EV/EBITDA · 원 크기 = 매출", "ls")
    return g.done()


def accretion():
    rows = ["360억", "390억", "420억", "450억"]
    cols = ["현금 100%", "현금 75%", "현금 50%", "현금 25%"]
    v = [[6.2, 4.8, 3.1, 1.2], [4.1, 2.9, 1.4, -0.3], [2.2, 1.1, -0.4, -1.9], [0.4, -0.8, -2.1, -3.6]]
    g = G(1080, 350, "인수가와 대금 구성에 따른 주당이익 증감 격자")
    left, ctop, cw, ch = 210, 64, 190, 54
    g.txt(30, 34, "값은 인수 첫해 주당이익 증감률(%) · 초록 = 증가, 적갈 = 감소 · 예시", "ls")
    for j, c in enumerate(cols):
        g.txt(left + cw * j + cw / 2, ctop - 12, c, "l", "middle", fill=INK3, weight=650, size=12)
    for i, r in enumerate(rows):
        y = ctop + ch * i
        g.txt(left - 16, y + ch / 2 + 5, "인수가 " + r, "l", "end", fill=INK, weight=650, size=12.5)
        for j, x in enumerate(v[i]):
            xx = left + cw * j
            pos = x >= 0
            o = .12 + .55 * min(abs(x) / 6.5, 1)
            g.rect(xx + 2, y + 2, cw - 4, ch - 4, TEAL if pos else CLAY, 3, o=o)
            g.txt(xx + cw / 2, y + ch / 2 + 5, "%+.1f%%" % x, "f", "middle",
                  fill=INK if o < .45 else "#fff", weight=700, size=13)
    g.rect(left + 2, ctop + ch * 2 + 2, cw * 3 - 4, ch - 4, "none", 3, stroke=INK, sw=1.8)
    g.txt(left + cw * 1.5, ctop + ch * 4 + 26, "제시가 420억 · 현금 50% 이하로 내려가면 희석으로 넘어갑니다",
          "l", "middle", fill=INK2, size=12.5)
    return g.done()


# ================================================================ 딜 구조
def payoff():
    g = G(1080, 380, "회수금액별 주주 배분 페이오프")
    ml, mr, mt, mb = 74, 240, 30, 44
    X1 = 600.0
    def PX(x): return sc(x, 0, X1, ml, 1080 - mr)
    def PY(y): return sc(y, 0, 320, 380 - mb, mt)
    for v in (100, 200, 300):
        g.line(ml, PY(v), 1080 - mr, PY(v), "var(--grid)", 1)
        g.txt(ml - 8, PY(v) + 4, fmt(v), "f", "end", fill=INK3, size=11)
    g.line(ml, 380 - mb, 1080 - mr, 380 - mb, "var(--rule)", 1)
    for v in (210, 300, 420):
        g.line(PX(v), mt, PX(v), 380 - mb, "var(--rule-soft)", 1, "4 4")
        g.txt(PX(v), 380 - mb + 18, fmt(v), "f", "middle", fill=INK3, size=11)

    def kink(pts, c, name, sub=""):
        g.poly([(PX(x), PY(y)) for x, y in pts], c, 3)
        x, y = pts[-1]
        g.txt(PX(x) + 12, PY(y) + 4, name, "l", fill=c, weight=800, size=13)
        if sub:
            g.txt(PX(x) + 12, PY(y) + 20, sub, "ls")
    kink([(0, 0), (210, 210), (600, 210)], SLATE, "인수금융 210억", "먼저, 전액")
    kink([(0, 0), (210, 0), (300, 90), (600, 90)], OCHRE, "우선주 90억", "1배 우선")
    kink([(0, 0), (300, 0), (600, 300)], NAVY, "보통주", "300억을 넘어야 시작")
    g.txt(1080 - mr, 380 - mb + 36, "회수금액 (억원) →", "lb", "end", fill=INK, weight=700)
    return g.done()


def ladder():
    g = G(1080, 360, "만기 분포와 유동성 한도")
    years = [("2026", [18, 24, 0]), ("2027", [18, 12, 0]), ("2028", [18, 0, 40]),
             ("2029", [12, 0, 0]), ("2030", [6, 0, 0])]
    names = ["시설자금", "운전자금", "회사채"]
    colors = [NAVY, TEAL, OCHRE]
    ml, mr, mt, mb = 70, 40, 56, 44
    mx = 66.0
    def PY(v): return sc(v, 0, mx, 360 - mb, mt)
    for i, (nm, c) in enumerate(zip(names, colors)):
        x = ml + i * 120
        g.rect(x, 22, 12, 12, c, 2)
        g.txt(x + 20, 32, nm, "l", fill=INK2, weight=650, size=12.5)
    step = (1080 - ml - mr) / 5
    for i, (yr, parts) in enumerate(years):
        cx = ml + step * i + step / 2
        acc = 0.0
        for p, c in zip(parts, colors):
            if p <= 0:
                continue
            h = (360 - mb - mt) * p / mx
            g.rect(cx - 44, PY(acc + p), 88, h, c, 2, o=.88)
            acc += p
        g.txt(cx, PY(acc) - 9, fmt(sum(parts)) + "억", "f", "middle", weight=800, size=13.5)
        g.txt(cx, 360 - mb + 20, yr, "l", "middle", fill=INK, weight=650)
    g.line(ml, PY(46), 1080 - mr, PY(46), CLAY, 2, "7 4")
    g.txt(1080 - mr, PY(46) - 9, "가용 유동성 46억", "f", "end", fill="var(--c-clay)", weight=800, size=12.5)
    g.line(ml, 360 - mb, 1080 - mr, 360 - mb, "var(--rule)", 1)
    return g.done()


def attribution():
    parts = [("EBITDA 성장", 112), ("차입금 상환", 78), ("배수 확대", 34), ("잉여현금", 16)]
    g = G(1080, 260, "지분가치 증가분 240억의 원천 분해")
    tot = sum(v for _, v in parts)
    g.txt(40, 34, "투자원금 2.4배 · IRR 19.2% · 지분가치 증가 240억", "t")
    x, bt, bh = 40, 62, 84
    ramps = [(NAVY, .95), (NAVY, .7), (SLATE, .8), (SAND, .95)]
    for (n, v), (c, o) in zip(parts, ramps):
        w = 1000 * v / tot
        g.rect(x, bt, w - 3, bh, c, 3, o=o)
        pct = round(v / tot * 100)
        g.txt(x + w / 2, bt + bh / 2 + 7, "%d%%" % pct, "fw" if o > .75 and c == NAVY else "f",
              "middle", size=19, weight=800, fill=None if (o > .75 and c == NAVY) else INK)
        g.txt(x + w / 2, bt + bh + 24, n, "l", "middle", fill=INK, weight=700, size=13)
        g.txt(x + w / 2, bt + bh + 44, fmt(v) + "억", "f", "middle", fill=INK3, size=12)
        x += w
    g.txt(40, bt + bh + 74, "배수 확대가 14%뿐이라 시장에 기댄 거래가 아닙니다. 합이 240억과 정확히 맞아야 합니다.",
          "ls")
    return g.done()


# ================================================================ 실적 분해
def pvm():
    items = [("2024 매출", 287, "tot"), ("물량", 18, "up"), ("단가", 21, "up"),
             ("믹스", 6, "up"), ("이탈", -12, "dn"), ("2025 매출", 320, "tot")]
    g = G(1080, 340, "물량 가격 믹스 매출 브릿지, 축 절단")
    pl, pr, pt, pb = 60, 1020, 56, 270
    LO, HI = 255.0, 345.0
    def py(v): return sc(v, LO, HI, pb, pt)
    stepw = (pr - pl) / len(items)
    run = 0.0
    for i, (lab, v, kind) in enumerate(items):
        cx = pl + stepw * i + stepw / 2
        if kind == "tot":
            g.rect(cx - 50, py(v), 100, pb - py(v), NAVY if i == 0 else INK, 2)
            g.txt(cx, py(v) - 10, fmt(v), "f", "middle", weight=800, size=15)
            for dyy in (10, 15):
                g.line(cx - 56, pb - dyy, cx - 44, pb - dyy - 6, "var(--plot)", 2.6)
                g.line(cx + 44, pb - dyy, cx + 56, pb - dyy - 6, "var(--plot)", 2.6)
            run = v
        else:
            y1, y0 = py(run), py(run + v)
            g.rect(cx - 40, min(y0, y1), 80, abs(y0 - y1), TEAL if v > 0 else CLAY, 2, o=.88)
            g.txt(cx, min(y0, y1) - 8, "%+d" % v, "f", "middle",
                  fill="var(--c-teal)" if v > 0 else "var(--c-clay)", weight=700, size=13)
            run += v
        if i < len(items) - 1:
            g.line(cx + (50 if kind == "tot" else 40), py(run),
                   cx + stepw - (50 if items[i + 1][2] == "tot" else 40), py(run),
                   INK3, 1, "3 3", .7)
        g.txt(cx, pb + 20, lab, "l", "middle", fill=INK, weight=600, size=12.5)
    g.line(pl, pb, pr, pb, "var(--rule)", 1)
    g.txt(pl, 36, "축은 255에서 절단 · 요인 합이 33억과 맞지 않으면 기타로 메우지 말고 다시 쪼갭니다", "ls")
    return g.done()


def dupont():
    g = G(1080, 300, "ROE 두 단 분해 트리")
    def node(x, w, y, h, kfill, k, v, sub="", dark=False):
        g.rect(x, y, w, h, kfill, 6, stroke=None if dark else "var(--rule)", sw=1)
        g.txt(x + w / 2, y + 22, k, "l", "middle",
              fill="var(--paper)" if dark else INK3, weight=800, size=12)
        g.txt(x + w / 2, y + h - 14, v, "f", "middle",
              fill="#fff" if dark else INK, size=20, weight=800)
        if sub:
            g.txt(x + w / 2, y + h + 16, sub, "ls", "middle")
    node(440, 200, 16, 64, INK, "ROE", "14.2%", dark=True)
    mids = [("순이익률", "6.5%", 90, NAVY), ("자산회전율", "1.32", 440, TEAL),
            ("재무레버리지", "1.66", 790, OCHRE)]
    for i, (k, v, x, c) in enumerate(mids):
        g.line(x + 100, 116, x + 100, 100, "var(--rule)", 1)
        g.line(x + 100, 100, 540, 100, "var(--rule)", 1)
        node(x, 200, 116, 58, "var(--plot)", k, v)
        g.rect(x, 116, 200, 3, c, 0)
        if i:
            g.txt(x - 36, 152, "×", "l", "middle", fill=INK3, size=24, weight=800)
    g.line(540, 80, 540, 100, "var(--rule)", 1)
    leafs = [("매출총이익률 27.8%", 66), ("판관비율 18.7%", 234),
             ("재고회전 5.4회", 416), ("채권회전 8.9회", 584),
             ("순차입금 82억", 766), ("자기자본 198억", 934)]
    for t, cx in leafs:
        g.line(cx, 198, cx, 174, "var(--rule-soft)", 1)
        g.rect(cx - 78, 198, 156, 40, "var(--panel)", 5)
        g.txt(cx, 222, t, "f", "middle", fill=INK2, size=12, weight=700)
    g.txt(40, 284, "동종 평균 순이익률은 7.1%로 더 높습니다. 이 ROE는 마진이 아니라 회전율이 만들었습니다.", "ls")
    return g.done()


def experience():
    pts = [(40, 1420), (80, 1250), (160, 1100), (320, 968)]
    g = G(1080, 340, "누적 생산량 로그축 대 단가 로그축 경험 곡선")
    ml, mr, mt, mb = 80, 250, 36, 46
    def PX(x): return sc(math.log(x), math.log(30), math.log(400), ml, 1080 - mr)
    def PY(y): return sc(math.log(y), math.log(900), math.log(1550), 340 - mb, mt)
    for v in (1000, 1200, 1400):
        g.line(ml, PY(v), 1080 - mr, PY(v), "var(--grid)", 1)
        g.txt(ml - 8, PY(v) + 4, fmt(v), "f", "end", fill=INK3, size=11)
    for x in (40, 80, 160, 320):
        g.line(PX(x), mt, PX(x), 340 - mb, "var(--rule-soft)", 1, "2 4")
        g.txt(PX(x), 340 - mb + 18, fmt(x), "f", "middle", fill=INK3, size=11)
    g.poly([(PX(x), PY(y)) for x, y in pts], NAVY, 3)
    for i, (x, y) in enumerate(pts):
        g.circle(PX(x), PY(y), 5.5, NAVY)
        g.txt(PX(x) + 10, PY(y) - 10, fmt(y) + "원", "f", size=12, weight=700, fill=INK2)
    g.bracket(PX(80), PX(160), PY(1175), "두 배 = −12%", drop=8, up=False)
    g.txt(1080 - mr + 16, PY(968) + 4, "누적 320천 톤", "l", fill=INK2, weight=650, size=12.5)
    g.txt(1080 - mr + 16, PY(968) + 22, "다음 두 배(640천 톤)면 852원", "ls")
    g.txt(1080 - mr, 340 - mb + 36, "누적 생산량 (천 톤, 로그) →", "lb", "end", fill=INK, weight=700)
    return g.done()


# ================================================================ 시장 · 경쟁
def mekko():
    segs = [("급식", 148, [76, 18, 6]), ("유통(오프)", 84, [70, 16, 14]),
            ("온라인", 28, [82, 20, -2]), ("가공", 60, [67, 20, 13])]
    names = ["매출원가", "판매관리비", "영업이익"]
    fills = [(NAVY, .85), (NAVY, .5), (TEAL, .9)]
    g = G(1080, 380, "가변 폭 마리메꼬: 폭이 매출, 칸이 구성비")
    ml, mr, mt, mb = 40, 40, 60, 60
    for i, (nm, (c, o)) in enumerate(zip(names, fills)):
        x = ml + i * 140
        g.rect(x, 24, 12, 12, c, 2, o=o)
        g.txt(x + 20, 34, nm, "l", fill=INK2, weight=650, size=12.5)
    tot = sum(s[1] for s in segs)
    x = ml
    ph = 380 - mt - mb
    for nm, rv, parts in segs:
        w = (1080 - ml - mr) * rv / tot
        y = mt
        possum = sum(q for q in parts if q > 0)
        for p, (c, o) in zip(parts, fills):
            if p <= 0:
                g.rect(x + 1.5, 380 - mb + 2, w - 3, 6, CLAY, 1)
                continue
            h = ph * p / possum
            g.rect(x + 1.5, y, w - 3, h, c, 0, o=o)
            if h > 24 and w > 60:
                g.txt(x + w / 2, y + h / 2 + 5, "%d%%" % p, "fw" if o > .6 else "f", "middle",
                      size=13, weight=800, fill=None if o > .6 else INK)
            y += h
        g.txt(x + w / 2, 380 - mb + 24, nm, "l", "middle", fill=INK, weight=700, size=12.5)
        g.txt(x + w / 2, 380 - mb + 42, "매출 %d억" % rv, "ls", "middle")
        x += w
    g.txt(ml + (1080 - ml - mr) * (148 + 84 + 14) / tot, mt - 8, "온라인은 영업적자라 이익 칸이 없습니다",
          "ls", "middle", fill="var(--c-clay)", weight=700)
    return g.done()


def spread_bubble():
    segs = [("급식", 4, 3.0, 90), ("유통(오프)", 6, 7.6, 55), ("온라인", 18, -5.1, 25), ("가공", 9, 9.2, 28)]
    g = G(1080, 380, "ROIC 스프레드와 성장의 버블 지도")
    ml, mr, mt, mb = 80, 70, 40, 50
    def PX(x): return sc(x, 0, 21, ml, 1080 - mr)
    def PY(y): return sc(y, -8, 12, 380 - mb, mt)
    g.line(ml, PY(0), 1080 - mr, PY(0), "var(--rule)", 1.4)
    g.txt(1080 - mr, PY(0) - 8, "스프레드 0 · 이 아래는 굴러갈수록 가치 파괴", "ls", "end")
    for v in (-5, 5, 10):
        g.line(ml, PY(v), 1080 - mr, PY(v), "var(--grid)", 1)
        g.txt(ml - 8, PY(v) + 4, "%+d%%p" % v, "f", "end", fill=INK3, size=11)
    rmax = 90
    for nm, x, y, r in segs:
        rr = 12 + 30 * (r / rmax) ** .5
        bad = y < 0
        g.circle(PX(x), PY(y), rr, CLAY if bad else NAVY)
        g.txt(PX(x), PY(y) - rr - 9, nm, "l", "middle",
              fill="var(--c-clay)" if bad else INK, weight=750, size=12.5)
        g.txt(PX(x), PY(y) + rr + 16, "%+.1f%%p" % y, "f", "middle",
              fill="var(--c-clay)" if bad else INK2, size=11.5, weight=700)
    g.txt(1080 - mr, 380 - mb + 30, "매출 성장률 (%) →", "lb", "end", fill=INK, weight=700)
    g.txt(ml, mt - 12, "세로 = ROIC − WACC · 원 크기 = 투하자본", "ls")
    return g.done()


def slope():
    rows = [("대한", 18.6, 18.2), ("한울", 15.8, 16.4), ("서린푸드", 12.6, 15.0),
            ("명진", 13.5, 13.1), ("가온", 12.2, 11.8)]
    g = G(1080, 360, "2023과 2025 사이 동종 마진 기울기 그래프")
    xl, xr, mt, mb = 330, 750, 46, 40
    def PY(v): return sc(v, 10.5, 19.5, 360 - mb, mt)
    g.line(xl, mt - 8, xl, 360 - mb + 6, "var(--rule)", 1)
    g.line(xr, mt - 8, xr, 360 - mb + 6, "var(--rule)", 1)
    g.txt(xl, 360 - mb + 24, "2023", "l", "middle", fill=INK3, weight=700)
    g.txt(xr, 360 - mb + 24, "2025", "l", "middle", fill=INK3, weight=700)
    for nm, a, b in rows:
        me = nm == "서린푸드"
        c = NAVY if me else SLATE
        g.line(xl, PY(a), xr, PY(b), c, 3.4 if me else 1.8, o=None if me else .75)
        g.circle(xl, PY(a), 5.5 if me else 4, c)
        g.circle(xr, PY(b), 5.5 if me else 4, c)
        g.txt(xl - 14, PY(a) + 4, "%s  %.1f" % (nm, a), "l", "end",
              fill=INK if me else INK3, weight=800 if me else 600, size=13 if me else 12)
        g.txt(xr + 14, PY(b) + 4, "%.1f  %s" % (b, nm), "l",
              fill=INK if me else INK3, weight=800 if me else 600, size=13 if me else 12)
    g.txt(760 + 120, PY(15.0) + 4, "두 계단 상승", "f", fill="var(--c-teal)", weight=800, size=13)
    return g.done()


def smallmult():
    segs = [("급식", [7.2, 7.0, 6.9, 6.8, 6.9, 6.8], False),
            ("유통(오프)", [12.8, 13.1, 13.3, 13.6, 13.5, 13.6], False),
            ("온라인", [1.2, 0.4, -0.2, -0.9, -1.4, -1.6], True),
            ("가공", [12.1, 12.5, 12.8, 13.0, 13.2, 13.3], False)]
    g = G(1080, 320, "네 사업부 분기 이익률 소형 다중 격자")
    pw, ph, gap, mt = 232, 190, 24, 64
    for i, (nm, vs, bad) in enumerate(segs):
        x0 = 40 + i * (pw + gap)
        g.rect(x0, mt, pw, ph, "var(--panel)", 4)
        g.txt(x0 + 12, mt - 12, nm, "l", fill="var(--c-clay)" if bad else INK, weight=800, size=13.5)
        lo, hi = -3, 15
        zero = sc(0, lo, hi, mt + ph - 12, mt + 12)
        g.line(x0 + 10, zero, x0 + pw - 10, zero, "var(--rule-soft)", 1)
        pts = [(x0 + 14 + (pw - 28) * j / 5, sc(v, lo, hi, mt + ph - 12, mt + 12))
               for j, v in enumerate(vs)]
        g.poly(pts, CLAY if bad else NAVY, 2.6)
        g.circle(*pts[-1], 4.5, CLAY if bad else NAVY)
        # 마지막 패널은 오른쪽에 자리가 없다. 라벨을 점 왼쪽으로 붙인다.
        anchor = "end" if i == len(segs) - 1 else "middle"
        lx = pts[-1][0] - (10 if anchor == "end" else 4)
        g.txt(lx, pts[-1][1] + (20 if bad else -10), "%.1f%%" % vs[-1], "f", anchor,
              fill="var(--c-clay)" if bad else INK2, size=12, weight=700)
    g.txt(40, mt + ph + 34, "같은 축(−3~15%), 같은 기간(6분기)입니다. 축을 패널마다 다르게 잡으면 이 형식은 거짓말이 됩니다.", "ls")
    return g.done()


def box():
    rows = [("2021", 7.1, 9.8, 12.9, 15.2, 17.4, 10.2), ("2022", 7.6, 10.2, 13.4, 15.6, 17.9, 11.4),
            ("2023", 8.2, 10.9, 13.8, 16.0, 18.0, 12.6), ("2024", 8.8, 11.3, 14.4, 16.2, 18.1, 13.9),
            ("2025", 9.4, 11.8, 15.0, 16.4, 18.2, 15.0)]
    g = G(1080, 360, "동종 12사 마진 분포 상자수염과 자사 위치")
    ml, mr, mt, mb = 150, 130, 40, 40
    def PX(v): return sc(v, 6, 20, ml, 1080 - mr)
    band = (360 - mt - mb) / 5
    for i, (yr, mn, q1, med, q3, mx, self_) in enumerate(rows):
        y = mt + band * i + band / 2
        g.line(PX(mn), y, PX(mx), y, "var(--rule)", 1.4)
        for v in (mn, mx):
            g.line(PX(v), y - 7, PX(v), y + 7, "var(--rule)", 1.4)
        g.rect(PX(q1), y - 11, PX(q3) - PX(q1), 22, SLATE, 3, o=.35)
        g.line(PX(med), y - 11, PX(med), y + 11, NAVY, 2.6)
        g.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z"
               % (PX(self_), y - 10, PX(self_) + 9, y, PX(self_), y + 10, PX(self_) - 9, y), OCHRE)
        g.txt(ml - 16, y + 4, yr, "l", "end", fill=INK, weight=650)
        g.txt(1080 - mr + 14, y + 4, "%.1f%%" % self_, "f", fill="var(--c-ochre)", weight=800, size=12.5)
    g.txt(ml, 360 - 12, "상자 = 1~3분위 · 세로선 = 중앙값 · 마름모 = 자사 · 2021년 1분위 밖에서 2025년 중앙값까지", "ls")
    return g.done()


def dumbbell():
    rows = [("가공", 13.3, 10.4), ("유통(오프)", 13.6, 11.9), ("급식", 6.8, 8.9), ("온라인", -1.6, 3.9)]
    g = G(1080, 320, "사업부 이익률과 동종 중앙값의 격차 덤벨")
    ml, mr, mt, mb = 190, 190, 44, 44
    def PX(v): return sc(v, -4, 16, ml, 1080 - mr)
    g.line(PX(0), mt - 8, PX(0), 320 - mb, "var(--rule-soft)", 1, "4 4")
    band = (320 - mt - mb) / 4
    for i, (nm, a, b) in enumerate(rows):
        y = mt + band * i + band / 2
        up = a >= b
        c = TEAL if up else CLAY
        g.line(PX(min(a, b)), y, PX(max(a, b)), y, c, 5, o=.85)
        g.circle(PX(b), y, 7, SLATE)
        g.circle(PX(a), y, 8.5, NAVY if up else CLAY)
        g.txt(ml - 16, y + 4, nm, "l", "end", fill=INK, weight=700, size=13)
        g.txt(1080 - mr + 14, y + 4, "%+.1f%%p" % (a - b), "f",
              fill="var(--c-teal)" if up else "var(--c-clay)", weight=800, size=13)
    g.txt(ml, 320 - 14, "진한 점 = 자사 · 회색 점 = 동종 중앙값 · 전사 평균 하나로는 네 사실이 다 지워집니다", "ls")
    return g.done()


# ================================================================ 고객 · 실행
def whale():
    profits = [5.2, 4.6, 3.9, 3.4, 3.1, 2.8, 2.6, 2.4,
               -0.1, -0.1, -0.2, -0.2, -0.3, -0.3, -0.3, -0.4, -0.4, -0.4,
               -0.5, -0.5, -0.5, -0.6, -0.6, -0.7]
    tot = sum(profits)
    g = G(1080, 380, "거래처별 누적 이익 고래 곡선")
    ml, mr, mt, mb = 80, 220, 36, 50
    n = len(profits)
    cum, pts, peak = 0.0, [], (0, 0.0)
    for i, p in enumerate(profits):
        cum += p
        pct = cum / tot * 100
        pts.append((sc(i + 1, 0, n, ml, 1080 - mr), pct))
        if pct > peak[1]:
            peak = (i + 1, pct)
    def PY(v): return sc(v, 0, 140, 380 - mb, mt)
    for v in (50, 100):
        g.line(ml, PY(v), 1080 - mr, PY(v), "var(--grid)" if v != 100 else "var(--rule)", 1,
               None if v != 100 else "5 4")
        g.txt(ml - 8, PY(v) + 4, "%d%%" % v, "f", "end", fill=INK3, size=11)
    g.area([(ml, PY(0))] + [(x, PY(y)) for x, y in pts] + [(pts[-1][0], PY(0))], TEAL, .12)
    g.poly([(x, PY(y)) for x, y in pts], NAVY, 3)
    px_, py_ = pts[peak[0] - 1][0], PY(peak[1])
    g.circle(px_, py_, 6, OCHRE)
    g.txt(px_ + 14, py_ + 24, "상위 %d곳에서 이익의 %d%%" % (peak[0], round(peak[1])), "f",
          fill="var(--c-ochre)", weight=800, size=13.5)
    g.txt(pts[-1][0] + 12, PY(100) + 4, "전체 24곳 = 100%", "l", fill=INK2, weight=650, size=12.5)
    # 오른쪽 끝에 두면 이 문장이 viewBox 밖으로 나가 잘린다. 빈 왼쪽 위로 올린다
    g.txt(ml + 6, mt + 10, "꼬리 16곳이 이익 28%를 도로 깎습니다", "ls")
    g.txt(1080 - mr, 380 - mb + 24, "거래처, 이익 큰 순 →", "lb", "end", fill=INK, weight=700)
    g.line(ml, PY(0), 1080 - mr, PY(0), "var(--rule)", 1)
    return g.done()


def synergy():
    q = ["1Q", "2Q", "3Q", "4Q", "5Q", "6Q", "7Q", "8Q"]
    plan = [0.5, 1.5, 3.0, 4.9, 6.8, 8.2, 9.0, 9.3]
    act = [0.4, 1.1, 2.1]
    g = G(1080, 360, "개선 이익 실현 곡선: 계획 대 실제")
    ml, mr, mt, mb = 80, 230, 40, 46
    def PX(i): return sc(i, 0, 7, ml, 1080 - mr)
    def PY(v): return sc(v, 0, 10.5, 360 - mb, mt)
    for v in (3, 6, 9):
        g.line(ml, PY(v), 1080 - mr, PY(v), "var(--grid)", 1)
        g.txt(ml - 8, PY(v) + 4, fmt(v), "f", "end", fill=INK3, size=11)
    g.poly([(PX(i), PY(v)) for i, v in enumerate(plan)], SLATE, 2.4, dash="7 5")
    g.txt(PX(7) + 12, PY(plan[-1]) + 4, "계획 9.3억", "l", fill=INK2, weight=700, size=12.5)
    g.poly([(PX(i), PY(v)) for i, v in enumerate(act)], NAVY, 3.4)
    g.circle(PX(2), PY(act[-1]), 6, NAVY)
    g.txt(PX(2) + 12, PY(act[-1]) - 10, "실제 2.1억 · 계획의 70%", "f", fill=INK, weight=800, size=13)
    g.line(PX(2), PY(act[-1]), PX(2), PY(plan[2]), CLAY, 1.6, "3 3")
    g.txt(PX(2) + 12, (PY(act[-1]) + PY(plan[2])) / 2 + 12, "지연은 전부 온라인 물류 통합", "ls")
    for i in (0, 2, 4, 7):
        g.txt(PX(i), 360 - mb + 20, q[i], "ls", "middle")
    g.line(ml, 360 - mb, 1080 - mr, 360 - mb, "var(--rule)", 1)
    return g.done()


def bowling():
    rows = [("외주 단가 재협상", ["done", "done", "on", "", "", ""]),
            ("S&OP 주간 사이클", ["done", "on", "on", "", "", ""]),
            ("SKU 하위 20% 정리", ["", "on", "risk", "", "", ""]),
            ("안전재고 재계약", ["", "", "on", "plan", "", ""]),
            ("3공장 증설 검토", ["", "on", "on", "plan", "plan", ""]),
            ("온라인 가격 재설계", ["done", "on", "", "", "", ""]),
            ("물류 3PL 통합", ["", "risk", "off", "plan", "", ""]),
            ("가공 캐파 재배정", ["", "", "on", "plan", "plan", ""])]
    q = ["25.4Q", "26.1Q", "26.2Q", "26.3Q", "26.4Q", "27.1Q"]
    style = {"done": (TEAL, "완료"), "on": (NAVY, "정상"), "risk": (OCHRE, "주의"),
             "off": (CLAY, "이탈"), "plan": (SLATE, "예정")}
    g = G(1080, 420, "과제별 분기 진행 상태 볼링 차트")
    left, ctop, cw, ch = 260, 66, 118, 38
    lx = left
    for k in ("done", "on", "risk", "off", "plan"):
        c, nm = style[k]
        g.circle(lx + 6, 30, 7, c, sw=0)
        g.txt(lx + 20, 34, nm, "l", fill=INK2, size=12, weight=650)
        lx += 96
    for j, name in enumerate(q):
        g.txt(left + cw * j + cw / 2, ctop - 10, name, "ls", "middle")
    for i, (task, cells) in enumerate(rows):
        y = ctop + ch * i
        off = any(c == "off" for c in cells)
        g.txt(left - 16, y + ch / 2 + 4, task, "l", "end",
              fill="var(--c-clay)" if off else INK, weight=750 if off else 600, size=12.5)
        for j, cell in enumerate(cells):
            if not cell:
                continue
            c, _ = style[cell]
            g.circle(left + cw * j + cw / 2, y + ch / 2, 10, c,
                     stroke="var(--c-clay)" if cell == "off" else None, sw=2)
        if i:
            g.line(left - 200, y, 1020, y, "var(--rule-soft)", 1)
    g.txt(left - 216, ctop + ch * 8 + 26,
          "여덟 과제 중 물류 3PL 통합이 이탈, SKU 정리가 주의입니다. 지연의 손익 영향은 실현 곡선에서 잽니다.", "ls")
    return g.done()


def fan():
    x = ["2023", "2024", "2025", "2026E", "2027E", "2028E"]
    p50 = [259, 287, 320, 352, 381, 406]
    b_out = ([259, 287, 320, 331, 344, 352], [259, 287, 320, 374, 422, 468])
    b_in = ([259, 287, 320, 343, 364, 381], [259, 287, 320, 363, 400, 433])
    g = G(1080, 380, "매출 전망 부채꼴")
    ml, mr, mt, mb = 80, 200, 40, 44
    lo, hi = 240, 500
    xs = [sc(i, 0, 5, ml, 1080 - mr) for i in range(6)]
    def PY(v): return sc(v, lo, hi, 380 - mb, mt)
    for (lo_b, hi_b), c, o in ((b_out, SLATE, .18), (b_in, SLATE, .3)):
        g.area([(xs[i], PY(hi_b[i])) for i in range(6)] +
               [(xs[i], PY(lo_b[i])) for i in range(5, -1, -1)], c, o)
    g.poly([(xs[i], PY(p50[i])) for i in range(6)], NAVY, 3.2)
    g.circle(xs[-1], PY(p50[-1]), 5.5, NAVY)
    g.line(xs[2], mt, xs[2], 380 - mb, "var(--ink-3)", 1, "4 4")
    g.txt(xs[2] + 8, mt + 14, "실적 | 전망", "ls")
    for v, lab, cls in ((468, "낙관 468", "vl mute"), (406, "중심 406억", "vl"),
                        (352, "보수 352", "vl mute")):
        g.txt(xs[-1] + 14, PY(v) + 4, lab, "f", size=13 if v == 406 else 11.5,
              weight=800 if v == 406 else 600, fill=INK if v == 406 else INK3)
    for i in range(6):
        g.txt(xs[i], 380 - mb + 20, x[i], "ls", "middle")
    g.line(ml, 380 - mb, 1080 - mr, 380 - mb, "var(--rule)", 1)
    g.txt(1080 - mr + 14, mt + 12, "실적 구간에는 띠가 없습니다", "ls")
    return g.done()


def tornado():
    base = 381
    rows = [("WACC ±1.0%p", 319, 456), ("EBITDA 마진 ±1.0%p", 344, 418),
            ("영구성장률 ±0.5%p", 356, 412), ("매출 성장률 ±2.0%p", 361, 403),
            ("운전자본 ±10일", 370, 393), ("설비투자 ±20%", 374, 388)]
    g = G(1080, 340, "가정별 일변량 토네이도")
    ml, mr, mt, mb = 300, 100, 30, 40
    lo, hi = 300, 475
    def PX(v): return sc(v, lo, hi, ml, 1080 - mr)
    cx = PX(base)
    g.line(cx, mt - 6, cx, 340 - mb + 6, "var(--ink)", 1.5)
    g.txt(cx, 340 - mb + 24, "기준 EV 381억", "f", "middle", weight=800, size=12.5)
    band = (340 - mt - mb) / len(rows)
    for i, (lab, a, b) in enumerate(rows):
        y = mt + band * i + band / 2
        g.rect(PX(a), y - 10, cx - PX(a), 20, SLATE, 2, o=.45)
        g.rect(cx, y - 10, PX(b) - cx, 20, NAVY, 2, o=.85)
        g.txt(ml - 16, y + 4, lab, "l", "end", fill=INK, weight=650, size=12.5)
        g.txt(PX(a) - 8, y + 4, fmt(a), "f", "end", fill=INK3, size=11.5)
        g.txt(PX(b) + 8, y + 4, fmt(b), "f", "start", fill=INK2, size=11.5, weight=700)
    return g.done()


def montecarlo():
    bins = [3, 7, 14, 26, 42, 63, 85, 102, 110, 105, 92, 74, 56, 40, 27, 17, 10, 6, 3, 2]
    x0, x1 = 260.0, 520.0
    g = G(1080, 360, "시뮬레이션 1만 회의 가치 분포와 누적확률")
    ml, mr, mt, mb = 60, 60, 44, 40
    n, tot, mx = len(bins), float(sum(bins)), max(bins)
    bw = (1080 - ml - mr) / n
    def PX(v): return sc(v, x0, x1, ml, 1080 - mr)
    for i, c in enumerate(bins):
        h = (360 - mt - mb) * c / mx
        g.rect(ml + bw * i + 1.5, 360 - mb - h, bw - 3, h, SLATE, 2, o=.4)
    cum, pts = 0.0, []
    for i, c in enumerate(bins):
        cum += c
        pts.append((ml + bw * (i + 1), mt + (360 - mt - mb) * (1 - cum / tot)))
    g.poly(pts, OCHRE, 2.6)
    for v, lab, strong in ((318, "P10  318", 0), (381, "P50  381억", 1), (452, "P90  452", 0)):
        g.line(PX(v), mt - 8, PX(v), 360 - mb, INK if strong else INK3,
               2 if strong else 1, None if strong else "5 4")
        g.txt(PX(v), mt - 14, lab, "f", "middle", weight=800 if strong else 600,
              size=12.5 if strong else 11.5, fill=INK if strong else INK3)
    g.line(ml, 360 - mb, 1080 - mr, 360 - mb, "var(--rule)", 1)
    g.txt(ml, 360 - mb + 20, fmt(x0) + "억", "f", fill=INK3, size=11)
    g.txt(1080 - mr, 360 - mb + 20, fmt(x1) + "억", "f", "end", fill=INK3, size=11)
    return g.done()


def cohort_pareto():
    import exhibits
    return exhibits.ex07()


ALL = {}
