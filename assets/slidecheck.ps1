<#
  html-slides 넘침 검증기.
  슬라이드 HTML을 Chrome(없으면 Edge) 헤드리스로 열어, 슬라이드마다
  '내용이 1280x720 캔버스 안에 들어오는지'를 실측한다.

  사용:  powershell -ExecutionPolicy Bypass -File slidecheck.ps1 "C:\경로\슬라이드.html"

  왜 눈으로 보면 안 되는가
    .slide 는 overflow:hidden 이라, 넘친 내용은 화면에서 '그냥 안 보인다'.
    한 줄이 잘려 나가도 레이아웃이 깨지지 않으므로 육안으로는 멀쩡해 보인다.
    그래서 재야 한다.

  읽는 법
    - 여유(px)가 음수면 그 슬라이드는 넘쳤다 → 항목을 줄이거나 슬라이드를 나눈다.
    - 여유가 20px 미만이면 폰트 로딩·줄바꿈 차이로 넘칠 수 있는 경계다.
    - 표지(cover)는 세로 가운데 정렬이라 여유가 크게 나오는 것이 정상이다.
    - 전시물 축소: SVG 는 viewBox 비율이 칸과 다르면 줄어든다. 넘치지 않으므로 넘침 검사로는
      안 잡히는데, 그 안의 글자만 작아져 가시성이 무너진다. 85% 미만이면 보고한다.
    - 제목 꼬리: 두 줄짜리 제목의 마지막 줄에 몇 자만 남으면 어설프다.
      기본 기준 4자. 문구를 줄이거나 어절 경계에 <br> 를 넣어 문장 단위로 끊는다.
    - 가로 넘침: 표지 둘째 줄(.mark)은 white-space:nowrap 이라 길면 접히지 않고 캔버스 밖으로 나간다.
    - 문장 줄바꿈: 문장 경계에서 끊어도 줄 수가 늘지 않는데 문장 중간에서 접힌 글을 찾는다.
      줄 수를 높이로 세면 안 된다. flex 형제가 길면 짧은 칸도 같이 늘어나므로 Range 로 센다.
#>
param(
  [Parameter(Mandatory=$true)][string]$Html,
  [int]$TailMin = 4,
  [int]$MinSlack = 0
)

$ErrorActionPreference = 'Stop'
$Html = (Resolve-Path $Html).Path
$src  = Get-Content $Html -Raw -Encoding UTF8

