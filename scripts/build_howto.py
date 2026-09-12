# -*- coding: utf-8 -*-
"""스킬 사용법 덱. 받는 사람이 교육 없이 혼자 쓸 수 있게 쓴다.

읽는 사람은 개발자가 아니다. 그래서 실제로 겪는 순서대로 놓았다.
    설치 → 무엇에 쓰나 → 색과 글꼴 → 내용 채우기 → 만든 다음 → 손질

제일 중요한 장은 '내용 채우기'다. 자료만 주면 모양은 나오고 이야기는 안 나온다.
읽는 사람, 발표인지 읽힘인지, 분량, 한 문장. 이 넷을 같이 적게 만드는 것이 이 덱의 목적이다.

이 덱 자체가 이 스킬로 만들어졌다. 시연이 곧 증거다.

문체 주의: 비유 명사(걸음·자리·갈래·칸·계단·사다리·층)를 쓰지 않는다.
셀 수 있으면 실제 이름을 부른다. 완성 후 검색해서 0건을 확인한다.

    python build_howto.py
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TPL = os.path.join(SKILL, "assets", "template.html")
OUT = os.path.join(SKILL, "reference", "스킬사용법.html")

TITLE = "HTML 슬라이드 스킬 사용법"

EXTRA = """
  /* ---- 사용법 덱 전용 ---- */
  .keys{display:flex; gap:14px; flex-wrap:wrap; flex:0 0 auto; margin-top:auto}
  .keycap{display:inline-flex; align-items:center; gap:9px; padding:16px 22px;
    border-radius:12px; background:var(--card); border:1px solid var(--line);
    box-shadow:var(--sh-sm)}
  .keycap kbd{display:inline-block; padding:5px 11px; border-radius:7px;
    background:var(--tint); border:1px solid var(--line);
    font-family:'SF Mono',ui-monospace,Consolas,monospace;
    font-size:15px; font-weight:700; color:var(--ink)}
  .keycap span{font-size:16.5px; font-weight:700; color:var(--ink)}
  .keycap i{font-style:normal; font-size:14px; color:var(--muted); font-weight:500}
  .slide > .rowsteps{margin-top:26px; margin-bottom:auto}
  .slide > .banner{margin-top:auto}
  .rowsteps{display:flex; align-items:stretch}
  .rowsteps .rs{flex:1; padding:20px; background:var(--tint);
    border-left:3px solid var(--c,var(--a1))}
  .rowsteps .rs + .rs{margin-left:10px}
  .rowsteps .rs b{display:block; font-size:16px; color:var(--ink); font-weight:800}
  .rowsteps .rs span{display:block; margin-top:8px; font-size:13.5px;
    color:var(--muted); line-height:1.5}

  /* 그대로 옮겨 쓰는 지시문 */
  .ask{flex:1; min-height:0; display:flex; flex-direction:column; justify-content:center}
  .ask .box{background:var(--tint); border-left:4px solid var(--a1);
    padding:20px 26px; border-radius:0 10px 10px 0}
  .ask .box p{margin:0 0 10px; font-size:16px; color:var(--muted); font-weight:700;
    letter-spacing:.02em}
  .ask .box ol{margin:0; padding-left:22px}
  .ask .box li{font-size:17px; line-height:1.6; color:var(--body); margin:8px 0}
  .ask .box li b{color:var(--ink); font-weight:800}
  .ask .box li i{font-style:normal; color:var(--muted)}
  .ask .why{display:flex; gap:26px; margin-top:18px}
  .ask .why div{flex:1; font-size:13.5px; color:var(--muted); line-height:1.55}
  .ask .why b{display:block; color:var(--ink); font-weight:800; font-size:14.5px;
    margin-bottom:5px}
