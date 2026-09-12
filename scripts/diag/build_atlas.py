# -*- coding: utf-8 -*-
"""고급 재무 전시물 아틀라스를 조립한다. 27종, 서린푸드 예시로 전부 이어진 숫자.

    python build_atlas.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import atlas_ex as A  # noqa: E402
import exhibits  # noqa: E402
import flow  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "reference", "전시물_아틀라스_독본.html")

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
.mast{border-bottom:2px solid var(--ink);padding:46px 0 30px;background:var(--panel)}
.mast .kick{display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;
  font-size:12px;letter-spacing:.12em;color:var(--ink-3);
  border-bottom:1px solid var(--rule);padding-bottom:14px;margin-bottom:28px}
.mast h1{font-family:'Noto Serif KR',serif;font-weight:900;font-size:42px;line-height:1.3}
.mast .sub{margin-top:14px;font-size:16.5px;color:var(--ink-2);max-width:48em}
.mast .meta{display:flex;gap:32px;flex-wrap:wrap;margin-top:22px;font-size:13px;color:var(--ink-3)}
.mast .meta b{color:var(--ink-2);font-weight:600;margin-right:7px}

nav.toc{position:sticky;top:0;z-index:20;background:var(--paper);border-bottom:1px solid var(--rule)}
nav.toc .wrap{display:flex;gap:0;overflow-x:auto}
nav.toc a{padding:11px 18px 10px;font-size:13px;font-weight:600;color:var(--ink-2);
  text-decoration:none;white-space:nowrap;border-bottom:2px solid transparent}
nav.toc a:hover{color:var(--ink);border-bottom-color:var(--c-ochre)}

.sect{margin:66px 0 0}
.sect-head{display:grid;grid-template-columns:110px 1fr;gap:24px;
  border-top:2px solid var(--ink);padding-top:20px}
.sect-head .num{font-family:'IBM Plex Mono',monospace;font-size:13px;color:var(--ink-3);padding-top:7px}
.sect-head h2{font-family:'Noto Serif KR',serif;font-weight:700;font-size:27px}
.sect-head p{margin-top:10px;color:var(--ink-2);max-width:62em}

.ex{margin:36px 0 0;background:var(--plot);border:1px solid var(--rule)}
.ex-head{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;
  padding:18px 28px 14px;border-bottom:1px solid var(--rule-soft)}
.ex-no{font-family:'IBM Plex Mono',monospace;font-size:11.5px;font-weight:700;
  letter-spacing:.1em;color:var(--plot);background:var(--ink);padding:3px 10px;border-radius:2px}
.ex-head h3{font-family:'Noto Serif KR',serif;font-weight:700;font-size:20px;flex:1;min-width:280px}
.ex-head .tag{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--ink-3)}
.ex-chart{padding:16px 22px 6px}
.ex-chart svg{width:100%;height:auto;display:block}
.ex-notes{display:flex;gap:30px;flex-wrap:wrap;padding:12px 28px 16px;
  border-top:1px solid var(--rule-soft);font-size:13px;color:var(--ink-2)}
.ex-notes .q b,.ex-notes .w b{font-weight:700}
.ex-notes .q{max-width:34em}
.ex-notes .q b{color:var(--c-navy)}
.ex-notes .w{max-width:34em}
.ex-notes .w b{color:var(--c-clay)}

svg text{font-family:'Pretendard Variable',Pretendard,sans-serif}
svg .t{font-size:13.5px;font-weight:700;fill:var(--ink)}
svg .l{font-size:12.5px;fill:var(--ink-2)}
svg .lb{font-size:12.5px;fill:var(--ink-2)}
svg .ls{font-size:11.5px;fill:var(--ink-3)}
svg .f{font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace;font-size:12.5px;fill:var(--ink)}
svg .fw{font-family:'IBM Plex Mono',ui-monospace,Consolas,monospace;font-size:12px;fill:#fff;font-weight:700}

.tblw{margin:0;border:0;background:var(--plot)}
table{border-collapse:collapse;width:100%;font-size:13.5px;table-layout:fixed}
th,td{text-align:left;padding:12px 18px;border-bottom:1px solid var(--rule-soft);
  vertical-align:top;word-break:keep-all}
th{font-size:12px;color:var(--ink-3);font-weight:600;background:var(--panel);white-space:nowrap}
td.num{font-family:'IBM Plex Mono',monospace;text-align:right;white-space:nowrap}
th.num{text-align:right}
tr.tot td{border-top:2px solid var(--ink);font-weight:700;border-bottom:0}

.method{margin:56px 0 0;padding:24px 0 0;border-top:1px solid var(--rule);
  font-size:13px;color:var(--ink-3);max-width:76em}
footer{margin:46px 0 0;padding:20px 0 64px;border-top:2px solid var(--ink);
  display:flex;justify-content:space-between;font-family:'IBM Plex Mono',monospace;
  font-size:11.5px;color:var(--ink-3);letter-spacing:.08em}
@media print{body{background:#fff}.ex{break-inside:avoid}.sect{break-before:page}}
"""