# --- 측정 스크립트를 사본에 심는다(원본은 건드리지 않는다) -------------------
# deck 의 scale 변환을 잠시 끄고, 슬라이드마다 가장 아래 요소의 바닥을 잰다.
# 캔버스 높이에서 아래 패딩을 뺀 값이 '내용이 들어와야 할 선'이다.
$probe = @'
<script id="slidecheck">
(function(){
  function run(){
    // 비활성 슬라이드의 [data-anim] 은 등장 전 상태(translateY(18px))로 누워 있다.
    // 그대로 재면 모든 슬라이드가 일정하게 넘친 것처럼 보인다 — 먼저 중화한다.
    var st = document.createElement('style');
    st.textContent = '[data-anim]{opacity:1!important;transform:none!important;animation:none!important}';
    document.head.appendChild(st);
    var deck = document.getElementById('deck');
    var keep = deck ? deck.style.transform : '';
    if (deck) deck.style.transform = 'none';
    var out = [];
    var wraps = [];
    var titles = [];
    var shrink = [];
    var over = [];
    var sent = [];
    var clip = [];
    // 덤프 인코딩과 무관하게 JSON 이 깨지지 않도록 라벨을 ASCII 로만 실어 보낸다.
    function asc(x){ return String(x).replace(/[^ -~]/g, function(c){
      return '\\u' + ('000' + c.charCodeAt(0).toString(16)).slice(-4); }); }
    // 폭이 고정된 라벨 칸들 — 글자가 길면 소리 없이 두 줄이 된다.
    var LBL = '.deflist .row .k, .deflist .row .c, .card .svc .k, .step h3, .role .lab, .panel .pk';
    // 두 줄 이상 흐르는 글 — 문장 경계가 있는데 딴 데서 접히면 읽다가 걸린다.
    var SENTSEL = '.sub, .banner, .cap, .lead, .note, .exnote .q, .exnote .w, .callout p, .panel p';
    // 글자가 실제로 놓인 줄 수. 높이로 세면 flex 형제를 따라 늘어난 빈 자리까지 센다
    function lineCount(el) {
      try {
        var r = document.createRange();
        r.selectNodeContents(el);
        var rects = r.getClientRects(), tops = [], k;
        for (k = 0; k < rects.length; k++) {
          if (rects[k].width < 0.5) continue;
          var tp = Math.round(rects[k].top);
          if (tops.indexOf(tp) < 0) tops.push(tp);
        }
        return tops.length || 1;
      } catch (e) { return 1; }
    }
    // 글 전체에서 i 번째 글자의 범위. 그 글자가 몇 번째 줄에 있는지 재려는 것이다
    function charRange(el, i) {
      var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), n, acc = 0;
      while ((n = w.nextNode())) {
        var L = n.nodeValue.length;
        if (acc + L > i) {
          var r = document.createRange();
          r.setStart(n, i - acc); r.setEnd(n, i - acc + 1); return r;
        }
        acc += L;
      }
      return null;
    }
    var slides = document.querySelectorAll('.slide');
    for (var i = 0; i < slides.length; i++) {
      var s = slides[i];
      var pv = s.style.visibility, po = s.style.opacity;
      s.style.visibility = 'visible'; s.style.opacity = '1';
      var cs = getComputedStyle(s);
      var padB = parseFloat(cs.paddingBottom) || 0;
      var H = s.getBoundingClientRect().height || 720;
      var top = s.getBoundingClientRect().top;
      var bottom = 0;
      var all = s.querySelectorAll('*');
      for (var j = 0; j < all.length; j++) {
        var r = all[j].getBoundingClientRect();
        if (r.height > 0) { var b = r.bottom - top; if (b > bottom) bottom = b; }
      }
      // 제목·부제 — 두 줄까지는 좋으나, 마지막 줄에 몇 글자만 남으면 어설프다.
    var TTL = s.querySelectorAll('.title, .head .sub');
    for (var t = 0; t < TTL.length; t++) {
      var el2 = TTL[t], cs2 = getComputedStyle(el2);
      var lh2 = parseFloat(cs2.lineHeight);
      if (!lh2 || isNaN(lh2)) lh2 = parseFloat(cs2.fontSize) * 1.2;
      var lines = Math.round(el2.offsetHeight / lh2);
      if (lines < 2) continue;
      // 마지막 줄 길이를 Range 로 실측한다(<br> 로 나눈 줄도 그대로 잡힌다).
      var rg = document.createRange(), tail = 0, txt = el2.textContent.trim();
      try {
        rg.selectNodeContents(el2);
        var rects = rg.getClientRects(), last = rects[rects.length - 1];
        if (last) tail = Math.round(last.width);
      } catch (e) {}
      var per = parseFloat(cs2.fontSize) * 0.92;   // 한글 한 글자 대략 폭
      titles.push({ n: i + 1, lines: lines, tailc: Math.max(1, Math.round(tail / per)),
                    t: asc(txt.replace(/\s+/g, ' ').slice(0, 30)) });
    }
    // 전시물 SVG — viewBox 비율이 칸과 다르면 meet 로 줄어들고 글자만 작아진다.
    var SV = s.querySelectorAll('svg[viewBox]');
    for (var v = 0; v < SV.length; v++) {
      var sv = SV[v], vb = (sv.getAttribute('viewBox') || '').split(/[ ,]+/);
      if (vb.length < 4) continue;
      var vw = parseFloat(vb[2]), vh = parseFloat(vb[3]);
      var rb = sv.getBoundingClientRect();
      if (!vw || !vh || !rb.width || !rb.height) continue;
      var sc = Math.min(rb.width / vw, rb.height / vh);
      if (sc < 0.85) {
        shrink.push({ n: i + 1, pct: Math.round(sc * 100),
                      vb: Math.round(vw) + 'x' + Math.round(vh),
                      box: Math.round(rb.width) + 'x' + Math.round(rb.height) });
      }
      // viewBox 밖에 그린 것은 SVG 가 잘라 버린다. 줄어드는 것이 아니라 사라진다
      try {
        var bb = sv.getBBox();
        var vx = parseFloat(vb[0]), vy = parseFloat(vb[1]);
        var cut = Math.round(Math.max(0, bb.x + bb.width - (vx + vw),
                                      bb.y + bb.height - (vy + vh),
                                      vx - bb.x, vy - bb.y));
        if (cut > 2) {
          clip.push({ n: i + 1, px: cut,
                      vb: Math.round(vw) + 'x' + Math.round(vh),
                      bb: Math.round(bb.width) + 'x' + Math.round(bb.height) });
        }
      } catch (e) {}
    }
    // 줄바꿈이 막힌 글자(.mark 등)는 길어지면 접히지 않고 오른쪽으로 나간다.
    // 세로 넘침만 재면 이것이 안 잡힌다.
    var sb = s.getBoundingClientRect();
    var padR = parseFloat(getComputedStyle(s).paddingRight) || 0;
    var NW = s.querySelectorAll('.mark, .title, .head .title, h1, h2');
    for (var q = 0; q < NW.length; q++) {
      var nel = NW[q];
      var nb = nel.getBoundingClientRect();
      var spill = Math.round(nb.right - (sb.right - padR));
      if (spill > 2) {
        over.push({ n: i + 1, px: spill,
                    t: asc(nel.textContent.replace(/[ ]+/g, ' ').trim().slice(0, 26)) });
      }
    }
    // 줄 수가 늘지 않는데도 문장 중간에서 접힌 글을 찾는다
    var SE = s.querySelectorAll(SENTSEL);
    for (var y = 0; y < SE.length; y++) {
      var e2 = SE[y];
      if (e2.querySelector('br')) continue;            // 이미 손으로 끊어 놓았다
      var t2 = e2.textContent.replace(/\s+/g, ' ').trim();
      var cs2 = getComputedStyle(e2);
      var lh2 = parseFloat(cs2.lineHeight);
      if (!lh2 || isNaN(lh2)) lh2 = parseFloat(cs2.fontSize) * 1.4;
      // 높이로 줄을 세면 안 된다. flex 형제가 길면 짧은 칸도 같이 늘어난다.
      // 글자가 실제로 놓인 줄만 센다.
      var ln2 = lineCount(e2);
      if (ln2 < 2) continue;
      var cand = [];
      for (var z = 0; z < t2.length - 2; z++) {
        // 마침표 뒤 빈칸이 문장 경계다. 앞뒤로 너무 짧으면 끊을 자리가 아니다
        if (t2.charAt(z) === '.' && t2.charAt(z + 1) === ' ' &&
            z >= 13 && t2.length - z >= 10) cand.push(z + 2);
      }
      if (!cand.length) continue;
      var W2 = e2.getBoundingClientRect().width;
      for (var c2 = 0; c2 < cand.length; c2++) {
        var i2 = cand[c2];
        var rA = charRange(e2, i2 - 2), rB = charRange(e2, i2);
        if (!rA || !rB) continue;
        // 이미 그 경계에서 줄이 갈렸으면 볼 것 없다
        if (Math.abs(rA.getBoundingClientRect().top - rB.getBoundingClientRect().top) > 1) break;
        var cl = e2.cloneNode(false);
        cl.style.position = 'absolute'; cl.style.visibility = 'hidden';
        cl.style.width = W2 + 'px'; cl.style.maxWidth = 'none';
        cl.appendChild(document.createTextNode(t2.slice(0, i2 - 1)));
        cl.appendChild(document.createElement('br'));
        cl.appendChild(document.createTextNode(t2.slice(i2)));
        e2.parentNode.appendChild(cl);
        var alt = lineCount(cl);
        cl.parentNode.removeChild(cl);
        if (alt <= ln2) {
          sent.push({ n: i + 1, lines: ln2,
                      t: asc(t2.slice(0, 22)),
                      at: asc(t2.slice(Math.max(0, i2 - 12), i2 + 12)) });
          break;
        }
      }
    }
    var lbl = s.querySelectorAll(LBL);
      for (var w = 0; w < lbl.length; w++) {
        var el = lbl[w], ecs = getComputedStyle(el);
        var lh = parseFloat(ecs.lineHeight);
        if (!lh || isNaN(lh)) lh = parseFloat(ecs.fontSize) * 1.35;
        if (el.offsetHeight > lh * 1.6) {
          wraps.push({ n: i + 1, lines: Math.round(el.offsetHeight / lh),
                       w: Math.round(el.offsetWidth),
                       t: asc(el.textContent.replace(/[ ]+/g, ' ').trim().slice(0, 26)) });
        }
      }
      s.style.visibility = pv; s.style.opacity = po;
      out.push({
        n: i + 1,
        cover: s.className.indexOf('cover') >= 0 ? 1 : 0,
        bottom: Math.round(bottom),
        limit: Math.round(H - padB),
        slack: Math.round(H - padB - bottom)
      });
    }
    if (deck) deck.style.transform = keep;
    var d = document.createElement('div');
    d.id = 'SLIDECHECK';
    d.textContent = JSON.stringify(out);
    document.body.appendChild(d);
    var d2 = document.createElement('div');
    d2.id = 'SLIDEWRAP';
    d2.textContent = JSON.stringify(wraps);
    document.body.appendChild(d2);
    var d3 = document.createElement('div');
    d3.id = 'SLIDETITLE';
    d3.textContent = JSON.stringify(titles);
    document.body.appendChild(d3);
    var d4 = document.createElement('div');
    d4.id = 'SLIDESHRINK';
    d4.textContent = JSON.stringify(shrink);
    document.body.appendChild(d4);
    var d5 = document.createElement('div');
    d5.id = 'SLIDEOVER';
    d5.textContent = JSON.stringify(over);
    document.body.appendChild(d5);
    var d6 = document.createElement('div');
    d6.id = 'SLIDESENT';
    d6.textContent = JSON.stringify(sent);
    document.body.appendChild(d6);
    var d7 = document.createElement('div');
    d7.id = 'SLIDECLIP';
    d7.textContent = JSON.stringify(clip);
    document.body.appendChild(d7);
  }
  // 웹폰트가 오면 줄바꿈이 바뀐다. 폰트가 준비된 뒤에 재야 한다.
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(run); } else { window.addEventListener('load', run); }
})();
</script>
'@

