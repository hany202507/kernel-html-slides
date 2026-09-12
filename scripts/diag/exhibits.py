# -*- coding: utf-8 -*-
"""Project Seorin 전시물 9종. 각 함수가 SVG 문자열 하나를 돌려준다."""
import data as D
from draw import G, sc, fmt

NAVY, OCHRE, TEAL, CLAY = "var(--c-navy)", "var(--c-ochre)", "var(--c-teal)", "var(--c-clay)"
SLATE, SAND = "var(--c-slate)", "var(--c-sand)"
INK2, INK3 = "var(--ink-2)", "var(--ink-3)"


# ================================================================ EX01
def ex01():
    g = G(1080, 400, "5개년 매출 막대와 영업이익률 선, CAGR 괄호와 증감 칩")
    top, bot, ml = 66, 300, 70
    step = (1030 - ml) / 5
    bw = 104

    for v in (100, 200, 300):
        y = sc(v, 0, 340, bot, top)
        g.line(ml, y, 1030, y, "var(--grid)", 1)
        g.txt(ml - 10, y + 4, fmt(v), "f", "end", fill=INK3, size=11.5)
    g.line(ml, bot, 1030, bot, "var(--rule)", 1)

    centers = []
    for i, (yr, rv, m) in enumerate(zip(D.YEARS, D.REV, D.OPM)):
        cx = ml + step * i + step / 2
        centers.append(cx)
        y = sc(rv, 0, 340, bot, top)
        g.rect(cx - bw / 2, y, bw, bot - y, NAVY, 2, o=.92 if yr == "2025" else .62)
        g.txt(cx, y - 10, fmt(rv), "f", "middle", fill="var(--ink)", size=14, weight=700)
        g.txt(cx, bot + 22, yr, "l", "middle", fill=INK2, weight=600)
        if i:
            yoy = (rv / D.REV[i - 1] - 1) * 100
            g.chip(cx, bot + 46, yoy, 1, "%")

    # 영업이익률 선 (0~12% 를 같은 캔버스에)
    pts = [(centers[i], sc(D.OPM[i], 0, 12, bot, top)) for i in range(5)]
    g.poly(pts, OCHRE, 3)
    for i, p in enumerate(pts):
        g.circle(*p, 4.5, OCHRE)
        if i in (0, 4):
            g.txt(p[0] + (14 if i else -14), p[1] + 4, "%.1f%%" % D.OPM[i], "f",
                  "start" if i else "end", fill="var(--c-ochre)", weight=700, size=13)
    g.txt(pts[2][0], pts[2][1] - 14, "영업이익률", "ls", "middle", fill="var(--c-ochre)", weight=700)

    g.bracket(centers[0], centers[4], 34, "매출 CAGR +8.5%  ·  영업이익률 +3.5%p", up=True)
    g.marker(centers[3], sc(D.REV[3], 0, 340, bot, top) - 30, 1)
    return g.done()


