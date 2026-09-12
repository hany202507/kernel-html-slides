# -*- coding: utf-8 -*-
"""전시물용 SVG 프리미티브. 좌표는 전부 계산으로 나온다.

주석 장치가 이 보고서의 밀도를 만든다:
    bracket   구간 괄호 (CAGR, 합계 표시)
    marker    번호 원 (본문 주석과 연결)
    band      참조 띠 (동종 사분위, 목표 구간)
    chip      증감 칩 (+9.1% 같은 것)
    refline   기준선 + 라벨
"""

E = lambda s: (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fmt(v, dec=0):
    return ("{:,.%df}" % dec).format(v)


def sc(v, v0, v1, p0, p1):
    """값 v 를 [v0,v1] 에서 픽셀 [p0,p1] 로."""
    return p0 + (p1 - p0) * (v - v0) / ((v1 - v0) or 1)


class G:
    """SVG 조각 누적기."""

    def __init__(self, w, h, label=""):
        self.w, self.h = w, h
        self.b = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (w, h, E(label))]

    def raw(self, s):
        self.b.append(s)
        return self

    def rect(self, x, y, w, h, fill, rx=0, o=None, stroke=None, sw=1, dash=None):
        a = ''
        if o is not None:
            a += ' opacity="%s"' % o
        if stroke:
            a += ' stroke="%s" stroke-width="%s"' % (stroke, sw)
            if dash:
                a += ' stroke-dasharray="%s"' % dash
        self.b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s"%s/>'
                      % (x, y, max(w, .4), max(h, .4), rx, fill, a))
        return self

    def line(self, x1, y1, x2, y2, stroke="var(--rule-soft)", sw=1, dash=None, o=None):
        a = ' stroke="%s" stroke-width="%s"' % (stroke, sw)
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if o is not None:
            a += ' opacity="%s"' % o
        self.b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"%s/>' % (x1, y1, x2, y2, a))
        return self

    def txt(self, x, y, t, cls="l", anchor="start", fill=None, size=None, weight=None):
        st = ""
        if fill or size or weight:
            st = ' style="%s%s%s"' % ("fill:%s;" % fill if fill else "",
                                      "font-size:%spx;" % size if size else "",
                                      "font-weight:%s;" % weight if weight else "")
        self.b.append('<text x="%.1f" y="%.1f" class="%s" text-anchor="%s"%s>%s</text>'
                      % (x, y, cls, anchor, st, E(t)))
        return self

    def circle(self, x, y, r, fill, stroke=None, sw=1):
        a = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
        self.b.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (x, y, r, fill, a))
        return self

    def poly(self, pts, stroke, sw=2.5, fill="none", dash=None, o=None):
        a = ""
        if dash:
            a += ' stroke-dasharray="%s"' % dash
        if o is not None:
            a += ' opacity="%s"' % o
        self.b.append('<polyline points="%s" fill="%s" stroke="%s" stroke-width="%s" '
                      'stroke-linecap="round" stroke-linejoin="round"%s/>'
                      % (" ".join("%.1f,%.1f" % p for p in pts), fill, stroke, sw, a))
        return self

    def area(self, pts, fill, o=None):
        a = ' opacity="%s"' % o if o is not None else ""
        self.b.append('<polygon points="%s" fill="%s"%s/>'
                      % (" ".join("%.1f,%.1f" % p for p in pts), fill, a))
        return self

    def path(self, d, fill="none", stroke=None, sw=1, o=None):
        a = ""
        if stroke:
            a += ' stroke="%s" stroke-width="%s"' % (stroke, sw)
        if o is not None:
            a += ' opacity="%s"' % o
        self.b.append('<path d="%s" fill="%s"%s/>' % (d, fill, a))
        return self

    # ---------------- 주석 장치 ----------------
    def bracket(self, x1, x2, y, label, drop=6, up=True):
        """구간 괄호. up=True 면 라벨이 위."""
        d = -drop if up else drop
        self.line(x1, y, x1, y + d, "var(--ink-3)", 1)
        self.line(x2, y, x2, y + d, "var(--ink-3)", 1)
        self.line(x1, y + d, x2, y + d, "var(--ink-3)", 1)
        self.txt((x1 + x2) / 2, y + d + (-6 if up else 14), label, "f", "middle",
                 fill="var(--ink-2)", weight=600)
        return self

    def marker(self, x, y, n):
        """본문 주석과 연결되는 번호 원."""
        self.circle(x, y, 9.5, "var(--paper)", "var(--ink-2)", 1.2)
        self.txt(x, y + 4, str(n), "f", "middle", fill="var(--ink)", size=11, weight=700)
        return self

    def chip(self, x, y, v, dec=0, unit="", good=None):
        """증감 칩. good 지정이 없으면 양수를 긍정으로."""
        pos = (v > 0) if good is None else good
        c = "var(--pos)" if pos else "var(--neg)"
        t = ("▲" if v > 0 else "▼") + fmt(abs(v), dec) + unit
        w = 12 + len(t) * 7.4
        self.rect(x - w / 2, y - 10, w, 20, "var(--plot)", 10, stroke=c, sw=1)
        self.txt(x, y + 4, t, "f", "middle", fill=c, size=11.5, weight=700)
        return self

    def refline_v(self, x, y1, y2, label, color="var(--hl)", dash=None, label_y=None):
        self.line(x, y1, x, y2, color, 1.5, dash)
        self.txt(x, label_y if label_y is not None else y1 - 8, label, "ls", "middle", fill=color, weight=700)
        return self

    def refline_h(self, x1, x2, y, label, color="var(--hl)", dash="6 4", anchor="end", lx=None):
        self.line(x1, x2, is_h=True) if False else None
        self.line(x1, y, x2, y, color, 1.5, dash)
        self.txt(lx if lx is not None else x2, y - 8, label, "ls", anchor, fill=color, weight=700)
        return self

    def band_h(self, x1, x2, y1, y2, fill="var(--c-slate)", o=.14):
        self.rect(x1, y1, x2 - x1, y2 - y1, fill, 0, o)
        return self

    def connector(self, x1, y1, x2, y2):
        """주석 상자로 가는 얇은 연결선."""
        self.line(x1, y1, x2, y2, "var(--ink-3)", 1, "2 2", .8)
        return self

    def note(self, x, y, lines, w=None, anchor="start"):
        """차트 위 주석 상자."""
        w = w or (max(len(l) for l in lines) * 12.4 + 24)
        h = 16 + len(lines) * 18
        cx = x if anchor == "start" else x - w
        self.rect(cx, y, w, h, "var(--plot)", 3, stroke="var(--rule)", sw=1)
        for i, l in enumerate(lines):
            self.txt(cx + 12, y + 21 + i * 18, l, "l", fill="var(--ink-2)", size=12.5)
        return self

    def done(self):
        self.b.append("</svg>")
        return "\n".join(self.b)
