# -*- coding: utf-8 -*-
"""매출에서 잉여현금까지 한 줄기로 흘리는 머니플로우 생키.

손익계산서에서 끊지 않는다. 영업이익에 감가상각이 합류해 EBITDA가 되고,
거기서 운전자본·설비·이자·세금이 갈라져 나간 나머지가 잉여현금이다.
분기와 합류가 실제로 있는 구조라서 생키가 정당하다.
"""
from draw import G, fmt

K = 1.05          # 억원 -> px
BW = 15           # 노드 막대 폭


def _grad(g, gid, c1, c2, o1=.55, o2=.5):
    g.raw('<defs><linearGradient id="%s" x1="0" x2="1">'
          '<stop offset="0" stop-color="%s" stop-opacity="%s"/>'
          '<stop offset="1" stop-color="%s" stop-opacity="%s"/>'
          '</linearGradient></defs>' % (gid, c1, o1, c2, o2))


def _ribbon(g, x1, y1, h1, x2, y2, h2, fill):
    m = (x1 + x2) / 2
    g.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f "
           "C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z"
           % (x1, y1, m, y1, m, y2, x2, y2, x2, y2 + h2,
              m, y2 + h2, m, y1 + h1, x1, y1 + h1), fill)


def _tag(g, x, y, text, color="var(--c-clay)"):
    w = len(text) * 11.6 + 30
    g.rect(x, y, w, 24, "var(--plot)", 12, stroke=color, sw=1.2)
    g.txt(x + 15, y + 16.5, text, "f", fill=color, size=11.5, weight=700)
    return w


