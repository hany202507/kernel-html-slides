# -*- coding: utf-8 -*-
"""고급 재무분석 전시물 — M&A · 경영컨설팅에서 쓰는 것들.

mkchart.py 가 기본 형태(막대·선·워터폴)를 맡고, 이 파일이 그 위를 맡는다.
전부 SVG 로 그린다. 좌표는 사람이 쓰지 않는다.

    tornado   토네이도        무엇이 값을 가장 많이 흔드나
    mc        확률분포        몬테카를로 결과와 P10/P50/P90
    fan       팬 차트         시나리오 밴드
    evbridge  EV-Equity 브릿지  기업가치에서 주주가치까지
    irr       수익 원천 분해   LBO 수익이 어디서 나왔나
    tree2     2단 분해 트리    듀폰을 두 층으로
    box       사분위 상자      동종 분포 안에서 자사 위치
    dumbbell  격차 막대        자사와 중앙값의 벌어진 폭
    trail     궤적 산점도      몇 해에 걸친 이동
    costcurve 원가 곡선        누적 물량 x 단가
    sankey    흐름도           매출이 어디로 흘러 이익이 되나
    ladder    만기 사다리      차입금이 언제 돌아오나
    cohort    코호트 삼각      기간이 갈수록 남는 비율
"""
from mkchart import W, H, col, esc, fmt, tail  # noqa: F401


# ------------------------------------------------------------------ 도형 helper
def svg(h=None):
    return ['<div class="chart">', '  <div class="plot">',
            '  <svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">'
            % (W, h or H)]


def done(out, s):
    out += ["  </svg>", "  </div>"]
    return tail(out, s)


def R(x, y, w, h, fill, rx=2, extra=""):
    return ('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s"%s/>'
            % (x, y, max(w, 0.4), max(h, 0.4), rx, fill, extra))


def L(x1, y1, x2, y2, style="stroke:var(--line); stroke-width:1"):
    return '    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" style="%s"/>' % (x1, y1, x2, y2, style)


def T(x, y, t, anchor="start", cls="lb", style=""):
    st = ' style="%s"' % style if style else ""
    return ('    <text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>'
            % (cls, x, y, anchor, st, esc(t)))


INK = "fill:var(--ink); font-weight:800"
NAME = "fill:var(--ink); font-size:15px; font-weight:750"


# ------------------------------------------------------------------ 1. 토네이도
def tornado(s):
    """가정 하나씩 흔들었을 때 값이 얼마나 움직이나. 많이 흔드는 것부터 위로."""
    base = float(s["base"])
    rows = sorted(s["rows"], key=lambda r: -(abs(r["hi"] - base) + abs(base - r["lo"])))
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 286.0, 96.0, 24.0, 36.0
    span = max(max(abs(r["hi"] - base), abs(base - r["lo"])) for r in rows) * 1.18
    half = (W - ml - mr) / 2
    cx = ml + half
    n = len(rows)
    band = (H - mt - mb) / n
    hgt = min(band * 0.6, 26)
    out = svg()
    out.append(L(cx, mt - 6, cx, H - mb + 4, "stroke:var(--rule); stroke-width:1.5"))
    out.append(T(cx, H - mb + 24, "기준 %s%s" % (fmt(base, dec), unit), "middle", "vl"))
    for i, r in enumerate(rows):
        y = mt + band * i + band / 2
        xl = cx + half * (r["lo"] - base) / span
        xh = cx + half * (r["hi"] - base) / span
        out.append(R(min(xl, cx), y - hgt / 2, abs(cx - xl), hgt, col("h4")))
        out.append(R(min(xh, cx), y - hgt / 2, abs(xh - cx), hgt, col("r2")))
        out.append(T(ml - 18, y + 5, r["label"], "end", "lb", NAME))
        out.append(T(min(xl, xh) - 8, y + 5, fmt(r["lo"], dec), "end", "vl mute"))
        out.append(T(max(xl, xh) + 8, y + 5, "%s%s" % (fmt(r["hi"], dec), unit), "start", "vl"))
    return done(out, s)


