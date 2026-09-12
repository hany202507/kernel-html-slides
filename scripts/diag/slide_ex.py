# -*- coding: utf-8 -*-
"""슬라이드 칸(1080 x 340 안팎)에 맞춰 다시 그린 전시물.

report 판(exhibits.py)은 세로로 긴 지면에 맞춰 그렸다. 그대로 슬라이드에 넣으면
viewBox 비율이 안 맞아 meet 로 축소되고, 넘치지도 않는데 글자만 작아진다.
여기 있는 것은 3.1:1 비율에 맞춘 슬라이드 전용 판이다.
"""
import data as D
from draw import G, sc, fmt

NAVY, OCHRE, TEAL, CLAY = "var(--c-navy)", "var(--c-ochre)", "var(--c-teal)", "var(--c-clay)"
SLATE = "var(--c-slate)"
INK, INK2, INK3 = "var(--ink)", "var(--ink-2)", "var(--ink-3)"

W, H = 1080, 340


# ================================================================ CCC 1/2
def ccc_timeline():
    """자금이 묶이는 구간. 뺄셈이 눈에 보이게 괄호로 묶는다."""
    g = G(W, H, "재고와 매출채권이 묶는 109일에서 매입채무 52일을 뺀 57일")
    ax0, ax1 = 250, 900
    top = 88

    def dx(d):
        return sc(d, 0, 115, ax0, ax1)

    for d in (0, 30, 60, 90):
        g.line(dx(d), top - 14, dx(d), top + 214, "var(--grid)", 1)
        g.txt(dx(d), top - 22, "%d일" % d, "ls", "middle")

    rows = [
        ("재고 (DIO)", 0, D.CCC["dio"], NAVY, "68일", "43억이 재고로"),
        ("매출채권 (DSO)", D.CCC["dio"], D.CCC["dso"], TEAL, "41일", "36억이 채권으로"),
        ("매입채무 (DPO)", 0, D.CCC["dpo"], None, "52일", "33억은 공급사가"),
    ]
    for i, (lab, start, ln, c, day, cash) in enumerate(rows):
        y = top + i * 52
        if c is None:
            g.rect(dx(start), y, dx(start + ln) - dx(start), 34, "var(--plot)", 3,
                   stroke=OCHRE, sw=2, dash="6 4")
            g.txt(dx(start + ln / 2), y + 23, day, "f", "middle",
                  fill="var(--c-ochre)", weight=800, size=16)
        else:
            g.rect(dx(start), y, dx(start + ln) - dx(start), 34, c, 3, o=.92)
            g.txt(dx(start + ln / 2), y + 23, day, "fw", "middle", size=16)
        g.txt(ax0 - 18, y + 23, lab, "l", "end", fill=INK, weight=700, size=16)
        g.txt(ax1 + 20, y + 23, cash, "f", "start", fill=INK2, weight=650, size=14)

    # 뺄셈을 눈에 보이게
    g.bracket(dx(0), dx(109), top - 46, "영업이 도는 데 109일", drop=10, up=True)
    y4 = top + 3 * 52 + 10
    g.rect(dx(D.CCC["dpo"]), y4, dx(115) - dx(D.CCC["dpo"]) - (dx(115) - dx(109)), 40, INK, 3)
    g.txt(dx(D.CCC["dpo"] + D.CCC_VAL / 2), y4 + 27, "현금 회전일 57일", "fw", "middle", size=17)
    g.txt(ax0 - 18, y4 + 27, "내 돈으로 버티는 구간", "l", "end", fill=INK, weight=800, size=16)
    g.txt(ax1 + 20, y4 + 27, "순 46억", "f", "start", fill=INK, weight=800, size=16)

    g.line(60, 300, 1020, 300, "var(--rule)", 1)
    g.txt(60, 326, "재고 68일  +  매출채권 41일  −  매입채무 52일  =  현금 회전일 57일",
          "f", fill=INK2, weight=700, size=15)
    return g.done()