def ex(no, title, en, svg, q, warn):
    return ('<figure class="ex" id="e%s"><div class="ex-head"><span class="ex-no">EXHIBIT %s</span>'
            '<h3>%s</h3><span class="tag">%s</span></div>'
            '<div class="ex-chart">%s</div>'
            '<div class="ex-notes"><div class="q"><b>답하는 질문.</b> %s</div>'
            '<div class="w"><b>함정.</b> %s</div></div></figure>'
            % (no, no, title, en, svg, q, warn))


def sect(sid, num, title, desc):
    return ('<section class="sect" id="%s"><div class="sect-head"><div class="num">%s</div>'
            '<div><h2>%s</h2><p>%s</p></div></div>' % (sid, num, title, desc))


SU_TABLE = """<div class="tblw"><table>
<thead><tr><th style="width:26%">조달</th><th class="num" style="width:16%">금액 (억원)</th>
<th style="width:8%"></th><th style="width:26%">사용</th><th class="num" style="width:16%">금액 (억원)</th></tr></thead>
<tbody>
<tr><td><b>인수금융</b> · EBITDA의 4.4배</td><td class="num">210</td><td></td>
    <td><b>지분 인수대금</b></td><td class="num">380</td></tr>
<tr><td><b>우선주</b></td><td class="num">90</td><td></td>
    <td><b>거래 비용</b></td><td class="num">18</td></tr>
<tr><td><b>보통주</b></td><td class="num">120</td><td></td>
    <td><b>운전자금</b></td><td class="num">22</td></tr>
<tr class="tot"><td>합계</td><td class="num">420</td><td></td><td>합계</td><td class="num">420</td></tr>
</tbody></table></div>"""

B = ["""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>고급 재무 전시물 아틀라스 · 서린푸드 판</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@700;900&family=IBM+Plex+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css">
<style>""" + CSS + """</style></head><body>

<header class="mast"><div class="wrap">
  <div class="kick"><span>EXHIBIT ATLAS · SEORIN EDITION</span><span>2026.09 · 예시 데이터</span></div>
  <h1>딜과 컨설팅의 전시물 27종,<br>한 회사의 숫자로 전부 그렸습니다</h1>
  <p class="sub">유형 카탈로그가 아닙니다. 매출 320억 식품회사 서린푸드(가칭) 하나를 27개 각도에서 자른 것이라, 전시물끼리 숫자가 이어지고 제목이 곧 발견입니다. 제목만 위에서 아래로 읽어도 한 편의 진단이 됩니다.</p>
  <div class="meta">
    <span><b>수록</b>가치평가 6 · 딜 구조 4 · 실적 분해 6 · 시장 6 · 고객과 실행 5</span>
    <span><b>기준</b>2025 회계연도 · 억원</span>
    <span><b>주의</b>회사명과 숫자는 전부 예시</span>
  </div>
</div></header>

<nav class="toc"><div class="wrap">
  <a href="#p1">I 가치평가</a><a href="#p2">II 딜 구조</a><a href="#p3">III 실적·현금 분해</a>
  <a href="#p4">IV 시장·경쟁</a><a href="#p5">V 고객·실행</a>
</div></nav>

<div class="wrap">
"""]

# ================================================================ PART I
B.append(sect("p1", "PART I", "가치평가 · 값은 범위로 말한다",
              "한 숫자를 내놓는 순간 방어할 수 없게 됩니다. 범위, 분포, 흔들리는 폭, 그리고 그 범위가 동종 대비 싼지까지가 한 세트입니다."))
B.append(ex("01", "제시가 380억은 다섯 방법 중 셋의 범위 안입니다", "Football Field",
            A.football(),
            "방법마다 나온 가치 범위가 어디서 겹치는가.",
            "방법 이름 옆에 가정을 함께 적습니다. EV인지 지분가치인지 섞이면 그림이 통째로 틀립니다."))
