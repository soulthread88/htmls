#!/usr/bin/env python3
"""
IssueLens EPx HTML → WordPress Custom HTML Block Converter
==========================================================
Usage:
    python convert_to_wp.py <input_file.html> [output_file.html]

Example:
    python convert_to_wp.py issuelens-ep6-eng.html
    → issuelens-ep6-eng_wordpress.html

What this script does:
    1. Extracts <style>, <body>, <script> from the standalone EPx HTML
    2. Scopes all CSS to #il-epx-wrap to prevent WordPress theme conflicts
    3. Removes IIFE wrapping so inline onclick handlers work globally
    4. Redesigns video boxes: click = PC file picker, Source field = YouTube embed
    5. Adds WordPress h2/h3/p reset overrides
    6. Outputs a single HTML file ready to paste into a WP Custom HTML block
"""

import re
import sys
import os


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def extract(pattern, html, default=''):
    m = re.search(pattern, html, re.DOTALL)
    return m.group(1) if m else default


def scope_css(css, wrapper_id):
    """
    Scope bare CSS selectors to #wrapper_id to prevent WP theme conflicts.
    Handles: :root, html, body, bare a{}, *, @keyframes, @media.
    """
    w = f'#{wrapper_id}'

    # CSS custom properties: :root → wrapper
    css = css.replace(':root{', f'{w}{{')

    # Universal selector
    css = css.replace(
        '*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}',
        f'{w} *,{w} *::before,{w} *::after{{box-sizing:border-box;margin:0;padding:0}}'
    )

    # html scroll-behavior (not needed inside a div)
    css = re.sub(r'html\{scroll-behavior:[^}]+\}', '', css)

    # body → wrapper
    css = re.sub(r'(?<![#.\w-])body\{', f'{w}{{', css)

    # bare a{ → wrapper a{
    css = re.sub(r'(?<![#.\w-])a\{', f'{w} a{{', css)

    return css


def make_video_box_html(vid_id):
    """
    Returns the new dual-mode video box HTML for a given ID (e.g. 's1v').
    - Click anywhere on box  → PC file picker (mp4/webm/mov etc.)
    - Source: field          → YouTube URL → iframe embed
    """
    return f'''<div class="mbox-wrap">
          <div class="mbox-label">🎬 Insert Video</div>
          <div class="mbox" id="mb-{vid_id}" data-t="vid" onclick="vidBoxClick('{vid_id}')">
            <div class="mbox-ph" id="ph-{vid_id}">
              <span class="ico">🎬</span>
              <p>Click to select video file from PC</p>
              <span class="hint">or enter a YouTube URL in the Source field below</span>
            </div>
            <div class="mctrl">
              <button class="mbtn rep" onclick="event.stopPropagation();vidReplace('{vid_id}')">↩ Replace</button>
              <button class="mbtn del" onclick="event.stopPropagation();mbDel('{vid_id}')">✕ Remove</button>
            </div>
          </div>
          <div class="vid-src-row" id="src-row-{vid_id}">
            <span class="vid-src-lbl">Source :</span>
            <input class="vid-src-inp" id="src-{vid_id}" type="text"
              placeholder="https://www.youtube.com/watch?v=..."
              autocomplete="off"
              onclick="event.stopPropagation()"
              onkeydown="if(event.key==='Enter')vidSrcApply('{vid_id}')"
              oninput="vidSrcPreview('{vid_id}',this.value)">
            <button class="vid-src-btn" onclick="event.stopPropagation();vidSrcApply('{vid_id}')">▶ Embed</button>
          </div>
          <input type="file" id="fi-{vid_id}" accept="video/*" style="display:none"
            onchange="vidLoadFile('{vid_id}',this)">
        </div>'''


# ══════════════════════════════════════════════════════════════
# CSS ADDITIONS
# ══════════════════════════════════════════════════════════════

VIDEO_BOX_CSS = """
/* ── Video Source row (added by convert_to_wp.py) ── */
.vid-src-row{display:flex;align-items:center;gap:8px;margin-top:8px;padding:0 2px}
.vid-src-lbl{font-family:var(--ft);font-size:clamp(13px,2.8vw,14px);font-weight:800;color:var(--ink3);white-space:nowrap;flex-shrink:0}
.vid-src-inp{flex:1;border:2px solid var(--bdr);border-radius:8px;padding:8px 12px;font-family:var(--fb);font-size:clamp(13px,2.8vw,14px);outline:none;transition:border-color .2s;color:var(--ink);background:#fff;min-width:0}
.vid-src-inp:focus{border-color:var(--red)}
.vid-src-inp.has-url{border-color:#22C55E;background:#F0FDF4}
.vid-src-btn{font-family:var(--ft);font-size:clamp(13px,2.8vw,14px);font-weight:800;padding:8px 16px;background:var(--red);color:#fff;border:none;border-radius:8px;cursor:pointer;white-space:nowrap;flex-shrink:0;transition:background .15s}
.vid-src-btn:hover{background:#a80018}
"""