# ------------------------------------------------------------------ 2. 확률분포
def mc(s):
    """몬테카를로 결과. 히스토그램 + 누적확률 곡선 + P10/P50/P90."""
    bins, x0, x1 = s["bins"], float(s["x0"]), float(s["x1"])
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 46.0, 46.0, 30.0, 38.0
    n = len(bins)
    tot = float(sum(bins)) or 1.0
    bw = (W - ml - mr) / n
    mx = max(bins) or 1

    def PX(v):
        return ml + (W - ml - mr) * (v - x0) / ((x1 - x0) or 1)

    def PY(c):
        return mt + (H - mt - mb) * (1 - c / mx)

    out = svg()
    for i, c in enumerate(bins):
        h = (H - mt - mb) * c / mx
        out.append(R(ml + bw * i + 1, H - mb - h, bw - 2, h, col("h4"), 1))
    # 누적확률 곡선
    cum, pts = 0.0, []
    for i, c in enumerate(bins):
        cum += c
        pts.append("%.1f,%.1f" % (ml + bw * (i + 1), mt + (H - mt - mb) * (1 - cum / tot)))
    out.append('    <polyline class="ln" style="--c:%s" points="%s"/>' % (col("a3"), " ".join(pts)))
    out.append(L(ml, H - mb, W - mr, H - mb, "stroke:var(--line); stroke-width:1"))
    for key, lab, cl in (("p10", "P10", "muted"), ("p50", "P50", "rule"), ("p90", "P90", "muted")):
        if s.get(key) is None:
            continue
        x = PX(float(s[key]))
        w = "2" if key == "p50" else "1"
        out.append(L(x, mt - 8, x, H - mb, "stroke:var(--%s); stroke-width:%s; stroke-dasharray:%s"
                     % (cl, w, "0" if key == "p50" else "5 4")))
        out.append(T(x, mt - 14, "%s  %s%s" % (lab, fmt(float(s[key]), dec), unit), "middle",
                     "vl" if key == "p50" else "vl mute"))
    out.append(T(ml, H - mb + 22, "%s%s" % (fmt(x0, dec), unit), "start"))
    out.append(T(W - mr, H - mb + 22, "%s%s" % (fmt(x1, dec), unit), "end"))
    return done(out, s)


# ------------------------------------------------------------------ 3. 팬 차트
def fan(s):
    """중앙 전망선과 시나리오 밴드. 바깥 밴드일수록 옅다."""
    x, p50, bands = s["x"], s["p50"], s["bands"]
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 52.0, 92.0, 26.0, 38.0
    allv = list(p50) + [v for b in bands for v in b["lo"] + b["hi"]]
    lo, hi = min(allv), max(allv)
    d = (hi - lo) or 1
    lo, hi = lo - d * 0.18, hi + d * 0.12
    n = len(x)
    xs = [ml + (W - ml - mr) * i / (n - 1) for i in range(n)]

    def PY(v):
        return mt + (H - mt - mb) * (1 - (v - lo) / (hi - lo))

    out = svg()
    shades = ["h2", "h3", "h4"]
    for k, b in enumerate(bands):
        pts = ["%.1f,%.1f" % (xs[i], PY(b["hi"][i])) for i in range(n)]
        pts += ["%.1f,%.1f" % (xs[i], PY(b["lo"][i])) for i in range(n - 1, -1, -1)]
        out.append('    <polygon points="%s" fill="%s"/>' % (" ".join(pts), col(shades[k % 3])))
        out.append(T(W - mr + 8, PY(b["hi"][-1]) + 5, "%s%s" % (fmt(b["hi"][-1], dec), unit),
                     "start", "vl mute"))
    out.append(T(W - mr + 8, PY(bands[0]["lo"][-1]) + 5,
                 "%s%s" % (fmt(bands[0]["lo"][-1], dec), unit), "start", "vl mute"))
    out.append('    <polyline class="ln" style="--c:%s" points="%s"/>'
               % (col("r1"), " ".join("%.1f,%.1f" % (xs[i], PY(p50[i])) for i in range(n))))
    out.append('    <circle class="pt" style="--c:%s" cx="%.1f" cy="%.1f" r="5"/>'
               % (col("r1"), xs[-1], PY(p50[-1])))
    out.append(T(W - mr + 8, PY(p50[-1]) + 5, "%s%s" % (fmt(p50[-1], dec), unit), "start", "vl"))
    out.append(L(ml, H - mb, W - mr, H - mb))
    for i, lb in enumerate(x):
        out.append(T(xs[i], H - mb + 22, lb, "middle"))
    if s.get("split") is not None:
        sx = xs[int(s["split"])]
        out.append(L(sx, mt, sx, H - mb, "stroke:var(--muted); stroke-width:1; stroke-dasharray:4 4"))
        out.append(T(sx + 8, mt + 12, "전망", "start", "lb", "fill:var(--muted); font-weight:750"))
    return done(out, s)