# ================================================================ EX02
def ex02():
    g = G(1080, 440, "2024년과 2025년의 EBITDA에서 잉여현금까지 폭포 두 개 비교")
    panels = [("2024", 40), ("2025", 570)]
    top, bot = 84, 350
    MX = 52.0

    def py(v):
        return sc(v, 0, MX, bot, top)

    fcf_x = {}
    for yr, x0 in panels:
        g.txt(x0, 44, "%s년  ·  EBITDA %d억" % (yr, dict(D.FCF_WALK[yr])["EBITDA"]),
              "t", fill="var(--ink)")
        walk = D.FCF_WALK[yr]
        n = len(walk) + 1
        stepw = 470 / n
        run = 0.0
        for i, (lab, v) in enumerate(walk):
            cx = x0 + stepw * i + stepw / 2
            if i == 0:
                g.rect(cx - 34, py(v), 68, bot - py(v), NAVY, 2)
                run = v
                g.txt(cx, py(v) - 9, fmt(v), "f", "middle", weight=700, size=13.5)
            else:
                y1, y0 = py(run), py(run + v)
                g.rect(cx - 30, min(y0, y1), 60, abs(y0 - y1), CLAY, 2, o=.85)
                g.txt(cx, min(y0, y1) - 8, fmt(v), "f", "middle",
                      fill="var(--c-clay)", weight=700, size=12.5)
                run += v
            g.line(cx + (34 if i == 0 else 30), py(run),
                   cx + stepw - 30, py(run), INK3, 1, "3 3", .7)
            g.txt(cx, bot + 20, lab.replace("운전자본 증가", "운전자본").replace("설비투자", "설비"),
                  "ls", "middle")
        cx = x0 + stepw * n - stepw / 2
        g.rect(cx - 34, py(run), 68, bot - py(run), TEAL, 2)
        g.txt(cx, py(run) - 9, fmt(run), "f", "middle", fill="var(--c-teal)", weight=800, size=14)
        g.txt(cx, bot + 20, "잉여현금", "ls", "middle")
        g.rect(cx - 46, bot + 34, 92, 24, "var(--plot)", 12, stroke="var(--rule)", sw=1)
        g.txt(cx, bot + 50, "전환율 %d%%" % D.CONV[yr], "f", "middle", fill=INK2, weight=700, size=12)
        fcf_x[yr] = (cx, py(run))
        g.line(x0, bot, x0 + 470, bot, "var(--rule)", 1)

    x1, y1 = fcf_x["2024"]
    x2, y2 = fcf_x["2025"]
    g.note(806, 96, ["EBITDA는 7억 늘었는데", "잉여현금은 그대로 14억입니다  ②"], 232)
    g.connector(x1 + 30, y1 - 12, 806, 150)
    g.connector(x2 - 6, y2 - 12, 920, 152)
    return g.done()