B.append(ex("02", "EV 381억이 주주 손에 오면 305억입니다", "EV-to-Equity Bridge",
            A.evbridge(),
            "기업가치와 지분가치 사이에서 누가 얼마를 먼저 가져가는가.",
            "순차입금에 리스부채·우선주를 넣었는지가 협상 단골 분쟁입니다. 각주로 못 박습니다."))
B.append(ex("03", "성장 대비 0.4배 싸게 평가받고 있습니다", "Multiple Regression Scatter",
            A.regression(),
            "우리 배수가 싼 것인가, 성장이 느려서 그 배수인 것인가.",
            "점 다섯 개로 회귀선을 긋는 건 장식입니다. R²와 표본 수를 함께 적고, 낮으면 선을 지웁니다."))
B.append(ex("04", "열 번 중 한 번은 318억 아래입니다", "Monte Carlo Value Distribution",
            A.montecarlo(),
            "이 가치가 나올 확률이 얼마나 되는가.",
            "분포는 가정의 결과지 사실이 아닙니다. 어떤 분포를 몇 회 돌렸는지 출처에 적습니다."))
B.append(ex("05", "WACC 하나가 137억을 흔듭니다", "Tornado Diagram",
            A.tornado(),
            "협상에서 어느 가정부터 다퉈야 하는가. 위 두 줄이면 끝납니다.",
            "일변량입니다. 두 가정이 같이 움직이는 경우는 시나리오로 따로 봅니다. 흔든 폭을 라벨에 적지 않으면 비교가 성립하지 않습니다."))
B.append(ex("06", "현금 인수라면 420억까지 이익이 늘어납니다", "Accretion / Dilution Grid",
            A.accretion(),
            "인수가와 대금 구성 중 어느 조합까지 주당이익이 버티는가.",
            "첫해 회계 효과일 뿐 가치 판단이 아닙니다. 증가한다고 싼 것도, 희석된다고 비싼 것도 아닙니다."))
B.append("</section>")

# ================================================================ PART II
B.append(sect("p2", "PART II", "딜 구조 · 돈이 어디서 와서 누구에게 가는가",
              "대주단과 투자자가 실제로 밤에 보는 것들입니다. 조달의 균형, 수익의 원천, 회수 시나리오별 배분, 그리고 만기."))
B.append(ex("07", "양쪽 합계 420억이 맞지 않으면 표가 아니라 계산이 틀린 것입니다", "Sources & Uses",
            SU_TABLE,
            "인수 자금이 어디서 와서 어디로 가는가.",
            "합계 행이 없는 조달·사용 표는 검증 불가능합니다. 인수금융 배수를 조달 칸에 함께 적습니다."))
B.append(ex("08", "수익의 47%가 EBITDA 성장에서 나왔습니다", "Value Creation Attribution",
            A.attribution(),
            "돈을 번 원천이 실력(이익 성장)인가 시장(배수)인가 레버리지인가.",
            "네 조각의 합이 지분가치 증가분과 정확히 맞아야 합니다. 잔차를 만들지 말고 다시 쪼갭니다."))
B.append(ex("09", "회수 300억 아래서는 보통주 몫이 없습니다", "Cap Table Payoff Diagram",
            A.payoff(),
            "회수금액별로 각 증권이 얼마를 받는가. 우선순위의 실감.",
            "참가부·전환권이 붙으면 꺾임 위치가 달라집니다. 권리 조건을 그림 밖 각주가 아니라 선 옆에 적습니다."))
B.append(ex("10", "2028년에 58억이 한꺼번에 돌아옵니다", "Maturity Ladder",
            A.ladder(),
            "총 차입금이 아니라, 언제 얼마가 몰려 돌아오는가.",
            "리볼빙·한도대는 만기와 성격이 다릅니다. 섞지 말고 주석으로 밝힙니다. 유동성 선이 없으면 이 그림은 반쪽입니다."))
B.append("</section>")

# ================================================================ PART III
B.append(sect("p3", "PART III", "실적·현금 분해 · 어디서 벌고 어디서 새는가",
              "요약하지 않고 분해합니다. 매출의 원천, 손익에서 현금까지의 흐름, 묶인 운전자본, 수익성의 구조."))
B.append(ex("11", "33억 증가분 중 27억이 단가와 믹스입니다", "Price-Volume-Mix Bridge",
            A.pvm(),
            "매출이 얼마 늘었나가 아니라 무엇이 늘렸나.",
            "요인 합이 증가분과 안 맞으면 기타로 메우지 않습니다. 못 나눈 것은 못 나눴다고 적습니다."))