# ================================================================ CCC 2/2
def ccc_trend():
    """추이와 동종 분포를 한 줄로 나란히."""
    g = G(W, H, "6분기 추이와 동종 12사 분포")
    # ---------- 좌: 추이
    g.txt(40, 26, "6분기 추이, 일", "t", size=15)
    bt, bb, bl, br = 62, 250, 110, 560
    Wt = D.WC_TREND
    lo, hi = 34, 76
    xs = [sc(i, 0, 5, bl, br) for i in range(6)]
    for d in (40, 55, 70):
        y = sc(d, lo, hi, bb, bt)
        g.line(bl, y, br, y, "var(--grid)", 1)
        g.txt(bl - 10, y + 5, str(d), "f", "end", fill=INK3, size=13)
    for key, c, lab in (("dio", NAVY, "재고"), ("dpo", OCHRE, "매입채무"), ("dso", TEAL, "매출채권")):
        pts = [(xs[i], sc(Wt[key][i], lo, hi, bb, bt)) for i in range(6)]
        g.poly(pts, c, 3)
        g.circle(*pts[-1], 5.5, c)
        g.txt(br + 14, pts[-1][1] + 5, "%s %d일" % (lab, Wt[key][-1]), "l",
              fill=c, weight=750, size=14)
    for i in (0, 5):
        g.txt(xs[i], bb + 22, Wt["x"][i], "ls", "middle", size=13)
    g.line(bl, bb, br, bb, "var(--rule)", 1)
    g.txt(40, 296, "채권은 잡았고", "f", fill=INK2, weight=700, size=15)
    g.txt(40, 320, "재고만 55에서 68일이 됐습니다", "f", fill=CLAY, weight=800, size=15)

    # ---------- 우: 동종 분포
    g.txt(640, 26, "동종 12사 분포, 일", "t", size=15)
    cl, cr, cy = 700, 1030, 150
    q = D.PEER_CCC_Q
    def px(v):
        return sc(v, 25, 75, cl, cr)
    g.band_h(px(q["q1"]), px(q["q3"]), cy - 34, cy + 34, SLATE, .18)
    g.line(px(q["med"]), cy - 40, px(q["med"]), cy + 40, NAVY, 2.5)
    g.line(cl, cy, cr, cy, "var(--rule)", 1)
    for d in D.PEER_CCC:
        g.circle(px(d), cy, 6, SLATE)
    sx = px(D.CCC_VAL)
    g.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z"
           % (sx, cy - 14, sx + 12, cy, sx, cy + 14, sx - 12, cy), OCHRE)
    g.txt(sx, cy - 26, "자사 57일", "f", "middle", fill="var(--c-ochre)", weight=800, size=15)
    g.txt(px(q["med"]), cy + 58, "중앙값 46일", "ls", "middle", size=13)
    g.txt(cl, cy + 58, "28", "f", "start", fill=INK3, size=12)
    g.txt(cr, cy + 58, "71", "f", "end", fill=INK3, size=12)
    g.txt(640, 296, "12사 중 10위", "f", fill=INK2, weight=700, size=15)
    g.txt(640, 320, "중앙값보다 11.5일 길고, 그 차이가 현금 8억입니다", "f",
          fill=CLAY, weight=800, size=15)
    return g.done()


# ================================================================ 원가 곡선
def costcurve():
    """공장별 단위원가와 판가. 주석은 그림 밖 오른쪽으로."""
    g = G(W, H, "공장별 단위원가 곡선과 판가선")
    pl, pr, ptop, pbot = 70, 700, 48, 262
    tot = sum(c[1] for c in D.COST_CURVE)
    MX = 2050

    def py(v):
        return sc(v, 0, MX, pbot, ptop)

    for v in (500, 1000, 1500, 2000):
        g.line(pl, py(v), pr, py(v), "var(--grid)", 1)
        g.txt(pl - 10, py(v) + 5, fmt(v), "f", "end", fill=INK3, size=13)
    x = pl
    for name, w, cost in D.COST_CURVE:
        bw = (pr - pl) * w / tot
        over = cost > D.PRICE
        g.rect(x + 1.5, py(cost), bw - 3, pbot - py(cost), CLAY if over else NAVY, 0,
               o=.88 if over else .82)
        dy = -10 if abs(cost - D.PRICE) > 150 else -26
        g.txt(x + bw / 2, py(cost) + dy, fmt(cost), "f", "middle", weight=800, size=15)
        g.txt(x + bw / 2, pbot + 22, name, "l", "middle", fill=INK, weight=700, size=14)
        g.txt(x + bw / 2, pbot + 40, "%d천 톤" % w, "ls", "middle", size=12.5)
        if name == "외주 위탁":
            g.rect(x + 1.5, py(D.RENEG), bw - 3, pbot - py(D.RENEG), "none", 0,
                   stroke=TEAL, sw=2, dash="6 4")
            g.txt(x + bw / 2, py(D.RENEG) + 30, "재협상 1,690", "fw", "middle", size=13)
        x += bw
    g.line(pl, py(D.PRICE), pr, py(D.PRICE), OCHRE, 2.5, "7 4")
    g.txt(pl + 8, py(D.PRICE) - 12, "평균 판가 1,620원", "f", "start",
          fill="var(--c-ochre)", weight=800, size=15)
    g.line(pl, pbot, pr, pbot, "var(--rule)", 1)
    g.txt(pl, pbot + 66, "가로 폭 = 생산량 · 단위당 총원가(고정비 배부 포함)", "ls", size=12.5)

    # 오른쪽 결론 칸
    g.line(760, 40, 760, 300, "var(--rule-soft)", 1)
    g.txt(792, 74, "외주 26천 톤", "f", fill=INK, weight=800, size=17)
    g.txt(792, 102, "판가보다 260원 비싸게", "l", fill=INK2, size=14)
    g.txt(792, 122, "만들고 있습니다", "l", fill=INK2, size=14)
    g.rect(792, 146, 230, 52, "var(--riskB)", 6)
    g.txt(808, 168, "연 6.8억", "f", fill="var(--c-clay)", weight=800, size=18)
    g.txt(808, 188, "역마진", "ls")
    g.txt(792, 232, "재협상 −190원이면", "l", fill=INK2, size=14)
    g.txt(792, 258, "연 4.9억 회복", "f", fill="var(--c-teal)", weight=800, size=17)
    g.txt(792, 284, "잔여는 3공장 증설로", "ls", size=12.5)
    return g.done()