# ================================================================ EX03
def ex03():
    g = G(1080, 580, "현금전환주기 3면: 자금이 묶이는 시간축, 6분기 추이, 동종 분포")
    # ---------- A. 타임라인
    g.txt(30, 30, "A. 자금이 묶이는 구간, 일", "t")
    ax0, ax1 = 200, 940

    def dx(d):
        return sc(d, 0, 115, ax0, ax1)

    for d in (0, 30, 60, 90):
        g.line(dx(d), 48, dx(d), 218, "var(--grid)", 1)
        g.txt(dx(d), 44, "%d일" % d, "ls", "middle")
    rows = [
        ("재고 (DIO)", 0, D.CCC["dio"], NAVY, "%d억 묶임" % round(D.CCC["dio"] * D.COGS_PER_DAY)),
        ("매출채권 (DSO)", D.CCC["dio"], D.CCC["dso"], TEAL, "%d억 묶임" % round(D.CCC["dso"] * D.REV_PER_DAY)),
        ("매입채무 (DPO)", 0, D.CCC["dpo"], OCHRE, "%d억 조달" % round(D.CCC["dpo"] * D.COGS_PER_DAY)),
        ("현금 회전일", D.CCC["dpo"], D.CCC_VAL, "var(--ink)", "순 46억"),
    ]
    for i, (lab, start, ln, c, cash) in enumerate(rows):
        y = 62 + i * 40
        hollow = i == 2
        if hollow:
            g.rect(dx(start), y, dx(start + ln) - dx(start), 26, "var(--plot)", 2,
                   stroke="var(--c-ochre)", sw=1.5, dash="5 3")
            g.txt(dx(start + ln / 2), y + 17, "%d일" % ln, "f", "middle",
                  fill="var(--c-ochre)", weight=700)
        else:
            g.rect(dx(start), y, dx(start + ln) - dx(start), 26, c, 2, o=.9)
            g.txt(dx(start + ln / 2), y + 17, "%d일" % ln, "fw", "middle")
        g.txt(ax0 - 14, y + 17, lab, "l", "end", fill="var(--ink)", weight=600)
        g.txt(ax1 + 14, y + 17, cash, "f", "start", fill=INK2, weight=600)
    g.marker(dx(D.CCC["dpo"] + D.CCC_VAL / 2), 62 + 3 * 40 - 12, 1)

    # ---------- B. 추이
    g.txt(30, 268, "B. 6분기 추이, 일", "t")
    bt, bb, bl, br = 288, 420, 200, 620
    W = D.WC_TREND
    lo, hi = 34, 74
    xs = [sc(i, 0, 5, bl, br) for i in range(6)]
    for d in (40, 55, 70):
        y = sc(d, lo, hi, bb, bt)
        g.line(bl, y, br, y, "var(--grid)", 1)
        g.txt(bl - 8, y + 4, str(d), "f", "end", fill=INK3, size=11)
    for key, c, lab in (("dio", NAVY, "재고"), ("dpo", OCHRE, "매입채무"), ("dso", TEAL, "매출채권")):
        pts = [(xs[i], sc(W[key][i], lo, hi, bb, bt)) for i in range(6)]
        g.poly(pts, c, 2.5)
        g.circle(*pts[-1], 4, c)
        g.txt(br + 10, pts[-1][1] + 4, "%s %d일" % (lab, W[key][-1]), "l", fill=c, weight=700, size=12)
    for i in (0, 5):
        g.txt(xs[i], bb + 18, W["x"][i], "ls", "middle")
    g.marker(xs[4], sc(W["dio"][4], lo, hi, bb, bt) - 16, 2)

    # ---------- C. 동종 분포
    g.txt(700, 268, "C. 동종 12사 분포, 일", "t")
    cl, cr, cy = 726, 1030, 350
    q = D.PEER_CCC_Q
    g.band_h(sc(q["q1"], 25, 75, cl, cr), sc(q["q3"], 25, 75, cl, cr), cy - 22, cy + 22, SLATE, .18)
    g.line(sc(q["med"], 25, 75, cl, cr), cy - 26, sc(q["med"], 25, 75, cl, cr), cy + 26, NAVY, 2)
    g.line(cl, cy, cr, cy, "var(--rule)", 1)
    for d in D.PEER_CCC:
        g.circle(sc(d, 25, 75, cl, cr), cy, 4.5, SLATE)
    sx = sc(D.CCC_VAL, 25, 75, cl, cr)
    g.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z"
           % (sx, cy - 11, sx + 9, cy, sx, cy + 11, sx - 9, cy), OCHRE)
    g.txt(sx, cy - 20, "자사 57일", "f", "middle", fill="var(--c-ochre)", weight=800, size=12.5)
    g.txt(sc(q["med"], 25, 75, cl, cr), cy + 42, "중앙값 %.0f일" % q["med"], "ls", "middle")
    g.txt(cl, cy + 42, "28", "f", "start", fill=INK3, size=11)
    g.txt(cr, cy + 42, "71", "f", "end", fill=INK3, size=11)
    g.marker(sx, cy + 62, 3)
    g.txt(700, 452, "동종보다 11.5일 깁니다. 그 차이가 곧", "l", fill=INK2, size=12.5)
    g.txt(700, 470, "묶인 현금 약 8억원입니다.", "l", fill=INK2, size=12.5)

    # ---------- 하단 결론 스트립
    g.line(30, 510, 1050, 510, "var(--rule)", 1)
    g.txt(30, 540, "운전자본 순투자", "ls")
    g.txt(30, 560, "46억", "f", fill="var(--ink)", size=17, weight=800)
    g.txt(300, 540, "원인 지목", "ls")
    g.txt(300, 560, "재고 55 → 68일", "f", fill="var(--c-navy)", size=17, weight=800)
    g.txt(620, 540, "동종 대비", "ls")
    g.txt(620, 560, "+11.5일 (10위/12사)", "f", fill="var(--c-clay)", size=17, weight=800)
    return g.done()


