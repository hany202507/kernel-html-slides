# -*- coding: utf-8 -*-
"""컨설팅 펌과 IR 에서 쓰는 전시물 아홉 종. 슬라이드 그림 영역(1080 x 340)에 맞춘 판.

서린푸드 한 회사의 숫자를 그대로 이어 쓴다. 급식이 다년 계약이라
계약 잔고·코호트 누적·획득비 회수가 이 회사에서 실제로 말이 된다.
"""
import math

import data as D
from draw import G, sc, fmt

NAVY, OCHRE, TEAL, CLAY = "var(--c-navy)", "var(--c-ochre)", "var(--c-teal)", "var(--c-clay)"
SLATE, SAND = "var(--c-slate)", "var(--c-sand)"
INK, INK2, INK3 = "var(--ink)", "var(--ink-2)", "var(--ink-3)"
W, H = 1080, 340


# ================================================================ 파워 커브
def power_curve():
    """동종 12사를 경제적 이익 순으로 세우면 가운데가 납작하고 양끝이 솟는다."""
    ep = [-9.2, -3.1, -1.4, -0.6, -0.2, 0.3, 0.8, 1.6, 2.9, 5.4, 11.8, 24.6]
    g = G(W, H, "동종 12사를 경제적 이익 순으로 세운 파워 커브")
    ml, mr, mt, mb = 70, 60, 44, 52
    n = len(ep)
    step = (W - ml - mr) / n
    LO, HI = -12.0, 28.0

    def py(v):
        return sc(v, LO, HI, H - mb, mt)

    zero = py(0)
    for v in (-10, 0, 10, 20):
        y = py(v)
        g.line(ml, y, W - mr, y, "var(--grid)" if v else "var(--rule)", 1 if v else 1.4)
        g.txt(ml - 10, y + 5, "%+d" % v if v else "0", "f", "end", fill=INK3, size=12)
    for i, v in enumerate(ep):
        cx = ml + step * i + step / 2
        me = i == 7                      # 서린푸드
        c = OCHRE if me else (SLATE if v < 0 else NAVY)
        y0, y1 = (py(v), zero) if v >= 0 else (zero, py(v))
        g.rect(cx - step * .32, y0, step * .64, y1 - y0, c, 2, o=1 if me else .85)
        if me:
            g.txt(cx, py(v) - 14, "서린푸드 +1.6", "f", "middle",
                  fill="var(--c-ochre)", weight=800, size=13)
    g.bracket(ml + step * 0.5, ml + step * 6.5, py(-11), "가운데 일곱 곳은 자본비용을 겨우 맞춘다",
              drop=8, up=False)
    g.txt(W - mr, py(24.6) - 16, "상위 두 곳이 업계 경제적 이익의 절반", "ls", "end")
    g.txt(ml, H - 14, "세로 = 경제적 이익(ROIC − WACC) × 투하자본, 억원 · 동종 12사", "ls", size=12)
    return g.done()