# ------------------------------------------------------------------ 4. EV-Equity 브릿지
def evbridge(s):
    """기업가치에서 주주가치까지. 항목마다 색이 다르고 기둥 사이를 연결선이 잇는다."""
    items = s["items"]                    # [라벨, 값, kind]  kind: tot|less|plus
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 24.0, 24.0, 34.0, 44.0
    tops, bots, run = [], [], 0.0
    for lab, v, kind in items:
        if kind == "tot":
            run = v
            bots.append(0.0)
            tops.append(v)
        else:
            a, b = (run, run + v) if v >= 0 else (run + v, run)
            bots.append(a)
            tops.append(b)
            run += v
    mx = max(tops) * 1.12 or 1
    n = len(items)
    step = (W - ml - mr) / n

    def PY(v):
        return mt + (H - mt - mb) * (1 - v / mx)

    fills = {"tot": col("rule"), "plus": col("r2"), "less": col("h4")}
    out = svg()
    run = 0.0
    for i, ((lab, v, kind), b, t) in enumerate(zip(items, bots, tops)):
        cx = ml + step * i + step / 2
        wdt = step * 0.56
        out.append(R(cx - wdt / 2, PY(t), wdt, PY(b) - PY(t), fills.get(kind, col("r2")), 3))
        sign = "" if kind == "tot" else ("+" if v > 0 else "")
        out.append(T(cx, PY(t) - 10, "%s%s%s" % (sign, fmt(v, dec), unit), "middle", "vl"))
        out.append(T(cx, H - mb + 22, lab, "middle", "lb", "fill:var(--ink); font-weight:750"))
        if kind != "tot" and s.get("pct"):
            out.append(T(cx, H - mb + 40, s["pct"][i], "middle"))
        run = v if kind == "tot" else run + v
        if i < n - 1:
            y = PY(run)
            out.append(L(cx + wdt / 2, y, cx + step - wdt / 2, y,
                         "stroke:var(--line); stroke-width:1; stroke-dasharray:3 3"))
    out.append(L(ml, H - mb, W - mr, H - mb))
    return done(out, s)


# ------------------------------------------------------------------ 5. 수익 원천 분해
def irr(s):
    """LBO 수익이 어디서 나왔나. 100% 로 쪼개고 절대금액을 아래에 단다."""
    parts = s["parts"]                    # {"label","v"}
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt = 24.0, 24.0, 58.0
    tot = float(sum(p["v"] for p in parts)) or 1.0
    bh = 96.0
    ramp = ["r1", "r2", "r3", "r4"]
    out = svg()
    if s.get("headline"):
        out.append(T(ml, 26, s["headline"], "start", "vl", "fill:var(--ink); font-size:19px"))
    x = ml
    for i, p in enumerate(parts):
        w = (W - ml - mr) * p["v"] / tot
        cn = ramp[i % len(ramp)]
        out.append(R(x, mt, w, bh, col(cn), 3, ' stroke="var(--bg)" stroke-width="2"'))
        pct = p["v"] / tot * 100
        if w > 60:
            fill = "fill:var(--ink)" if cn in ("r4", "r5") else "fill:var(--bg)"
            out.append(T(x + w / 2, mt + bh / 2 + 7, "%d%%" % round(pct), "middle", "vl",
                         fill + "; font-size:20px"))
        out.append(T(x + w / 2, mt + bh + 28, p["label"], "middle", "lb",
                     "fill:var(--ink); font-size:15px; font-weight:750"))
        out.append(T(x + w / 2, mt + bh + 50, "%s%s" % (fmt(p["v"], dec), unit), "middle", "vl mute"))
        x += w
    return done(out, s)