# ================================================================ EX04
def ex04():
    g = G(1080, 440, "재고 43억을 카테고리와 연령으로 나눈 매트릭스와 행 합계 막대")
    left, ctop = 190, 70
    cw, ch = 158, 54
    g.txt(30, 34, "억원  ·  진할수록 크다  ·  붉은 테두리는 61일 이상 과다 구간", "ls")
    for j, c in enumerate(D.INV_COLS):
        g.txt(left + cw * j + cw / 2, ctop - 12, c, "l", "middle", fill=INK3, weight=600)
    mx = max(max(r) for r in D.INV)
    for i, (name, row) in enumerate(zip(D.INV_ROWS, D.INV)):
        y = ctop + ch * i
        g.txt(left - 14, y + ch / 2 + 5, name, "l", "end", fill="var(--ink)", weight=600)
        for j, v in enumerate(row):
            x = left + cw * j
            o = .06 + .84 * (v / mx) ** .7
            g.rect(x + 2, y + 2, cw - 4, ch - 4, NAVY, 3, o=o)
            g.txt(x + cw / 2, y + ch / 2 + 5, "%.1f" % v, "f", "middle",
                  fill="#fff" if o > .5 else "var(--ink)", weight=700, size=13)
        # 행 합계 막대
        tot = sum(row)
        bx = left + cw * 4 + 26
        g.rect(bx, y + ch / 2 - 9, sc(tot, 0, 15, 0, 170), 18, SLATE, 2, o=.75)
        g.txt(bx + sc(tot, 0, 15, 0, 170) + 8, y + ch / 2 + 5, fmt(tot, 1), "f",
              fill=INK2, weight=700, size=12.5)
    # 61일 이상 과다 칸
    g.rect(left + cw * 2 + 2, ctop + ch * 3 + 2, cw * 2 - 4, ch - 4, "none", 3,
           stroke="var(--c-clay)", sw=2)
    g.marker(left + cw * 3, ctop + ch * 3 - 10, 1)
    yb = ctop + ch * 5 + 16
    for j in range(4):
        colsum = sum(D.INV[i][j] for i in range(5))
        g.txt(left + cw * j + cw / 2, yb + 6, fmt(colsum, 1), "f", "middle", fill=INK2, weight=700)
    g.txt(left - 14, yb + 6, "연령 합계", "ls", "end")
    g.line(30, yb + 26, 1050, yb + 26, "var(--rule)", 1)
    g.txt(30, yb + 56, "61일 초과", "ls")
    g.txt(30, yb + 78, "8.0억 (19%)", "f", fill="var(--c-clay)", size=17, weight=800)
    g.txt(300, yb + 56, "그중 유통 완제품", "ls")
    g.txt(300, yb + 78, "3.0억  ·  회전 없는 SKU 41개", "f", fill="var(--ink)", size=17, weight=800)
    g.txt(700, yb + 56, "12일 단축 시 풀리는 현금", "ls")
    g.txt(700, yb + 78, "7.6억 (일회성)", "f", fill="var(--c-teal)", size=17, weight=800)
    return g.done()


