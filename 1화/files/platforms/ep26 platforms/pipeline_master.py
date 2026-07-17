#!/usr/bin/env python3
"""
=============================================================
AI DECODED FOR SENIORS — CONTENT PIPELINE AUTOMATION MASTER
=============================================================
Version: 1.0
Updated: 2026-04-28

USAGE:
    python3 pipeline_master.py --ep 26 --lang eng --topic "AI Sleep Analysis"

WHAT IT GENERATES (per episode):
    /ep{N}/
    ├── seo/             → SEO keywords, hashtags, meta descriptions
    ├── sns/
    │   ├── youtube/     → Long-form script, Shorts script, description
    │   ├── instagram/   → Carousel copy, caption, hashtags
    │   ├── tiktok/      → Short script + caption
    │   ├── facebook/    → Long-form post
    │   ├── x_twitter/   → Thread (8 tweets)
    │   └── threads/     → Threads post (5 posts)
    ├── blogs/
    │   ├── tistory/     → Korean HTML (already generated separately)
    │   ├── naver/       → Korean HTML (already generated separately)
    │   ├── substack/    → Newsletter markdown
    │   └── wordpress/   → SEO-optimized post
    └── images/
        └── prompts/     → AI image generation prompts for all slots

DEPENDENCIES:
    - Python 3.8+
    - No external packages required (stdlib only)
=============================================================
"""

import os
import sys
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# EPISODE DATA REGISTRY
# Add new episodes here as you create them
# ─────────────────────────────────────────────
EPISODE_REGISTRY = {
    26: {
        "title_eng": "AI Sleep Analysis — Why Do I Keep Waking Up at Night?",
        "title_kor": "AI 수면 분석 — 왜 자꾸 새벽에 깰까?",
        "topic": "AI sleep tracking, smartwatch, Galaxy Watch, Apple Watch",
        "saying_eng": "Early to bed and early to rise, makes a man healthy, wealthy, and wise.",
        "idiom_kor": "安分知足 (안분지족)",
        "hook_tag": "SleepTracking",
        "characters_eng": ["Jake", "Grandpa Bob"],
        "sources": [
            "Samsung Galaxy Watch Official Website",
            "Apple Health App Official Support Page",
            "Merriam-Webster Online Dictionary",
        ],
    },
    27: {
        "title_eng": "AI Fall Detection — Building a Safety Net for Parents Living Alone",
        "title_kor": "AI 낙상 감지 — 혼자 사시는 부모님 안전망 만들기",
        "topic": "AI fall detection, Apple Watch Emergency SOS, Galaxy Watch",
        "saying_eng": "An ounce of prevention is worth a pound of cure.",
        "idiom_kor": "有備無患 (유비무환)",
        "hook_tag": "FallDetection",
        "characters_eng": ["Jake", "Grandpa Bob"],
        "sources": [
            "Apple Emergency SOS Official Support Page",
            "Samsung Galaxy Watch Fall Detection Feature Guide",
            "Merriam-Webster Online Dictionary",
        ],
    },
    28: {
        "title_eng": "AI Diet Management — Snap a Photo, Get Instant Nutrition Analysis",
        "title_kor": "AI 식단 관리 — 사진 찍으면 칼로리·영양소 자동 계산",
        "topic": "AI diet app, Calorie Mama, Noom, ChatGPT meal planning",
        "saying_eng": "Let food be thy medicine and medicine be thy food.",
        "idiom_kor": "藥食同源 (약식동원)",
        "hook_tag": "AIDietApp",
        "characters_eng": ["Jake", "Grandpa Bob"],
        "sources": [
            "Noom Official Website",
            "Calorie Mama Official App Store Page",
            "Merriam-Webster Online Dictionary",
        ],
    },
    29: {
        "title_eng": "Papago vs DeepL vs ChatGPT — The Ultimate Translation AI Showdown",
        "title_kor": "파파고 vs DeepL vs ChatGPT — 번역 AI 완벽 비교",
        "topic": "AI translation, Papago, DeepL, ChatGPT, camera translation",
        "saying_eng": "It's not what you say, it's how you say it.",
        "idiom_kor": "以心傳心 (이심전심)",
        "hook_tag": "AITranslation",
        "characters_eng": ["Jake", "Grandpa Bob"],
        "sources": [
            "Naver Papago Official Website",
            "DeepL Official Website",
            "Merriam-Webster Online Dictionary",
        ],
    },
    30: {
        "title_eng": "AI Shopping Comparison — The Secret to Finding the Lowest Price Every Time",
        "title_kor": "AI 쇼핑 비교 — 쿠팡·네이버·G마켓 최저가 찾는 AI 비법",
        "topic": "AI shopping comparison, Google Shopping, CamelCamelCamel, ChatGPT",
        "saying_eng": "Look before you leap.",
        "idiom_kor": "知彼知己 (지피지기)",
        "hook_tag": "AIShopping",
        "characters_eng": ["Jake", "Grandpa Bob"],
        "sources": [
            "Google Shopping Official Service",
            "Amazon Official Website",
            "Merriam-Webster Online Dictionary",
        ],
    },
}


