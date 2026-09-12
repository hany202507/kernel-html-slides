# -*- coding: utf-8 -*-
"""숫자 -> 인쇄 안전 차트 조각(HTML) 생성기.

좌표와 백분율을 손으로 쓰지 않기 위한 도구다. 축을 0에서 시작시키고,
라벨을 붙일 지점을 골라주고, 강조 하나만 색을 남긴다.

    python mkchart.py spec.json          # 조각을 stdout 으로
    python mkchart.py spec.json -o f.html

spec 예시는 파일 맨 아래 SPECS 참고. type 은 여섯 가지:
    bars   가로 막대   항목 비교(순위)
    sbar   100% 누적   구성비 (파이 대신)
    cols   세로 막대   시간 흐름 / 단일 계열
    stack  누적 세로   구성비 x 시간
    wf     워터폴      A 에서 B 로 간 이유
    line   꺾은선      시계열 추세 (계열 1~3)
    dot    산점        두 변수의 관계

색은 토큰 이름으로만 준다: a1 a2 a3 risk rule line.
"""
import io
import json
import sys

TOKEN = {"a1", "a2", "a3", "risk", "rule", "line", "faint", "muted",
         "r1", "r2", "r3", "r4", "r5", "h1", "h2", "h3", "h4", "h5",
         "bg", "card", "tint", "ink", "body"}

# 구성비는 서로 다른 색이 아니라 한 색의 농담으로 쌓는다. 그래야 총량이 먼저 읽힌다
RAMP = ["r2", "r3", "r4"]
LIGHT = {"r4", "r5", "h1", "h2", "h3", "h4", "h5"}   # 흰 글자가 안 보이는 칸


def col(name):
    if name not in TOKEN:
        raise SystemExit("색은 토큰 이름만 쓴다: %s" % sorted(TOKEN))
    return "var(--%s)" % name


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fmt(v, dec=0):
    """실무 반올림. 임원 자료에 소수점을 끌고 가지 않는다."""
    if dec == 0:
        return "{:,.0f}".format(v)
    return ("{:,.%df}" % dec).format(v)


# --------------------------------------------------------------- 막대류
def bars(s):
    rows = s["rows"]                      # [[라벨, 값], ...]
    hi = s.get("hi", [])                  # 강조할 행 번호 목록 (없으면 전부 강조)
    hi = [hi] if isinstance(hi, int) else list(hi)
    c = col(s.get("color", "a1"))
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    mx = max(abs(v) for _, v in rows) or 1
    out = ['<div class="chart">', '  <div class="bars" style="--lw:%s">' % s.get("labelw", "190px")]
    for i, (lab, v) in enumerate(rows):
        mute = "" if (not hi or i in hi) else " mute"
        out.append(
            '    <div class="b%s" style="--c:%s"><div class="bl">%s</div>'
            '<div class="bt"><div class="bf" style="--p:%.1f%%"></div>'
            '<div class="bv">%s%s</div></div></div>'
            % (mute, c, esc(lab), abs(v) / mx * 88, fmt(v, dec), esc(unit))
        )
    out.append("  </div>")
    return tail(out, s)


def sbar(s):
    names = s["names"]                    # 구간 이름
    colors = s.get("colors", RAMP)
    out = ['<div class="chart">', '  <div class="lg">']
    for n, cn in zip(names, colors):
        out.append('    <span style="--c:%s"><i></i>%s</span>' % (col(cn), esc(n)))
    out += ["  </div>", '  <div class="sbar" style="--lw:%s">' % s.get("labelw", "168px")]
    for row in s["rows"]:                 # {"label":.., "parts":[..]}
        tot = sum(row["parts"]) or 1
        out.append('    <div class="s"><div class="sl">%s</div><div class="st">' % esc(row["label"]))
        for j, p in enumerate(row["parts"]):
            pct = p / tot * 100
            cn = colors[j % len(colors)]
            cls = "lt" if cn in LIGHT else ""
            show = "<b>%d%%</b>" % round(pct) if pct >= 7 else ""
            out.append('      <i class="%s" style="--p:%.2f%%; --c:%s">%s</i>'
                       % (cls, pct, col(cn), show))
        out.append("    </div></div>")
    out.append("  </div>")
    return tail(out, s)