# ================================================================ EX05
def ex05():
    g = G(1080, 470, "사업부 이익 풀: 폭이 매출, 높이가 이익률, 면적이 이익. 오른쪽은 ROIC와 WACC 격차")
    # ---------- 좌: profit pool
    g.txt(30, 34, "A. 이익 풀  ·  폭 = 매출, 높이 = 영업이익률, 면적 = 영업이익", "t")
    pl, pr, ptop, pbot = 70, 620, 70, 400
    zero = sc(0, -4, 16, pbot, ptop)
    tot = sum(s[1] for s in D.SEGMENTS)
    for m in (5, 10, 15):
        y = sc(m, -4, 16, pbot, ptop)
        g.line(pl, y, pr, y, "var(--grid)", 1)
        g.txt(pl - 8, y + 4, "%d%%" % m, "f", "end", fill=INK3, size=11)
    g.line(pl, zero, pr, zero, "var(--rule)", 1.2)
    x = pl
    colors = [NAVY, TEAL, CLAY, OCHRE]
    for (name, rv, opm, _), c in zip(D.SEGMENTS, colors):
        w = (pr - pl) * rv / tot
        y = sc(opm, -4, 16, pbot, ptop)
        if opm >= 0:
            g.rect(x + 1.5, y, w - 3, zero - y, c, 0, o=.88)
        else:
            g.rect(x + 1.5, zero, w - 3, y - zero, c, 0, o=.88)
        op = rv * opm / 100
        ly = y - 26 if opm >= 0 else y + 34
        g.txt(x + w / 2, ly, name, "l", "middle", fill="var(--ink)", weight=700, size=12.5)
        g.txt(x + w / 2, ly + 16, "%.1f%%  ·  %s억" % (opm, fmt(op, 1)), "f", "middle",
              fill=INK2, size=11.5)
        g.txt(x + w / 2, zero + (16 if opm >= 0 else -8), "%d억" % rv, "ls", "middle")
        x += w
    g.marker(pl + (pr - pl) * (148 + 84 + 14) / tot, zero + 38, 1)

    # ---------- 우: ROIC vs WACC
    g.txt(700, 34, "B. ROIC 대 자본비용", "t")
    rl, rr = 826, 1030
    rows_y = [90, 160, 230, 300]

    def rx(v):
        return sc(v, 0, 20, rl, rr)

    g.refline_v(rx(D.WACC), 66, 330, "WACC %.1f%%" % D.WACC, SLATE, "4 3", label_y=352)
    for (name, _, _, roic), y in zip(D.SEGMENTS, rows_y):
        good = roic >= D.WACC
        c = TEAL if good else CLAY
        g.line(rx(D.WACC), y, rx(roic), y, c, 5)
        g.circle(rx(roic), y, 7, c)
        g.txt(rl - 106, y + 4, name, "l", "end", fill="var(--ink)", weight=600, size=12)
        g.txt(rx(roic) + (12 if good else -12), y + 4, "%.1f%%" % roic, "f",
              "start" if good else "end", fill=c, weight=800, size=12.5)
    g.marker(rx(3.1) - 62, rows_y[2], 2)
    g.txt(700, 400, "온라인만 자본비용을 밑돕니다. 매출 28억이", "l", fill=INK2, size=12.5)
    g.txt(700, 418, "굴러갈수록 기업가치를 깎는 구간입니다.", "l", fill=INK2, size=12.5)
    return g.done()


# ================================================================ EX06
def ex06():
    g = G(1080, 450, "공장별 원가 곡선: 가로 누적 물량, 세로 단가, 판가선과 재협상 시나리오")
    pl, pr, ptop, pbot = 90, 1030, 40, 300
    tot = sum(c[1] for c in D.COST_CURVE)
    MX = 2050

    def py(v):
        return sc(v, 0, MX, pbot, ptop)

    for v in (500, 1000, 1500, 2000):
        g.line(pl, py(v), pr, py(v), "var(--grid)", 1)
        g.txt(pl - 8, py(v) + 4, fmt(v), "f", "end", fill=INK3, size=11)
    x = pl
    for name, w, cost in D.COST_CURVE:
        bw = (pr - pl) * w / tot
        over = cost > D.PRICE
        g.rect(x + 1.5, py(cost), bw - 3, pbot - py(cost), CLAY if over else NAVY, 0,
               o=.85 if over else .8)
        dy = -8 if abs(cost - D.PRICE) > 130 else -22
        g.txt(x + bw / 2, py(cost) + dy, fmt(cost), "f", "middle", weight=700, size=13)
        g.txt(x + bw / 2, pbot + 18, name, "l", "middle", fill="var(--ink)", weight=600, size=12)
        g.txt(x + bw / 2, pbot + 34, "%d천 톤" % w, "ls", "middle")
        if name == "외주 위탁":
            g.rect(x + 1.5, py(D.RENEG), bw - 3, pbot - py(D.RENEG), "none", 0,
                   stroke="var(--c-teal)", sw=1.8, dash="6 4")
            g.txt(x + bw / 2, py(D.RENEG) + 30, "재협상 목표 %s" % fmt(D.RENEG), "fw", "middle")
        x += bw
    g.line(pl, py(D.PRICE), pr, py(D.PRICE), OCHRE, 2, "7 4")
    g.txt(pl + 8, py(D.PRICE) - 10, "평균 판가 %s원" % fmt(D.PRICE), "ls", "start",
          fill="var(--c-ochre)", weight=800)
    g.note(pl, pbot + 56,
           ["외주 26천 톤 × (1,880 − 1,620) = 연 6.8억 역마진  ①",
            "재협상 −190원 성사 시 연 4.9억 회복  ·  잔여는 3공장 증설로"], 470)
    g.txt(pl + 500, pbot + 78, "단위당 총원가는 고정비 배부 포함 기준입니다.", "ls", size=11.5)
    g.txt(pl + 500, pbot + 96, "변동비 기준으로는 외주도 판가를 밑돌지 않습니다.", "ls", size=11.5)
    return g.done()