# ================================================================ 전략적 통제 지도
def control_map():
    """장부가치 대비 시장가치. 같은 시가총액 곡선 위에서 어디에 서 있나."""
    firms = [("명진식품", 640, 1.6), ("대한푸드", 430, 2.4), ("한울에프앤비", 210, 2.6),
             ("세일무역", 300, 1.2), ("가온에프씨", 95, 2.1), ("서린푸드", 198, 1.9)]
    g = G(W, H, "장부가치와 시장가치 배율 평면 위의 전략적 통제 지도")
    ml, mr, mt, mb = 70, 210, 34, 50
    X0, X1, Y0, Y1 = 0.0, 720.0, 0.8, 3.0

    def PX(v):
        return sc(v, X0, X1, ml, W - mr)

    def PY(v):
        return sc(v, Y0, Y1, H - mb, mt)

    # 등시가총액 곡선 (장부 x 배율 = 일정)
    for cap, lab in ((300, "300억"), (600, "600억"), (1000, "1,000억")):
        pts = []
        for k in range(24):
            x = X0 + (X1 - X0) * (k + 1) / 24
            y = cap / x
            if Y0 <= y <= Y1:
                pts.append((PX(x), PY(y)))
        if len(pts) > 1:
            g.poly(pts, SLATE, 1.2, dash="5 4", o=.7)
            g.txt(pts[0][0] + 4, pts[0][1] - 7, lab, "ls", size=11)
    for v in (1.0, 1.5, 2.0, 2.5):
        g.txt(ml - 10, PY(v) + 5, "%.1fx" % v, "f", "end", fill=INK3, size=12)
    g.line(ml, H - mb, W - mr, H - mb, "var(--rule)", 1)
    g.line(ml, mt, ml, H - mb, "var(--rule)", 1)
    for nm, bk, mx in firms:
        me = nm == "서린푸드"
        g.circle(PX(bk), PY(mx), 9 if me else 6.5, OCHRE if me else SLATE)
        g.txt(PX(bk), PY(mx) - (18 if me else 14), nm, "l", "middle",
              fill=INK if me else INK3, weight=800 if me else 650, size=13 if me else 12)
    g.txt(W - mr, H - mb + 26, "장부가치 (억원) →", "lb", "end", fill=INK, weight=700)
    g.txt(ml, mt - 12, "시장가치 / 장부가치", "ls")
    g.line(W - mr + 30, 40, W - mr + 30, 300, "var(--rule-soft)", 1)
    g.txt(W - mr + 56, 76, "점선은 같은 시가총액", "l", fill=INK2, size=13)
    g.txt(W - mr + 56, 100, "오른쪽 위로 갈수록 크다", "l", fill=INK2, size=13)
    g.txt(W - mr + 56, 148, "서린푸드 376억", "f", fill=INK, weight=800, size=17)
    g.txt(W - mr + 56, 172, "198억 × 1.9배", "ls")
    g.txt(W - mr + 56, 214, "한 곡선 위를 오른쪽으로", "l", fill=INK2, size=13)
    g.txt(W - mr + 56, 236, "가려면 장부를 키우고,", "l", fill=INK2, size=13)
    g.txt(W - mr + 56, 258, "위로 가려면 배율을 올린다", "l", fill=INK2, size=13)
    return g.done()


# ================================================================ 세 지평선
def horizons():
    """기존 사업이 꺼지는 속도보다 새 사업이 뜨는 속도가 빠른가."""
    yrs = ["2023", "2024", "2025", "2026E", "2027E", "2028E"]
    h1 = [180, 172, 148, 138, 126, 112]        # 급식
    h2 = [62, 78, 112, 142, 176, 208]          # 유통·가공
    h3 = [17, 37, 60, 72, 96, 128]             # 온라인·신사업
    g = G(W, H, "기존·성장·신사업 세 사업의 매출 누적과 구성 전환")
    ml, mr, mt, mb = 66, 230, 36, 46
    tot = [a + b + c for a, b, c in zip(h1, h2, h3)]
    MX = max(tot) * 1.1
    xs = [sc(i, 0, 5, ml, W - mr) for i in range(6)]

    def py(v):
        return sc(v, 0, MX, H - mb, mt)

    layers = [(h1, NAVY, "급식 · 기존"), (h2, TEAL, "유통·가공 · 성장"), (h3, OCHRE, "온라인 · 신사업")]
    base = [0.0] * 6
    for vals, c, nm in layers:
        top = [base[i] + vals[i] for i in range(6)]
        pts = [(xs[i], py(top[i])) for i in range(6)] + \
              [(xs[i], py(base[i])) for i in range(5, -1, -1)]
        g.area(pts, c, .85)
        g.txt(W - mr + 14, py((base[-1] + top[-1]) / 2) + 5,
              "%s %d억" % (nm, vals[-1]), "l", fill=c, weight=750, size=13)
        base = top
    # 전망 구간은 흰 막을 덮어 실적보다 흐리게 둔다. 같은 색으로 두면 실적처럼 읽힌다
    g.rect(xs[2], mt, W - mr - xs[2], H - mb - mt, "var(--bg)", o=.42)
    g.line(xs[2], mt, xs[2], H - mb, INK3, 1, "4 4")
    g.txt(xs[2] + 8, mt + 12, "실적 | 전망", "ls")
    for i in (0, 2, 5):
        g.txt(xs[i], H - mb + 20, yrs[i], "ls", "middle")
    g.line(ml, H - mb, W - mr, H - mb, "var(--rule)", 1)
    g.txt(ml, H - 12, "급식 비중 69% → 25%. 꺼지는 속도보다 뜨는 속도가 빠릅니다", "ls", size=12.5)
    return g.done()