def _grid(out, mx, dec=0, unit=""):
    """옅은 가로 격자 둘. 그보다 많으면 데이터보다 격자가 진해진다"""
    for f in (0.5, 1.0):
        out.append('    <i class="gr" style="--gy:%.3f"><b>%s%s</b></i>'
                   % (f * 0.88, fmt(mx * f, dec), esc(unit)))


def cols(s):
    x, v = s["x"], s["v"]
    hi = s.get("hi", [])
    hi = [hi] if isinstance(hi, int) else list(hi)
    c = col(s.get("color", "a1"))
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    mx = max(v) or 1                      # 축은 0 에서 시작한다
    out = ['<div class="chart">', '  <div class="cols">']
    _grid(out, mx, dec, unit)
    for i, (lx, lv) in enumerate(zip(x, v)):
        mute = "" if (not hi or i in hi) else " mute"
        out.append(
            '    <div class="col%s"><div class="cv">%s%s</div>'
            '<div class="stk" style="--h:%.1f%%"><i style="--c:%s"></i></div>'
            '<div class="cx">%s</div></div>'
            % (mute, fmt(lv, dec), esc(unit), lv / mx * 88, c, esc(lx))
        )
    out.append("  </div>")
    return tail(out, s)


def stack(s):
    x, series = s["x"], s["series"]       # series: [{"name":.., "v":[..]}]
    colors = s.get("colors", RAMP)
    totals = [sum(sr["v"][i] for sr in series) for i in range(len(x))]
    mx = max(totals) or 1
    out = ['<div class="chart">', '  <div class="lg">']
    for sr, cn in zip(series, colors):
        out.append('    <span style="--c:%s"><i></i>%s</span>' % (col(cn), esc(sr["name"])))
    out += ["  </div>", '  <div class="cols">']
    _grid(out, mx, s.get("dec", 0), s.get("unit", ""))
    for i, lx in enumerate(x):
        t = totals[i]
        out.append('    <div class="col"><div class="cv">%s</div>'
                   '<div class="stk" style="--h:%.1f%%">' % (fmt(t, s.get("dec", 0)), t / mx * 88))
        for j, sr in enumerate(series):
            out.append('      <i style="--s:%.2f%%; --c:%s"></i>'
                       % (sr["v"][i] / (t or 1) * 100, col(colors[j % len(colors)])))
        out.append('    </div><div class="cx">%s</div></div>' % esc(lx))
    out.append("  </div>")
    return tail(out, s)


def wf(s):
    """items: [[라벨, 값, 종류], ...]

    종류는 색을 정한다. 부호가 아니라 **좋고 나쁨**으로 고른다 -- 마감일이 줄어드는 것은
    음수지만 좋은 일이므로 good 이다.
        tot   시작·끝 기둥 (잉크색)
        good  유리하게 움직인 항목 (강조색)
        bad   불리하게 움직인 항목 (경고색)
        ""    지정 안 하면 음수를 bad 로 본다 (금액 기준)
    """
    items = s["items"]
    dec, unit = s.get("dec", 0), s.get("unit", "")
    base, tops, bots, running = 0.0, [], [], 0.0
    for lab, v, kind in items:
        if kind == "tot":
            running = v
            bots.append(0.0); tops.append(v)
        else:
            lo, hi_ = (running, running + v) if v >= 0 else (running + v, running)
            bots.append(lo); tops.append(hi_)
            running += v
    mx = max(tops) or 1
    levels = []                           # 각 기둥이 끝나는 높이 (연결선 자리)
    run = 0.0
    for lab, v, kind in items:
        run = v if kind == "tot" else run + v
        levels.append(run)
    out = ['<div class="chart">', '  <div class="cols" style="--ml:0px">']
    for idx, ((lab, v, kind), lo, hi_) in enumerate(zip(items, bots, tops)):
        if kind == "tot":
            cls = "col fl tot"
        elif kind == "good":
            cls = "col fl"
        elif kind == "bad":
            cls = "col fl dn"
        else:
            cls = "col fl" + (" dn" if v < 0 else "")
        h = (hi_ - lo) / mx * 88
        y = lo / mx * 88
        sign = "" if kind == "tot" else ("+" if v > 0 else "")
        cn = ('<i class="cn" style="--cy:%.4f"></i>' % (levels[idx] / mx * 0.88)
              if idx < len(items) - 1 else "")
        out.append(
            '    <div class="%s" style="--y:%.1f%%"><div class="cv">%s%s%s</div>'
            '<div class="stk" style="--h:%.1f%%"><i style="--c:%s"></i></div>'
            '%s<div class="cx">%s</div></div>'
            % (cls, y, sign, fmt(v, dec), esc(unit), max(h, 1.2),
               col(s.get("color", "a1")), cn, esc(lab))
        )
    out.append("  </div>")
    return tail(out, s)