WP_HEADING_OVERRIDES = """
/* ── WordPress theme heading reset (added by convert_to_wp.py) ── */
#IL_WRAPPER h1, #IL_WRAPPER h2, #IL_WRAPPER h3,
#IL_WRAPPER h4, #IL_WRAPPER h5, #IL_WRAPPER h6 {
  all: unset;
  display: block;
}
#IL_WRAPPER .sec-ttl {
  font-family: var(--ft) !important;
  font-size: clamp(1.25rem,4.5vw,1.6rem) !important;
  font-weight: 800 !important;
  color: var(--ink) !important;
  padding: 16px 18px 16px 22px !important;
  border-left: 7px solid var(--red) !important;
  background: linear-gradient(90deg,var(--redbg) 0%,#fff 65%) !important;
  border-radius: 0 12px 12px 0 !important;
  margin-bottom: 22px !important;
  line-height: 1.42 !important;
  display: flex !important;
  align-items: center !important;
  gap: 11px !important;
  box-shadow: var(--sh) !important;
  letter-spacing: -.02em !important;
}
#IL_WRAPPER .sec-ttl.b2 {
  background: linear-gradient(90deg,var(--blubg) 0%,#fff 65%) !important;
  border-left-color: var(--blu) !important;
  color: var(--blu) !important;
}
#IL_WRAPPER p { margin: 0 !important; padding: 0 !important; }
"""


# ══════════════════════════════════════════════════════════════
# JAVASCRIPT ADDITIONS
# ══════════════════════════════════════════════════════════════

VIDEO_BOX_JS = """
// ── Dual-mode video box functions (added by convert_to_wp.py) ──

// Click on box → PC file picker
function vidBoxClick(id){
  const box=document.getElementById('mb-'+id);
  if(box.classList.contains('filled'))return;
  document.getElementById('fi-'+id).click();
}
function vidReplace(id){vidClear(id);document.getElementById('fi-'+id).click()}
function vidClear(id){
  const box=document.getElementById('mb-'+id);
  const vid=box.querySelector('video'),ifr=box.querySelector('iframe');
  if(vid)vid.remove();
  if(ifr)ifr.remove();
  box.classList.remove('filled');
  const ph=document.getElementById('ph-'+id);
  if(ph)ph.style.display='';
  const inp=document.getElementById('src-'+id);
  if(inp){inp.value='';inp.classList.remove('has-url')}
  removeItem(id);
}

// PC file → <video> tag
function vidLoadFile(id,inp){
  if(!inp.files||!inp.files[0])return;
  const file=inp.files[0];
  const url=URL.createObjectURL(file);
  _applyVid(id,url,false);
  const srcInp=document.getElementById('src-'+id);
  if(srcInp){srcInp.value=file.name;srcInp.classList.add('has-url')}
}
function _applyVid(id,src,save){
  const box=document.getElementById('mb-'+id);
  if(!box)return;
  const ph=document.getElementById('ph-'+id);
  if(ph)ph.style.display='none';
  const ifr=box.querySelector('iframe');if(ifr)ifr.remove();
  let vid=box.querySelector('video');
  if(!vid){
    vid=document.createElement('video');
    vid.style.cssText='width:100%;height:100%;min-height:200px;display:block;border-radius:12px;background:#000';
    vid.controls=true;
    box.insertBefore(vid,box.querySelector('.mctrl'));
  }
  vid.src=src;
  box.classList.add('filled');
  box.style.minHeight='220px';
  box.onclick=null;
}

// Source field: real-time preview (green border when YouTube URL detected)
function vidSrcPreview(id,val){
  const inp=document.getElementById('src-'+id);
  if(ytEmbed(val)){inp.classList.add('has-url')}
  else{inp.classList.remove('has-url')}
}

// Source field: Enter or ▶ Embed button
function vidSrcApply(id){
  const inp=document.getElementById('src-'+id);
  const val=inp.value.trim();
  if(!val)return;
  const em=ytEmbed(val);
  if(em){
    _applyYt(id,em,true);
    inp.classList.add('has-url');
  } else if(val.startsWith('http')){
    _applyVid(id,val,false);
    inp.classList.add('has-url');
  } else {
    inp.style.borderColor='var(--red)';
    setTimeout(()=>{inp.style.borderColor=''},1200);
  }
}
"""