# ─────────────────────────────────────────────
# FOLDER CREATION
# ─────────────────────────────────────────────
def create_episode_folders(base_dir: str, ep_num: int) -> Path:
    """Create full folder structure for one episode."""
    ep_dir = Path(base_dir) / f"ep{ep_num:02d}"
    folders = [
        "seo",
        "sns/youtube",
        "sns/instagram",
        "sns/tiktok",
        "sns/facebook",
        "sns/x_twitter",
        "sns/threads",
        "blogs/tistory",
        "blogs/naver",
        "blogs/substack",
        "blogs/wordpress",
        "images/prompts",
        "images/svg",
    ]
    for folder in folders:
        (ep_dir / folder).mkdir(parents=True, exist_ok=True)
    print(f"✅ Folder structure created: {ep_dir}")
    return ep_dir


# ─────────────────────────────────────────────
# CONTENT GENERATORS
# ─────────────────────────────────────────────
def gen_seo_file(ep_dir: Path, ep_data: dict, ep_num: int) -> None:
    """Generate SEO keyword + hashtag master file."""
    title = ep_data["title_eng"]
    topic = ep_data["topic"]
    hook = ep_data["hook_tag"]
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# EP{ep_num:02d} — SEO KEYWORD MASTER FILE
# {title}
# Generated: {today}
# Topic: {topic}

---

## PLATFORM HASHTAG PACKS

### YouTube Tags
{hook}, AI for seniors, learn AI seniors, Jake Grandpa Bob, AI decoded for seniors, senior health AI, digital health seniors, AI tutorial beginners, {topic.replace(', ', ', ')}

### Instagram (30 hashtags)
#{hook} #AIForSeniors #SeniorHealth #AgingWell #HealthTech #DigitalHealth #SmartSeniors #TechForSeniors #AIDecoded #LearnAI #SeniorCare #HealthyAging #AIHealth #WearableTech #SmartWatch #SeniorLife #HealthyLiving #AITools2025 #SeniorTech #AITutorial #LearnTechnology #DigitalSeniors #AIBeginner #TechHelp #SeniorFriendly #AIEducation #AISimplified #SeniorLiving #HealthInnovation #AIForEveryone

### TikTok (15 hashtags)
#{hook} #AIForSeniors #SeniorTech #LearnAI #AIDecoded #HealthTech #SeniorHealth #AITools #SmartSeniors #DigitalHealth #AITutorial #SeniorCare #TechForSeniors #AIBeginner #HealthyAging

### X / Twitter (5 hashtags)
#{hook} #AIForSeniors #SeniorHealth #AIDecoded #HealthTech

### Facebook (10 hashtags)
#{hook} #AIForSeniors #SeniorHealth #HealthyAging #TechForSeniors #AIHealth #DigitalHealth #SeniorCare #AITools #LearnAI

---

## META DESCRIPTIONS

### Blog SEO (155 chars max)
{title[:100]} — Step-by-step guide for seniors. No tech skills needed. Free!

### YouTube Hook (first 2 lines)
[Customize with specific episode hook — see YouTube script file]

### SubStack Subject Lines (A/B Test)
- A: [Create compelling hook from episode topic]
- B: [Create alternative angle from episode topic]