sank, _ = flow.sankey({"rev": 320, "cogs": 231, "sga": 60, "op": 29, "dep": 19, "ebitda": 48,
                       "outs": [("운전자본 증가", 14, "leak"), ("설비투자", 11, "mid"),
                                ("이자", 4, "mid"), ("법인세", 5, "mid"), ("잉여현금", 14, "final")],
                       "final_sub": "전환율 29%"}, "at", H=540)
B.append(ex("12", "320억이 들어와서 14억이 남습니다", "P&L-to-Cash Sankey",
            sank.done(),
            "1,000원이 들어와 최종적으로 얼마가 남고 나머지는 어디로 갔는가. 손익에서 끊지 않고 현금까지 잇습니다.",
            "화려해서 남용되기 쉽습니다. 흐름이 실제로 분기·합류하는 구조가 아니면 그냥 폭포가 낫습니다."))
B.append(ex("13", "매입에서 수금까지 109일, 그중 57일이 회사 돈입니다", "Cash Conversion Cycle 3면",
            exhibits.ex03(),
            "며칠이 걸리고, 몇 년째 그런지, 그게 돈으로 얼마인지를 한 장에서.",
            "DSO는 매출, DIO·DPO는 매출원가로 나눕니다. 평잔인지 기말인지 밝히지 않으면 계절성이 통째로 들어옵니다."))
B.append(ex("14", "이 ROE는 마진이 아니라 회전율이 만들었습니다", "DuPont Decomposition",
            A.dupont(),
            "ROE가 어느 항에서 왔고, 그 항은 또 무엇으로 되어 있는가.",
            "세 항의 곱이 ROE와 안 맞으면 평잔·기말이 섞인 것입니다. 두 단까지만 내려갑니다. 세 단이면 못 읽습니다."))
B.append(ex("15", "누적 생산 두 배마다 단가가 12% 내렸습니다", "Experience Curve (log-log)",
            A.experience(),
            "원가 하락이 우연인가 규모의 학습인가. 다음 두 배의 원가를 예측할 수 있는가.",
            "로그축임을 크게 적습니다. 선형으로 읽으면 하락이 멈춘 것처럼 보입니다. 원료가 급변한 해는 따로 표시합니다."))
B.append(ex("16", "외주 26천 톤은 판가보다 260원 비싸게 만듭니다", "Cost Curve",
            exhibits.ex06(),
            "어느 생산 구간이 판가를 밑도는가.",
            "고정비 배부 포함인지 변동비 기준인지에 따라 결론이 뒤집힙니다. 이 그림 하나로 계약 해지를 결정하지 않습니다."))
B.append("</section>")

# ================================================================ PART IV
B.append(sect("p4", "PART IV", "시장·경쟁 · 동종 안에서 어디에 있는가",
              "순위는 비교군이 바뀌면 뒤집힙니다. 분포의 어디인지, 어느 방향으로 움직이는지, 규모와 수익성을 동시에 봅니다."))
B.append(ex("17", "매출은 급식이 크고 이익률은 가공이 높습니다", "Marimekko",
            A.mekko(),
            "규모와 구성비를 한 그림에서. 면적이 곧 금액입니다.",
            "기둥이 다섯을 넘으면 라벨이 죽습니다. 작은 것은 기타로 묶고 묶었다고 밝힙니다."))
B.append(ex("18", "온라인만 스프레드가 음수인데 성장은 가장 빠릅니다", "ROIC Spread vs Growth",
            A.spread_bubble(),
            "성장이 가치를 만드는 사업인가 태우는 사업인가.",
            "스프레드가 음수인 사업의 성장은 축하가 아니라 경보입니다. 원 크기(투하자본)까지 세 변수라 그 이상 얹지 않습니다."))
B.append(ex("19", "2년 사이 서린푸드가 두 곳을 제쳤습니다", "Slope Graph",
            A.slope(),
            "순위가 어떻게 바뀌었는가. 시계열 다섯 개를 겹치는 것보다 두 시점이 명확할 때.",
            "중간 연도의 궤적은 지워집니다. 중간에 반전이 있었다면 이 형식이 그걸 숨깁니다."))
B.append(ex("20", "온라인만 여섯 분기 연속 내리막입니다", "Small Multiples",
            A.smallmult(),
            "네 사업부의 궤적을 겹치지 않고 나란히. 한 패널에 겹치면 선 네 개가 엉킵니다.",
            "모든 패널의 축과 기간을 동일하게 잡습니다. 패널마다 축이 다르면 이 형식은 거짓말이 됩니다."))