# ================================================================ EX07
def ex07():
    g = G(1080, 470, "왼쪽 수주 코호트 유지율 삼각, 오른쪽 상위 거래처 집중도 파레토")
    # ---------- 좌: 코호트
    g.txt(30, 34, "A. 수주 코호트 유지율, 거래처 금액 기준 %", "t")
    left, ctop = 140, 64
    cw, ch = 66, 52
    for j, c in enumerate(D.COHORT_COLS):
        g.txt(left + cw * j + cw / 2, ctop - 8, c, "ls", "middle")
    for i, (name, vals) in enumerate(D.COHORTS):
        y = ctop + ch * i
        g.txt(left - 12, y + ch / 2 + 4, name, "l", "end", fill="var(--ink)", weight=600, size=12)
        for j, v in enumerate(vals):
            x = left + cw * j
            o = .08 + .8 * ((v - 72) / 28) ** 1.1
            g.rect(x + 2, y + 2, cw - 4, ch - 4, NAVY, 3, o=max(o, .08))
            g.txt(x + cw / 2, y + ch / 2 + 4, str(v), "f", "middle",
                  fill="#fff" if o > .5 else "var(--ink)", weight=700, size=12)
    # 2023 코호트 3년차
    g.rect(left + cw * 3 + 2, ctop + ch * 2 + 2, cw - 4, ch - 4, "none", 3,
           stroke="var(--c-clay)", sw=2)
    g.marker(left + cw * 4 + 18, ctop + ch * 2 + ch / 2, 1)

    # ---------- 우: 파레토
    g.txt(620, 34, "B. 거래처 집중도, 매출 320억 기준", "t")
    bl, br, btop, bbot = 640, 1030, 74, 330
    n = len(D.TOP_CUST)
    stepw = (br - bl) / (n + 1)
    total = sum(v for _, v in D.TOP_CUST) + D.OTHERS
    cum = 0
    pts = []
    for i, (name, v) in enumerate(D.TOP_CUST):
        cx = bl + stepw * i + stepw / 2
        h = sc(v, 0, 65, 0, bbot - btop)
        c = NAVY if i < 3 else SLATE
        g.rect(cx - stepw * .32, bbot - h, stepw * .64, h, c, 1, o=.9 if i < 3 else .55)
        g.txt(cx, bbot + 15, name, "ls", "middle")
        cum += v
        pts.append((cx, sc(cum / total * 100, 0, 100, bbot, btop)))
    cx = bl + stepw * n + stepw / 2
    h = sc(D.OTHERS, 0, 130, 0, bbot - btop)
    g.rect(cx - stepw * .32, bbot - h, stepw * .64, h, SAND, 1, o=.8)
    g.txt(cx, bbot + 15, "기타", "ls", "middle")
    pts.append((cx, sc(100, 0, 100, bbot, btop)))
    g.poly(pts, OCHRE, 2.5)
    for i in (2, len(pts) - 1):
        g.circle(*pts[i], 4.5, OCHRE)
    g.txt(pts[2][0] + 12, pts[2][1] - 16, "상위 3사 42%", "f", fill="var(--c-ochre)", weight=800, size=13)
    g.marker(pts[2][0] - 32, pts[2][1] - 16, 2)
    g.line(bl, bbot, br, bbot, "var(--rule)", 1)

    g.line(30, 366, 1050, 366, "var(--rule)", 1)
    g.txt(30, 394, "이상 신호", "ls")
    g.txt(30, 416, "2023년 수주만 3년차 80%", "f", fill="var(--c-clay)", size=16, weight=800)
    g.txt(430, 394, "확인 결과", "ls")
    g.txt(430, 416, "그해 대형 신규 2건이 저마진 조건  ·  이탈 12억의 출처", "f",
          fill="var(--ink)", size=16, weight=800)
    return g.done()