# ================================================================ 성장 원천 분해
def growth_decomp():
    """성장이 기존 거래처에서 왔나 신규에서 왔나."""
    items = [("2024 매출", 287, "tot"), ("기존 거래처 증가", 26, "up"),
             ("신규 수주", 19, "up"), ("이탈", -12, "dn"), ("2025 매출", 320, "tot")]
    g = G(W, H, "기존 신규 이탈로 나눈 성장 원천 분해")
    pl, pr, pt, pb = 60, 780, 60, 258
    LO, HI = 255.0, 345.0

    def py(v):
        return sc(v, LO, HI, pb, pt)

    stepw = (pr - pl) / len(items)
    run = 0.0
    for i, (lab, v, kind) in enumerate(items):
        cx = pl + stepw * i + stepw / 2
        if kind == "tot":
            g.rect(cx - 46, py(v), 92, pb - py(v), NAVY if i == 0 else INK, 2)
            g.txt(cx, py(v) - 10, fmt(v), "f", "middle", weight=800, size=15)
            for d in (10, 15):
                g.line(cx - 52, pb - d, cx - 40, pb - d - 6, "var(--plot)", 2.6)
                g.line(cx + 40, pb - d, cx + 52, pb - d - 6, "var(--plot)", 2.6)
            run = v
        else:
            y1, y0 = py(run), py(run + v)
            g.rect(cx - 38, min(y0, y1), 76, abs(y0 - y1), TEAL if v > 0 else CLAY, 2, o=.88)
            g.txt(cx, min(y0, y1) - 8, "%+d" % v, "f", "middle",
                  fill="var(--c-teal)" if v > 0 else "var(--c-clay)", weight=800, size=13)
            run += v
        if i < len(items) - 1:
            g.line(cx + (46 if kind == "tot" else 38), py(run),
                   cx + stepw - (46 if items[i + 1][2] == "tot" else 38), py(run),
                   INK3, 1, "3 3", .7)
        g.txt(cx, pb + 20, lab, "l", "middle", fill=INK, weight=650, size=12.5)
    g.line(pl, pb, pr, pb, "var(--rule)", 1)
    g.line(840, 46, 840, 300, "var(--rule-soft)", 1)
    g.txt(872, 84, "순증 33억", "f", fill=INK, weight=800, size=18)
    g.txt(872, 112, "기존이 26억, 신규가 19억", "l", fill=INK2, size=13)
    g.txt(872, 134, "이탈이 12억을 되가져갔다", "l", fill=INK2, size=13)
    g.rect(872, 168, 168, 52, "var(--a2b)", 6)
    g.txt(888, 190, "유지율 92%", "f", fill="var(--c-teal)", weight=800, size=17)
    g.txt(888, 210, "기존 거래처 금액 기준", "ls")
    g.txt(872, 258, "신규만 늘려서는", "l", fill=INK2, size=13)
    g.txt(872, 280, "이탈을 못 덮습니다", "l", fill=INK2, size=13)
    return g.done()