# ================================================================ 코호트 + 파레토
def cohort_pareto():
    g = G(W, H, "수주 코호트 유지율과 거래처 집중도")
    # ---------- 좌: 코호트
    g.txt(40, 26, "수주 코호트 유지율, %", "t", size=15)
    left, ctop = 150, 54
    cw, ch = 62, 46
    for j, c in enumerate(D.COHORT_COLS):
        g.txt(left + cw * j + cw / 2, ctop - 10, c, "ls", "middle", size=12.5)
    for i, (name, vals) in enumerate(D.COHORTS):
        y = ctop + ch * i
        g.txt(left - 12, y + ch / 2 + 5, name.replace(" 수주", ""), "l", "end",
              fill=INK, weight=700, size=14)
        for j, v in enumerate(vals):
            x = left + cw * j
            o = .08 + .8 * ((v - 72) / 28) ** 1.1
            g.rect(x + 2, y + 2, cw - 4, ch - 4, NAVY, 3, o=max(o, .08))
            g.txt(x + cw / 2, y + ch / 2 + 5, str(v), "f", "middle",
                  fill="#fff" if o > .5 else INK, weight=700, size=13.5)
    g.rect(left + cw * 3 + 2, ctop + ch * 2 + 2, cw - 4, ch - 4, "none", 3, stroke=CLAY, sw=2.4)
    g.txt(left + cw * 4 + 16, ctop + ch * 2 + ch / 2 + 5, "3년차에만 꺾였습니다", "f",
          fill="var(--c-clay)", weight=800, size=13.5)
    g.txt(40, 320, "그해 대형 신규 2건이 저마진 조건 · 이탈 12억의 출처", "f",
          fill=INK2, weight=700, size=14)

    # ---------- 우: 파레토
    g.txt(640, 26, "거래처 집중도, 매출 320억", "t", size=15)
    bl, br, btop, bbot = 660, 1030, 58, 252
    n = len(D.TOP_CUST)
    stepw = (br - bl) / (n + 1)
    total = sum(v for _, v in D.TOP_CUST) + D.OTHERS
    cum, pts = 0, []
    for i, (name, v) in enumerate(D.TOP_CUST):
        cx = bl + stepw * i + stepw / 2
        h = sc(v, 0, 66, 0, bbot - btop)
        g.rect(cx - stepw * .34, bbot - h, stepw * .68, h, NAVY if i < 3 else SLATE, 1,
               o=.9 if i < 3 else .5)
        cum += v
        pts.append((cx, sc(cum / total * 100, 0, 100, bbot, btop)))
    cx = bl + stepw * n + stepw / 2
    h = sc(D.OTHERS, 0, 132, 0, bbot - btop)
    g.rect(cx - stepw * .34, bbot - h, stepw * .68, h, "var(--c-sand)", 1, o=.8)
    g.txt(cx, bbot + 18, "기타", "ls", "middle", size=12)
    pts.append((cx, sc(100, 0, 100, bbot, btop)))
    g.poly(pts, OCHRE, 2.8)
    g.circle(*pts[2], 6, OCHRE)
    g.txt(pts[2][0] + 12, pts[2][1] - 12, "상위 3사 42%", "f",
          fill="var(--c-ochre)", weight=800, size=15)
    g.line(bl, bbot, br, bbot, "var(--rule)", 1)
    g.txt(bl, bbot + 18, "A사", "ls", "start", size=12)
    g.txt(640, 320, "신규를 조건 없이 받는 관행이 3년 뒤 이탈로 돌아옵니다", "f",
          fill=INK2, weight=700, size=14)
    return g.done()