# ================================================================ EX08
def ex08():
    g = G(1080, 500, "축을 절단한 기업가치 브릿지와 실행 리스크 토네이도")
    g.txt(30, 30, "A. 세 가지 개입이 미는 기업가치, 억원  ·  EV/EBITDA 7.9배 유지  ·  축은 330에서 절단", "t")
    pl, pr, ptop, pbot = 60, 1030, 88, 258
    LO, HI = 330.0, 485.0

    def py(v):
        return sc(v, LO, HI, pbot, ptop)

    items = [("현재 EV", D.EV_BASE, "tot")] + [(n, e, "up") for n, _, e in D.PLAN] + \
            [("계획 EV", D.EV_PLAN, "tot")]
    stepw = (pr - pl) / len(items)
    run = 0.0
    centers = []
    for i, (lab, v, kind) in enumerate(items):
        cx = pl + stepw * i + stepw / 2
        centers.append(cx)
        if kind == "tot":
            g.rect(cx - 52, py(v), 104, pbot - py(v), "var(--ink)" if i else NAVY, 2)
            g.txt(cx, py(v) - 10, fmt(v), "f", "middle", weight=800, size=15)
            # 축 절단 표시
            g.line(cx - 58, pbot - 13, cx - 46, pbot - 19, "var(--plot)", 2.6)
            g.line(cx - 58, pbot - 9, cx - 46, pbot - 15, "var(--plot)", 2.6)
            g.line(cx + 46, pbot - 13, cx + 58, pbot - 19, "var(--plot)", 2.6)
            g.line(cx + 46, pbot - 9, cx + 58, pbot - 15, "var(--plot)", 2.6)
            run = v
        else:
            y1, y0 = py(run), py(run + v)
            g.rect(cx - 42, y0, 84, y1 - y0, TEAL, 2, o=.88)
            g.txt(cx, y0 - 8, "+" + fmt(v), "f", "middle", fill="var(--c-teal)", weight=700, size=13)
            run += v
        if i < len(items) - 1:
            g.line(cx + (52 if kind == "tot" else 42), py(run),
                   cx + stepw - (52 if items[i + 1][2] == "tot" else 42), py(run),
                   INK3, 1, "3 3", .7)
        g.txt(cx, pbot + 18, lab, "l", "middle", fill="var(--ink)", weight=600, size=12)
        if kind == "up":
            op = [p[1] for p in D.PLAN if p[0] == lab][0]
            g.txt(cx, pbot + 34, "영업이익 +%.1f억/년" % op, "ls", "middle")
    g.bracket(centers[0], centers[-1], 62, "+74억 (+19%)", up=True)
    g.line(pl, pbot, pr, pbot, "var(--rule)", 1)

    g.txt(30, 314, "B. 계획 455억이 흔들리는 폭  ·  실행 리스크 일변량", "t")
    tl, tr = 420, 1000
    base = D.EV_PLAN
    cx0 = sc(base, 380, 500, tl, tr)
    g.line(cx0, 330, cx0, 470, "var(--ink)", 1.4)
    g.txt(cx0, 486, "계획 %d" % base, "f", "middle", weight=700, size=12)
    for i, (lab, lo, hi) in enumerate(D.TORNADO):
        y = 344 + i * 32
        xl, xh = sc(lo, 380, 500, tl, tr), sc(hi, 380, 500, tl, tr)
        g.rect(min(xl, cx0), y - 9, abs(cx0 - xl), 18, CLAY, 1, o=.7)
        if hi > base:
            g.rect(cx0, y - 9, xh - cx0, 18, TEAL, 1, o=.7)
        g.txt(tl - 16, y + 4, lab, "l", "end", fill="var(--ink)", weight=600, size=12)
        g.txt(min(xl, xh) - 8, y + 4, fmt(lo), "f", "end", fill=INK3, size=11.5)
        if hi != base:
            g.txt(max(xl, xh) + 8, y + 4, fmt(hi), "f", "start", fill=INK3, size=11.5)
    g.marker(sc(416, 380, 500, tl, tr) - 52, 344, 1)
    return g.done()