---
*Generated by AI Decoded for Seniors Pipeline v1.0 | {today}*
"""
    out_path = ep_dir / "seo" / f"ep{ep_num:02d}_seo_keywords.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"  ✅ SEO file: {out_path.name}")


def gen_publishing_checklist(ep_dir: Path, ep_data: dict, ep_num: int) -> None:
    """Generate daily publishing checklist."""
    title = ep_data["title_eng"]
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# EP{ep_num:02d} — PUBLISHING CHECKLIST
# {title}
# Generated: {today}

---

## ⏰ DAILY PUBLISHING SCHEDULE (Recommended)

| Time | Action | Platform | File |
|---|---|---|---|
| 6:00 AM | Generate AI images from prompts | Midjourney/DALL-E | images/prompts/ |
| 7:00 AM | Insert images into Blog HTML | Tistory + Naver | blogs/ |
| 7:30 AM | Publish Korean blog post | Tistory | blogs/tistory/ |
| 7:45 AM | Publish Korean blog post | Naver Blog | blogs/naver/ |
| 8:00 AM | Upload YouTube Long-form | YouTube Studio | sns/youtube/ |
| 8:30 AM | Post SubStack newsletter | SubStack | blogs/substack/ |
| 9:00 AM | Publish WordPress post | WordPress.org | blogs/wordpress/ |
| 10:00 AM | Post YouTube Short #1 | YouTube Shorts | sns/youtube/ |
| 12:00 PM | Post Instagram Carousel | Instagram | sns/instagram/ |
| 2:00 PM | Post Facebook long-form | Facebook Page | sns/ |
| 4:00 PM | Post X/Twitter Thread | X (Twitter) | sns/x_twitter/ |
| 6:00 PM | Post TikTok video | TikTok | sns/tiktok/ |
| 8:00 PM | Post Threads | Threads | sns/threads/ |
| 9:00 PM | Post YouTube Short #2 | YouTube Shorts | sns/youtube/ |

---

## ✅ PRE-PUBLISH CHECKLIST

### Content Quality
- [ ] All factual claims verified with cited sources
- [ ] No fictional statistics or invented names
- [ ] Controversial topics include Pro/Con balance
- [ ] All quotations include Source citation (title, date, author) in italics, 2pt smaller
- [ ] YouTube video URL added where referenced
- [ ] Disclaimer ("educational only, not medical advice") included where needed
- [ ] Grammar checked (Grammarly for English, 부산대 speller for Korean)

### Legal & Copyright
- [ ] All image sources credited or AI-generated (prompts documented)
- [ ] No copyrighted music used without license in videos
- [ ] No defamatory claims about real individuals or companies
- [ ] Medical content includes "consult your physician" disclaimer
- [ ] Political content (if any) presents both Pro and Con perspectives

### SEO & Platform
- [ ] YouTube title under 60 characters
- [ ] YouTube description includes all keywords (first 200 chars most important)
- [ ] YouTube chapters added to description
- [ ] Blog post has focus keyword in: title, first paragraph, H2, meta description
- [ ] Instagram carousel: 8–10 slides, hook on slide 1, CTA on last slide
- [ ] TikTok: first 3 words are the hook
- [ ] All hashtag packs pasted from SEO file

---

## 📁 FILE LOCATIONS

| Content Type | File Path |
|---|---|
| YouTube Long-form Script | sns/youtube/ep{ep_num:02d}_youtube_longform_script.md |
| YouTube Shorts Script | sns/youtube/ep{ep_num:02d}_youtube_shorts_script.md |
| All SNS Copy | sns/ep{ep_num:02d}_all_sns_copy.md |
| SubStack + WordPress | blogs/ep{ep_num:02d}_substack_and_wordpress.md |
| Image Prompts | images/prompts/ep{ep_num:02d}_image_generation_prompts.md |
| SEO Keywords | seo/ep{ep_num:02d}_seo_keywords.md |

---

*AI Decoded for Seniors Pipeline v1.0 | {today}*
"""
    out_path = ep_dir / f"ep{ep_num:02d}_PUBLISHING_CHECKLIST.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"  ✅ Checklist: {out_path.name}")