# ================================================================ 이익 풀
def profit_pool():
    """폭 = 매출, 높이 = 영업이익률, 면적 = 영업이익.

    100% 누적 마리메꼬는 정작 볼 것(이익)이 바닥의 얇은 띠로 깔린다.
    높이를 이익률로 바꾸면 면적이 곧 이익이 되어 눈으로 크기를 잰다.
    적자 사업부는 0선 아래로 내려가므로 따로 표시할 필요가 없다.
    """
    segs = sorted(D.SEGMENTS, key=lambda x: -x[2])
    g = G(W, H, "폭이 매출이고 높이가 이익률이라 면적이 곧 영업이익인 이익 풀")
    pl, pr, ptop, pbot = 70, 830, 56, 268
    tot = sum(s[1] for s in segs)
    LO, HI = -4.0, 16.0

    def py(v):
        return sc(v, LO, HI, pbot, ptop)

    zero = py(0)
    for v in (5, 10, 15):
        g.line(pl, py(v), pr, py(v), "var(--grid)", 1)
        g.txt(pl - 10, py(v) + 5, "%d%%" % v, "f", "end", fill=INK3, size=13)
    g.line(pl, zero, pr, zero, "var(--rule)", 1.6)

    x = pl
    for name, rv, opm, _ in segs:
        w = (pr - pl) * rv / tot
        y = py(opm)
        neg = opm < 0
        g.rect(x + 1.5, zero if neg else y, w - 3, abs(y - zero),
               CLAY if neg else NAVY, 0, o=.9 if neg else .84)
        op = rv * opm / 100
        if neg:
            # 적자 막대는 0선 아래로 얇게 깔린다. 라벨을 아래로 더 내려 매출 줄과 안 겹치게.
            g.txt(x + w / 2, y + 30, name, "l", "middle", fill=CLAY, weight=800, size=14)
            g.txt(x + w / 2, y + 50, "%.1f%%" % opm, "f", "middle",
                  fill=CLAY, weight=800, size=13.5)
            g.txt(x + w / 2, y + 68, "%.1f억" % op, "f", "middle",
                  fill=CLAY, weight=700, size=12.5)
        else:
            g.txt(x + w / 2, y - 30, name, "l", "middle", fill=INK, weight=750, size=15)
            g.txt(x + w / 2, y - 11, "%.1f%%" % opm, "f", "middle", fill=INK, weight=800, size=15)
            if w > 130:
                g.txt(x + w / 2, (y + zero) / 2 + 6, "영업이익 %.1f억" % op, "fw", "middle", size=14)
        if not neg:
            g.txt(x + w / 2, pbot + 24, "매출 %d억" % rv, "ls", "middle", size=12.5)
        else:
            g.txt(x + w / 2, y + 86, "매출 %d억" % rv, "ls", "middle", size=12)
        x += w
    g.txt(pl, pbot + 52, "가로 폭 = 매출 320억 · 세로 = 영업이익률 · 칠한 면적 = 영업이익", "ls", size=12.5)

    # 오른쪽 결론
    g.line(880, 46, 880, 300, "var(--rule-soft)", 1)
    g.txt(910, 78, "유통이 급식보다", "l", fill=INK2, size=14)
    g.txt(910, 100, "매출은 작고 이익은 큽니다", "l", fill=INK, weight=750, size=14)
    for i, (nm, val, c) in enumerate([("유통(오프)", "11.4억", TEAL), ("급식", "10.1억", INK2)]):
        yy = 132 + i * 30
        g.txt(910, yy, nm, "l", fill=INK3, size=13)
        g.txt(1040, yy, val, "f", "end", fill=c, weight=800, size=15)
    g.rect(910, 186, 130, 46, "var(--riskB)", 6)
    g.txt(924, 206, "온라인", "ls")
    g.txt(924, 226, "−0.4억", "f", fill=CLAY, weight=800, size=16)
    g.txt(910, 262, "매출 28억을 굴려", "l", fill=INK2, size=13)
    g.txt(910, 282, "이익을 깎고 있습니다", "l", fill=INK2, size=13)
    return g.done()