B.append(ex("21", "5년에 걸쳐 1분위 밖에서 중앙값까지 왔습니다", "Box Plot",
            A.box(),
            "순위가 아니라 분포의 어디에 있는가, 그리고 어느 방향으로 움직였는가.",
            "표본이 열둘이면 사분위가 성립하는 하한선입니다. 다섯 곳으로 상자를 그리지 않습니다."))
B.append(ex("22", "가공은 2.9%p 앞서고 온라인은 5.5%p 뒤집니다", "Dumbbell / Gap Chart",
            A.dumbbell(),
            "자사와 기준값이 항목별로 얼마나 벌어져 있는가.",
            "행끼리 단위가 같아야 합니다. 마진과 회전일을 한 그림에 놓으면 축이 무너집니다."))
B.append("</section>")

# ================================================================ PART V
B.append(sect("p5", "PART V", "고객·실행 · 남는 고객, 굴러가는 과제",
              "고객이 남아 있는가, 이익은 어느 고객에게서 오는가, 그리고 약속한 개선이 실제로 실현되고 있는가."))
B.append(ex("23", "상위 여덟 곳이 이익의 128%를 법니다", "Whale Curve",
            A.whale(),
            "이익이 어느 고객에게서 오고, 어느 고객이 도로 깎아 가는가.",
            "고객별 이익 배부(물류·영업비)가 절반의 싸움입니다. 배부 기준이 바뀌면 꼬리의 명단이 바뀝니다."))
B.append(ex("24", "2023년에 받은 거래처가 다릅니다", "Cohort Triangle + Pareto",
            A.cohort_pareto(),
            "언제 들어온 고객이 얼마나 남고, 매출은 몇 곳에 몰려 있는가.",
            "코호트의 빈 칸은 아직 그 기간을 안 지난 것입니다. 0으로 채우면 통째로 거짓말이 됩니다."))
B.append(ex("25", "3분기째, 실현은 계획의 70%입니다", "Synergy Phasing Curve",
            A.synergy(),
            "약속한 개선 이익이 계획 곡선 위에 있는가.",
            "계획선을 나중에 다시 그리면 이 그림은 무의미해집니다. 착수 시점의 계획선을 박제합니다."))
B.append(ex("26", "여덟 과제 중 하나가 궤도를 벗어났습니다", "Bowling Chart",
            A.bowling(),
            "과제별로 어느 분기에 무엇이 밀렸는가. 경영회의 한 장 요약.",
            "상태 색은 규칙으로 정합니다(지연 N주 = 주의). 담당자 자기 신고에 맡기면 전부 초록이 됩니다."))
B.append(ex("27", "2028년 매출은 352억에서 468억 사이입니다", "Fan Chart",
            A.fan(),
            "전망이 얼마나 넓게 벌어지는가. 실행 계획의 결과 범위를 정직하게.",
            "실적 구간에 띠를 씌우지 않습니다. 밴드는 둘까지, 셋이면 농담이 안 갈립니다."))
B.append("</section>")

B.append("""
<div class="method">
  <p><b>고르는 기준.</b> 막대로 답할 수 있으면 막대로 답합니다. 여기 27종은 전부 읽는 데 품이 더 드는 형식이라, 품을 들일 값이 있을 때만 씁니다. 분기·합류가 없으면 생키 대신 폭포, 두 시점이면 기울기, 분포면 상자, 세 변수면 버블까지. 네 번째 변수가 필요해지면 그림을 나눕니다.</p>
  <p><b>제목 규칙.</b> 유형 이름은 오른쪽 위 태그로 밀고, 제목 자리에는 그림이 발견한 사실을 적습니다. "토네이도 민감도"가 아니라 "WACC 하나가 137억을 흔듭니다"입니다.</p>
  <p><b>연속성.</b> 매출 320억 · EBITDA 48억 · CCC 57일 · EV 381억. 모든 전시물이 같은 회사의 같은 숫자에서 나왔고, 재무진단·머니플로우 보고서와도 이어집니다. 전부 예시 데이터입니다.</p>
</div>

<footer><span>EXHIBIT ATLAS · SEORIN EDITION · 2026.09</span><span>예시 데이터 · 배포 전 검토 필요</span></footer>
</div></body></html>""")

io.open(OUT, "w", encoding="utf-8").write("\n".join(B))
print("wrote", OUT, os.path.getsize(OUT), "bytes")
