# -*- coding: utf-8 -*-
"""Project Seorin 재무진단 보고서를 조립한다.

    python build.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exhibits  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "reference", "재무진단_서린푸드.html")

CSS = """
:root{
  --paper:#EDF0F3; --panel:#F7F8FA; --plot:#FFFFFF;
  --ink:#0F1E2B; --ink-2:#3E5364; --ink-3:#758798;
  --rule:#C6D0D8; --rule-soft:#DDE3E8; --grid:#DCE3E8;
  --c-navy:#1B3A57; --c-ochre:#B3762B; --c-teal:#2E6F6B; --c-clay:#8C3B36;
  --c-slate:#7A8C9B; --c-sand:#C9B893;
  --pos:#2E6F6B; --neg:#8C3B36; --hl:#B3762B; --maxw:1140px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--paper);color:var(--ink);
  font-family:'Pretendard Variable',Pretendard,-apple-system,'Malgun Gothic',sans-serif;
  font-size:15.5px;line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 34px}
.serif{font-family:'Noto Serif KR','Pretendard Variable',serif}
.mono{font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace}

/* ---- masthead ---- */
.mast{border-bottom:2px solid var(--ink);padding:46px 0 34px;background:var(--panel)}
.mast .kick{display:flex;justify-content:space-between;align-items:baseline;
  font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.12em;color:var(--ink-3);
  border-bottom:1px solid var(--rule);padding-bottom:14px;margin-bottom:30px}
.mast h1{font-family:'Noto Serif KR',serif;font-weight:900;font-size:44px;line-height:1.28;
  letter-spacing:-.01em;max-width:21em}
.mast .sub{margin-top:18px;font-size:17px;color:var(--ink-2);max-width:46em}
.mast .meta{display:flex;gap:34px;flex-wrap:wrap;margin-top:26px;font-size:13px;color:var(--ink-3)}
.mast .meta b{color:var(--ink-2);font-weight:600;margin-right:7px}

/* ---- verdict ---- */
.verdict{margin:44px 0 0;padding:30px 34px;background:var(--plot);
  border:1px solid var(--rule);border-left:4px solid var(--c-ochre)}
.verdict .k{font-family:'IBM Plex Mono',monospace;font-size:11.5px;letter-spacing:.16em;
  color:var(--c-ochre);font-weight:700}
.verdict h2{font-family:'Noto Serif KR',serif;font-weight:700;font-size:25px;line-height:1.45;margin:10px 0 14px}
.verdict p{color:var(--ink-2);max-width:66em;margin-top:10px}
.verdict p b{color:var(--ink);font-weight:700}

/* ---- stat strip ---- */
.stats{display:grid;grid-template-columns:repeat(6,1fr);gap:1px;background:var(--rule);
  border:1px solid var(--rule);margin:26px 0 0}
.stat{background:var(--panel);padding:18px 20px}
.stat .k{font-size:11.5px;color:var(--ink-3);letter-spacing:.04em}
.stat .v{font-family:'IBM Plex Mono',monospace;font-size:21px;font-weight:700;margin-top:6px}
.stat .d{font-size:12px;color:var(--ink-3);margin-top:3px}
.stat .v.up{color:var(--pos)} .stat .v.dn{color:var(--neg)} .stat .v.hl{color:var(--c-ochre)}

/* ---- section ---- */
.sect{margin:74px 0 0}
.sect-head{display:grid;grid-template-columns:120px 1fr;gap:26px;
  border-top:2px solid var(--ink);padding-top:22px}
.sect-head .num{font-family:'IBM Plex Mono',monospace;font-size:13px;color:var(--ink-3);
  letter-spacing:.1em;padding-top:8px}
.sect-head h2{font-family:'Noto Serif KR',serif;font-weight:700;font-size:29px;line-height:1.4}
.sect-head p{margin-top:12px;color:var(--ink-2);max-width:62em}

/* ---- exhibit ---- */
.ex{margin:42px 0 0;background:var(--plot);border:1px solid var(--rule)}
.ex-head{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap;
  padding:20px 28px 16px;border-bottom:1px solid var(--rule-soft)}
.ex-no{font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:700;
  letter-spacing:.1em;color:var(--plot);background:var(--ink);padding:3px 10px;border-radius:2px}