# ================================================================ Rule of 40
def rule40():
    """성장률과 잉여현금 마진을 더해 40을 넘는가."""
    firms = [("명진식품", 2.1, 9.4), ("대한푸드", 4.2, 12.8), ("세일무역", 6.0, 6.2),
             ("한울에프앤비", 9.8, 10.1), ("가온에프씨", 14.6, 2.8), ("서린푸드", 11.5, 4.4)]
    g = G(W, H, "성장률과 잉여현금 마진의 합이 40을 넘는지 보는 산점도")
    ml, mr, mt, mb = 70, 220, 34, 48
    X0, X1, Y0, Y1 = 0.0, 20.0, 0.0, 16.0

    def PX(v):
        return sc(v, X0, X1, ml, W - mr)

    def PY(v):
        return sc(v, Y0, Y1, H - mb, mt)

    for th, lab, c in ((40, "합 40", NAVY), (20, "합 20", SLATE)):
        pts = [(PX(x), PY(th - x)) for x in (X0, X1) if Y0 <= th - x <= Y1]
        if len(pts) < 2:
            xs_ = [x for x in (X0, X1, th - Y0, th - Y1) if X0 <= x <= X1]
            pts = [(PX(x), PY(th - x)) for x in sorted(set(xs_)) if Y0 <= th - x <= Y1]
        if len(pts) > 1:
            g.poly(pts, c, 1.6, dash="6 4")
            # 라벨은 선의 위쪽 끝에 붙인다. 아래쪽 끝은 x축 선과 겹친다
            g.txt(pts[0][0] + 10, pts[0][1] + 16, lab, "ls", "start", fill=INK2, weight=700)
    for v in (5, 10, 15):
        g.line(ml, PY(v), W - mr, PY(v), "var(--grid)", 1)
        g.txt(ml - 10, PY(v) + 5, "%d%%" % v, "f", "end", fill=INK3, size=12)
    g.line(ml, H - mb, W - mr, H - mb, "var(--rule)", 1)
    for nm, gr, fc in firms:
        me = nm == "서린푸드"
        g.circle(PX(gr), PY(fc), 9 if me else 6.5, OCHRE if me else SLATE)
        g.txt(PX(gr), PY(fc) - (18 if me else 13), nm, "l", "middle",
              fill=INK if me else INK3, weight=800 if me else 650, size=13 if me else 11.5)
    g.txt(W - mr, H - mb + 26, "매출 성장률 (%) →", "lb", "end", fill=INK, weight=700)
    g.txt(ml, mt - 12, "잉여현금 마진 (%)", "ls")
    g.line(W - mr + 30, 44, W - mr + 30, 300, "var(--rule-soft)", 1)
    g.txt(W - mr + 56, 86, "서린푸드 15.9", "f", fill=INK, weight=800, size=18)
    g.txt(W - mr + 56, 110, "성장 11.5 + 마진 4.4", "ls")
    g.txt(W - mr + 56, 156, "40 은커녕 20 도", "l", fill=INK2, size=13)
    g.txt(W - mr + 56, 178, "못 넘습니다", "l", fill=INK2, size=13)
    g.txt(W - mr + 56, 224, "성장은 동종 2위인데", "l", fill=INK2, size=13)
    g.txt(W - mr + 56, 246, "현금 마진이 끌어내립니다", "l", fill=CLAY, weight=750, size=13)
    return g.done()