# ------------------------------------------------------------------ 6. 2단 분해 트리
def tree2(s):
    """위 한 칸이 아래 여러 칸의 곱. 그 아래가 또 쪼개진다."""
    root = s["root"]                      # {"label","v"}
    mid = s["mid"]                        # [{"label","v","op"}]
    leaf = s.get("leaf", {})              # {mid_index: [{"label","v"}]}
    ml, mr = 30.0, 30.0
    bw = (W - ml - mr - 40 * (len(mid) - 1)) / len(mid)
    out = svg()
    rw, rh = 250.0, 62.0
    rx = W / 2 - rw / 2
    out.append(R(rx, 6, rw, rh, col("rule"), 8))
    out.append(T(W / 2, 28, root["label"], "middle", "lb", "fill:var(--faint); font-weight:800"))
    out.append(T(W / 2, 54, root["v"], "middle", "vl", "fill:var(--bg); font-size:26px"))
    ytop = 104.0
    for i, m in enumerate(mid):
        x = ml + (bw + 40) * i
        cx = x + bw / 2
        out.append(L(cx, 84, cx, ytop, "stroke:var(--line); stroke-width:1"))
        out.append(L(cx, 84, W / 2, 84, "stroke:var(--line); stroke-width:1"))
        out.append(L(W / 2, 68 + rh - 62, W / 2, 84, "stroke:var(--line); stroke-width:1"))
        out.append(R(x, ytop, bw, 60, col("bg"), 8,
                     ' stroke="var(--line)" stroke-width="1"'))
        out.append(R(x, ytop, bw, 3, col(["r2", "r3", "r4"][i % 3]), 0))
        out.append(T(cx, ytop + 24, m["label"], "middle", "lb",
                     "fill:var(--muted); font-weight:800"))
        out.append(T(cx, ytop + 50, m["v"], "middle", "vl", "fill:var(--ink); font-size:24px"))
        if i:
            out.append(T(x - 20, ytop + 38, m.get("op", "×"), "middle", "lb",
                         "fill:var(--faint); font-size:22px; font-weight:800"))
        kids = leaf.get(str(i)) or leaf.get(i) or []
        if kids:
            kw = (bw - 12 * (len(kids) - 1)) / len(kids)
            for j, k in enumerate(kids):
                kx = x + (kw + 12) * j
                out.append(L(kx + kw / 2, ytop + 60, kx + kw / 2, ytop + 76,
                             "stroke:var(--line2); stroke-width:1"))
                out.append(R(kx, ytop + 76, kw, 46, col("h1"), 6))
                out.append(T(kx + kw / 2, ytop + 95, k["label"], "middle", "lb",
                             "fill:var(--muted); font-size:12.5px; font-weight:700"))
                out.append(T(kx + kw / 2, ytop + 114, k["v"], "middle", "vl",
                             "fill:var(--ink); font-size:16px"))
    return done(out, s)


