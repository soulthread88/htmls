#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║   IssueLens English Master Automation Pipeline  v1.0            ║
║   Target: US / Global English-speaking audience                  ║
║   Output: 4 Blogs + 7 SNS platforms — publish-ready content     ║
╚══════════════════════════════════════════════════════════════════╝

Usage:
    python3 issuelens_pipeline_eng.py --ep ep01-eng-raw.html
    python3 issuelens_pipeline_eng.py --all ./  (processes all ep*-eng-raw.html)
"""

import os, re, sys, json, argparse
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
import html as html_lib

BASE_DIR = Path(__file__).parent.parent

SNS_LINKS = {
    "youtube":   "https://www.youtube.com/@IssueLens",
    "instagram": "https://www.instagram.com/issuelens",
    "tiktok":    "https://www.tiktok.com/@issuelens",
    "threads":   "https://www.threads.net/@issuelens",
    "twitter":   "https://x.com/issuelens",
    "facebook":  "https://www.facebook.com/issuelens",
    "substack":  "https://issuelens.substack.com",
    "wordpress": "https://issuelens.com",
}

# ── Meta extractor ──────────────────────────────────────────────
class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title=""; self.description=""; self.keywords=[]
        self.og_title=""; self.og_description=""; self._in_title=False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag=="title": self._in_title=True
        elif tag=="meta":
            n=a.get("name",""); p=a.get("property",""); c=a.get("content","")
            if n=="description":       self.description=c
            elif n=="keywords":        self.keywords=[k.strip() for k in c.split(",")]
            elif p=="og:title":        self.og_title=c
            elif p=="og:description":  self.og_description=c

    def handle_endtag(self, tag):
        if tag=="title": self._in_title=False

    def handle_data(self, data):
        if self._in_title: self.title += data.strip()


def strip(s): return re.sub(r'<[^>]+>','', s).strip()

def extract_meta(html_path: Path) -> dict:
    raw = html_path.read_text(encoding="utf-8")
    p = MetaParser(); p.feed(raw)

    ep_m = re.search(r'EP\.?(\d+)', p.title, re.IGNORECASE)
    ep_num = ep_m.group(1).zfill(2) if ep_m else "00"

    h1_m = re.search(r'class="headline"[^>]*>(.*?)</h1>', raw, re.DOTALL)
    h1   = strip(h1_m.group(1)) if h1_m else p.og_title

    sec_titles = [strip(t) for t in re.findall(
        r'class="sec-ttl[^"]*"[^>]*>.*?<span class="num">\d+</span>(.*?)</h2>', raw, re.DOTALL)]

    intro_m = re.search(r'class="intro[^"]*"[^>]*>(.*?)</p>', raw, re.DOTALL)
    intro   = strip(intro_m.group(1)) if intro_m else ""

    pq_m = re.search(r'class="pq-txt"[^>]*>(.*?)</div>', raw, re.DOTALL)
    pq   = strip(pq_m.group(1)) if pq_m else ""

    # Pull-quote fallback
    if not pq:
        pq_m2 = re.search(r'<blockquote[^>]*>(.*?)</blockquote>', raw, re.DOTALL)
        pq = strip(pq_m2.group(1))[:200] if pq_m2 else ""

    ac_titles = [strip(t) for t in re.findall(r'class="ac-ttl"[^>]*>(.*?)</div>', raw, re.DOTALL)]
    ac_descs  = [strip(t) for t in re.findall(r'class="ac-desc"[^>]*>(.*?)</div>', raw, re.DOTALL)]
    actions   = [{"title":t,"desc":d} for t,d in zip(ac_titles,ac_descs)]

    tags    = re.findall(r'class="tag[^"]*">(#[^<]+)</span>', raw)
    bignums = [strip(b) for b in re.findall(r'class="bignum">(.*?)</span>', raw, re.DOTALL)]
    biglbls = [strip(b) for b in re.findall(r'class="biglbl">(.*?)</span>', raw, re.DOTALL)]
    stats   = [(strip(n), strip(l)) for n,l in re.findall(
        r'class="stat-n">(.*?)</span>.*?class="stat-l">(.*?)</span>', raw, re.DOTALL)]

    # Unescape HTML entities in key fields
    def uesc(s): return html_lib.unescape(s)

    return {
        "ep_num": ep_num, "title": uesc(p.title), "h1": uesc(h1),
        "description": uesc(p.description), "keywords": p.keywords,
        "og_title": uesc(p.og_title), "og_description": uesc(p.og_description),
        "section_titles": [uesc(s) for s in sec_titles],
        "intro": uesc(intro), "pq": uesc(pq),
        "actions": [{"title":uesc(a["title"]),"desc":uesc(a["desc"])} for a in actions],
        "tags": tags, "bignums": bignums, "biglbls": biglbls,
        "stats": [(uesc(n),uesc(l)) for n,l in stats],
        "raw": raw, "path": html_path,
    }


# ── Folder scaffold ──────────────────────────────────────────────
def scaffold(ep_dir: Path):
    for sub in [
        "blogs/tistory","blogs/naver","blogs/substack","blogs/wordpress",
        "sns/youtube_longform","sns/youtube_shorts","sns/instagram",
        "sns/tiktok","sns/facebook","sns/x_twitter","sns/threads",
        "assets","seo"]:
        (ep_dir / sub).mkdir(parents=True, exist_ok=True)


# ════════════════════════════════════════════════════════════════
#  BLOG GENERATORS
# ════════════════════════════════════════════════════════════════

def make_tistory(m, out):
    html = m["raw"]
    # Inject real SNS links
    for key, url in SNS_LINKS.items():
        html = re.sub(rf'href="#{re.escape(key.upper())}_URL"', f'href="{url}"', html, flags=re.IGNORECASE)
    banner = (f'<!-- ▶ Tistory English Edition | IssueLens EP.{m["ep_num"]} ◀ -->\n'
              f'<div style="background:#C8001A;color:#fff;text-align:center;padding:10px 16px;'
              f'font-family:Inter,sans-serif;font-size:14px;font-weight:700;letter-spacing:.04em">'
              f'📌 IssueLens EP.{m["ep_num"]} — Tistory English Edition · New Episode Every Day</div>')
    html = html.replace('<div id="pb"></div>', f'<div id="pb"></div>\n{banner}')
    (out/"blogs"/"tistory"/f'issuelens-ep{m["ep_num"]}-eng-tistory.html').write_text(html, encoding="utf-8")
    print(f'  ✅ Tistory: issuelens-ep{m["ep_num"]}-eng-tistory.html')


def make_naver(m, out):
    kw  = ", ".join(m["keywords"][:20])
    stats_html = "\n".join([
        f'<span style="display:inline-block;background:#FFF0F3;border:2px solid #FFCCD5;border-radius:12px;'
        f'padding:10px 18px;margin:5px;text-align:center">'
        f'<strong style="font-size:1.4rem;color:#C8001A">{n}</strong>'
        f'<br><small style="color:#4B5563">{l}</small></span>'
        for n,l in m["stats"]]) if m["stats"] else ""
    sec_li  = "\n".join([f"<li>{t}</li>" for t in m["section_titles"]])
    act_html = "\n".join([
        f'<p style="margin:8px 0;padding:12px 16px;background:#F7F9FC;border-left:4px solid #1E3A8A;border-radius:4px">'
        f'<strong style="color:#C8001A">▶ {a["title"]}</strong><br>{a["desc"]}</p>'
        for a in m["actions"]])
    tags_str = "  ".join(m["tags"][:15])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{m['title']}</title>
<meta name="description" content="{m['description']}">
<meta name="keywords" content="{kw}">
<style>
body{{font-family:'Inter','Segoe UI',sans-serif;font-size:18px;line-height:1.85;color:#0A0A0A;max-width:860px;margin:0 auto;padding:20px;word-break:normal}}
h1{{font-size:2rem;font-weight:800;color:#0A0A0A;line-height:1.3;border-bottom:4px solid #C8001A;padding-bottom:12px;margin-bottom:20px}}
h2{{font-size:1.25rem;font-weight:700;color:#fff;background:#C8001A;padding:10px 16px;border-radius:6px;margin:32px 0 16px}}
.intro-box{{background:#FFFBEB;border-left:6px solid #F59E0B;padding:18px 20px;border-radius:4px;margin:20px 0;font-weight:500}}
.stat-row{{text-align:center;margin:20px 0}}
.quote-box{{background:#FFF8F0;border-top:4px solid #0A0A0A;border-bottom:4px solid #0A0A0A;padding:24px;text-align:center;font-size:1.2rem;font-weight:800;margin:28px 0;font-style:italic}}
.tag-area{{margin:16px 0}}
.tag{{display:inline-block;background:#FFF0F3;border:2px solid #FFCCD5;color:#C8001A;font-weight:700;padding:4px 12px;border-radius:20px;margin:3px;font-size:14px}}
.footer-note{{background:#F7F9FC;border:1px solid #CBD5E1;padding:16px;border-radius:8px;font-size:15px;color:#4B5563;margin-top:32px;text-align:center}}
img{{max-width:100%;border-radius:10px;margin:16px 0}}
.media-placeholder{{background:#F1F5F9;border:2px dashed #CBD5E1;border-radius:12px;padding:30px;text-align:center;color:#64748B;margin:20px 0}}
cite{{font-style:italic;font-size:15px;color:#6B7280}}
</style>
</head>
<body>

<p style="background:#C8001A;color:#fff;padding:10px 14px;border-radius:6px;font-size:14px;font-weight:700;text-align:center">
📌 IssueLens EP.{m["ep_num"]} — Naver Blog English Edition · New Episode Daily
</p>

<h1>{m["og_title"]}</h1>

<div class="stat-row">{stats_html}</div>

<div class="intro-box">{m["intro"]}</div>

<div class="tag-area">{tags_str}</div>

<hr style="border:none;border-top:2px solid #E2E8F0;margin:28px 0">

<h2>📋 What You'll Learn in This Issue</h2>
<ol style="padding-left:20px;line-height:2.2">{sec_li}</ol>

<hr style="border:none;border-top:2px solid #E2E8F0;margin:28px 0">

<div class="media-placeholder">
🖼️ Image: Section 1 — Insert relevant image here (1200×675px recommended)
</div>

<div style="background:#FFF0F3;border:2px solid #FFCCD5;border-top:5px solid #C8001A;padding:20px;border-radius:12px;margin:20px 0">
<strong style="color:#C8001A;font-size:1.1rem">📊 Key Data: {m["bignums"][0] if m["bignums"] else ""}</strong><br>
<span style="color:#4B5563">{m["biglbls"][0] if m["biglbls"] else ""}</span>
</div>

<div class="media-placeholder">
🖼️ Image: Section 2 — Insert relevant image here (1200×675px recommended)
</div>

<div style="background:#EFF6FF;border:2px solid #BFDBFE;border-top:5px solid #1E3A8A;padding:20px;border-radius:12px;margin:20px 0">
<strong style="color:#1E3A8A">📌 Context</strong><br>{m["og_description"]}
</div>

<div class="media-placeholder">
🖼️ Image: Section 3 — Insert relevant image here (1200×675px recommended)
</div>

<div class="quote-box">"{m["pq"]}"</div>

<h2>🛡️ Action Items — What You Can Do Right Now</h2>
{act_html}

<hr style="border:none;border-top:2px solid #E2E8F0;margin:28px 0">

<div class="footer-note">
<strong>IssueLens</strong> | EP.{m["ep_num"]} | Daily in-depth issue analysis<br>
YouTube · Instagram · TikTok · Threads · X · Facebook: <strong>@IssueLens</strong><br>
<cite>All statistics and claims are sourced from official government publications, peer-reviewed research, and credible news organizations. Sources cited inline throughout.</cite>
</div>

</body>
</html>"""
    (out/"blogs"/"naver"/f'issuelens-ep{m["ep_num"]}-eng-naver.html').write_text(html, encoding="utf-8")
    print(f'  ✅ Naver (EN): issuelens-ep{m["ep_num"]}-eng-naver.html')


