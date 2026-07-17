# AI DECODED FOR SENIORS — CONTENT PIPELINE
## Complete Multi-Platform Automation System
### Version 1.0 | 2026-04-28

---

## 📁 FOLDER STRUCTURE (Per Episode)

```
content_pipeline/
├── pipeline_master.py          ← Run this for any new episode
├── README_PIPELINE.md          ← This file
│
└── ep26/                       ← One folder per episode
    ├── ep26_PUBLISHING_CHECKLIST.md   ← Daily schedule
    ├── seo/
    │   └── ep26_seo_keywords.md       ← Keywords + hashtags for ALL platforms
    ├── sns/
    │   ├── ep26_all_sns_copy.md       ← Instagram + TikTok + Facebook + X + Threads
    │   └── youtube/
    │       ├── ep26_youtube_longform_script.md
    │       └── ep26_youtube_shorts_script.md
    ├── blogs/
    │   └── ep26_substack_and_wordpress.md
    └── images/
        └── prompts/
            └── ep26_image_generation_prompts.md
```

---

## 🚀 HOW TO USE FOR A NEW EPISODE

### Step 1 — Add to Registry
Open `pipeline_master.py` → find `EPISODE_REGISTRY` → add your episode data:
```python
31: {
    "title_eng": "AI Video Calling — FaceTime & Google Meet for Seniors",
    "title_kor": "AI 화상통화 — 시니어를 위한 페이스타임 완전 정복",
    "topic": "FaceTime, Google Meet, video calling AI, senior communication",
    "saying_eng": "A picture is worth a thousand words.",
    "idiom_kor": "百聞不如一見 (백문불여일견)",
    "hook_tag": "AIVideoCall",
    ...
}
```

### Step 2 — Run Pipeline
```bash
python3 pipeline_master.py --ep 31
```

### Step 3 — Generate Images
- Open `images/prompts/ep31_image_generation_prompts.md`
- Copy each prompt → paste into Midjourney or DALL-E
- Save generated images → insert into HTML

### Step 4 — Publish (Follow Checklist)
Follow the timed schedule in `ep31_PUBLISHING_CHECKLIST.md`

---

## 📊 PLATFORM-SPECIFIC OPTIMIZATION GUIDE

### 🔴 YouTube (Long-form)
| Factor | Target |
|---|---|
| Video length | 8–12 minutes optimal for seniors content |
| Upload time | 7–9 AM local time |
| Thumbnail | Text overlay + before/after emotion |
| Chapters | Add at every 1.5 min mark |
| End screen | 20-second subscribe + next video |
| Posting frequency | 3–5x per week to build algorithm momentum |
| Description | First 200 characters = most important for SEO |

### 📱 YouTube Shorts
| Factor | Target |
|---|---|
| Length | 55–60 seconds (sweet spot) |
| Hook | First 2 seconds = make or break |
| Post frequency | Daily for first 30 days |
| Time | 7–9 AM or 7–9 PM |
| CTA | Always end with "Follow for more" |

### 📸 Instagram
| Factor | Target |
|---|---|
| Best format | 8–10 slide carousel (highest reach) |
| Caption length | 150–200 words optimal |
| Hashtags | 20–30, mix high/medium/niche |
| Post time | 12 PM or 6–8 PM local |
| Reels | 30–60 seconds, same as TikTok script |
| Stories | Post 3–5 stories per day (behind-the-scenes works well) |

### 🎵 TikTok
| Factor | Target |
|---|---|
| Length | 30–60 seconds peak engagement |
| Hook words | First 3 words must grab attention |
| Trend sounds | Check TikTok Trending weekly |
| Post time | 6–10 AM or 7–11 PM |
| Frequency | 1–3x per day for algorithm |
| Text overlays | Essential — many watch with sound off |

### 👥 Facebook
| Factor | Target |
|---|---|
| Format | Long-form text + image or video |
| Audience | 55+ users still very active on FB |
| Length | 300–500 words gets highest engagement |
| Groups | Share in relevant senior tech groups |
| Best time | 1–4 PM weekdays |
| Video | Native Facebook video outperforms YouTube links |