# ══════════════════════════════════════════════════════════════
# MAIN CONVERTER
# ══════════════════════════════════════════════════════════════

def convert(input_path, output_path, wrapper_id='il-epx-wrap'):
    with open(input_path, 'r', encoding='utf-8') as f:
        original = f.read()

    # ── Detect EP number for wrapper ID ──
    ep_match = re.search(r'ep[-_]?(\d+)', input_path, re.IGNORECASE)
    if ep_match:
        wrapper_id = f'il-ep{ep_match.group(1)}-wrap'

    print(f"  Wrapper ID : #{wrapper_id}")

    # ── Extract sections ──
    style  = extract(r'<style>(.*?)</style>', original)
    body   = extract(r'<body>(.*?)</body>',   original)
    scripts = re.findall(r'<script>(.*?)</script>', original, re.DOTALL)
    script = '\n'.join(scripts)

    body_clean = re.sub(r'<script>.*?</script>', '', body, flags=re.DOTALL).strip()

    # ── Scope CSS ──
    scoped_css = scope_css(style, wrapper_id)

    # ── Replace video boxes ──
    vid_ids = re.findall(r'id="mb-(s\dv)"', body_clean)
    vid_ids = list(dict.fromkeys(vid_ids))  # deduplicate, preserve order
    print(f"  Video boxes: {vid_ids}")

    for vid_id in vid_ids:
        old_pattern = (
            r'<div class="mbox-wrap">\s*'
            r'<div class="mbox-label">🎬[^<]*</div>\s*'
            r'<div class="mbox" id="mb-' + re.escape(vid_id) + r'".*?'
            r'</div>\s*'   # mctrl
            r'</div>\s*'   # mbox
            r'</div>'      # mbox-wrap
        )
        new_html = make_video_box_html(vid_id)
        body_clean, n = re.subn(old_pattern, new_html, body_clean, flags=re.DOTALL)
        print(f"    {vid_id}: {'✅ replaced' if n else '⚠️  not found'}")

    # ── Fix mbClick for image boxes only (remove old vid branch) ──
    script = script.replace(
        "function mbClick(id){const box=document.getElementById('mb-'+id);if(box.classList.contains('filled'))return;if(box.dataset.t==='img')document.getElementById('fi-'+id).click();else ytOpen(id)}",
        "function mbClick(id){const box=document.getElementById('mb-'+id);if(box.classList.contains('filled'))return;document.getElementById('fi-'+id).click()}"
    )
    script = script.replace(
        "function mbReplace(id){mbClear(id);const box=document.getElementById('mb-'+id);if(box.dataset.t==='img')document.getElementById('fi-'+id).click();else ytOpen(id)}",
        "function mbReplace(id){mbClear(id);document.getElementById('fi-'+id).click()}"
    )

    # ── Build heading overrides with correct wrapper ID ──
    heading_overrides = WP_HEADING_OVERRIDES.replace('#IL_WRAPPER', f'#{wrapper_id}')

    # ── Assemble output ──
    output = f"""<!-- 
  ╔══════════════════════════════════════════════════════╗
  ║  IssueLens — WordPress Custom HTML Block             ║
  ║  Generated by convert_to_wp.py                       ║
  ║                                                      ║
  ║  HOW TO USE:                                         ║
  ║  1. WordPress Block Editor → Add block               ║
  ║  2. Search "Custom HTML" → paste entire file         ║
  ║  3. Preview → Publish                                ║
  ║                                                      ║
  ║  MEDIA BOXES:                                        ║
  ║  🖼️  Image  : click box → select file from PC        ║
  ║  🎬 Video  : click box → select video file from PC  ║
  ║             Source field → paste YouTube URL         ║
  ╚══════════════════════════════════════════════════════╝
-->

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Noto+Sans:wght@400;500;700;900&display=swap" rel="stylesheet">

<style>
{scoped_css}
{VIDEO_BOX_CSS}
{heading_overrides}
</style>

<div id="{wrapper_id}">
{body_clean}
</div>

<script>
{script}
{VIDEO_BOX_JS}
</script>"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"  Output     : {output_path} ({size_kb:.1f} KB)")
    return output_path


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: file not found → {input_file}")
        sys.exit(1)

    base = os.path.splitext(input_file)[0]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else f"{base}_wordpress.html"

    print(f"\n🔄 IssueLens EPx → WordPress Converter")
    print(f"  Input      : {input_file}")
    convert(input_file, output_file)
    print(f"  ✅ Done!\n")