def make_substack(m, out):
    today  = datetime.now().strftime("%B %d, %Y")
    kw_str = " · ".join(m["keywords"][:12])
    acts   = "\n".join([f"**{a['title']}**\n{a['desc']}\n" for a in m["actions"]])
    stats_md = "\n".join([f"| {n} | {l} |" for n,l in m["stats"]]) if m["stats"] else "| — | — |"
    secs   = "".join([f"- {t}\n" for t in m["section_titles"]])

    md = f"""# {m["og_title"]}

**IssueLens EP.{m["ep_num"]}** · {today}

> *{m["description"]}*

---

## 📊 Key Numbers

| Stat | What It Means |
|------|--------------|
{stats_md}

---

## The Big Picture

{m["intro"]}

---

## In This Issue

{secs}

---

## Key Data Points

{"".join([f'- **{n}** — {l}\n' for n,l in zip(m["bignums"],m["biglbls"])])}

---

> **"{m["pq"]}"**

---

## 🛡️ Action Items

{acts}

---

## 🔍 Keywords

{kw_str}

---

*IssueLens EP.{m["ep_num"]} · All statistics sourced from official government publications, peer-reviewed research, and credible news organizations.*

*[YouTube]({SNS_LINKS["youtube"]}) · [Instagram]({SNS_LINKS["instagram"]}) · [TikTok]({SNS_LINKS["tiktok"]}) · [Threads]({SNS_LINKS["threads"]}) · [X]({SNS_LINKS["twitter"]})*
"""
    (out/"blogs"/"substack"/f'issuelens-ep{m["ep_num"]}-eng-substack.md').write_text(md, encoding="utf-8")
    print(f'  ✅ Substack: issuelens-ep{m["ep_num"]}-eng-substack.md')