### 🐦 X (Twitter)
| Factor | Target |
|---|---|
| Format | Thread (8–10 tweets) |
| Hook tweet | Must be standalone and shareable |
| Reply engagement | Respond within 1 hour of posting |
| Best time | 8–10 AM or 6–9 PM |
| Pinned tweet | Pin your best performing thread |

### 🧵 Threads
| Factor | Target |
|---|---|
| Length | 5–7 connected posts work best |
| Format | Conversational, personal voice |
| Cross-post | Same content as X, slightly more casual |
| Images | Add to every post for reach |

---

## 📈 90-DAY GROWTH ROADMAP

### Month 1 (Days 1–30): Foundation
**Goal:** 1,000 subscribers / followers per platform
- Post EVERY DAY without exception (algorithm rewards consistency above all)
- Focus on YouTube Shorts + TikTok first (fastest organic reach)
- Use all trending hashtags from SEO file
- Respond to every single comment within 2 hours
- A/B test 2 thumbnail styles per week

**KPIs to track:**
- YouTube: Views, Watch Time, Subscriber Growth
- Instagram: Reach, Saves, Profile Visits
- TikTok: Views, Follows, Shares

### Month 2 (Days 31–60): Acceleration
**Goal:** 10,000 subscribers / followers per platform
- Collaborate with one other senior tech creator (cross-promotion)
- Create one "pillar" long-form YouTube video (20+ min deep dive)
- Start email list via SubStack (offer free "AI for Seniors Starter Pack" PDF)
- Test paid promotion: $5–10/day Facebook ad targeting 60+ age group

### Month 3 (Days 61–90): Scale
**Goal:** 50,000–100,000 subscribers (realistic; 1M requires exceptional virality)
- Weekly live Q&A on YouTube / Facebook Live
- Guest appearances: senior tech podcasts, AARP community forums
- SEO-optimized blog posts (WordPress + Tistory) start ranking on Google
- Newsletter becomes primary audience asset (email open rates: 40%+)

**Realistic 3-month target:** 50K–100K combined across all platforms
**Path to 1M:** 6–12 months with consistent daily publishing + 1–2 viral Shorts

---

## ⚖️ LEGAL & COPYRIGHT COMPLIANCE

### Content Rules
✅ All factual claims must be verifiable from reputable sources
✅ Health/medical content: always include "educational only, consult physician" disclaimer
✅ Citations format: *Source: "Title," Author Name, Publication, Date* (italic, 2pt smaller)
✅ Political topics: ALWAYS present Pro and Con perspectives in balanced format
✅ Real companies: factual descriptions only, no fictional quotes or invented statistics
✅ Real people: only verified, publicly documented statements
✅ YouTube videos cited: *Source: URL* in italic text

### Image Rights
✅ AI-generated images: original, no copyright (check each tool's commercial terms)
✅ Stock photos: use Unsplash (free), Pexels (free), or cite source
✅ Never use images from Google Image Search without explicit license verification
✅ Screenshots: always note "Screenshot: [App Name] / [Company], [Date]"

### Defamation Prevention
✅ Never make false factual claims about individuals or organizations
✅ Opinions must be clearly framed as opinions, not facts
✅ Product reviews: base only on verified, documented information
✅ Do not republish or paraphrase entire copyrighted articles (brief quotes with citation are fine)

---

## 🛠️ RECOMMENDED TOOLS (Free or Low Cost)

| Tool | Use | Cost |
|---|---|---|
| Midjourney | AI image generation | $10/month |
| Canva | Thumbnail + carousel design | Free / $13/month Pro |
| CapCut | Short video editing | Free |
| DaVinci Resolve | Long-form video editing | Free |
| SubStack | Newsletter + content hub | Free |
| WordPress.org | Blog (self-hosted) | ~$10/month hosting |
| Grammarly | English proofreading | Free / $12/month |
| 부산대 맞춤법 검사기 | Korean spell check | Free |
| TubeBuddy | YouTube SEO | Free / $9/month |
| Later.com | Social media scheduling | Free tier available |
| Notion | Content calendar + planning | Free |

---

*AI Decoded for Seniors | Content Pipeline v1.0 | 2026-04-28*
*For questions about this system, review pipeline_master.py*