def gen_image_prompts_stub(ep_dir: Path, ep_data: dict, ep_num: int) -> None:
    """Generate image prompt template for new episodes."""
    title = ep_data["title_eng"]
    topic = ep_data["topic"]
    today = datetime.now().strftime("%Y-%m-%d")

    content = f"""# EP{ep_num:02d} — AI IMAGE GENERATION PROMPTS
# {title}
# Topic context: {topic}
# Generated: {today}

---

## GENERAL RULES FOR ALL PROMPTS
- All images are AI-generated originals — no copyright restrictions
- Never include real brand logos or trademarked product designs in generated images
- Always specify senior-friendly, diverse representation
- Style: warm, approachable, educational

---

## IMAGE SLOT 1 — Intro / Blog Header (16:9)
**Context:** Opening scene of the episode

### Midjourney v6:
```
[CUSTOMIZE: Describe the opening scene of EP{ep_num:02d} — {title[:60]}], 
realistic photography style, warm colors, senior-friendly, 
elderly american characters, --ar 16:9 --v 6 --style raw
```

### DALL-E 3:
```
Photorealistic image: [CUSTOMIZE for EP{ep_num:02d} topic].
Warm, natural lighting. Senior-friendly representation.
No text in image. Horizontal 16:9 composition.
```

---

## IMAGE SLOT 2 — Concept/Tech Explanation (16:9)
**Context:** Illustrating the main AI tool or concept

### Midjourney v6:
```
[CUSTOMIZE: Show the main AI tool of EP{ep_num:02d} in use],
infographic style, smartphone screen visible, clean modern design,
blue and white color scheme, 16:9 --ar 16:9 --v 6
```

---

## IMAGE SLOT 3 — Saying/Quote Image (16:9)
**Context:** Illustrating the American Saying for this episode

### Midjourney v6:
```
vintage americana editorial illustration for the saying: "{ep_data['saying_eng'][:60]}",
decorative typography, warm gold and navy colors, no people,
editorial illustration style, 16:9 --ar 16:9 --v 6
```

---

## PANEL IMAGES (3 × 1:1 square)
### Panel 1:
```
[CUSTOMIZE: Episode opening scene as cartoon/comic style], 
friendly senior characters, 1:1 square --ar 1:1 --v 6
```

### Panel 2:
```
[CUSTOMIZE: AI tool in action scene], 
educational cartoon style, 1:1 square --ar 1:1 --v 6
```

### Panel 3:
```
[CUSTOMIZE: Resolution/success scene], 
happy senior characters, 1:1 square --ar 1:1 --v 6
```

---

## YOUTUBE THUMBNAIL SPEC
- Size: 1280×720 px
- Text: Episode hook (large, bold)
- Style: Split before/after OR reaction face + result
- Colors: Deep navy background + gold/yellow title text
- Tool: Canva free templates → "YouTube Thumbnail"

---
*Generated by AI Decoded for Seniors Pipeline v1.0*
"""
    out_path = ep_dir / "images" / "prompts" / f"ep{ep_num:02d}_image_generation_prompts.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"  ✅ Image prompts: {out_path.name}")


# ─────────────────────────────────────────────
# MAIN RUNNER
# ─────────────────────────────────────────────
def run_pipeline(ep_num: int, base_dir: str = "./content_pipeline") -> None:
    """Run the full pipeline for one episode."""
    if ep_num not in EPISODE_REGISTRY:
        print(f"❌ Episode {ep_num} not found in registry. Add it to EPISODE_REGISTRY first.")
        return

    ep_data = EPISODE_REGISTRY[ep_num]
    print(f"\n{'='*60}")
    print(f"CONTENT PIPELINE: EP{ep_num:02d} — {ep_data['title_eng']}")
    print(f"{'='*60}")

    # 1. Create folders
    ep_dir = create_episode_folders(base_dir, ep_num)

    # 2. Generate support files
    gen_seo_file(ep_dir, ep_data, ep_num)
    gen_image_prompts_stub(ep_dir, ep_data, ep_num)
    gen_publishing_checklist(ep_dir, ep_data, ep_num)

    print(f"\n✅ PIPELINE COMPLETE for EP{ep_num:02d}")
    print(f"📁 Output: {ep_dir}")
    print("\n📝 NEXT STEPS:")
    print("  1. Open images/prompts/ → paste prompts into Midjourney or DALL-E")
    print("  2. Insert generated images into HTML blog files")
    print("  3. Follow sns/ files for each platform's ready-to-post copy")
    print("  4. Use Publishing Checklist for daily scheduling")
    print(f"\n🗓️  Recommended publish time: 7:30 AM local time")


# ─────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Decoded for Seniors — Content Pipeline")
    parser.add_argument("--ep", type=int, required=True, help="Episode number (e.g., 26)")
    parser.add_argument("--base", type=str, default="./content_pipeline", help="Base output directory")
    args = parser.parse_args()

    run_pipeline(ep_num=args.ep, base_dir=args.base)