def make_wordpress(m, out):
    html = m["raw"]
    comment = (f'<!--\n  WordPress.org English Edition | IssueLens EP.{m["ep_num"]}\n'
               f'  Recommended plugins: Yoast SEO, WP Rocket, Smush\n'
               f'  Tags: {", ".join(m["keywords"][:10])}\n-->\n')
    html = html.replace("<!DOCTYPE html>", f"<!DOCTYPE html>\n{comment}")
    banner = (f'<div style="background:#C8001A;color:#fff;text-align:center;padding:10px 16px;'
              f'font-family:Inter,sans-serif;font-size:14px;font-weight:700">'
              f'📌 IssueLens EP.{m["ep_num"]} | WordPress English Edition · '
              f'<a href="{SNS_LINKS["wordpress"]}" style="color:#FCA5A5">issuelens.com</a></div>')
    html = html.replace('<div id="pb"></div>', f'<div id="pb"></div>\n{banner}')
    for key, url in SNS_LINKS.items():
        html = re.sub(rf'href="#{re.escape(key.upper())}_URL"', f'href="{url}"', html, flags=re.IGNORECASE)
    (out/"blogs"/"wordpress"/f'issuelens-ep{m["ep_num"]}-eng-wordpress.html').write_text(html, encoding="utf-8")
    print(f'  ✅ WordPress: issuelens-ep{m["ep_num"]}-eng-wordpress.html')


# ════════════════════════════════════════════════════════════════
#  SNS GENERATORS  (English / US-Global optimized)
# ════════════════════════════════════════════════════════════════