# 임시 폴더. $env:TEMP 는 Windows 에만 있다 — mac/Linux 의 pwsh 에서는 비어 있어
# Join-Path 가 터진다. .NET 의 GetTempPath() 는 세 플랫폼 모두에서 답을 준다.
$tmpDir = [IO.Path]::GetTempPath()

$tmp = Join-Path $tmpDir ('slidecheck_' + [IO.Path]::GetFileNameWithoutExtension($Html) + '.html')
($src -replace '(?i)</body>', ($probe + "`n</body>")) | Set-Content $tmp -Encoding UTF8

# Windows·macOS·Linux 의 설치 위치를 순서대로 훑는다.
# 없는 플랫폼의 경로는 Test-Path 에서 그냥 걸러지므로 한 목록으로 둬도 된다.
$browser = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
  '/usr/bin/microsoft-edge'
) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1

# 그래도 못 찾으면 PATH 에 걸린 이름으로 한 번 더 본다(리눅스 배포판마다 경로가 다르다).
if (-not $browser) {
  $browser = @('google-chrome','chromium','chromium-browser','msedge','chrome') |
             ForEach-Object { (Get-Command $_ -ErrorAction SilentlyContinue).Source } |
             Where-Object { $_ } | Select-Object -First 1
}
if (-not $browser) { throw 'Chrome 또는 Edge를 찾지 못했다. CHROME 경로를 직접 확인하라.' }