# ================================================================ 코호트 레이어케이크
def layer_cake():
    """수주 연도별 코호트가 쌓여 매출이 된다. 새 거래처가 이탈을 덮는가."""
    yrs = ["2021", "2022", "2023", "2024", "2025"]
    # 코호트별 그 해 기여 매출(억). 앞 코호트는 유지율만큼 줄어든다
    coh = [("2021년 수주", [231, 213, 199, 187, 178]),
           ("2022년 수주", [0, 31, 29, 27, 26]),
           ("2023년 수주", [0, 0, 31, 28, 26]),
           ("2024년 수주", [0, 0, 0, 45, 43]),
           ("2025년 수주", [0, 0, 0, 0, 47])]
    g = G(W, H, "수주 연도별 코호트를 쌓아 올린 매출 누적")
    ml, mr, mt, mb = 66, 210, 34, 46
    tot = [sum(c[1][i] for c in coh) for i in range(5)]
    MX = max(tot) * 1.12
    xs = [sc(i, 0, 4, ml, W - mr) for i in range(5)]

    def py(v):
        return sc(v, 0, MX, H - mb, mt)

    ramp = ["r1", "r2", "r3", "r4", "r5"]
    base = [0.0] * 5
    for (nm, vals), tk in zip(coh, ramp):
        top = [base[i] + vals[i] for i in range(5)]
        pts = [(xs[i], py(top[i])) for i in range(5)] + \
              [(xs[i], py(base[i])) for i in range(4, -1, -1)]
        g.area(pts, "var(--%s)" % tk, .95)
        # 어느 해에 딴 거래처인지 띠 안에 직접 적는다. 범례를 따로 두면 눈이 왕복한다
        th = py(base[-1]) - py(top[-1])
        if th >= 15:
            lab = nm if th >= 40 else nm.replace("년 수주", "")
            g.txt(W - mr - 14, (py(base[-1]) + py(top[-1])) / 2 + 4.5, lab, "f", "end",
                  fill="var(--bg)" if tk in ("r1", "r2", "r3") else INK,
                  weight=750, size=12.5)
        base = top
    for i in range(5):
        g.txt(xs[i], py(tot[i]) - 10, fmt(tot[i]), "f", "middle", weight=800, size=13)
        g.txt(xs[i], H - mb + 20, yrs[i], "ls", "middle")
    g.line(ml, H - mb, W - mr, H - mb, "var(--rule)", 1)
    g.line(W - mr + 26, 44, W - mr + 26, 300, "var(--rule-soft)", 1)
    g.txt(W - mr + 52, 80, "2021년 코호트", "l", fill=INK2, size=13)
    g.txt(W - mr + 52, 104, "231억 → 178억", "f", fill=CLAY, weight=800, size=17)
    g.txt(W - mr + 52, 126, "4년에 23% 빠졌다", "ls")
    g.txt(W - mr + 52, 176, "새 코호트 누적", "l", fill=INK2, size=13)
    g.txt(W - mr + 52, 200, "+142억", "f", fill="var(--c-teal)", weight=800, size=17)
    g.txt(W - mr + 52, 248, "새로 딴 거래처가", "l", fill=INK2, size=13)
    g.txt(W - mr + 52, 270, "덮고도 남습니다", "l", fill=INK2, size=13)
    return g.done()