def make_youtube_longform(m, out):
    ep  = m["ep_num"]
    kws = m["keywords"]

    # Build EP-specific title variants from real headline
    base_title = m["og_title"]
    script = f"""╔══════════════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — YouTube LONG-FORM Script (English)      ║
║  Target Runtime: 12–18 minutes · US / Global Audience        ║
╚══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎬 TITLE A/B/C TESTS (pick highest CTR)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A. {base_title}
B. {m["h1"]} — FULL BREAKDOWN [{datetime.now().year}]
C. The Truth They Don't Want You to Know: {m["og_description"][:80]}... | IssueLens EP.{ep}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎤 HOOK  (0:00–0:35) — Pattern Interrupt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SCREEN: fast-cut montage relevant to topic]

NARRATION:
"{m["description"][:200]}

In the next {12 if ep < "08" else 15} minutes, I'm going to show you exactly what's happening,
what the data says, and — most importantly — what you can do about it.

If you find this useful, hit subscribe. New episode every single day."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 CHAPTER CARD  (0:35–1:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"Here's what we're covering today:
{"".join([f"{chr(10)}  {chr(9312+i)} {t}" for i,t in enumerate(m["section_titles"][:4])])}
  ⑤ What you can do RIGHT NOW

Let's get into it."

{"".join([f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📌 SECTION {i+1}: {t}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SCREEN: relevant B-roll / data graphic]

NARRATION:
"Let's talk about {t.lower() if t else "this"}. 

{m["og_description"] if i==0 else "This is where it gets really serious."}

[ADD YOUR SOURCED CONTENT HERE — see SEO master file for talking points]

Source your data on-screen:
  Italic caption: Source: [Publication], [Date], [Author]"

[DATA CALLOUT CARD: {"No data" if i >= len(m["bignums"]) else m["bignums"][i]} — {"" if i >= len(m["biglbls"]) else m["biglbls"][i]}]
''' for i,t in enumerate(m["section_titles"][:4])])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🛡️ ACTION ITEMS + CLOSE  (last 2 min)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NARRATION:
"So what do you actually DO with all of this? Here's your action plan:

{"".join([f"  Step {i+1}: {a['title']} — {a['desc'][:100]}{chr(10)}" for i,a in enumerate(m["actions"])])}

I'll leave you with this:

"{m["pq"]}"

If this episode opened your eyes, subscribe and share it with someone who needs to hear this.
I publish a new deep-dive EVERY DAY. See you tomorrow — IssueLens."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📝 YOUTUBE DESCRIPTION  (copy-paste ready)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{m["og_description"]}

{m["description"]}

📌 TIMESTAMPS:
0:00 Hook
0:35 Overview
{"".join([f"~{(i+1)*3}:00 {t}{chr(10)}" for i,t in enumerate(m["section_titles"][:4])])}Final: Action Plan + Close

🔔 Subscribe for a new deep-dive EVERY DAY: {SNS_LINKS["youtube"]}
📱 Instagram: {SNS_LINKS["instagram"]}
🎵 TikTok: {SNS_LINKS["tiktok"]}
🧵 Threads: {SNS_LINKS["threads"]}
🐦 X: {SNS_LINKS["twitter"]}
📘 Facebook: {SNS_LINKS["facebook"]}

⚠️ DISCLAIMER: All information is based on official government reports, credible journalism, and peer-reviewed sources. This is factual public-interest journalism. Sources cited on-screen throughout.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🏷️ YOUTUBE TAGS  (500-char limit)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{", ".join(kws[:25])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎨 THUMBNAIL GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Size: 1280×720px
Background: #C8001A → #0A0A0A gradient (left to right)
Main text: Bold white caps — e.g. "{m["og_title"][:30].upper()}..."
Sub text:  Bright yellow — "THE TRUTH [2025]"
Accent: IssueLens EP.{ep} badge (top-left)
Face/reaction: Optional — shocked expression for emotional CTR
"""
    (out/"sns"/"youtube_longform"/f'issuelens-ep{ep}-eng-youtube-longform.txt').write_text(script, encoding="utf-8")
    print(f'  ✅ YouTube Longform: issuelens-ep{ep}-eng-youtube-longform.txt')


def make_youtube_shorts(m, out):
    ep = m["ep_num"]
    script = f"""╔══════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — YouTube SHORTS Script (English) ║
║  Target: under 60 seconds · 9:16 vertical            ║
╚══════════════════════════════════════════════════════╝

━━━ TITLE OPTIONS (A/B test)
A. {m["og_title"][:60]} #Shorts
B. The {m["section_titles"][0][:40] if m["section_titles"] else "truth"} — 30-second version #Shorts
C. You need to know this NOW 🚨 #{m["keywords"][0].replace(" ","") if m["keywords"] else "IssueLens"} #Shorts

━━━ 60-SECOND SCRIPT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[0–4s] HOOK — STOP THE SCROLL
On-screen text: "{m["og_title"][:45]}..."
Voice: "Stop. Before you scroll, you need to hear this."

[4–15s] THE SHOCKING FACT
Voice: "{m["description"][:160].split(".")[0]}."
[STAT CARD: {m["bignums"][0] if m["bignums"] else "Key stat"} — {m["biglbls"][0] if m["biglbls"] else ""}]

[15–35s] WHY IT MATTERS
Voice: "{m["og_description"][:160]}"
[B-ROLL or animated text cards]

[35–50s] WHAT TO DO
{"".join([f"Voice: Step {i+1}: {a['title']}.{chr(10)}" for i,a in enumerate(m["actions"][:2])])}

[50–58s] QUOTE CARD
"{m["pq"][:100]}"

[58–60s] CTA
"Follow @IssueLens — new episode EVERY day. ↑↑↑"

━━━ SHORTS DESCRIPTION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{m["og_title"]} — 60-second breakdown. Full video on @IssueLens
{" ".join(["#"+k.replace(" ","") for k in m["keywords"][:6]])} #Shorts #IssueLens
"""
    (out/"sns"/"youtube_shorts"/f'issuelens-ep{ep}-eng-youtube-shorts.txt').write_text(script, encoding="utf-8")
    print(f'  ✅ YouTube Shorts: issuelens-ep{ep}-eng-youtube-shorts.txt')