.ex-head h3{font-family:'Noto Serif KR',serif;font-weight:700;font-size:21px;flex:1;min-width:280px}
.ex-head .tag{font-family:'IBM Plex Mono',monospace;font-size:11.5px;color:var(--ink-3)}
.ex-chart{padding:20px 24px 8px}
.ex-chart svg{width:100%;height:auto;display:block}
.ex-notes{display:flex;gap:26px;flex-wrap:wrap;padding:14px 28px 8px;border-top:1px solid var(--rule-soft)}
.ex-notes .n{display:flex;gap:9px;font-size:13px;color:var(--ink-2);max-width:31em;line-height:1.55}
.ex-notes .n i{flex:0 0 20px;height:20px;border:1.2px solid var(--ink-2);border-radius:50%;
  font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:700;
  display:flex;align-items:center;justify-content:center;margin-top:2px}
.ex-src{padding:8px 28px 16px;font-size:11.5px;color:var(--ink-3)}

/* ---- svg text ---- */
svg text{font-family:'Pretendard Variable',Pretendard,sans-serif}
svg .t{font-size:13.5px;font-weight:700;fill:var(--ink)}
svg .l{font-size:12.5px;fill:var(--ink-2)}
svg .ls{font-size:11.5px;fill:var(--ink-3)}
svg .f{font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace;font-size:12.5px;fill:var(--ink)}
svg .fw{font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace;font-size:12px;fill:#fff;font-weight:700}

/* ---- closing table ---- */
.tblw{margin:42px 0 0;border:1px solid var(--rule);background:var(--plot);overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:13.5px;table-layout:fixed}
th,td{text-align:left;padding:13px 16px;border-bottom:1px solid var(--rule-soft);vertical-align:top;word-break:keep-all}
th{font-size:12px;color:var(--ink-3);font-weight:600;background:var(--panel);letter-spacing:.03em;white-space:nowrap}
td.num{font-family:'IBM Plex Mono',monospace;text-align:right;white-space:nowrap}
th.num{text-align:right}
td b{font-weight:700}
tr:last-child td{border-bottom:0}
tr.tot td{border-top:2px solid var(--ink);font-weight:700}

.method{margin:60px 0 0;padding:26px 0 0;border-top:1px solid var(--rule);
  font-size:13px;color:var(--ink-3);max-width:74em}
.method p{margin-bottom:8px}
footer{margin:50px 0 0;padding:20px 0 70px;border-top:2px solid var(--ink);
  display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;
  font-size:11.5px;color:var(--ink-3);letter-spacing:.08em}

@media print{
  body{background:#fff}
  .sect{break-before:page;margin-top:0;padding-top:30px}
  .ex,.verdict,.tblw{break-inside:avoid}
}
"""


def ex(no, title, tag, svg, notes, src):
    n = "".join('<div class="n"><i>%d</i><span>%s</span></div>' % (i + 1, t)
                for i, t in enumerate(notes))
    return ('<figure class="ex"><div class="ex-head"><span class="ex-no">EXHIBIT %s</span>'
            '<h3>%s</h3><span class="tag">%s</span></div>'
            '<div class="ex-chart">%s</div>'
            '<div class="ex-notes">%s</div>'
            '<div class="ex-src">%s</div></figure>' % (no, title, tag, svg, n, src))


def sect(num, title, desc):
    return ('<section class="sect"><div class="sect-head"><div class="num">%s</div>'
            '<div><h2>%s</h2><p>%s</p></div></div>' % (num, title, desc))


B = []
B.append("""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>서린푸드 재무진단 · Project Seorin</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700;900&family=IBM+Plex+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>""" + CSS + """</style></head><body>""")

B.append("""
<header class="mast"><div class="wrap">
  <div class="kick"><span>PROJECT SEORIN · FINANCIAL DIAGNOSTIC</span><span>2026.09 · CONFIDENTIAL · 예시 데이터</span></div>
  <h1 class="serif">48억을 벌어 14억이 남는 회사,<br>34억의 행방과 되찾는 순서</h1>
  <p class="sub">주식회사 서린푸드(가칭) 재무진단. 5개년 재무제표와 동종 12개사 비교에서 출발해, 현금이 묶인 자리를 지목하고, 3년 내 기업가치 74억원을 미는 세 가지 개입의 크기와 순서를 제시합니다.</p>
  <div class="meta">
    <span><b>대상</b>식품 제조·유통, 매출 320억</span>
    <span><b>기준</b>2025 회계연도 · 단위 억원</span>
    <span><b>구성</b>전시물 9매 · 진단 요약 1매</span>
    <span><b>주의</b>회사명과 숫자는 전부 예시</span>
  </div>
</div></header>

<div class="wrap">

<div class="verdict">
  <div class="k">VERDICT · 한 줄 판정</div>
  <h2 class="serif">손익은 최상급으로 좋아졌고, 그 이익의 71%가 회사 안에 갇혀 있습니다.</h2>
  <p>매출은 2년에 24% 늘고 영업이익률은 6.6%에서 9.1%로 올랐습니다. 여기까지만 보면 이 회사는 잘 굴러갑니다. 그런데 EBITDA 48억 중 잉여현금으로 나온 것은 14억, <b>전환율 29%</b>입니다. 늘어난 재고가 14억을 삼켰고, 판가보다 비싼 외주 물량이 연 6.8억을 되돌려 놓고 있으며, 온라인 채널은 굴러갈수록 자본비용을 밑도는 수익을 냅니다.</p>
  <p>결론은 매각도 긴축도 아닙니다. <b>재고 12일, 외주 단가 190원, 온라인 손익분기.</b> 이 세 숫자를 18개월 안에 움직이면 연간 영업이익 9.3억이 더해지고, 같은 배수에서 기업가치는 381억에서 455억으로 갑니다.</p>
  <div class="stats">
    <div class="stat"><div class="k">매출 (2025)</div><div class="v">320억</div><div class="d">전년 +11.5%</div></div>
    <div class="stat"><div class="k">EBITDA 마진</div><div class="v up">15.0%</div><div class="d">동종 중앙값과 동률</div></div>
    <div class="stat"><div class="k">FCF 전환율</div><div class="v dn">29%</div><div class="d">전년 34%에서 하락</div></div>
    <div class="stat"><div class="k">현금 회전일</div><div class="v dn">57일</div><div class="d">동종 중앙값 45.5일</div></div>
    <div class="stat"><div class="k">ROIC 대 WACC</div><div class="v">+2.7%p</div><div class="d">온라인만 역전</div></div>
    <div class="stat"><div class="k">계획 기업가치</div><div class="v hl">455억</div><div class="d">현재 381억, +19%</div></div>
  </div>
</div>
""")

# ---------------- Section A
B.append(sect("PART I", "실적의 표면과 실질",
              "손익계산서가 말하는 것과 현금흐름표가 말하는 것이 갈라지는 지점부터 확인합니다. 갈라지는 폭이 이 진단 전체의 출발점입니다."))
B.append(ex("01", "성장의 질은 좋습니다. 단가와 믹스가 만든 24%입니다", "손익 5개년 · 억원, %",
            exhibits.ex01(),
            ["2024~2025년 증분 33억 중 27억이 단가 인상과 제품 믹스 개선분입니다. 물량으로 밀어붙인 성장이 아니므로 마진과 동행합니다. 다만 같은 기간 대형 거래처 2곳 이탈로 12억이 빠졌고, 그 출처는 Exhibit 07에서 다룹니다."],
            "예시 데이터 · 감사보고서 5개년, 관리회계 월 마감"))
B.append(ex("02", "EBITDA는 7억 늘었는데 잉여현금은 그대로입니다", "EBITDA → FCF 2개년 · 억원",
            exhibits.ex02(),
            ["운전자본 투자가 9억에서 14억으로 늘며 이익 증가분을 전부 삼켰습니다.",
             "전환율 29%는 동종 상위권(50~60%)의 절반 수준입니다. 이 갭이 닫히면 연 10억 안팎의 현금이 추가로 풀립니다."],
            "예시 데이터 · 현금흐름표 재구성, 이자·법인세는 현금 지급 기준"))
B.append("</section>")

# ---------------- Section B
B.append(sect("PART II", "현금이 묶인 자리",
              "묶인 현금 46억을 시간축, 추이, 동종 분포의 세 방향에서 봅니다. 세 방향이 전부 같은 곳을 가리킵니다. 재고입니다."))
B.append(ex("03", "매입에서 수금까지 109일, 그중 57일이 회사 돈입니다", "현금전환주기 3면 분석 · 2025 평잔",
            exhibits.ex03(),
            ["공급사가 대주는 52일을 빼면 순 46억이 운전자본에 상시 잠겨 있습니다.",
             "6분기 동안 매출채권은 46→41일로 잡혔습니다. 못 잡은 것은 재고 하나입니다. 55일에서 68일이 됐습니다.",
             "동종 12사 중 10위. 중앙값과의 격차 11.5일은 현금 약 8억원과 같습니다."],
            "예시 데이터 · DSO는 매출, DIO·DPO는 매출원가 기준. 평잔. 동종은 매출 100~500억 식품 제조 12사"))
B.append(ex("04", "재고 43억을 열어 보면 문제는 두 칸에 몰려 있습니다", "카테고리 × 연령 · 억원",
            exhibits.ex04(),
            ["61일이 지난 유통 완제품 3.0억은 회전이 사실상 멈춘 SKU 41개입니다. 정리 대상이지 관리 대상이 아닙니다.",
             "원재료 14억 중 8억은 주요 곡물의 안전재고 약정분이라 구조적입니다. 손댈 수 있는 것과 없는 것을 갈라야 목표 12일이 현실이 됩니다."],
            "예시 데이터 · 재고수불부 2025.12 기준, 연령은 최종 입고일 기산"))
B.append("</section>")

# ---------------- Section C
B.append(sect("PART III", "사업의 구조",
              "전사 평균이 지우고 있는 것들입니다. 어느 사업부가 가치를 만들고 어느 채널이 깎는지, 원가는 어느 구간에서 새는지, 고객 기반은 어느 해에 금이 갔는지."))
B.append(ex("05", "온라인 28억은 굴러갈수록 가치를 깎습니다", "이익 풀과 자본수익률 · 2025",
            exhibits.ex05(),
            ["급식과 오프라인 유통이 이익의 3분의 2를 만들고, 이익률은 가공이 가장 높습니다. 면적이 곧 영업이익이므로 어디를 키울지가 이 그림에서 정해집니다.",
             "온라인은 ROIC 3.1%로 자본비용 8.2%를 밑돕니다. 성장 투자가 아니라 손익 설계 문제입니다. 물류비 단가가 오프라인의 2.6배입니다."],
            "예시 데이터 · 사업부 손익은 본사비 배부 후, ROIC는 투하자본 평잔 기준"))
B.append(ex("06", "외주 26천 톤은 판가보다 260원 비싸게 만듭니다", "원가 곡선 · 원/kg, 천 톤",
            exhibits.ex06(),
            ["연 6.8억의 역마진이 전사 평균 원가에 가려져 있었습니다. 재협상으로 190원을 회수하면 연 4.9억, 잔여 70원은 3공장 증설 타당성 검토와 함께 묶어서 판단합니다."],
            "예시 데이터 · 단위당 총원가(고정비 배부 포함), 폭은 2025년 생산량"))
B.append(ex("07", "2023년에 받은 거래처가 다릅니다", "수주 코호트와 집중도",
            exhibits.ex07(),
            ["다른 해 수주는 3년차에 84~86%를 지키는데 2023년 수주만 80%로 꺾였습니다. 그해 대형 신규 2건이 저마진·단기 조건이었고, Exhibit 01의 이탈 12억이 바로 이 두 건입니다.",
             "상위 3사가 매출의 42%입니다. 집중 자체보다, 신규를 조건 없이 받는 관행이 코호트를 통해 3년 뒤 이탈로 돌아온다는 것이 교훈입니다."],
            "예시 데이터 · 거래처 금액 기준 유지율, 개시년 100 기준"))
B.append("</section>")

# ---------------- Section D
B.append(sect("PART IV", "가치와 실행",
              "세 가지 개입을 기업가치로 환산하고, 18개월의 실행 순서와 3년 현금 궤적으로 닫습니다. 숫자 하나가 아니라 범위와 리스크를 함께 놓습니다."))
B.append(ex("08", "같은 배수에서 기업가치 381억이 455억이 됩니다", "가치 브릿지와 실행 리스크 · 억원",
            exhibits.ex08(),
            ["가장 큰 리스크는 외주 재협상 폭입니다. 전혀 성사되지 않으면 계획 455억이 416억까지 내려옵니다. 그래도 현재보다 35억 위입니다.",
             "배수 확대는 계획에 넣지 않았습니다. 7.9배 유지 가정이므로, 시장이 좋아지면 위 숫자는 보수적인 쪽입니다."],
            "예시 데이터 · EV/EBITDA 7.9배 고정, 개입별 연간 영업이익 효과 × 배수"))
B.append(ex("09", "18개월의 순서와 3년의 현금 궤적", "실행 로드맵 · 누적 FCF 억원",
            exhibits.ex09(),
            ["재협상과 S&OP는 투자 없이 바로 시작합니다. 증설 검토만 자본이 걸리므로 타당성 관문을 26.4Q에 둡니다. 3년 누적 잉여현금은 현행 56억, 계획 89억, 하방 시나리오로도 68억입니다."],
            "예시 데이터 · 밴드는 개입 성사율 시나리오(하방: 재협상 절반, 온라인 1년 지연)"))

# ---------------- 진단 요약표
B.append("""
<div class="tblw"><table>
<thead><tr><th style="width:19%">진단</th><th style="width:24%">개입</th>
<th class="num" style="width:13%">연간 손익 효과</th><th class="num" style="width:12%">기업가치 효과</th><th style="width:8%">시한</th><th>먼저 확인할 것</th></tr></thead>
<tbody>
<tr><td><b>재고 68일</b><span style="color:var(--ink-3)"> · 동종 +11.5일</span></td>
    <td>S&amp;OP 도입 · SKU 정리 · 약정 재계약. 효과는 일회성 현금 방출</td>
    <td class="num">이자 0.4억</td><td class="num">+7.6억</td>
    <td>12개월</td><td>안전재고 약정의 해지 조항</td></tr>
<tr><td><b>외주 역마진 연 6.8억</b></td>
    <td>단가 재협상 −190원, 잔여는 증설 검토</td>
    <td class="num">+4.9억</td><td class="num">+39억</td>
    <td>6개월</td><td>외주사 원가 구조와 대체 공급선</td></tr>
<tr><td><b>온라인 ROIC 3.1%</b></td>
    <td>가격·믹스 재설계, 물류 3PL 통합</td>
    <td class="num">+1.8억</td><td class="num">+14억</td>
    <td>12개월</td><td>채널별 배송비 실측 데이터</td></tr>
<tr><td><b>가공 마진 13.3%</b></td>
    <td>믹스 확대 (캐파 내 우선 배정)</td>
    <td class="num">+2.6억</td><td class="num">+21억</td>
    <td>18개월</td><td>3공장 잔여 캐파 실사</td></tr>
<tr class="tot"><td>합계</td><td></td><td class="num">+9.3억</td>
    <td class="num">+74억 (+19%)</td><td colspan="2"></td></tr>
</tbody></table></div>

<div class="method">
  <p><b>방법과 한계.</b> 회사명·숫자·동종 비교군은 전부 예시입니다. DSO는 매출, DIO·DPO는 매출원가로 나눴고 평잔 기준입니다. 기업가치 환산은 EV/EBITDA 7.9배 고정 가정이며 배수 변동은 Exhibit 08의 토네이도에만 반영했습니다. 사업부 손익은 본사비 배부 후 기준이라 배부 기준이 바뀌면 온라인의 적자 폭이 달라질 수 있습니다.</p>
  <p><b>이 보고서가 답하지 않은 것.</b> 인수·매각 등 구조적 대안, 세무 최적화, 그리고 증설 투자의 상세 타당성. 셋 다 이 진단의 후속 과제입니다.</p>
</div>

<footer><span>PROJECT SEORIN · 2026.09</span><span>예시 데이터 · 배포 전 검토 필요</span></footer>
</div></body></html>""")

io.open(OUT, "w", encoding="utf-8").write("\n".join(B))
print("wrote", OUT, "bytes", os.path.getsize(OUT))