# 이미 떠 있는 브라우저에 위임되지 않도록 별도 프로필을 쓴다(printcheck.ps1과 같은 이유).
$profileDir = Join-Path $tmpDir ('slidecheck_profile_' + [IO.Path]::GetRandomFileName())
$dump = Join-Path $tmpDir ('slidecheck_dom_' + [IO.Path]::GetRandomFileName() + '.html')

$args = @(
  '--headless','--disable-gpu','--run-all-compositor-stages-before-draw',
  '--virtual-time-budget=12000','--window-size=1280,720','--dump-dom',
  ('--user-data-dir="' + $profileDir + '"'),
  ('"' + $tmp + '"')
)
& $browser @args 2>$null | Set-Content $dump -Encoding UTF8
if (Test-Path $profileDir) { Remove-Item $profileDir -Recurse -Force -ErrorAction SilentlyContinue }

$dom = Get-Content $dump -Raw -Encoding UTF8
$m = [regex]::Match($dom, '<div id="SLIDECHECK">(.*?)</div>', 'Singleline')
if (-not $m.Success) { throw '측정 결과를 찾지 못했다(페이지가 로드되지 않았거나 스크립트가 막혔다).' }

$mw = [regex]::Match($dom, '<div id="SLIDEWRAP">(.*?)</div>', 'Singleline')
$wraps = @()
if ($mw.Success -and $mw.Groups[1].Value.Trim() -ne '[]') {
  foreach ($x in (ConvertFrom-Json -InputObject ($mw.Groups[1].Value -replace '&quot;','"'))) { $wraps += $x }
}