def make_instagram(m, out):
    ep    = m["ep_num"]
    tags  = " ".join(["#"+k.replace(" ","") for k in m["keywords"][:15]])
    extra = "#awareness #viral #trending #fyp #factcheck #breakingnews #IssueLens #education #news #truth"

    content = f"""╔══════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — Instagram CAROUSEL  (10 slides) ║
╚══════════════════════════════════════════════════════╝

━━━ SLIDE 1 — COVER
Headline: {m["og_title"][:50]}
Subhead:  "Swipe to find out →"
Style: IssueLens Red (#C8001A) + Dark gradient
Badge: EP.{ep} top-left | @IssueLens bottom-right
Size: 1080×1080px

━━━ SLIDE 2 — THE SHOCKING NUMBERS
Title: "By the Numbers"
Content:
{chr(10).join([f"  📊 {n} — {l}" for n,l in m["stats"][:4]]) if m["stats"] else "  📊 [Insert key stats here]"}

━━━ SLIDE 3 — THE PROBLEM
Title: "{m["section_titles"][0] if m["section_titles"] else "The Issue"}"
Body: "{m["intro"][:200]}..."
Visual: Relevant infographic / icon

━━━ SLIDE 4 — HOW IT WORKS
Title: "How This Actually Happens"
Body: Data flow / process breakdown
Visual: Step-by-step diagram (arrows)

━━━ SLIDE 5 — THE DATA
Title: "The Hard Numbers"
{chr(10).join([f"  • {n} — {l}" for n,l in zip(m["bignums"],m["biglbls"])])}

━━━ SLIDE 6 — {m["section_titles"][1][:40] if len(m["section_titles"])>1 else "Why This Matters"}
Body: [Content from section 2]
Source citation (italic, -2pt): *Source: [Publication], [Date], [Author]*

━━━ SLIDE 7 — {m["section_titles"][2][:40] if len(m["section_titles"])>2 else "The Big Picture"}
Body: [Content from section 3]

━━━ SLIDE 8 — PRO vs. CON  (if politically contested)
PRO side: [Argument in favor]
CON side: [Argument against]
⚖️ Balanced — both sides shown equally

━━━ SLIDE 9 — ACTION ITEMS
Title: "What You Can Do RIGHT NOW"
{chr(10).join([f"  {i+1}. {a['title']}" for i,a in enumerate(m["actions"])])}

━━━ SLIDE 10 — CTA
"Save this. Share it. Follow @IssueLens."
Subtext: "New deep-dive every single day."
Visual: All platform icons

━━━ CAPTION  (≤2200 chars) ━━━━━━━━━━━━━━━━━━━━━━━━━

{m["og_title"]} 🚨

{m["description"]}

💬 "{m["pq"][:150]}"

👉 Full breakdown at link in bio — IssueLens EP.{ep}
🔔 Follow @IssueLens for a new deep-dive EVERY DAY.

{tags} {extra}

━━━ HASHTAGS (comment drop — 30 max) ━━━━━━━━━━━━━━━
{tags} {extra}
"""
    (out/"sns"/"instagram"/f'issuelens-ep{ep}-eng-instagram.txt').write_text(content, encoding="utf-8")
    print(f'  ✅ Instagram: issuelens-ep{ep}-eng-instagram.txt')


def make_tiktok(m, out):
    ep = m["ep_num"]
    content = f"""╔══════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — TikTok Script (English)         ║
║  30s + 60s versions · 9:16 · auto-captions ON        ║
╚══════════════════════════════════════════════════════╝

━━━ TIKTOK TITLE
{m["og_title"][:80]} 😱 #{m["keywords"][0].replace(" ","") if m["keywords"] else "IssueLens"} #FYP

━━━ 30-SECOND SCRIPT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[0–3s] HOOK
"Wait — you haven't heard about this yet? 🚨"

[3–10s] THE FACT BOMB
"{m["description"][:120].split(".")[0]}."
[TEXT OVERLAY: {m["bignums"][0] if m["bignums"] else "KEY STAT"}]

[10–22s] THE DEEPER PROBLEM
"{m["og_description"][:140]}"
[Fast-cut text cards]

[22–27s] ACTION
"Right now: {m["actions"][0]["title"] if m["actions"] else "Stay informed"}."

[27–30s] CTA
"Follow for daily truth drops. @IssueLens 🔥"

━━━ 60-SECOND EXTENSION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[30–50s]
{chr(10).join([f"Point {i+2}: {t}" for i,t in enumerate(m["section_titles"][1:3])])}
"And here's what most people completely miss..."

[50–58s] QUOTE
"{m["pq"][:100]}"

[58–60s]
"Like + Follow = you'll never miss an episode. @IssueLens"

━━━ TIKTOK CAPTION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{m["og_title"][:80]} 👀

{" ".join(["#"+k.replace(" ","") for k in m["keywords"][:8]])} #FYP #fypage #viral #IssueLens #news #truth

━━━ PRODUCTION NOTES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Format: 1080×1920 (9:16 vertical)
• Captions: Auto-caption ON (accessibility + no-sound viewers)
• Hook font: Bold white + black stroke (max readability)
• BGM: TikTok free library — tension / news beat
• Post time: Tue/Thu/Sat 7–10 PM local
• Hook must land in FIRST 2 SECONDS or viewers scroll
"""
    (out/"sns"/"tiktok"/f'issuelens-ep{ep}-eng-tiktok.txt').write_text(content, encoding="utf-8")
    print(f'  ✅ TikTok: issuelens-ep{ep}-eng-tiktok.txt')