# ================================================================ 획득비 회수 곡선
def cac_payback():
    """새 거래처를 따는 데 쓴 돈을 몇 달 만에 회수하나."""
    months = list(range(0, 25, 3))
    curves = [("2023년 수주", [-100, -74, -50, -28, -8, 10, 27, 43, 58], SLATE),
              ("2024년 수주", [-100, -70, -43, -18, 4, 25, 45, 63, 80], TEAL),
              ("2025년 수주", [-100, -63, -30, 0, 27, 52, 75, 96, 116], NAVY)]
    g = G(W, H, "수주 코호트별 고객 획득비 회수 곡선")
    ml, mr, mt, mb = 74, 210, 34, 48
    X1 = 24.0
    LO, HI = -110.0, 130.0

    def PX(m):
        return sc(m, 0, X1, ml, W - mr)

    def PY(v):
        return sc(v, LO, HI, H - mb, mt)

    g.line(ml, PY(0), W - mr, PY(0), "var(--rule)", 1.4)
    g.txt(ml - 10, PY(0) + 5, "0", "f", "end", fill=INK3, size=12)
    for v in (-100, 100):
        g.line(ml, PY(v), W - mr, PY(v), "var(--grid)", 1)
        g.txt(ml - 10, PY(v) + 5, "%+d" % v, "f", "end", fill=INK3, size=12)
    for k, (nm, vals, c) in enumerate(curves):
        g.poly([(PX(months[i]), PY(vals[i])) for i in range(len(vals))], c, 3)
        g.circle(PX(months[-1]), PY(vals[-1]), 5, c)
        g.txt(W - mr + 12, PY(vals[-1]) + 5, nm, "l", fill=c, weight=750, size=13)
        # 손익분기 지점
        for i in range(1, len(vals)):
            if vals[i - 1] < 0 <= vals[i]:
                t = -vals[i - 1] / (vals[i] - vals[i - 1])
                mx_ = months[i - 1] + t * (months[i] - months[i - 1])
                g.circle(PX(mx_), PY(0), 4.5, c)
                # 세 지점이 가까워 같은 높이에 두면 글자가 붙는다. 층을 달리한다
                g.txt(PX(mx_), PY(0) - 12 - 17 * k, "%.0f개월" % mx_, "f", "middle",
                      fill=c, weight=800, size=12)
                break
    for m in (0, 12, 24):
        g.txt(PX(m), H - mb + 20, "%d개월" % m, "ls", "middle")
    g.txt(ml, mt - 12, "누적 회수 (획득비 100 기준)", "ls")
    g.txt(ml, H - 12, "0 을 넘는 지점이 회수 완료. 최근 코호트일수록 빨라지고 있습니다", "ls", size=12.5)
    return g.done()


# ================================================================ 설비투자 강도와 잉여현금
def capex_fcf():
    """설비투자를 늘리면 잉여현금이 줄어든다. 어디까지 감당하나."""
    yrs = ["2021", "2022", "2023", "2024", "2025"]
    capex_r = [2.9, 3.1, 3.0, 3.2, 3.1]        # 매출 대비 %. 5년 내내 3% 언저리
    fcf = [8, 10, 12, 14, 14]                   # 억원
    g = G(W, H, "설비투자 강도와 잉여현금을 겹친 막대와 선")
    ml, mr, mt, mb = 70, 76, 40, 46
    n = len(yrs)
    step = (W - ml - mr) / n
    for v in (4, 8, 12, 16):
        y = sc(v, 0, 18, H - mb, mt)
        g.line(ml, y, W - mr, y, "var(--grid)", 1)
        g.txt(ml - 10, y + 5, fmt(v), "f", "end", fill=INK3, size=12)
    for i, v in enumerate(fcf):
        cx = ml + step * i + step / 2
        y = sc(v, 0, 18, H - mb, mt)
        g.rect(cx - step * .26, y, step * .52, H - mb - y, NAVY, 2, o=.82)
        g.txt(cx, y - 10, "%d억" % v, "f", "middle", weight=800, size=13.5)
        g.txt(cx, H - mb + 20, yrs[i], "ls", "middle")
    pts = [(ml + step * i + step / 2, sc(capex_r[i], 2.0, 4.2, H - mb - 14, mt + 10))
           for i in range(n)]
    g.poly(pts, OCHRE, 3)
    for i in (0, n - 1):
        g.circle(*pts[i], 5, OCHRE)
        # 첫 점은 막대 값 라벨과 높이가 겹친다. 그 하나만 점 아래에 적는다
        g.txt(pts[i][0], pts[i][1] + (22 if i == 0 else -13), "%.1f%%" % capex_r[i],
              "f", "middle", fill="var(--c-ochre)", weight=800, size=13)
    # 마지막 두 해가 같은 값이라는 것이 이 그림의 요점이다. 눈에 걸리게 잇는다
    ys = sc(fcf[-1], 0, 18, H - mb, mt)
    g.line(ml + step * 3 + step / 2, ys, ml + step * 4 + step / 2, ys, CLAY, 1.6, "5 4")
    g.txt(ml + step * 4, ys - 30, "2년째 14억", "f", "middle", fill=CLAY, weight=800, size=13)
    g.line(ml, H - mb, W - mr, H - mb, "var(--rule)", 1)
    g.rect(ml, 22, 14, 14, NAVY, 3, o=.82)
    g.txt(ml + 22, 34, "잉여현금 (억원)", "ls")
    g.rect(ml + 190, 22, 14, 14, OCHRE, 3)
    g.txt(ml + 212, 34, "설비투자 / 매출 (%)", "ls")
    g.txt(ml, H - 12, "설비투자 강도는 3% 대에서 안정적입니다. 잉여현금이 멈춘 것은 투자가 아니라 운전자본 탓입니다",
          "ls", size=12.5)
    return g.done()