# ================================================================ EX09
def ex09():
    g = G(1080, 560, "18개월 실행 로드맵과 3년 누적 잉여현금 전망 밴드")
    # ---------- A. 로드맵
    g.txt(30, 34, "A. 18개월 실행 순서", "t")
    ql = ["25.4Q", "26.1Q", "26.2Q", "26.3Q", "26.4Q", "27.1Q"]
    gl, gr, gtop = 250, 1030, 58
    qw = (gr - gl) / 6
    rowh = 26
    for j, q in enumerate(ql):
        g.txt(gl + qw * j + qw / 2, gtop - 4, q, "ls", "middle")
        g.line(gl + qw * j, gtop + 4, gl + qw * j, gtop + 8 * rowh + 10, "var(--grid)", 1)
    tcolor = {"재고": NAVY, "원가": TEAL, "온라인": OCHRE}
    seen = set()
    for i, (track, task, q0, ln) in enumerate(D.ROADMAP):
        y = gtop + 12 + i * rowh
        if track not in seen:
            seen.add(track)
            g.txt(38, y + 12, track, "l", fill=tcolor[track], weight=800, size=12.5)
        g.rect(gl + qw * q0 + 3, y, qw * ln - 6, 17, tcolor[track], 8, o=.8)
        g.txt(gl + qw * q0 + 12, y + 12.5, task, "fw", size=11)
    # ---------- B. FCF 팬
    g.txt(30, 330, "B. 누적 잉여현금, 억원", "t")
    fl, fr, ftop, fbot = 250, 950, 352, 512
    P = D.FCF_PATH
    xs = [sc(i, 0, 3, fl, fr) for i in range(4)]

    def fy(v):
        return sc(v, 0, 115, fbot, ftop)

    band = [(xs[i], fy(P["hi"][i])) for i in range(4)] + \
           [(xs[i], fy(P["lo"][i])) for i in range(3, -1, -1)]
    g.area(band, TEAL, .16)
    g.poly([(xs[i], fy(P["base"][i])) for i in range(4)], SLATE, 2, dash="6 4")
    g.poly([(xs[i], fy(P["p50"][i])) for i in range(4)], TEAL, 3)
    g.circle(xs[-1], fy(P["p50"][-1]), 5, TEAL)
    g.txt(xs[-1] + 12, fy(P["p50"][-1]) + 4, "계획 89억", "f", fill="var(--c-teal)", weight=800, size=13.5)
    g.txt(xs[-1] + 12, fy(P["base"][-1]) + 4, "현행 56억", "f", fill=INK3, weight=700, size=12.5)
    g.txt(xs[-1] + 12, fy(P["hi"][-1]) + 4, fmt(P["hi"][-1]), "f", fill=INK3, size=11)
    g.txt(xs[-1] + 12, fy(P["lo"][-1]) + 4, fmt(P["lo"][-1]), "f", fill=INK3, size=11)
    for i in range(4):
        g.txt(xs[i], fbot + 18, P["x"][i], "ls", "middle")
    g.line(fl, fbot, fr, fbot, "var(--rule)", 1)
    g.bracket(xs[-1] - 4, xs[-1] + 4, fy((P["p50"][-1] + P["base"][-1]) / 2), "", up=False) if False else None
    g.marker(xs[2], fy(P["p50"][2]) - 18, 1)
    return g.done()


ALL = {
    "01": ex01, "02": ex02, "03": ex03, "04": ex04, "05": ex05,
    "06": ex06, "07": ex07, "08": ex08, "09": ex09,
}