def make_facebook(m, out):
    ep  = m["ep_num"]
    tags = " ".join(["#"+k.replace(" ","") for k in m["keywords"][:10]])
    post = f"""📌 [IssueLens EP.{ep}] {m["og_title"]}

{m["description"]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Key Points:
{"".join([f"  ▶ {t}{chr(10)}" for t in m["section_titles"]])}

📊 The Numbers:
{"".join([f"  • {n} — {l}{chr(10)}" for n,l in zip(m["bignums"],m["biglbls"])])}

🛡️ What You Can Do:
{"".join([f"  {i+1}. {a['title']}: {a['desc'][:80]}...{chr(10)}" for i,a in enumerate(m["actions"])])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 "{m["pq"]}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 Read the full breakdown: [BLOG URL]
🔔 Follow IssueLens for a new episode every day!
📹 YouTube · Instagram · TikTok: @IssueLens

⚠️ All data sourced from official government reports & credible journalism.

{tags} #IssueLens #news #factcheck
"""
    (out/"sns"/"facebook"/f'issuelens-ep{ep}-eng-facebook.txt').write_text(post, encoding="utf-8")
    print(f'  ✅ Facebook: issuelens-ep{ep}-eng-facebook.txt')


def make_x_twitter(m, out):
    ep = m["ep_num"]
    kws5 = " ".join(["#"+k.replace(" ","") for k in m["keywords"][:5]])
    thread = f"""╔══════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — X (Twitter) THREAD              ║
║  Each tweet ≤ 280 chars · 7-tweet thread             ║
╚══════════════════════════════════════════════════════╝

━━━ TWEET 1/7 — HOOK  (pin this one)
🚨 {m["og_title"][:180]}

Thread 🧵👇

━━━ TWEET 2/7 — THE HARD FACTS
{m["description"][:240]}

━━━ TWEET 3/7 — DATA POINT
📊 {m["bignums"][0] if m["bignums"] else "KEY STAT"}: {m["biglbls"][0] if m["biglbls"] else ""}

{m["og_description"][:180]}

━━━ TWEET 4/7 — DEEPER CONTEXT
{m["section_titles"][1] if len(m["section_titles"])>1 else "Here's what most people miss:"}

[Expand with sourced content — 240 chars max]

Source: *[Publication name], [Date]*

━━━ TWEET 5/7 — THE QUOTE
"{m["pq"][:220]}"

━━━ TWEET 6/7 — ACTION ITEMS
What to do RIGHT NOW:

{"".join([f"{i+1}. {a['title']}{chr(10)}" for i,a in enumerate(m["actions"][:3])])}

━━━ TWEET 7/7 — CTA
📌 Full breakdown: [BLOG URL]
🔔 Follow @IssueLens — new deep-dive every single day.

{kws5} #IssueLens
"""
    (out/"sns"/"x_twitter"/f'issuelens-ep{ep}-eng-x-twitter.txt').write_text(thread, encoding="utf-8")
    print(f'  ✅ X (Twitter): issuelens-ep{ep}-eng-x-twitter.txt')


def make_threads(m, out):
    ep   = m["ep_num"]
    tags = " ".join(["#"+k.replace(" ","") for k in m["keywords"][:8]])
    post = f"""╔══════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — Threads Post (English)          ║
╚══════════════════════════════════════════════════════╝

━━━ MAIN POST  (≤500 chars)
🚨 {m["og_title"][:200]}

{m["description"][:200]}

"{m["pq"][:100]}"

👉 Full breakdown at link in bio — IssueLens EP.{ep}

{tags} #IssueLens

━━━ REPLY 1
The hard numbers:
{"".join([f"• {n} — {l}{chr(10)}" for n,l in zip(m["bignums"][:3],m["biglbls"][:3])])}
Source: Official government reports & credible journalism.

━━━ REPLY 2 — ACTION ITEMS
What you can do right now:
{"".join([f"  {i+1}. {a['title']}{chr(10)}" for i,a in enumerate(m["actions"])])}

━━━ REPLY 3 — CTA
Full episode: [BLOG URL]
New deep-dive every single day → Follow @IssueLens
"""
    (out/"sns"/"threads"/f'issuelens-ep{ep}-eng-threads.txt').write_text(post, encoding="utf-8")
    print(f'  ✅ Threads: issuelens-ep{ep}-eng-threads.txt')


# ════════════════════════════════════════════════════════════════
#  ASSETS: Image Prompts + SEO Master
# ════════════════════════════════════════════════════════════════