# --------------------------------------------------------------- SVG 류
# 캔버스 비율을 본문 자리(약 1088 x 250)에 맞춘다.
# 이 비율이 어긋나면 meet 로 축소되면서 SVG 안의 글자만 작아진다
W, H = 1160.0, 250.0
ML, MR, MT, MB = 46.0, 74.0, 26.0, 36.0


def _axis(out, xs, labels):
    out.append('    <line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
               % (ML, H - MB, W - MR, H - MB))
    for px, lb in zip(xs, labels):
        out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                   % (px, H - MB + 22, esc(lb)))


def line(s):
    x, series = s["x"], s["series"]       # [{"name":.., "v":[..], "color":"a1"}]
    dec, unit = s.get("dec", 0), s.get("unit", "")
    allv = [v for sr in series for v in sr["v"]]
    if s.get("zero", True):
        lo, hi_ = 0.0, (max(allv) or 1)
    else:
        # 축을 자를 때는 위아래로 숨 쉴 자리를 남긴다. 선이 천장에 붙으면 라벨이 겹친다
        d = (max(allv) - min(allv)) or 1
        lo, hi_ = min(allv) - d * 0.25, max(allv) + d * 0.18
    span = (hi_ - lo) or 1
    n = len(x)
    # 계열 이름은 오른쪽 끝에 붙는다. 이름이 길면 그만큼 여백을 넓혀야 잘리지 않는다.
    # 16px 글꼴 기준으로 한글 한 자 16px, 영문·숫자·빈칸은 그 절반으로 본다
    def _nw(t):
        return sum(16.0 if ord(c) > 0x2000 else 8.0 for c in t)
    MRx = max(MR, max(_nw(sr["name"]) for sr in series) + 20)
    xs = [ML + (W - ML - MRx) * (i / (n - 1 if n > 1 else 1)) for i in range(n)]

    def py(v):
        return MT + (H - MT - MB) * (1 - (v - lo) / span)

    out = ['<div class="chart">', '  <div class="plot">',
           '  <svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    for g in range(1, 4):                 # 옅은 가로 격자 3줄 이상 쓰지 않는다
        gy = MT + (H - MT - MB) * g / 4
        out.append('    <line class="gl" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                   % (ML, gy, W - MRx, gy))
    _axis(out, xs, x)
    for k, sr in enumerate(series):
        c = col(sr.get("color", ["a1", "a2", "a3"][k % 3]))
        mute = " mute" if sr.get("mute") else ""
        pts = " ".join("%.1f,%.1f" % (px, py(v)) for px, v in zip(xs, sr["v"]))
        out.append('    <polyline class="ln%s" style="--c:%s" points="%s"/>' % (mute, c, pts))
        # 라벨은 끝점과 꼭짓점. 계열이 둘 이상이면 첫 점은 안 찍는다 -- 서로 겹친다
        if sr.get("mute"):
            mark = set()
        else:
            mark = {n - 1}
            if len(series) <= 2:                 # 계열이 셋이면 꼭짓점 라벨이 옆 선을 밟는다
                mark.add(sr["v"].index(max(sr["v"])))
            if len(series) == 1:
                mark.add(0)
        for i in sorted(mark):
            out.append('    <circle class="pt%s" style="--c:%s" cx="%.1f" cy="%.1f" r="4.5"/>'
                       % (mute, c, xs[i], py(sr["v"][i])))
            anc = "start" if i == 0 else ("end" if i == n - 1 else "middle")
            dx = 8 if i == 0 else (-8 if i == n - 1 else 0)
            out.append('    <text class="vl%s" x="%.1f" y="%.1f" text-anchor="%s">%s%s</text>'
                       % (mute, xs[i] + dx, py(sr["v"][i]) - 12, anc, fmt(sr["v"][i], dec), esc(unit)))
        out.append('    <text class="vl%s" style="fill:%s" x="%.1f" y="%.1f">%s</text>'
                   % (mute, c, W - MRx + 10, py(sr["v"][-1]) + 5, esc(sr["name"])))
    out += ["  </svg>", "  </div>"]
    return tail(out, s)


def dot(s):
    pts = s["points"]                     # [[x, y, 라벨(선택)], ...]
    xl, yl = s.get("xlabel", ""), s.get("ylabel", "")
    xv = [p[0] for p in pts]; yv = [p[1] for p in pts]
    xlo, xhi = 0.0, max(xv) or 1
    ylo, yhi = 0.0, max(yv) or 1
    out = ['<div class="chart">', '  <div class="plot">',
           '  <svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    out.append('    <line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (ML, H - MB, W - MR, H - MB))
    out.append('    <line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (ML, MT, ML, H - MB))
    for p in pts:
        px = ML + (W - ML - MR) * (p[0] - xlo) / ((xhi - xlo) or 1)
        py = MT + (H - MT - MB) * (1 - (p[1] - ylo) / ((yhi - ylo) or 1))
        hi_ = len(p) > 3 and p[3]
        out.append('    <circle class="pt%s" style="--c:%s" cx="%.1f" cy="%.1f" r="%s"/>'
                   % ("" if hi_ else " mute", col(s.get("color", "a1")), px, py, 7 if hi_ else 5))
        if len(p) > 2 and p[2]:
            out.append('    <text class="vl%s" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                       % ("" if hi_ else " mute", px, py - 13, esc(p[2])))
    if xl:
        out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="end">%s</text>' % (W - MR, H - MB + 24, esc(xl)))
    if yl:
        out.append('    <text class="lb" x="%.1f" y="%.1f">%s</text>' % (ML, MT - 8, esc(yl)))
    out += ["  </svg>", "  </div>"]
    return tail(out, s)


# --------------------------------------------------------------- 재무분석 뷰
def ccc(s):
    """운전자본 회전(Cash Conversion Cycle). dio + dso - dpo"""
    dio, dso, dpo = float(s["dio"]), float(s["dso"]), float(s["dpo"])
    cyc = dio + dso
    val = cyc - dpo
    mx = max(cyc, dpo) or 1
    unit = s.get("unit", "일")

    def row(cls, lab, x, w, c, txt, v, hollow=False):
        return ('    <div class="r%s"><div class="rl">%s</div><div class="rt">'
                '<div class="rb%s" style="--x:%.2f%%; --w:%.2f%%; --c:%s">%s</div>'
                '</div><div class="rv">%s%s</div></div>'
                % (cls, esc(lab), " hollow" if hollow else "",
                   x / mx * 100, w / mx * 100, c, txt, fmt(v), esc(unit)))

    out = ['<div class="chart">', '  <div class="ccc" style="--lw:%s">' % s.get("labelw", "168px")]
    out.append(row("", "재고 (DIO)", 0, dio, col("a1"), "매입에서 판매까지", dio))
    out.append(row("", "매출채권 (DSO)", dio, dso, col("a2"), "판매에서 수금까지", dso))
    out.append(row("", "매입채무 (DPO)", 0, dpo, col("a3"), "지급을 미룬 기간", dpo, hollow=True))
    out.append(row(" tot", "현금 회전일", dpo, val, col("rule"), "내 돈으로 버티는 구간", val))
    out.append("  </div>")
    return tail(out, s)


def heat(s):
    """민감도 표. 값의 크기를 다섯 칸으로만 나눈다"""
    rows, cols_, v = s["rows"], s["cols"], s["v"]
    dec, unit = s.get("dec", 0), s.get("unit", "")
    flat = [x for r in v for x in r]
    lo, hi_ = min(flat), max(flat)
    span = (hi_ - lo) or 1
    base = s.get("base")                  # [행번호, 열번호] 기준 시나리오
    hw = s.get("headw", 20)
    cw = (100.0 - hw) / len(cols_)
    out = ['<div class="tbl">', "  <table>",
           '    <colgroup><col style="width:%d%%">' % hw
           + '<col style="width:%.1f%%">' % cw * len(cols_) + "</colgroup>",
           '    <thead><tr><th>%s</th>' % esc(s.get("corner", ""))
           + "".join('<th class="num">%s</th>' % esc(c) for c in cols_) + "</tr></thead>",
           "    <tbody>"]
    for i, rl in enumerate(rows):
        cells = []
        for j, x in enumerate(v[i]):
            band = min(5, int((x - lo) / span * 5) + 1)
            b = " base" if base and base[0] == i and base[1] == j else ""
            cells.append('<td class="num h%d%s">%s%s</td>' % (band, b, fmt(x, dec), esc(unit)))
        out.append("      <tr><td><b>%s</b></td>%s</tr>" % (esc(rl), "".join(cells)))
    out += ["    </tbody>", "  </table>"]
    if s.get("cap"):
        out.append('  <div class="cap">%s</div>' % s["cap"])
    out.append("</div>")
    return "\n".join(out)


def rng(s):
    """축구장(football field). 방법마다 나온 값의 범위를 한 축에 겹쳐 놓는다"""
    rows = s["rows"]                      # {"label","lo","hi","color"}
    unit, dec = s.get("unit", ""), s.get("dec", 0)
    ref = s.get("ref")                    # {"label","v"}
    ml, mr, mt, mb = 240.0, 62.0, 16.0, 34.0
    hi_ = max(r["hi"] for r in rows)
    lo_ = min(r["lo"] for r in rows)
    if ref:
        hi_, lo_ = max(hi_, ref["v"]), min(lo_, ref["v"])
    # 축구장은 크기 비교가 아니라 범위 비교다. 여기서만 0 기준선을 풀어 준다
    lo_ = s.get("xmin", lo_ * 0.88)
    hi_ = s.get("xmax", hi_ * 1.05)
    n = len(rows)
    band = (H - mt - mb) / n

    def px(v):
        return ml + (W - ml - mr) * (v - lo_) / ((hi_ - lo_) or 1)

    out = ['<div class="chart">', '  <div class="plot">',
           '  <svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    if ref:
        rx = px(ref["v"])
        out.append('    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                   'style="stroke:var(--rule); stroke-width:2"/>' % (rx, mt - 4, rx, H - mb + 2))
        out.append('    <text class="vl" x="%.1f" y="%.1f" text-anchor="middle">%s %s%s</text>'
                   % (rx, H - mb + 22, esc(ref["label"]), fmt(ref["v"], dec), esc(unit)))
    for i, r in enumerate(rows):
        y = mt + band * i + band / 2
        c = col(r.get("color", ["a1", "a2", "a3"][i % 3]))
        x1, x2 = px(r["lo"]), px(r["hi"])
        out.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="22" rx="5" fill="%s"/>'
                   % (x1, y - 11, max(x2 - x1, 3), c))
        out.append('    <text x="%.1f" y="%.1f" text-anchor="end" '
                   'style="fill:var(--ink); font-size:15px; font-weight:750">%s</text>'
                   % (ml - 14, y + 5, esc(r["label"])))
        out.append('    <text class="vl mute" x="%.1f" y="%.1f" text-anchor="end">%s</text>'
                   % (x1 - 8, y + 5, fmt(r["lo"], dec)))
        out.append('    <text class="vl" x="%.1f" y="%.1f">%s%s</text>'
                   % (x2 + 8, y + 5, fmt(r["hi"], dec), esc(unit)))
    out += ["  </svg>", "  </div>"]
    return tail(out, s)


def bubble(s):
    """두 축 + 크기. 세그먼트 배치, 성장-수익성 매트릭스"""
    pts = s["points"]                     # {"x","y","r","label","hi"}
    ml, mr, mt, mb = 58.0, 58.0, 30.0, 42.0
    xs = [p["x"] for p in pts]
    ys = [p["y"] for p in pts]
    x0 = s.get("xmin", min(xs + [0]))
    x1 = s.get("xmax", max(xs) * 1.15)
    y0 = s.get("ymin", min(ys + [0]))
    y1 = s.get("ymax", max(ys) * 1.2)
    rmax = max(p.get("r", 1) for p in pts) or 1

    def PX(v):
        return ml + (W - ml - mr) * (v - x0) / ((x1 - x0) or 1)

    def PY(v):
        return mt + (H - mt - mb) * (1 - (v - y0) / ((y1 - y0) or 1))

    out = ['<div class="chart">', '  <div class="plot">',
           '  <svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    if s.get("xmid") is not None:
        out.append('    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                   'style="stroke:var(--line); stroke-width:1; stroke-dasharray:5 5"/>'
                   % (PX(s["xmid"]), mt, PX(s["xmid"]), H - mb))
    if s.get("ymid") is not None:
        out.append('    <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                   'style="stroke:var(--line); stroke-width:1; stroke-dasharray:5 5"/>'
                   % (ml, PY(s["ymid"]), W - mr, PY(s["ymid"])))
    out.append('    <line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (ml, H - mb, W - mr, H - mb))
    out.append('    <line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (ml, mt, ml, H - mb))
    for p in pts:
        cx, cy = PX(p["x"]), PY(p["y"])
        rr = 11 + 28 * (p.get("r", 1) / rmax) ** 0.5
        c = col(p.get("color", "a1")) if p.get("hi") else "var(--line)"
        out.append('    <circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, rr, c))
        out.append('    <text class="vl%s" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                   % ("" if p.get("hi") else " mute", cx, cy - rr - 9, esc(p.get("label", ""))))
    dec = s.get("dec", 0)
    out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
               % (ml, H - mb + 24, fmt(x0, dec)))
    out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
               % (W - mr, H - mb + 24, fmt(x1, dec)))
    out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="end">%s</text>'
               % (ml - 10, H - mb + 4, fmt(y0, dec)))
    out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="end">%s</text>'
               % (ml - 10, mt + 10, fmt(y1, dec)))
    if s.get("xlabel"):
        out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="end" '
                   'style="fill:var(--ink); font-weight:750">%s</text>'
                   % (W - mr, min(H - 6.0, H - mb + 42), esc(s["xlabel"])))
    if s.get("ylabel"):
        out.append('    <text class="lb" x="%.1f" y="%.1f" '
                   'style="fill:var(--ink); font-weight:750">%s</text>'
                   % (ml - 10, max(14.0, mt - 22), esc(s["ylabel"])))
    out += ["  </svg>", "  </div>"]
    return tail(out, s)


def combo(s):
    """막대 하나 + 선 하나. 축이 둘이면 범례에 단위를 함께 적는다"""
    x = s["x"]
    bv, lv = s["bars"]["v"], s["line"]["v"]
    ml, mr, mt, mb = 52.0, 52.0, 26.0, 38.0
    bmax = max(bv) or 1
    lmax = max(lv) or 1
    n = len(x)
    step = (W - ml - mr) / n
    bc = col(s["bars"].get("color", "a1"))
    lc = col(s["line"].get("color", "a3"))
    out = ['<div class="chart">', '  <div class="lg">',
           '    <span style="--c:%s"><i></i>%s</span>' % (bc, esc(s["bars"]["name"])),
           '    <span style="--c:%s"><i></i>%s</span>' % (lc, esc(s["line"]["name"])),
           "  </div>", '  <div class="plot">',
           '  <svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    out.append('    <line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (ml, H - mb, W - mr, H - mb))
    for i, v in enumerate(bv):
        h = (H - mt - mb) * v / bmax * 0.82
        cx = ml + step * i + step / 2
        out.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s"/>'
                   % (cx - step * 0.26, H - mb - h, step * 0.52, h, bc))
        out.append('    <text class="vl" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                   % (cx, H - mb - h - 9, fmt(v, s.get("bdec", 0))))
        out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                   % (cx, H - mb + 22, esc(x[i])))
    pts = " ".join("%.1f,%.1f" % (ml + step * i + step / 2,
                                  mt + (H - mt - mb) * (1 - v / lmax * 0.82))
                   for i, v in enumerate(lv))
    out.append('    <polyline class="ln" style="--c:%s" points="%s"/>' % (lc, pts))
    for i, v in enumerate(lv):
        cx = ml + step * i + step / 2
        cy = mt + (H - mt - mb) * (1 - v / lmax * 0.82)
        out.append('    <circle class="pt" style="--c:%s" cx="%.1f" cy="%.1f" r="4.5"/>' % (lc, cx, cy))
        if i in (0, n - 1):
            out.append('    <text class="vl" style="fill:%s" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                       % (lc, cx, cy - 13, fmt(v, s.get("ldec", 1))))
    out += ["  </svg>", "  </div>"]
    return tail(out, s)


def mekko(s):
    """가변 폭 누적 세로 막대. 폭이 규모, 높이가 구성비다"""
    cs = s["cols"]                        # {"label","w","parts","wlabel"}
    names = s["names"]
    palette = s.get("colors", RAMP)
    ml, mr, mt, mb = 34.0, 34.0, 22.0, 46.0
    gap = 8.0
    tw = sum(c["w"] for c in cs) or 1
    avail = (W - ml - mr) - gap * (len(cs) - 1)
    out = ['<div class="chart">', '  <div class="lg">']
    for nm, cn in zip(names, palette):
        out.append('    <span style="--c:%s"><i></i>%s</span>' % (col(cn), esc(nm)))
    out += ["  </div>", '  <div class="plot">',
            '  <svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid meet" role="img">' % (W, H)]
    xcur = ml
    for c in cs:
        w = avail * c["w"] / tw
        tot = sum(c["parts"]) or 1
        ytop = mt
        for j, p in enumerate(c["parts"]):
            h = (H - mt - mb) * p / tot
            out.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                       'stroke="var(--bg)" stroke-width="1.5"/>'
                       % (xcur, ytop, w, h, col(palette[j % len(palette)])))
            if h > 22 and w > 48:
                cn = palette[j % len(palette)]
                fill = "var(--ink)" if cn in LIGHT else "var(--bg)"
                out.append('    <text x="%.1f" y="%.1f" text-anchor="middle" '
                           'style="fill:%s; font-size:14px; font-weight:800">%d%%</text>'
                           % (xcur + w / 2, ytop + h / 2 + 5, fill, round(p / tot * 100)))
            ytop += h
        out.append('    <text x="%.1f" y="%.1f" text-anchor="middle" '
                   'style="fill:var(--ink); font-size:15px; font-weight:750">%s</text>'
                   % (xcur + w / 2, H - mb + 22, esc(c["label"])))
        out.append('    <text class="lb" x="%.1f" y="%.1f" text-anchor="middle">%s</text>'
                   % (xcur + w / 2, H - mb + 41, esc(c.get("wlabel", ""))))
        xcur += w + gap
    out += ["  </svg>", "  </div>"]
    return tail(out, s)


# --------------------------------------------------------------- 공통 꼬리
def tail(out, s):
    if s.get("note"):
        out.append('  <div class="cnote">%s</div>' % s["note"])
    if s.get("source"):
        out.append('  <div class="csrc">%s</div>' % esc(s["source"]))
    out.append("</div>")
    return "\n".join(out)


BUILDERS = {"bars": bars, "sbar": sbar, "cols": cols, "stack": stack,
            "wf": wf, "line": line, "dot": dot,
            "ccc": ccc, "heat": heat, "range": rng, "bubble": bubble,
            "combo": combo, "mekko": mekko}


def build(spec):
    t = spec.get("type")
    if t not in BUILDERS:
        try:                              # 고급 전시물은 mkchart_adv 가 맡는다
            import mkchart_adv
            BUILDERS.update(mkchart_adv.BUILDERS)
        except ImportError:
            pass
    if t not in BUILDERS:
        raise SystemExit("type 은 %s 중 하나" % ", ".join(sorted(BUILDERS)))
    return BUILDERS[t](spec)


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    spec = json.loads(io.open(argv[0], encoding="utf-8").read())
    html = "\n\n".join(build(x) for x in spec) if isinstance(spec, list) else build(spec)
    if "-o" in argv:
        io.open(argv[argv.index("-o") + 1], "w", encoding="utf-8").write(html)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(html)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