def sankey(d, sfx, deltas=None, H=560, k=None):
    """d: 흐름 사전. sfx: 그라디언트 id 접미사. deltas: 노드별 증감 문구.

    k 는 억원->px 축척. 캔버스를 줄이면 축척도 같이 줄여야 리본이 안 넘친다.
    """
    deltas = deltas or {}
    K = k if k else globals()["K"]
    g = G(1080, H, "매출에서 잉여현금까지의 자금 흐름 생키")
    NAVY, SLATE, OCHRE, TEAL, CLAY, SAND = ("#1B3A57", "#7A8C9B", "#B3762B",
                                            "#2E6F6B", "#8C3B36", "#C9B893")
    for gid, c1, c2, o1, o2 in (
            ("rc" + sfx, NAVY, SLATE, .5, .42), ("rs" + sfx, NAVY, OCHRE, .5, .42),
            ("ro" + sfx, NAVY, TEAL, .5, .55), ("oe" + sfx, TEAL, TEAL, .55, .6),
            ("de" + sfx, SAND, TEAL, .7, .45), ("ew" + sfx, TEAL, CLAY, .5, .5),
            ("ex" + sfx, TEAL, SLATE, .5, .45), ("ef" + sfx, TEAL, TEAL, .6, .85)):
        _grad(g, gid, c1, c2, o1, o2)

    rev, cogs, sga, op = d["rev"], d["cogs"], d["sga"], d["op"]
    dep, ebitda = d["dep"], d["ebitda"]
    outs = d["outs"]                       # [(이름, 값, 종류)] 종류: leak / final
    x_rev, x_s1, x_eb, x_s3 = 70, 420, 660, 916

    y0 = 96
    h_cogs, h_sga, h_op = cogs * K, sga * K, op * K
    s_cogs, s_sga, s_op = y0, y0 + h_cogs, y0 + h_cogs + h_sga
    d_cogs = y0 - 22
    d_sga = d_cogs + h_cogs + 30
    d_op = d_sga + h_sga + 30

    # ---- 매출 노드
    g.rect(x_rev, y0, BW, rev * K, "var(--c-navy)", 2)
    g.txt(x_rev - 12, y0 + rev * K / 2 - 8, "매출", "l", "end", fill="var(--ink)", weight=800, size=15)
    g.txt(x_rev - 12, y0 + rev * K / 2 + 12, fmt(rev) + "억", "f", "end", size=14, weight=700)

    # ---- 1단 분기
    _ribbon(g, x_rev + BW, s_cogs, h_cogs, x_s1, d_cogs, h_cogs, "url(#rc%s)" % sfx)
    _ribbon(g, x_rev + BW, s_sga, h_sga, x_s1, d_sga, h_sga, "url(#rs%s)" % sfx)
    _ribbon(g, x_rev + BW, s_op, h_op, x_s1, d_op, h_op, "url(#ro%s)" % sfx)

    g.rect(x_s1, d_cogs, BW, h_cogs, "var(--c-slate)", 2)
    g.txt(x_s1 + 26, d_cogs + h_cogs / 2 - 6, "매출원가  %s" % fmt(cogs, d.get("dec", 0)), "l",
          fill="var(--ink)", weight=800, size=14)
    g.txt(x_s1 + 26, d_cogs + h_cogs / 2 + 13, "매출의 %.0f%%" % (cogs / rev * 100), "ls")
    if "cogs" in deltas:
        g.txt(x_s1 + 26, d_cogs + h_cogs / 2 + 32, deltas["cogs"], "f",
              fill="var(--c-teal)", weight=700, size=12)

    g.rect(x_s1, d_sga, BW, h_sga, "var(--c-ochre)", 2)
    g.txt(x_s1 + 26, d_sga + h_sga / 2 + 1, "판매관리비  %s" % fmt(sga, d.get("dec", 0)), "l",
          fill="var(--ink)", weight=800, size=14)
    g.txt(x_s1 + 26, d_sga + h_sga / 2 + 20, "매출의 %.0f%%" % (sga / rev * 100), "ls")
    if "sga" in deltas:
        g.txt(x_s1 + 194, d_sga + h_sga / 2 + 1, deltas["sga"], "f",
              fill="var(--c-teal)", weight=700, size=12)

    # ---- 2단: 영업이익 + 감가상각 -> EBITDA
    h_eb = ebitda * K
    e_bot = d_op + h_op
    e_top = e_bot - h_eb
    h_dep = dep * K
    _ribbon(g, x_s1 + BW, d_op, h_op, x_eb, e_top + h_dep, h_op, "url(#oe%s)" % sfx)
    g.txt((x_s1 + x_eb) / 2 + 10, d_op + h_op + 18, "영업이익  %s" % fmt(op, d.get("dec", 0)),
          "l", "middle", fill="var(--c-teal)", weight=800, size=13.5)
    if "op" in deltas:
        g.txt((x_s1 + x_eb) / 2 + 10, d_op + h_op + 36, deltas["op"], "f", "middle",
              fill="var(--c-teal)", weight=700, size=12)

    dx, dy = x_s1 + 132, e_top - 86
    g.rect(dx, dy, BW, h_dep, "var(--c-sand)", 2)
    g.txt(dx + 24, dy - 6, "감가상각  %s" % fmt(dep), "l", fill="var(--ink)", weight=700, size=12.5)
    g.txt(dx + 24, dy + 11, "비현금 가산", "ls")
    _ribbon(g, dx + BW, dy, h_dep, x_eb, e_top, h_dep, "url(#de%s)" % sfx)

    g.rect(x_eb, e_top, BW, h_eb, "var(--c-teal)", 2)
    g.txt(x_eb + 8, e_bot + 20, "EBITDA %s억" % fmt(ebitda, d.get("dec", 0)), "l", "middle",
          fill="var(--ink)", weight=800, size=13.5)

    pos = {"cogs": (x_s1, d_cogs, h_cogs), "sga": (x_s1, d_sga, h_sga),
           "ebitda": (x_eb, e_top, h_eb), "outs": []}
    # ---- 3단 분기
    tot_out = sum(v for _, v, _ in outs)
    assert abs(tot_out - ebitda) < .35, (tot_out, ebitda)
    gaps = [16] * (len(outs) - 1) + [30]
    fan_h = sum(v * K for _, v, _ in outs) + sum(gaps)
    dt = max(e_top + h_eb / 2 - fan_h / 2, 46)
    sy = e_top
    for i, (name, v, kind) in enumerate(outs):
        hv = v * K
        fill = "url(#ef%s)" % sfx if kind == "final" else (
            "url(#ew%s)" % sfx if kind == "leak" else "url(#ex%s)" % sfx)
        _ribbon(g, x_eb + BW, sy, hv, x_s3, dt, hv, fill)
        bar_c = {"final": "var(--c-teal)", "leak": "var(--c-clay)"}.get(kind, "var(--c-slate)")
        g.rect(x_s3, dt, BW - 3, hv, bar_c, 2)
        big = kind == "final"
        g.txt(x_s3 + 24, dt + hv / 2 + (0 if big else 4.5),
              name, "l", fill="var(--ink)", weight=800 if big else 650,
              size=14.5 if big else 12.5)
        val = "%s억" % fmt(v, d.get("dec", 0))
        if big:
            g.txt(x_s3 + 24 + len(name) * 15 + 10, dt + hv / 2, val, "f",
                  fill="var(--c-teal)", size=17, weight=800)
            # 마지막 줄기가 바닥에 붙으면 이 설명이 viewBox 밖으로 나가 잘린다.
            # 아래로 넘칠 때만 값 위로 올린다
            sy = dt + hv / 2 + 21
            if sy > H - 6:
                sy = dt + hv / 2 - 20
            g.txt(x_s3 + 24, sy, d.get("final_sub", ""), "ls")
        else:
            g.txt(x_s3 + 24 + len(name) * 12.8 + 8, dt + hv / 2 + 4.5, val, "f",
                  fill="var(--ink-2)", size=12.5, weight=700)
        key = "out%d" % i
        if key in deltas:
            g.txt(x_s3 + 24, dt + hv / 2 + (40 if big else 22), deltas[key], "f",
                  fill="var(--c-teal)", weight=700, size=12)
        pos["outs"].append((x_s3, dt, hv))
        sy += hv
        dt += hv + gaps[i]

    return g, pos