def make_image_prompts(m, out):
    ep = m["ep_num"]
    secs = m["section_titles"]
    content = f"""╔══════════════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} (English) — AI Image Generation Guide     ║
║  Tools: DALL-E 3 · Midjourney v6 · Adobe Firefly · Canva    ║
╚══════════════════════════════════════════════════════════════╝

━━━━━ SECTION 1 IMAGE (s1i) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: {secs[0] if secs else m["og_title"]}

[DALL-E 3]
Editorial news illustration, dramatic lighting, red #C8001A and dark navy #1E3A8A color palette,
{secs[0] if secs else m["og_title"]} concept, infographic style, high contrast, bold typography space,
16:9 ratio, no text in image, professional journalism aesthetic.

[Midjourney]
/imagine {(secs[0] if secs else m["og_title"]).lower()}, editorial infographic style,
red and dark navy dramatic lighting, news magazine quality --ar 16:9 --v 6 --style raw

[Unsplash search] "{m["keywords"][0] if m["keywords"] else "data security"}" / "{m["keywords"][1] if len(m["keywords"])>1 else "privacy"}"
[Pexels search]   "{m["keywords"][2] if len(m["keywords"])>2 else "surveillance"}"

━━━━━ SECTION 1 VIDEO (s1v) — YouTube search terms ━━━━━━━━━━
• "{m["keywords"][0] if m["keywords"] else ""} explained"
• "{m["keywords"][1] if len(m["keywords"])>1 else ""} documentary"
• "IssueLens EP.{ep} related footage"
Source caption (required): *Source: [YouTube URL]*

━━━━━ SECTION 2 IMAGE (s2i) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: {secs[1] if len(secs)>1 else "Data flow / risk"}

[DALL-E 3]
Data flow diagram illustration, glowing red warning lines connecting smartphones to government servers,
map of US and Asia, editorial news style, ominous atmosphere, 16:9 no text.

[Midjourney]
/imagine data surveillance government national security concept, red warning signals,
map infographic, dramatic editorial news style --ar 16:9 --v 6

[Unsplash] "government surveillance" / "cybersecurity threat" / "data center"

━━━━━ SECTION 2 VIDEO (s2v) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• "{m["keywords"][3] if len(m["keywords"])>3 else "national security"} congressional hearing"
• "{m["keywords"][4] if len(m["keywords"])>4 else "data privacy"} news report"

━━━━━ SECTION 3 IMAGE (s3i) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: {secs[2] if len(secs)>2 else "Asymmetric comparison"}

[DALL-E 3]
Asymmetric balance scale infographic, one side blocked (firewall/censorship),
other side open data flowing, flat design, red and blue contrast, editorial news, 16:9.

[Midjourney]
/imagine asymmetric trade data imbalance infographic, editorial flat design,
red and blue high contrast --ar 16:9 --v 6

━━━━━ YOUTUBE THUMBNAIL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[DALL-E 3]
YouTube thumbnail, ultra high contrast, shocked person holding phone, red background,
large bold white text space on left, warning icons, 1280x720px, no actual text generated.
Color: #C8001A background, white text area, black accents.

[Canva Guide]
Size: 1280×720px
BG: #C8001A → #0A0A0A left-to-right gradient
Main text: "{m["og_title"][:35].upper()}" — Inter Black, white, 80–90pt
Sub text: "THE TRUTH [2025]" — Inter Bold, #FCD34D yellow, 50pt
Badge: IssueLens EP.{ep} — top left

━━━━━ INSTAGRAM CAROUSEL (10 slides) ━━━━━━━━━━━━━━━━━━━━━━━
Size: 1080×1080px (square) or 1080×1350px (portrait — more reach)
Design tool: Canva → search "news card dark"
Palette: #C8001A, #1E3A8A, #FFFFFF, #0A0A0A, #FCD34D (accent)
Font: Inter Black + Inter Regular

━━━━━ FREE IMAGE SOURCES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Unsplash.com — high quality, free commercial use
2. Pexels.com — free stock photo + video
3. Pixabay.com — free, no attribution required
4. Flaticon.com — icons (attribution required on free plan)
5. Wikimedia Commons — government/official photos (check license)
6. AP Images (apimages.com) — editorial use (subscription)
"""
    (out/"assets"/f'issuelens-ep{ep}-eng-image-prompts.txt').write_text(content, encoding="utf-8")
    print(f'  ✅ Image Prompts: issuelens-ep{ep}-eng-image-prompts.txt')