$mt2 = [regex]::Match($dom, '<div id="SLIDETITLE">(.*?)</div>', 'Singleline')
$titles = @()
if ($mt2.Success -and $mt2.Groups[1].Value.Trim() -ne '[]') {
  foreach ($x in (ConvertFrom-Json -InputObject ($mt2.Groups[1].Value -replace '&quot;','"'))) { $titles += $x }
}
# 마지막 줄에 TailMin 자 미만만 남으면 어설프게 끊긴 것이다.
$orphans = @($titles | Where-Object { $_.tailc -lt $TailMin -or $_.lines -gt 2 })

$ms = [regex]::Match($dom, '<div id="SLIDESHRINK">(.*?)</div>', 'Singleline')
$shrinks = @()
if ($ms.Success -and $ms.Groups[1].Value.Trim() -ne '[]') {
  foreach ($x in (ConvertFrom-Json -InputObject ($ms.Groups[1].Value -replace '&quot;','"'))) { $shrinks += $x }
}

$mo = [regex]::Match($dom, '<div id="SLIDEOVER">(.*?)</div>', 'Singleline')
$overs = @()
if ($mo.Success -and $mo.Groups[1].Value.Trim() -ne '[]') {
  foreach ($x in (ConvertFrom-Json -InputObject ($mo.Groups[1].Value -replace '&quot;','"'))) { $overs += $x }
}

$mse = [regex]::Match($dom, '<div id="SLIDESENT">(.*?)</div>', 'Singleline')
$sents = @()
if ($mse.Success -and $mse.Groups[1].Value.Trim() -ne '[]') {
  foreach ($x in (ConvertFrom-Json -InputObject ($mse.Groups[1].Value -replace '&quot;','"'))) { $sents += $x }
}