"""


def cover(eyebrow, en, t1, t2, sub):
    return ('      <section class="slide cover">\n'
            '        <div class="eyebrow" data-anim style="--d:0"><b>%s</b>'
            '<span class="en">· %s</span></div>\n'
            '        <h1 class="title" data-anim style="--d:1">%s<br>'
            '<span class="mark">%s</span></h1>\n'
            '        <p class="sub" data-anim style="--d:2">%s</p>\n'
            "      </section>\n" % (eyebrow, en, t1, t2, sub))


def body(n, eyebrow, en, title, sub, inner):
    return ('      <section class="slide">\n'
            '        <div class="head" data-n="%s">\n'
            '          <div class="eyebrow" data-anim style="--d:0">%s '
            '<span class="en">%s</span></div>\n'
            '          <h2 class="title" data-anim style="--d:1">%s</h2>\n'
            '          <p class="sub" data-anim style="--d:2">%s</p>\n'
            "        </div>\n" % (n, eyebrow, en, title, sub)
            + inner + "      </section>\n")


def card(c, idx, h3, p, tag):
    return ('          <div class="card" style="--c:var(--%s); --ct:var(--%st)">\n'
            '            <div class="idx">%s</div><h3>%s</h3>\n'
            '            <p>%s</p>\n'
            '            <div class="tag">%s</div>\n'
            "          </div>\n" % (c, c, idx, h3, p, tag))


def rows(items, d=4):
    return ('        <div class="rowsteps" data-anim style="--d:%d">\n' % d
            + "".join('          <div class="rs" style="--c:var(--%s)"><b>%s</b>'
                      '<span>%s</span></div>\n' % r for r in items)
            + "        </div>\n")


def banner(text, d=5):
    return '        <div class="banner" data-anim style="--d:%d">%s</div>\n' % (d, text)


S = []

# ================================================================ 표지
S.append(cover("사용법", "HOW TO USE",
               "자료를 붙이고 한 줄 치면",
               "제안서가 나옵니다",
               "설치, 색 맞추기, 내용 채우기, 손질까지 여섯 장입니다. "
               "이 덱도 같은 스킬로 만들었습니다."))

# ================================================================ 1. 설치
S.append(body("01", "설치하기", "INSTALL",
              "폴더에 넣는 것이 전부입니다",
              "설치 프로그램도, 계정 만들기도 없습니다",
              '        <div class="cards" data-anim style="--d:3">\n'
              + card("a1", "1", "내 컴퓨터에 저장한다",
                     "폴더 두 개가 나옵니다. <b>html-slides</b> 는 발표용, "
                     "<b>html-report</b> 는 읽는 보고서입니다. "
                     "공유 폴더에서 받았다면 <b>잘라내지 말고 복사</b>합니다.",
                     "받은 파일 그대로")
              + card("a2", "2", "폴더에 넣는다",
                     "일하는 폴더 안에 <b>.claude/skills</b> 를 만들고 그 안에 둡니다. "
                     "점으로 시작하는 이름이 안 만들어지면 <b>.claude.</b> 처럼 "
                     "끝에 점을 하나 더 붙입니다.",
                     ".claude/skills/")
              + card("a3", "3", "확인한다",
                     "그 폴더에서 클로드 코드를 켜고 <b>「무슨 스킬 있어」</b> 라고 물어봅니다. "
                     "두 개가 보이면 됩니다.",
                     "한 번만 하면 된다")
              + "        </div>\n"
              + banner("컴퓨터 전체에서 쓰려면 <b>내 사용자 폴더 안의 .claude/skills</b> 에 넣습니다. "
                       "그러면 폴더마다 넣지 않아도 됩니다", 4)))

# ================================================================ 2. 무엇에 쓰나
S.append(body("02", "무엇에 쓰나", "WHEN",
              "매달 다시 만드는 것이면 이쪽이 낫습니다",
              "파워포인트를 버리라는 말이 아닙니다. 하는 일이 다릅니다",
              '        <div class="duo">\n'
              '          <div class="panel" data-anim style="--d:3; --pc:var(--a1); '
              '--pct:var(--a1t); --pbg:var(--a1b)">\n'
              '            <div class="pk">이 스킬이 낫다</div>\n'
              '            <h3>매달 다시 만드는 것</h3>\n'
              '            <ul class="pts">\n'
              '              <li>결산 보고, 월간 실적, 정기 제안서</li>\n'
              '              <li>숫자만 바꾸면 <b>표와 그래프가 따라 바뀐다</b></li>\n'
              '              <li>급해도 <b>모양이 흔들리지 않는다</b></li>\n'
              '              <li>글자가 잘렸는지 <b>기계가 대신 잰다</b></li>\n'
              '              <li>파일 하나라 메일에 붙이면 그냥 열린다</li>\n'
              '            </ul>\n'
              '          </div>\n'
              '          <div class="panel" data-anim style="--d:4; --pc:var(--a3); '
              '--pct:var(--a3t); --pbg:var(--a3b)">\n'
              '            <div class="pk">파워포인트가 낫다</div>\n'
              '            <h3>이번 한 번만 그리는 것</h3>\n'
              '            <ul class="pts">\n'
              '              <li>도형을 <b>원하는 데로 끌어다</b> 놓아야 할 때</li>\n'
              '              <li>애니메이션과 화면 전환이 필요할 때</li>\n'
              '              <li>여럿이 <b>동시에 고치고 댓글</b>을 달 때</li>\n'
              '              <li>받는 쪽이 <b>ppt 파일을 요구</b>할 때</li>\n'
              '            </ul>\n'
              '          </div>\n'
              '        </div>\n'
              + banner("발표는 <b>F</b> 로 전체화면에 놓고 방향키로 넘깁니다. "
                       "파일로 보내야 하면 <b>Ctrl+P 로 PDF 저장</b>입니다", 5)))

# ================================================================ 3. 색과 글꼴
S.append(body("03", "색과 글꼴 맞추기", "BRAND",
              "홈페이지 주소를 주면 회사 색으로 맞춥니다",
              "색을 새로 고르지 않습니다. 이미 쓰고 있는 색을 가져옵니다",
              '        <div class="ask" data-anim style="--d:3">\n'
              '          <div class="box">\n'
              '            <p>그대로 옮겨 쓰십시오</p>\n'
              '            <ol>\n'
              '              <li>우리 회사 홈페이지는 <i>www.우리회사.co.kr</i> 입니다.</li>\n'
              '              <li>거기서 쓰는 <b>강조색과 제목 글꼴</b>을 확인해서 이 덱에 맞춰 주십시오.</li>\n'
              '              <li>글꼴은 <b>상대 컴퓨터에 없을 때 대신 쓸 것</b>도 같이 지정해 주십시오.</li>\n'
              '            </ol>\n'
              '          </div>\n'
              '          <div class="why">\n'
              '            <div><b>색은 세 줄로 끝난다</b>산출된 파일 머리에 강조색 세 개가 있습니다. '
              '그 세 줄만 바뀌면 표도 그래프도 배지도 한꺼번에 따라옵니다. 장마다 고치지 않습니다.</div>\n'
              '            <div><b>글꼴은 받는 사람 컴퓨터를 탄다</b>회사 전용 글꼴은 상대 컴퓨터에 '
              '없으면 다르게 보입니다. 그래서 대신 쓸 글꼴을 함께 적어 둡니다.</div>\n'
              '          </div>\n'
              '        </div>\n'
              + banner("로고는 <b>이미지 파일을 같이 주고 표지에 넣어 달라</b>고 하면 됩니다", 5)))

# ================================================================ 4. 내용 채우기
S.append(body("04", "내용 채우기", "BRIEF",
              "자료만 주면 모양은 나오고 이야기는 안 나옵니다",
              "네 가지를 같이 적으십시오. 이 스킬을 쓰는 데 제일 중요한 장입니다",
              '        <div class="ask" data-anim style="--d:3">\n'
              '          <div class="box">\n'
              '            <p>자료를 붙이고 아래 넷을 같이 적습니다</p>\n'
              '            <ol>\n'
              '              <li><b>읽는 사람과 그가 내릴 결정.</b> '
              '<i>대표와 재무팀장. 아웃소싱으로 넘길지 정합니다</i></li>\n'
              '              <li><b>발표용인지 혼자 읽히는지.</b> '
              '<i>미팅에서 15분 발표. 끝나고 따로 읽히지는 않습니다</i></li>\n'
              '              <li><b>총 몇 장.</b> <i>12장</i></li>\n'
              '              <li><b>덱 전체가 한 문장이라면.</b> '
              '<i>지금 인원으로는 마감이 안 줄고, 넘기면 12일이 4일이 됩니다</i></li>\n'
              '            </ol>\n'
              '          </div>\n'
              '          <div class="why">\n'
              '            <div><b>혼자 읽히는 자료는 글이 길어야 한다</b>발표는 내가 옆에서 말하지만 '
              '읽히는 자료는 나 없이 읽힙니다. 부제와 본문이 훨씬 길어집니다.</div>\n'
              '            <div><b>한 문장이 목차를 정한다</b>그 문장이 없으면 자료에 있는 것을 '
              '전부 늘어놓게 됩니다. 있으면 그것을 받치는 장만 남습니다.</div>\n'
              '          </div>\n'
              '        </div>\n'
              + banner("자료는 정리해서 줄 필요가 없습니다. 회의 메모도 됩니다. "
                       "다만 <b>숫자는 표로</b> 주십시오", 5)))

# ================================================================ 5. 만든 다음
S.append(body("05", "만든 다음", "AFTER",
              "열고, 넘기고, 잘린 데를 확인합니다",
              "받은 파일 하나가 곧 산출물입니다. 따로 저장할 것이 없습니다",
              '        <div class="keys" data-anim style="--d:3">\n'
              '          <div class="keycap"><kbd>F</kbd><span>전체화면</span>'
              '<i>발표는 이 상태로</i></div>\n'
              '          <div class="keycap"><kbd>←</kbd><kbd>→</kbd><span>장 넘기기</span>'
              '<i>리모컨도 된다</i></div>\n'
              '          <div class="keycap"><kbd>Ctrl</kbd><kbd>P</kbd><span>PDF 저장</span>'
              '<i>메일에 붙일 때</i></div>\n'
              '        </div>\n'
              + rows([("a1", "잘린 데 확인", "「잘린 데 없는지 확인해줘」 라고 하면 기계가 잽니다. "
                       "글자가 넘치면 화면에서 그냥 안 보입니다"),
                      ("a2", "고칠 것 말하기", "「3장 그래프를 막대로 바꿔줘」 처럼 "
                       "장 번호로 말하면 그 장만 다시 만듭니다"),
                      ("a3", "숫자는 사람이 본다", "모양은 스킬이 맞추지만 "
                       "숫자가 맞는지는 봐주지 않습니다")], 4)))

# ================================================================ 6. 손질
S.append(body("06", "직접 손질하기", "EDIT",
              "브라우저에서 글자를 눌러 고칩니다",
              "오탈자 하나 고치자고 다시 만들지 않습니다",
              '        <div class="keys" data-anim style="--d:3">\n'
              '          <div class="keycap"><kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>E</kbd>'
              '<span>손질 모드</span><i>위에 검은 띠가 뜬다</i></div>\n'
              '          <div class="keycap"><span>글자를 클릭</span>'
              '<i>누른 데서 바로 고친다</i></div>\n'
              '          <div class="keycap"><kbd>Alt</kbd><span>+ 클릭</span>'
              '<i>색이 차례로 돈다</i></div>\n'
              '          <div class="keycap"><kbd>Ctrl</kbd><kbd>S</kbd>'
              '<span>저장</span><i>고친 그대로 파일 하나</i></div>\n'
              '        </div>\n'
              + rows([("a1", "고쳐지는 것", "제목, 본문, 표 안 글자, 그래프 안 이름표까지 됩니다. "
                       "색은 글자를 고른 뒤 Alt+클릭하면 그 부분만 바뀝니다"),
                      ("a3", "안 고쳐지는 것", "막대 길이나 축 범위처럼 계산이 걸린 값입니다. "
                       "글자만 바꾸면 그림과 어긋납니다"),
                      ("a2", "순서", "내용을 먼저 다 채우고 손질은 마지막에 합니다. "
                       "다시 만들면 손질한 것이 덮입니다")], 4)))

# ================================================================ 마무리
S.append(cover("마무리", "CLOSING",
               "고를 것은 디자인이 아니라",
               "누구에게 무엇을 말하느냐입니다",
               "모양은 스킬이 맞춥니다. 사람이 정할 것은 읽는 사람, 분량, 그리고 한 문장입니다."))

# ================================================================ 조립
tpl = io.open(TPL, encoding="utf-8").read()
tpl = tpl.replace("  /* =================== chrome (fixed UI) =================== */",
                  EXTRA + "  /* =================== chrome (fixed UI) =================== */", 1)
open_tag = '<div class="deck" id="deck">'
close = '\n    </div>\n  </div>\n\n  <div class="brandbar"'
a = tpl.index(open_tag) + len(open_tag)
b = tpl.index(close)
out = tpl[:a] + "\n\n" + "\n".join(S) + tpl[b:]
out = out.replace("{{DECK_TITLE}}", TITLE)
out = out.replace('<section class="slide cover">', '<section class="slide cover active">', 1)
io.open(OUT, "w", encoding="utf-8").write(out)
print("wrote", OUT, "slides =", out.count('<section class="slide'))