def make_seo_master(m, out):
    ep  = m["ep_num"]
    kws = m["keywords"]
    content = f"""╔══════════════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} (English) — SEO MASTER FILE                ║
║  Target: US / Global English Audience                          ║
║  Goal: 1 Million Subscribers in 30 Days                        ║
╚══════════════════════════════════════════════════════════════╝

━━━━━ 1. META TAGS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title (≤60 chars):    {m["title"][:60]}
Description (≤160):   {m["description"][:160]}
OG Title:             {m["og_title"]}
OG Description:       {m["og_description"]}

━━━━━ 2. PRIMARY KEYWORDS (high-volume, Google/YouTube) ━━━━━━━
{chr(10).join([f"  • {k}" for k in kws[:15]])}

━━━━━ 3. LONG-TAIL KEYWORDS (low competition, high intent) ━━━━━
  • {kws[0] if kws else ""} 2026
  • is {kws[0] if kws else "this"} dangerous
  • how to protect yourself from {kws[1] if len(kws)>1 else ""}
  • {kws[2] if len(kws)>2 else ""} explained simply
  • what the FBI says about {kws[0] if kws else ""}
  • {kws[3] if len(kws)>3 else ""} threat to democracy
  • should I be worried about {kws[1] if len(kws)>1 else ""}
  • {kws[0] if kws else ""} vs privacy rights
  • government warning {kws[2] if len(kws)>2 else ""}
  • {kws[4] if len(kws)>4 else ""} national security risk

━━━━━ 4. YOUTUBE-SPECIFIC SEARCH TERMS ━━━━━━━━━━━━━━━━━━━━━━━━
  • {(kws[0]+" explained video") if kws else ""}
  • {(kws[1]+" documentary 2026") if len(kws)>1 else ""}
  • {(kws[0]+" should i be worried") if kws else ""}
  • {(kws[2]+" full breakdown") if len(kws)>2 else ""}

━━━━━ 5. INSTAGRAM / TIKTOK HASHTAG STRATEGY ━━━━━━━━━━━━━━━━━━
[Tier 1 — Mega (>1M posts, broad reach)]
#news #viral #fyp #trending #politics #technology #security

[Tier 2 — Mid (100K–1M, targeted)]
{" ".join(["#"+k.replace(" ","") for k in kws[:8]])}

[Tier 3 — Niche (exact match, high conversion)]
{" ".join(["#"+k.replace(" ","").replace("'","") for k in kws[8:15]])}

[Brand]
#IssueLens #IssueLensEP{ep} #DailyDeepDive

━━━━━ 6. PLATFORM PUBLISHING SCHEDULE ━━━━━━━━━━━━━━━━━━━━━━━━━
[Blog Posts]
  • SubStack:   8:00 AM EST (newsletter open-rate peak)
  • WordPress:  8:30 AM EST
  • Tistory:    7:00 AM KST
  • Naver Blog: 8:00 AM KST

[Video]
  • YouTube Longform: 9:00 AM EST (Thu/Fri best for subscribers)
  • YouTube Shorts:   12:00 PM EST (lunch scroll)

[Social]
  • Instagram: 7–9 PM local (Tue/Thu/Sun best)
  • TikTok:    7–10 PM local (Tue/Thu/Sat best)
  • Threads:   8 PM local
  • X:         8:30 PM local
  • Facebook:  9 PM local

━━━━━ 7. CONTROVERSIAL TOPICS — PRO/CON BALANCE NOTE ━━━━━━━━━━
Per IssueLens editorial policy:
  ✅ Political topics → ALWAYS show PRO and CON equally
  ✅ All statistics → cite source inline (italic, -2pt)
  ✅ YouTube video embeds → Source: [URL]
  ✅ No speculative content — verified facts only
  ✅ No named individuals without documented evidence

━━━━━ 8. 30-DAY GROWTH ROADMAP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1 — Foundation
  • Publish EP.01–03 across all 11 platforms
  • Optimize YouTube channel: banner, description, playlist
  • Unify all accounts: @IssueLens everywhere

Week 2 — Cross-promotion
  • Each platform drives to others
  • Reply to EVERY comment within 2 hours (algorithm signal)
  • Tag relevant accounts (researchers, journalists, NGOs)

Week 3 — Viral amplification
  • Identify best-performing format → double down
  • Shorts/Reels drive traffic → blog/YouTube
  • Pitch to newsletters in your niche

Week 4 — Scale
  • Press release to tech/security journalists
  • Guest post on Medium / Substack in same niche
  • EP.13 finale — special long-form
  • Begin EP.14+ planning
"""
    (out/"seo"/f'issuelens-ep{ep}-eng-seo-master.txt').write_text(content, encoding="utf-8")
    print(f'  ✅ SEO Master: issuelens-ep{ep}-eng-seo-master.txt')


# ════════════════════════════════════════════════════════════════
#  PIPELINE RUNNER
# ════════════════════════════════════════════════════════════════

def run(html_path: Path, output_base: Path):
    print(f"\n{'='*62}")
    print(f"  🚀 IssueLens ENGLISH Pipeline | {html_path.name}")
    print(f"{'='*62}")

    m   = extract_meta(html_path)
    ep  = m["ep_num"]
    print(f"  📌 EP.{ep}: {m['og_title'][:60]}")

    ep_dir = output_base / f"ep{ep}-eng"
    scaffold(ep_dir)

    print(f"\n  📝 Blog versions:")
    make_tistory(m,   ep_dir)
    make_naver(m,     ep_dir)
    make_substack(m,  ep_dir)
    make_wordpress(m, ep_dir)

    print(f"\n  📱 SNS content:")
    make_youtube_longform(m, ep_dir)
    make_youtube_shorts(m,   ep_dir)
    make_instagram(m,        ep_dir)
    make_tiktok(m,           ep_dir)
    make_facebook(m,         ep_dir)
    make_x_twitter(m,        ep_dir)
    make_threads(m,          ep_dir)

    print(f"\n  🎨 Assets:")
    make_image_prompts(m, ep_dir)
    make_seo_master(m,    ep_dir)

    total = sum(1 for _ in ep_dir.rglob("*") if _.is_file())
    print(f"\n{'='*62}")
    print(f"  ✅ EP.{ep} English complete! | {total} files → {ep_dir.name}/")
    print(f"{'='*62}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep",  help="Single episode HTML path")
    ap.add_argument("--all", help="Folder — process all ep*-eng-raw.html files")
    ap.add_argument("--out", default=str(BASE_DIR))
    args = ap.parse_args()

    base = Path(args.out)
    if args.ep:
        run(Path(args.ep), base)
    elif args.all:
        files = sorted(Path(args.all).glob("ep*-eng-raw.html"))
        print(f"  📂 Found {len(files)} English episodes")
        for f in files:
            run(f, base)
    else:
        print("Usage: python3 issuelens_pipeline_eng.py --ep <file.html>")
        print("       python3 issuelens_pipeline_eng.py --all <folder>")