# ================================================================ 듀폰 격차 분해
def dupont_gap():
    """동종 중앙값 ROE 에서 자사 ROE 까지, 세 항이 각각 얼마를 밀었나.

    상자에 숫자만 늘어놓으면 '무엇이 만들었나'가 안 보인다.
    한 항씩 자사 값으로 갈아 끼우며 ROE 를 다시 계산하면 기여가 폭포로 드러난다.
    """
    self_, peer = D.DUPONT_SELF, D.DUPONT_PEER

    def roe(t):
        return t[0] * t[1] * t[2]

    cur, cum = list(peer), [round(roe(peer), 1)]
    for i in range(3):
        cur[i] = self_[i]
        cum.append(round(roe(cur), 1))
    eff = [round(cum[i + 1] - cum[i], 1) for i in range(3)]

    g = G(W, H, "동종 중앙값 ROE 에서 자사 ROE 까지 세 항의 기여를 폭포로")
    pl, pr, ptop, pbot = 76, 660, 74, 254
    LO, HI = 10.0, 15.4

    def py(v):
        return sc(v, LO, HI, pbot, ptop)

    g.txt(40, 30, "ROE 격차 분해, %p", "t", size=15)
    for v in (11, 13, 15):
        g.line(pl, py(v), pr, py(v), "var(--grid)", 1)
        g.txt(pl - 10, py(v) + 5, str(v), "f", "end", fill=INK3, size=12.5)

    items = [("동종 중앙값", cum[0], "tot")] + \
            [(D.DUPONT_NAMES[i], eff[i], "up" if eff[i] > 0 else "dn") for i in range(3)] + \
            [("자사", cum[3], "tot")]
    stepw = (pr - pl) / len(items)
    run = 0.0
    for i, (lab, v, kind) in enumerate(items):
        cx = pl + stepw * i + stepw / 2
        if kind == "tot":
            g.rect(cx - 42, py(v), 84, pbot - py(v), NAVY if i == 0 else INK, 3)
            g.txt(cx, py(v) - 11, "%.1f" % v, "f", "middle", weight=800, size=17)
            for d in (10, 15):
                g.line(cx - 48, pbot - d, cx - 36, pbot - d - 6, "var(--plot)", 2.6)
                g.line(cx + 36, pbot - d, cx + 48, pbot - d - 6, "var(--plot)", 2.6)
            run = v
        else:
            y1, y0 = py(run), py(run + v)
            g.rect(cx - 34, min(y0, y1), 68, abs(y0 - y1), TEAL if v > 0 else CLAY, 3, o=.9)
            g.txt(cx, min(y0, y1) - 9, "%+.1f" % v, "f", "middle",
                  fill="var(--c-teal)" if v > 0 else "var(--c-clay)", weight=800, size=15)
            run += v
        if i < len(items) - 1:
            g.line(cx + (42 if kind == "tot" else 34), py(run),
                   cx + stepw - (42 if items[i + 1][2] == "tot" else 34), py(run),
                   INK3, 1, "3 3", .7)
        g.txt(cx, pbot + 22, lab, "l", "middle", fill=INK, weight=700, size=13.5)
    g.line(pl, pbot, pr, pbot, "var(--rule)", 1)
    g.txt(pl, pbot + 50, "동종 중앙값 ROE 에서 한 항씩 자사 값으로 갈아 끼운 결과", "ls", size=12.5)

    # ---------- 오른쪽: 세 항의 자사 대 동종
    g.line(712, 46, 712, 300, "var(--rule-soft)", 1)
    g.txt(744, 30, "자사와 동종 중앙값", "t", size=14)
    for i in range(3):
        y = 76 + i * 78
        s_, p_ = self_[i], peer[i]
        win = eff[i] > 0
        c = TEAL if win else CLAY
        g.txt(744, y, D.DUPONT_NAMES[i], "l", fill=INK, weight=750, size=14)
        g.txt(1040, y, D.DUPONT_SUB[i], "ls", "end", size=11.5)
        bx0, bx1 = 744, 1000
        mx = max(s_, p_) * 1.18
        g.line(bx0, y + 30, bx0 + (bx1 - bx0) * p_ / mx, y + 30, "var(--h4)", 9)
        g.line(bx0, y + 44, bx0 + (bx1 - bx0) * s_ / mx, y + 44, c, 9)
        fs = ("%.1f%%" if i == 0 else "%.2f")
        g.txt(bx0 + (bx1 - bx0) * p_ / mx + 10, y + 35, fs % p_, "f",
              fill=INK3, size=12, weight=650)
        g.txt(bx0 + (bx1 - bx0) * s_ / mx + 10, y + 49, fs % s_, "f",
              fill=c, size=13, weight=800)
    g.txt(744, 314, "위 = 동종 중앙값 · 아래 = 자사", "ls", size=11.5)
    return g.done()