$mc = [regex]::Match($dom, '<div id="SLIDECLIP">(.*?)</div>', 'Singleline')
$clips = @()
if ($mc.Success -and $mc.Groups[1].Value.Trim() -ne '[]') {
  foreach ($x in (ConvertFrom-Json -InputObject ($mc.Groups[1].Value -replace '&quot;','"'))) { $clips += $x }
}

$rows = $m.Groups[1].Value |
        ForEach-Object { $_ -replace '&quot;','"' } |
        ConvertFrom-Json

"파일  : $Html"
"슬라이드: $($rows.Count)장   (캔버스 1280x720, 여유 기준 {0}px)" -f $MinSlack
''
$bad = @(); $tight = @()
foreach ($r in $rows) {
  $flag = ''
  # 본문 슬라이드는 대개 flex:1 로 캔버스를 꽉 채우므로 여유 0 이 정상이다.
  # 음수만 진짜 넘침이다(중첩 상자가 자기 칸을 넘어선 경우까지 여기서 잡힌다).
  if ($r.slack -lt 0) { $flag = '  <-- 넘침'; $bad += $r.n }
  elseif ($MinSlack -gt 0 -and $r.slack -lt $MinSlack -and $r.cover -eq 0) { $flag = '  <-- 여유 부족'; $tight += $r.n }
  $kind = if ($r.cover -eq 1) { 'cover ' } else { '      ' }
  "  s{0,-3} {1} 바닥 {2,4}px / 한계 {3,4}px   여유 {4,5}px{5}" -f $r.n, $kind, $r.bottom, $r.limit, $r.slack, $flag
}
''
if ($wraps.Count) {
  '라벨 줄바꿈 — 폭이 고정된 칸이다. 칸을 넓히지 말고 글자를 줄인다:'
  foreach ($w in $wraps) { '  s' + ([string]$w.n).PadRight(3) + ' ' + [string]$w.lines + '줄 / 폭 ' + [string]$w.w + 'px   ' + [regex]::Replace($w.t, '\\u([0-9a-fA-F]{4})', { param($m) [string][char][convert]::ToInt32($m.Groups[1].Value, 16) }) }
  ''
}
if ($orphans.Count) {
  "제목 줄바꿈 — 두 줄까지는 좋으나 마지막 줄이 $TailMin 자 미만이면 어설프다."
  '문장·어절 단위로 <br> 를 직접 넣거나 문구를 줄인다:'
  foreach ($t in $orphans) {
    $txt = [regex]::Replace($t.t, '\\u([0-9a-fA-F]{4})', { param($mm) [string][char][convert]::ToInt32($mm.Groups[1].Value, 16) })
    '  s' + ([string]$t.n).PadRight(3) + ' ' + [string]$t.lines + '줄 / 끝줄 ~' + [string]$t.tailc + '자   ' + $txt
  }
  ''
}
if ($shrinks.Count) {
  '전시물 축소 — viewBox 비율이 칸과 달라 그림이 줄었다. 넘치지 않아도 글자만 작아진다.'
  'viewBox 높이를 칸 비율에 맞추거나(가로 1080 기준 높이 330~360), 내용을 두 장으로 나눈다:'
  foreach ($z in $shrinks) {
    '  s' + ([string]$z.n).PadRight(3) + ' ' + [string]$z.pct + '%   viewBox ' + $z.vb + ' -> 칸 ' + $z.box
  }
  ''
}
if ($overs.Count) {
  '가로 넘침 — 제목이 캔버스 오른쪽으로 나갔다. 표지 둘째 줄(.mark)은 줄바꿈이 막혀 있어 접히지 않는다.'
  '78px 표지 제목은 한글 열다섯 자 안쪽으로 줄인다:'
  foreach ($o in $overs) {
    $txt = [regex]::Replace($o.t, '\\u([0-9a-fA-F]{4})', { param($mm) [string][char][convert]::ToInt32($mm.Groups[1].Value, 16) })
    '  s' + ([string]$o.n).PadRight(3) + ' +' + [string]$o.px + 'px   ' + $txt
  }
  ''
}
if ($clips.Count) {
  '그림 잘림 — viewBox 밖에 그린 것이 있다. 줄어드는 것이 아니라 그냥 안 보인다.'
  'viewBox 를 넓히거나 그 요소를 안쪽으로 옮긴다:'
  foreach ($p2 in $clips) {
    '  s' + ([string]$p2.n).PadRight(3) + ' ' + [string]$p2.px + 'px 밖   viewBox ' + $p2.vb + ' / 내용 ' + $p2.bb
  }
  ''
}
if ($sents.Count) {
  '문장 줄바꿈 — 문장 경계에서 끊어도 줄 수가 늘지 않는데 문장 중간에서 접혔다.'
  '해당 자리에 <br> 를 넣는다:'
  foreach ($v in $sents) {
    $t1 = [regex]::Replace($v.t,  '\\u([0-9a-fA-F]{4})', { param($mm) [string][char][convert]::ToInt32($mm.Groups[1].Value, 16) })
    $t2 = [regex]::Replace($v.at, '\\u([0-9a-fA-F]{4})', { param($mm) [string][char][convert]::ToInt32($mm.Groups[1].Value, 16) })
    '  s' + ([string]$v.n).PadRight(3) + ' ' + [string]$v.lines + '줄   ' + $t1 + ' ...   끊을 자리: ' + $t2
  }
  ''
}
if ($bad.Count -eq 0 -and $tight.Count -eq 0 -and $wraps.Count -eq 0 -and $orphans.Count -eq 0 -and $shrinks.Count -eq 0 -and $overs.Count -eq 0 -and $sents.Count -eq 0 -and $clips.Count -eq 0) {
  '판정: 통과 — 캔버스 안에 들어오고, 접힌 라벨도 어설픈 줄바꿈도 없다.'
} else {
  if ($bad.Count)   { "판정: 넘침 — 슬라이드 $(($bad | Sort-Object -Unique) -join ', '). 항목을 줄이거나 슬라이드를 나눈다(폰트를 줄이지 않는다)." }
  if ($tight.Count) { "판정: 여유 부족 — 슬라이드 $(($tight | Sort-Object -Unique) -join ', '). 폰트 로딩·줄바꿈 차이로 넘칠 수 있다." }
  if ($wraps.Count) { "판정: 라벨 줄바꿈 — 슬라이드 $((($wraps | ForEach-Object { $_.n }) | Sort-Object -Unique) -join ', '). 라벨 글자를 줄이고 설명은 옆 칸으로 옮긴다." }
  if ($orphans.Count) { "판정: 제목 꼬리 — 슬라이드 $((($orphans | ForEach-Object { $_.n }) | Sort-Object -Unique) -join ', '). 문구를 줄이거나 어절 경계에 <br> 를 넣는다." }
  if ($overs.Count) { "판정: 가로 넘침 — 슬라이드 $((($overs | ForEach-Object { $_.n }) | Sort-Object -Unique) -join ', '). 제목 글자를 줄인다. 표지 둘째 줄은 접히지 않는다." }
  if ($clips.Count) { "판정: 그림 잘림 — 슬라이드 $((($clips | ForEach-Object { $_.n }) | Sort-Object -Unique) -join ', '). viewBox 밖에 그린 것이 잘렸다." }
  if ($sents.Count) { "판정: 문장 줄바꿈 — 슬라이드 $((($sents | ForEach-Object { $_.n }) | Sort-Object -Unique) -join ', '). 문장 경계에 <br> 를 넣는다(줄 수는 그대로다)." }
  if ($shrinks.Count) { "판정: 전시물 축소 — 슬라이드 $((($shrinks | ForEach-Object { $_.n }) | Sort-Object -Unique) -join ', '). viewBox 비율을 칸에 맞추거나 두 장으로 나눈다." }
}