# ================================================================ 계약 잔고와 커버리지
def backlog():
    """급식은 다년 계약이라 잔고가 다음 해 매출을 얼마나 덮는지가 보인다."""
    qs = ["24.1Q", "24.2Q", "24.3Q", "24.4Q", "25.1Q", "25.2Q"]
    near = [118, 124, 131, 139, 146, 152]      # 12개월 내 인식
    far = [86, 92, 89, 101, 108, 117]          # 그 이후
    cov = [46, 48, 49, 51, 52, 54]             # 향후 12개월 매출 커버리지 %
    g = G(W, H, "분기별 계약 잔고와 향후 12개월 매출 커버리지")
    ml, mr, mt, mb = 70, 92, 44, 46
    n = len(qs)
    step = (W - ml - mr) / n
    MX = 300.0
    for v in (100, 200, 300):
        y = sc(v, 0, MX, H - mb, mt)
        g.line(ml, y, W - mr, y, "var(--grid)", 1)
        g.txt(ml - 10, y + 5, fmt(v), "f", "end", fill=INK3, size=12)
    for i in range(n):
        cx = ml + step * i + step / 2
        h1 = (H - mb - mt) * near[i] / MX
        h2 = (H - mb - mt) * far[i] / MX
        g.rect(cx - step * .3, H - mb - h1, step * .6, h1, NAVY, 2, o=.9)
        g.rect(cx - step * .3, H - mb - h1 - h2, step * .6, h2, "var(--h4)", 2)
        g.txt(cx, H - mb - h1 - h2 - 10, fmt(near[i] + far[i]), "f", "middle", weight=800, size=13)
        g.txt(cx, H - mb + 20, qs[i], "ls", "middle")
    pts = [(ml + step * i + step / 2, sc(cov[i], 40, 60, H - mb - 20, mt + 16)) for i in range(n)]
    g.poly(pts, OCHRE, 3)
    for i in (0, n - 1):
        g.circle(*pts[i], 5, OCHRE)
        g.txt(pts[i][0], pts[i][1] - 13, "%d%%" % cov[i], "f", "middle",
              fill="var(--c-ochre)", weight=800, size=13)
    g.line(ml, H - mb, W - mr, H - mb, "var(--rule)", 1)
    g.rect(ml, 22, 14, 14, NAVY, 3, o=.9)
    g.txt(ml + 22, 34, "12개월 내 인식", "ls")
    g.rect(ml + 150, 22, 14, 14, "var(--h4)", 3)
    g.txt(ml + 172, 34, "그 이후", "ls")
    g.rect(ml + 268, 22, 14, 14, OCHRE, 3)
    g.txt(ml + 290, 34, "향후 12개월 매출 커버리지 (%)", "ls")
    g.txt(ml, H - 12, "잔고 269억, 커버리지 54%. 다음 해 매출의 절반은 이미 계약으로 잡혀 있습니다",
          "ls", size=12.5)
    return g.done()