# ------------------------------------------------------------------ 7. 사분위 상자
def box(s):
    """동종 분포를 상자로 그리고 자사를 마름모로 얹는다."""
    rows = s["rows"]                      # {"label","min","q1","med","q3","max","self"}
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 250.0, 60.0, 26.0, 36.0
    allv = [v for r in rows for v in (r["min"], r["max"], r["self"])]
    lo, hi = min(allv), max(allv)
    d = (hi - lo) or 1
    lo, hi = lo - d * 0.1, hi + d * 0.1
    n = len(rows)
    band = (H - mt - mb) / n

    def PX(v):
        return ml + (W - ml - mr) * (v - lo) / (hi - lo)

    out = svg()
    for i, r in enumerate(rows):
        y = mt + band * i + band / 2
        bh = min(band * 0.5, 24)
        out.append(L(PX(r["min"]), y, PX(r["max"]), y, "stroke:var(--line); stroke-width:1.5"))
        for k in ("min", "max"):
            out.append(L(PX(r[k]), y - bh / 3, PX(r[k]), y + bh / 3,
                         "stroke:var(--line); stroke-width:1.5"))
        out.append(R(PX(r["q1"]), y - bh / 2, PX(r["q3"]) - PX(r["q1"]), bh, col("h3"), 3))
        out.append(L(PX(r["med"]), y - bh / 2, PX(r["med"]), y + bh / 2,
                     "stroke:var(--r1); stroke-width:2.5"))
        sx = PX(r["self"])
        out.append('    <polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                   % (sx, y - 10, sx + 9, y, sx, y + 10, sx - 9, y, col("a3")))
        out.append(T(ml - 18, y + 5, r["label"], "end", "lb", NAME))
        out.append(T(W - mr + 8, y + 5, "%s%s" % (fmt(r["self"], dec), unit), "start", "vl",
                     "fill:var(--a3t)"))
    out.append(T(ml, H - mb + 22, "상자 = 1~3분위 · 세로선 = 중앙값 · 마름모 = 자사", "start"))
    return done(out, s)


# ------------------------------------------------------------------ 8. 격차 막대
def dumbbell(s):
    """자사와 기준값을 점 두 개로 찍고 벌어진 폭을 선으로 잇는다."""
    rows = sorted(s["rows"], key=lambda r: -(r["a"] - r["b"]))
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 250.0, 96.0, 26.0, 36.0
    allv = [v for r in rows for v in (r["a"], r["b"])]
    lo, hi = min(allv), max(allv)
    d = (hi - lo) or 1
    lo, hi = lo - d * 0.15, hi + d * 0.15
    n = len(rows)
    band = (H - mt - mb) / n

    def PX(v):
        return ml + (W - ml - mr) * (v - lo) / (hi - lo)

    out = svg()
    for i, r in enumerate(rows):
        y = mt + band * i + band / 2
        xa, xb = PX(r["a"]), PX(r["b"])
        up = r["a"] >= r["b"]
        out.append(L(min(xa, xb), y, max(xa, xb), y,
                     "stroke:var(--%s); stroke-width:5" % ("r3" if up else "riskB")))
        out.append('    <circle cx="%.1f" cy="%.1f" r="7" fill="%s"/>' % (xb, y, col("h4")))
        out.append('    <circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>'
                   % (xa, y, col("r1") if up else col("risk")))
        out.append(T(ml - 18, y + 5, r["label"], "end", "lb", NAME))
        gap = r["a"] - r["b"]
        out.append(T(W - mr + 10, y + 5, "%s%s%s" % ("+" if gap > 0 else "", fmt(gap, dec), unit),
                     "start", "vl", "fill:var(--%s)" % ("a1t" if up else "riskT")))
    out.append(T(ml, H - mb + 22, s.get("legend", "옅은 점 = 동종 중앙값 · 진한 점 = 자사"), "start"))
    return done(out, s)


# ------------------------------------------------------------------ 9. 궤적 산점도
def trail(s):
    """같은 회사가 몇 해에 걸쳐 어디로 움직였나."""
    paths = s["paths"]                    # {"label","pts":[[x,y,연도]], "hi":bool}
    ml, mr, mt, mb = 60.0, 60.0, 34.0, 44.0
    xs = [p[0] for pa in paths for p in pa["pts"]]
    ys = [p[1] for pa in paths for p in pa["pts"]]
    x0 = s.get("xmin", min(xs) - (max(xs) - min(xs)) * 0.15)
    x1 = s.get("xmax", max(xs) + (max(xs) - min(xs)) * 0.15)
    y0 = s.get("ymin", min(ys) - (max(ys) - min(ys)) * 0.2)
    y1 = s.get("ymax", max(ys) + (max(ys) - min(ys)) * 0.25)

    def PX(v):
        return ml + (W - ml - mr) * (v - x0) / ((x1 - x0) or 1)

    def PY(v):
        return mt + (H - mt - mb) * (1 - (v - y0) / ((y1 - y0) or 1))

    out = svg()
    if s.get("xmid") is not None:
        out.append(L(PX(s["xmid"]), mt, PX(s["xmid"]), H - mb,
                     "stroke:var(--line); stroke-width:1; stroke-dasharray:5 5"))
    if s.get("ymid") is not None:
        out.append(L(ml, PY(s["ymid"]), W - mr, PY(s["ymid"]),
                     "stroke:var(--line); stroke-width:1; stroke-dasharray:5 5"))
    out.append(L(ml, H - mb, W - mr, H - mb))
    out.append(L(ml, mt, ml, H - mb))
    for pa in paths:
        hi = pa.get("hi")
        c = col("r1") if hi else col("h4")
        pts = " ".join("%.1f,%.1f" % (PX(p[0]), PY(p[1])) for p in pa["pts"])
        out.append('    <polyline points="%s" style="fill:none; stroke:%s; stroke-width:%s; '
                   'stroke-linecap:round; stroke-linejoin:round"/>'
                   % (pts, c, "3" if hi else "2"))
        for j, p in enumerate(pa["pts"]):
            last = j == len(pa["pts"]) - 1
            out.append('    <circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>'
                       % (PX(p[0]), PY(p[1]), 7 if last else 4, c))
            if len(p) > 2 and (last or j == 0) and hi:
                out.append(T(PX(p[0]), PY(p[1]) - 13, p[2], "middle", "vl mute"))
        rightward = pa["pts"][-1][0] >= pa["pts"][0][0]
        lx = PX(pa["pts"][-1][0]) + (12 if rightward else -12)
        out.append(T(lx, PY(pa["pts"][-1][1]) + 5, pa["label"],
                     "start" if rightward else "end",
                     "vl" if hi else "vl mute",
                     "fill:var(--a1t)" if hi else ""))
    if s.get("xlabel"):
        out.append(T(W - mr, H - mb + 30, s["xlabel"], "end", "lb", INK))
    if s.get("ylabel"):
        out.append(T(ml - 12, mt - 14, s["ylabel"], "start", "lb", INK))
    return done(out, s)


# ------------------------------------------------------------------ 10. 원가 곡선
def costcurve(s):
    """가로가 누적 물량, 세로가 단가. 폭이 곧 규모다."""
    cols_ = sorted(s["cols"], key=lambda c: c["cost"])
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 52.0, 40.0, 30.0, 44.0
    tw = float(sum(c["w"] for c in cols_)) or 1.0
    mx = max(c["cost"] for c in cols_) * 1.15
    price = s.get("price")
    out = svg()
    x = ml
    for c in cols_:
        w = (W - ml - mr) * c["w"] / tw
        h = (H - mt - mb) * c["cost"] / mx
        below = price is not None and c["cost"] <= price
        out.append(R(x, H - mb - h, w, h, col("r2" if below else "h4"), 0,
                     ' stroke="var(--bg)" stroke-width="1.5"'))
        if w > 42:
            out.append(T(x + w / 2, H - mb - h - 9, fmt(c["cost"], dec), "middle", "vl"))
            out.append(T(x + w / 2, H - mb + 22, c["label"], "middle", "lb",
                         "fill:var(--ink); font-weight:750"))
        x += w
    out.append(L(ml, H - mb, W - mr, H - mb))
    if price is not None:
        py = H - mb - (H - mt - mb) * price / mx
        out.append(L(ml, py, W - mr, py, "stroke:var(--a3); stroke-width:2; stroke-dasharray:6 4"))
        out.append(T(ml + 8, py - 10, "%s %s%s" % (s.get("pricelabel", "판가"), fmt(price, dec), unit),
                     "start", "vl", "fill:var(--a3t)"))
    out.append(T(ml, H - mb + 40, s.get("xlabel", "누적 물량"), "start", "lb", INK))
    return done(out, s)


# ------------------------------------------------------------------ 11. 흐름도
def sankey(s):
    """매출이 어디로 갈라져 이익이 되나. 띠 두께가 금액이다.

    이름과 금액은 띠 위에 얹지 않고 흰 칩으로 띄운다. 얇은 칸에서는 칩끼리 부딪히므로
    최소 간격만큼 밀어내고 마디에서 칩까지 가는 선을 긋는다.
    """
    stages = s["stages"]
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    mt, mb = 46.0, 20.0
    ph = H - mt - mb
    src = stages[0]
    tot = float(src["v"]) or 1.0
    cw = 22.0
    CH, GAP = 44.0, 50.0
    xs = [44.0, W * 0.38, W * 0.66]
    out = svg()

    def chip(x, ycen, name, val, anchor="start"):
        w = 158.0
        cx = x if anchor == "start" else x - w
        out.append(R(cx, ycen - CH / 2, w, CH, "var(--bg)", 7,
                     ' stroke="var(--line)" stroke-width="1"'))
        out.append(T(cx + 13, ycen - 3, name, "start", "lb",
                     "fill:var(--ink); font-size:14px; font-weight:750"))
        out.append(T(cx + 13, ycen + 17, "%s%s" % (fmt(val, dec), unit), "start", "vl",
                     "fill:var(--a1t); font-size:16px"))
        return cx

    def ribbon(x1, y1, x2, y2, h, c):
        m = (x1 + x2) / 2
        out.append('    <path d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f '
                   'L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" fill="%s"/>'
                   % (x1, y1, m, y1, m, y2, x2, y2,
                      x2, y2 + h, m, y2 + h, m, y1 + h, x1, y1 + h, c))

    def spread(centers):
        """칩이 겹치지 않게 아래로 밀고, 넘치면 통째로 올린다."""
        ys = list(centers)
        for i in range(1, len(ys)):
            ys[i] = max(ys[i], ys[i - 1] + GAP)
        over = (ys[-1] + CH / 2) - (H - 2)
        if over > 0:
            ys = [y - over for y in ys]
        return ys

    # 마디 좌표를 먼저 잡는다
    lvl1, y = [], mt
    for i, p in enumerate(stages[1]["parts"]):
        h = ph * p["v"] / tot
        lvl1.append((p, y, h))
        y += h

    out.append(R(xs[0], mt, cw, ph, col("r1"), 3))
    out.append(T(xs[0], mt - 14, "%s %s%s" % (src["label"], fmt(src["v"], dec), unit), "start",
                 "vl", "fill:var(--ink); font-size:17px"))

    for i, (p, y1, h) in enumerate(lvl1):
        ribbon(xs[0] + cw, y1, xs[1], y1, h, col("h4" if i == 0 else "h3"))
        out.append(R(xs[1], y1, cw, h, col("h4" if i == 0 else "r2"), 3))

    for i, (p, y1, h) in enumerate(lvl1):
        chip(xs[1] - 12, y1 + h / 2, p["label"], p["v"], "end")

    # 마지막 단은 칸이 얇아 칩이 부딪힌다. 밀어내고 선으로 잇는다
    leaves = []
    for p, y1, h in lvl1:
        if not p.get("split"):
            continue
        st = float(p["v"]) or 1.0
        y3 = y1
        for j, q in enumerate(p["split"]):
            hh = h * q["v"] / st
            leaves.append((q, y3, hh, j))
            y3 += hh
    if leaves:
        cys = spread([y3 + hh / 2 for _, y3, hh, _ in leaves])
        for (q, y3, hh, j), cy in zip(leaves, cys):
            ribbon(xs[1] + cw, y3, xs[2], y3, hh, col("h3" if j == 0 else "h2"))
            out.append(R(xs[2], y3, cw, hh, col("h4" if j == 0 else "r1"), 3))
            lx = xs[2] + cw + 26
            out.append(L(xs[2] + cw + 2, y3 + hh / 2, lx - 2, cy,
                         "stroke:var(--line); stroke-width:1"))
            chip(lx, cy, q["label"], q["v"])
    return done(out, s)


# ------------------------------------------------------------------ 12. 만기 사다리
def ladder(s):
    """차입금이 언제 돌아오나. 가용 유동성 선을 함께 긋는다."""
    years = s["years"]                    # {"label","parts":[..]}
    names = s["names"]
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ml, mr, mt, mb = 52.0, 40.0, 30.0, 44.0
    tots = [sum(y["parts"]) for y in years]
    mx = max(tots + [s.get("liquidity", 0)]) * 1.18 or 1
    n = len(years)
    step = (W - ml - mr) / n
    ramp = ["r1", "r2", "r3", "r4"]
    out = svg()
    for i, y in enumerate(years):
        cx = ml + step * i + step / 2
        wdt = step * 0.5
        acc = 0.0
        for j, p in enumerate(y["parts"]):
            h = (H - mt - mb) * p / mx
            out.append(R(cx - wdt / 2, H - mb - acc - h, wdt, h, col(ramp[j % len(ramp)]), 2,
                         ' stroke="var(--bg)" stroke-width="1.5"'))
            acc += h
        out.append(T(cx, H - mb - acc - 10, "%s%s" % (fmt(tots[i], dec), unit), "middle", "vl"))
        out.append(T(cx, H - mb + 22, y["label"], "middle", "lb",
                     "fill:var(--ink); font-weight:750"))
    if s.get("liquidity"):
        ly = H - mb - (H - mt - mb) * s["liquidity"] / mx
        out.append(L(ml, ly, W - mr, ly, "stroke:var(--a3); stroke-width:2; stroke-dasharray:6 4"))
        out.append(T(W - mr, ly - 10, "가용 유동성 %s%s" % (fmt(s["liquidity"], dec), unit),
                     "end", "vl", "fill:var(--a3t)"))
    out.append(L(ml, H - mb, W - mr, H - mb))
    lg = ['<div class="chart">', '  <div class="lg">']
    for nm, cn in zip(names, ramp):
        lg.append('    <span style="--c:%s"><i></i>%s</span>' % (col(cn), esc(nm)))
    lg.append("  </div>")
    body = done(out, s)
    return body.replace('<div class="chart">', "\n".join(lg), 1)


# ------------------------------------------------------------------ 13. 코호트 삼각
def cohort(s):
    """행이 갈수록 짧아지는 삼각 히트맵. 기간이 갈수록 남는 비율."""
    rows = s["rows"]                      # {"label", "v":[..]}
    cols_ = s["cols"]
    ml, mt = 132.0, 44.0
    cw = (W - ml - 20) / len(cols_)
    ch = (H - mt - 18) / len(rows)
    flat = [x for r in rows for x in r["v"]]
    lo, hi = min(flat), max(flat)
    span = (hi - lo) or 1
    out = svg()
    for j, c in enumerate(cols_):
        out.append(T(ml + cw * j + cw / 2, mt - 14, c, "middle", "lb",
                     "fill:var(--faint); font-weight:800"))
    for i, r in enumerate(rows):
        y = mt + ch * i
        out.append(T(ml - 14, y + ch / 2 + 5, r["label"], "end", "lb",
                     "fill:var(--ink); font-weight:750"))
        for j, v in enumerate(r["v"]):
            band = min(5, int((v - lo) / span * 5) + 1)
            out.append(R(ml + cw * j + 1.5, y + 1.5, cw - 3, ch - 3,
                         "var(--h%d)" % band, 3))
            out.append(T(ml + cw * j + cw / 2, y + ch / 2 + 5, "%d%%" % round(v), "middle", "vl",
                         "fill:var(--ink); font-size:14px"))
    return done(out, s)


BUILDERS = {"tornado": tornado, "mc": mc, "fan": fan, "evbridge": evbridge, "irr": irr,
            "tree2": tree2, "box": box, "dumbbell": dumbbell, "trail": trail,
            "costcurve": costcurve, "sankey": sankey, "ladder": ladder, "cohort": cohort}
