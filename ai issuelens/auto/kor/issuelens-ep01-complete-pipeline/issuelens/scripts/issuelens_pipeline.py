#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║   IssueLens Master Automation Pipeline  v1.0                    ║
║   작성: IssueLens 편집부 자동화 시스템                            ║
║   기능: EP HTML → 4대 블로그 + 7대 SNS 플랫폼 출력물 일괄 생성    ║
╚══════════════════════════════════════════════════════════════════╝

사용법:
    python3 issuelens_pipeline.py --ep issuelens-ep01-data_privilege.html
    python3 issuelens_pipeline.py --all ./episodes/

출력물:
    ep{NN}/blogs/tistory/     → 티스토리용 HTML
    ep{NN}/blogs/naver/       → 네이버 블로그용 HTML
    ep{NN}/blogs/substack/    → 서브스택용 Markdown
    ep{NN}/blogs/wordpress/   → 워드프레스용 HTML
    ep{NN}/sns/youtube_longform/ → 유튜브 롱폼 스크립트
    ep{NN}/sns/youtube_shorts/   → 유튜브 쇼츠 스크립트
    ep{NN}/sns/instagram/        → 인스타그램 캐러셀 + 해시태그
    ep{NN}/sns/tiktok/           → 틱톡 스크립트
    ep{NN}/sns/facebook/         → 페이스북 포스트
    ep{NN}/sns/x_twitter/        → X(트위터) 스레드
    ep{NN}/sns/threads/          → 스레드 포스트
    ep{NN}/assets/               → 이미지 생성 프롬프트
    ep{NN}/seo/                  → SEO 키워드 마스터 파일
"""

import os
import re
import sys
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser

# ─────────────────────────────────────────────
#  설정 상수
# ─────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.parent
EPISODES_DIR = BASE_DIR / "episodes"
OUTPUT_DIR   = BASE_DIR

PLATFORM_CHAR_LIMITS = {
    "x_twitter":  280,
    "threads":    500,
    "instagram": 2200,
    "facebook":  63206,
    "tiktok":    2200,
}

TISTORY_SNS_LINKS = {
    "yt": "https://www.youtube.com/@IssueLens",
    "ig": "https://www.instagram.com/issuelens",
    "tt": "https://www.tiktok.com/@issuelens",
    "th": "https://www.threads.net/@issuelens",
    "xb": "https://x.com/issuelens",
    "fb": "https://www.facebook.com/issuelens",
}

# ─────────────────────────────────────────────
#  HTML 파서: EP 메타데이터 추출
# ─────────────────────────────────────────────
class EPMetaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.keywords = []
        self.og_title = ""
        self.og_description = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attrs.get("name", "")
            prop = attrs.get("property", "")
            content = attrs.get("content", "")
            if name == "description":
                self.description = content
            elif name == "keywords":
                self.keywords = [k.strip() for k in content.split(",")]
            elif prop == "og:title":
                self.og_title = content
            elif prop == "og:description":
                self.og_description = content

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()


def extract_ep_meta(html_path: Path) -> dict:
    """HTML 파일에서 에피소드 메타데이터를 추출합니다."""
    content = html_path.read_text(encoding="utf-8")
    parser = EPMetaExtractor()
    parser.feed(content)

    # EP 번호 추출
    ep_match = re.search(r'EP\.?(\d+)', parser.title, re.IGNORECASE)
    ep_num = ep_match.group(1) if ep_match else "00"

    # 주요 제목 추출 (headline h1)
    h1_match = re.search(r'<h1[^>]*class="headline"[^>]*>(.*?)</h1>', content, re.DOTALL)
    h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else parser.title

    # 섹션 제목들 추출
    sec_titles = re.findall(r'class="sec-ttl[^"]*"[^>]*>.*?<span class="num">\d+</span>(.*?)</h2>', content, re.DOTALL)
    sec_titles = [re.sub(r'<[^>]+>', '', t).strip() for t in sec_titles]

    # 소개문(intro) 추출
    intro_match = re.search(r'<p class="intro[^"]*"[^>]*>(.*?)</p>', content, re.DOTALL)
    intro_text = re.sub(r'<[^>]+>', '', intro_match.group(1)).strip() if intro_match else ""

    # 인용구(pq) 추출
    pq_match = re.search(r'<div class="pq-txt">(.*?)</div>', content, re.DOTALL)
    pq_text = re.sub(r'<[^>]+>', '', pq_match.group(1)).strip() if pq_match else ""

    # 실천 강령 추출
    action_titles = re.findall(r'<div class="ac-ttl">(.*?)</div>', content, re.DOTALL)
    action_descs  = re.findall(r'<div class="ac-desc">(.*?)</div>', content, re.DOTALL)
    actions = []
    for t, d in zip(action_titles, action_descs):
        actions.append({
            "title": re.sub(r'<[^>]+>', '', t).strip(),
            "desc":  re.sub(r'<[^>]+>', '', d).strip(),
        })

    # 태그 추출
    tags = re.findall(r'<span class="tag[^"]*">(#[^<]+)</span>', content)

    # 데이터 콜아웃(bignum/biglbl) 추출
    bignums = re.findall(r'<span class="bignum">(.*?)</span>', content, re.DOTALL)
    biglbls = re.findall(r'<span class="biglbl">(.*?)</span>', content, re.DOTALL)
    stats_hero = re.findall(r'<span class="stat-n">(.*?)</span>.*?<span class="stat-l">(.*?)</span>', content, re.DOTALL)

    return {
        "ep_num":         ep_num,
        "title":          parser.title,
        "h1_text":        h1_text,
        "description":    parser.description,
        "keywords":       parser.keywords,
        "og_title":       parser.og_title,
        "og_description": parser.og_description,
        "section_titles": sec_titles,
        "intro_text":     intro_text,
        "pq_text":        pq_text,
        "actions":        actions,
        "tags":           tags,
        "bignums":        [re.sub(r'<[^>]+>', '', b).strip() for b in bignums],
        "biglbls":        [re.sub(r'<[^>]+>', '', b).strip() for b in biglbls],
        "stats_hero":     [(re.sub(r'<[^>]+>', '', n).strip(), re.sub(r'<[^>]+>', '', l).strip()) for n, l in stats_hero],
        "raw_html":       content,
        "html_path":      html_path,
    }


# ─────────────────────────────────────────────
#  블로그 플랫폼 생성기
# ─────────────────────────────────────────────

def make_tistory(meta: dict, out_dir: Path):
    """티스토리: SNS 링크 실삽입 + 미디어 박스 안내 추가 버전."""
    html = meta["raw_html"]

    # SNS 링크 실삽입
    for key, url in TISTORY_SNS_LINKS.items():
        html = html.replace(f"#{'YT' if key=='yt' else key.upper()}_URL", url, 1)
        html = html.replace(f'href="#{key.upper()}_URL"', f'href="{url}"', 1)

    # 티스토리 전용 상단 배너 삽입 (body 직후)
    tistory_banner = f"""<!-- ▶▶ 티스토리 발행 버전 | IssueLens EP.{meta['ep_num']} ◀◀ -->
<div style="background:#1E3A8A;color:#fff;text-align:center;padding:10px 16px;font-family:'Pretendard Variable',sans-serif;font-size:14px;font-weight:700;letter-spacing:.05em">
  📌 IssueLens EP.{meta['ep_num']} — 티스토리 공식 발행본 · 매일 새 에피소드 발행 중
</div>"""
    html = html.replace('<div id="pb"></div>', f'<div id="pb"></div>\n{tistory_banner}')

    out_path = out_dir / f"issuelens-ep{meta['ep_num']}-tistory.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ 티스토리: {out_path.name}")


def make_naver(meta: dict, out_dir: Path):
    """네이버 블로그: JS 최소화 + 네이버 에디터 호환 단순 HTML."""
    kw_str = ", ".join(meta["keywords"][:20])
    tags_str = "  ".join(meta["tags"][:15])
    actions_html = "\n".join([
        f'<p style="margin:8px 0;padding:12px 16px;background:#F7F9FC;border-left:4px solid #1E3A8A;border-radius:4px"><strong style="color:#C8001A">▶ {a["title"]}</strong><br>{a["desc"]}</p>'
        for a in meta["actions"]
    ])
    sec_list = "\n".join([f"<li>{t}</li>" for t in meta["section_titles"]])
    stats_html = "\n".join([
        f'<span style="display:inline-block;background:#FFF0F3;border:2px solid #FFCCD5;border-radius:12px;padding:10px 16px;margin:5px;text-align:center"><strong style="font-size:1.4rem;color:#C8001A">{n}</strong><br><small style="color:#4B5563">{l}</small></span>'
        for n, l in meta["stats_hero"]
    ])

    naver_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta['title']}</title>
<meta name="description" content="{meta['description']}">
<meta name="keywords" content="{kw_str}">
<style>
body{{font-family:'Noto Sans KR','Apple SD Gothic Neo',sans-serif;font-size:18px;line-height:1.9;color:#0A0A0A;max-width:860px;margin:0 auto;padding:20px;word-break:keep-all}}
h1{{font-size:2rem;font-weight:800;color:#0A0A0A;line-height:1.3;border-bottom:4px solid #C8001A;padding-bottom:12px;margin-bottom:20px}}
h2{{font-size:1.3rem;font-weight:700;color:#fff;background:#C8001A;padding:10px 16px;border-radius:6px;margin:32px 0 16px}}
.intro-box{{background:#FFFBEB;border-left:6px solid #F59E0B;padding:18px 20px;border-radius:4px;margin:20px 0;font-weight:500}}
.stat-row{{text-align:center;margin:20px 0}}
.data-box{{background:#FFF0F3;border:2px solid #FFCCD5;border-top:5px solid #C8001A;padding:20px;border-radius:12px;margin:20px 0}}
.ctx-box{{background:#EFF6FF;border:2px solid #BFDBFE;border-top:5px solid #1E3A8A;padding:20px;border-radius:12px;margin:20px 0}}
.quote-box{{background:#FFF8F0;border-top:4px solid #0A0A0A;border-bottom:4px solid #0A0A0A;padding:24px;text-align:center;font-size:1.3rem;font-weight:800;margin:28px 0}}
.tag-area{{margin:20px 0}}
.tag{{display:inline-block;background:#FFF0F3;border:2px solid #FFCCD5;color:#C8001A;font-weight:700;padding:4px 12px;border-radius:20px;margin:3px;font-size:14px}}
.footer-note{{background:#F7F9FC;border:1px solid #CBD5E1;padding:16px;border-radius:8px;font-size:15px;color:#4B5563;margin-top:32px;text-align:center}}
img{{max-width:100%;border-radius:10px;margin:16px 0}}
</style>
</head>
<body>

<p style="background:#1E3A8A;color:#fff;padding:10px 14px;border-radius:6px;font-size:14px;font-weight:700;text-align:center">
  📌 IssueLens EP.{meta['ep_num']} — 네이버 블로그 공식 발행본 · 매일 새 에피소드
</p>

<h1>{meta['og_title']}</h1>

<div class="stat-row">{stats_html}</div>

<div class="intro-box">{meta['intro_text']}</div>

<div class="tag-area">{tags_str}</div>

<hr style="border:none;border-top:2px solid #E2E8F0;margin:28px 0">

<h2>📋 이 글의 핵심 내용</h2>
<ol style="padding-left:20px;line-height:2.2">
{sec_list}
</ol>

<hr style="border:none;border-top:2px solid #E2E8F0;margin:28px 0">

<!-- 이미지 삽입 위치 1 -->
<div style="background:#F1F5F9;border:2px dashed #CBD5E1;border-radius:12px;padding:30px;text-align:center;color:#64748B;margin:20px 0">
  🖼️ 이미지 삽입 위치 (섹션 1 관련 이미지)<br>
  <small>권장: 데이터 보안·개인정보 관련 이미지 (1200×675px)</small>
</div>

<div class="data-box">
  <strong style="color:#C8001A;font-size:1.1rem">📊 핵심 데이터: {meta['bignums'][0] if meta['bignums'] else ''}</strong><br>
  <span style="color:#4B5563">{meta['biglbls'][0] if meta['biglbls'] else ''}</span>
</div>

<!-- 이미지 삽입 위치 2 -->
<div style="background:#F1F5F9;border:2px dashed #CBD5E1;border-radius:12px;padding:30px;text-align:center;color:#64748B;margin:20px 0">
  🖼️ 이미지 삽입 위치 (섹션 2 관련 이미지)<br>
  <small>권장: 해외직구·데이터 흐름 관련 인포그래픽 (1200×675px)</small>
</div>

<div class="ctx-box">
  <strong style="color:#1E3A8A">📌 핵심 맥락</strong><br>
  {meta['og_description']}
</div>

<!-- 이미지 삽입 위치 3 -->
<div style="background:#F1F5F9;border:2px dashed #CBD5E1;border-radius:12px;padding:30px;text-align:center;color:#64748B;margin:20px 0">
  🖼️ 이미지 삽입 위치 (섹션 3 관련 이미지)<br>
  <small>권장: 비교·대비 관련 이미지 (1200×675px)</small>
</div>

<div class="quote-box">
  {meta['pq_text']}
</div>

<h2>🛡️ 실천 강령 — 지금 바로 할 수 있는 것</h2>
{actions_html}

<hr style="border:none;border-top:2px solid #E2E8F0;margin:28px 0">

<div class="footer-note">
  <strong>IssueLens</strong> | EP.{meta['ep_num']} | 매일 발행되는 심층 이슈 분석<br>
  YouTube · Instagram · TikTok · Threads · X · Facebook: @IssueLens<br>
  <small>※ 본 게시물은 공신력 있는 언론 보도 및 정부 기관 발표 자료를 바탕으로 작성된 공익 논평입니다.</small>
</div>

</body>
</html>"""

    out_path = out_dir / f"issuelens-ep{meta['ep_num']}-naver.html"
    out_path.write_text(naver_html, encoding="utf-8")
    print(f"  ✅ 네이버: {out_path.name}")


def make_substack(meta: dict, out_dir: Path):
    """서브스택: Markdown 포맷."""
    today = datetime.now().strftime("%Y년 %m월 %d일")
    kw_str = " · ".join(meta["keywords"][:12])
    tags_str = "  ".join(meta["tags"][:12])
    actions_md = "\n".join([
        f"**{a['title']}**\n{a['desc']}\n"
        for a in meta["actions"]
    ])
    stats_md = "\n".join([
        f"| {n} | {l} |"
        for n, l in meta["stats_hero"]
    ])

    md = f"""# {meta['og_title']}

**IssueLens EP.{meta['ep_num']}** · {today}

---

> {meta['description']}

---

## 📊 핵심 수치

| 수치 | 설명 |
|------|------|
{stats_md}

---

## 들어가며

{meta['intro_text']}

---

## 이 글에서 다루는 내용

{"".join([f'- {t}{chr(10)}' for t in meta['section_titles']])}

---

## 주요 데이터 포인트

{"".join([f'- **{n}** — {l}{chr(10)}' for n, l in zip(meta['bignums'], meta['biglbls'])])}

---

> **"{meta['pq_text']}"**

---

## 🛡️ 실천 강령

{actions_md}

---

## 🔍 이 글의 핵심 키워드

{kw_str}

---

## 태그

{tags_str}

---

*IssueLens EP.{meta['ep_num']} · 공신력 있는 언론 보도 및 정부 기관 발표 자료 기반 공익 논평.*

*YouTube · Instagram · TikTok · Threads · X · Facebook: @IssueLens*
"""
    out_path = out_dir / f"issuelens-ep{meta['ep_num']}-substack.md"
    out_path.write_text(md, encoding="utf-8")
    print(f"  ✅ 서브스택: {out_path.name}")


def make_wordpress(meta: dict, out_dir: Path):
    """WordPress.org: 전체 HTML + Yoast SEO 호환 메타 블록 포함."""
    html = meta["raw_html"]

    # WordPress 전용 헤드 주석 삽입
    wp_comment = f"""<!-- 
  WordPress.org 발행 버전 | IssueLens EP.{meta['ep_num']}
  권장 플러그인: Yoast SEO, WP Rocket, Smush
  카테고리: 데이터주권, 개인정보보호, 이슈분석
  태그: {', '.join(meta['keywords'][:10])}
-->"""
    html = html.replace("<!DOCTYPE html>", f"<!DOCTYPE html>\n{wp_comment}")

    # WordPress body 상단 배너
    wp_banner = f"""<!-- WordPress 발행 배너 -->
<div style="background:#1E3A8A;color:#fff;text-align:center;padding:10px 16px;font-family:sans-serif;font-size:14px;font-weight:700">
  📌 IssueLens EP.{meta['ep_num']} | WordPress 공식 발행본 · <a href="https://issuelens.com" style="color:#93C5FD">issuelens.com</a>
</div>"""
    html = html.replace('<div id="pb"></div>', f'<div id="pb"></div>\n{wp_banner}')

    # SNS 링크 실삽입
    for key, url in TISTORY_SNS_LINKS.items():
        html = html.replace(f'href="#{key.upper()}_URL"', f'href="{url}"')

    out_path = out_dir / f"issuelens-ep{meta['ep_num']}-wordpress.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ 워드프레스: {out_path.name}")


# ─────────────────────────────────────────────
#  SNS 콘텐츠 생성기
# ─────────────────────────────────────────────

def make_youtube_longform(meta: dict, out_dir: Path):
    """유튜브 롱폼: 전체 스크립트 + 썸네일 프롬프트 + 설명란 + 태그."""
    ep  = meta["ep_num"]
    kws = meta["keywords"]

    script = f"""╔══════════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — YouTube 롱폼 영상 스크립트           ║
║  예상 러닝타임: 12~18분                                    ║
╚══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎬 영상 제목 (A/B 테스트 3개)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A. 알리·테무 앱, 내 개인정보 어디로 갑니까? 충격 실태 공개 [IssueLens EP.{ep}]
B. 500원 양말의 진짜 가격 — 당신의 개인정보 유출 경로 완전 해부
C. 과징금 20억! 알리익스프레스 개인정보 유출 사건의 전말 | 데이터 주권 시리즈 EP.{ep}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎙️ 오프닝 훅 (0:00~0:30) — 주목 끌기
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[화면: 알리/테무 앱 다운로드 화면 → 개인정보 수집 동의 창]

나레이션:
"여러분, 알리익스프레스나 테무 앱 써보셨습니까?
500원짜리 양말, 천 원짜리 휴대폰 케이스...
정말 매력적이죠.
그런데 오늘, 그 싼 가격의 진짜 대가를 알려드리겠습니다.
여러분의 이름, 주소, 연락처, 구매 패턴...
심지어 지인 관계까지 — 지금 이 순간에도 해외 서버로 흘러가고 있습니다."

[자막: '알리·테무 개인정보 유출 — 충격 실태']

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 목차 안내 (0:30~1:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"오늘 이 영상에서 다룰 내용입니다.

1️⃣ 500원짜리 양말에 담긴 개인정보 상납의 진실
2️⃣ 해외 서버 전송이 왜 안보 위협이 되는가
3️⃣ 상호주의 없는 시장 개방 — 누가 이득을 보는가
4️⃣ 지금 당장 할 수 있는 개인정보 보호 실천법

구독과 좋아요 먼저 눌러주시면 채널 성장에 큰 힘이 됩니다!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 SECTION 1: {meta['section_titles'][0] if meta['section_titles'] else ''}
  (1:00~5:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[화면: 개인정보 수집 플로우 차트 애니메이션]

나레이션:
"먼저 알리·테무 같은 앱을 설치하면 정확히 무슨 일이 일어나는지 봅시다.

앱을 설치하는 순간, 여러분은 동의 버튼을 누릅니다.
아무도 읽지 않는 긴 이용약관 — 거기에 담긴 내용이 뭔지 아십니까?

개인정보보호위원회의 2024년 7월 공식 발표를 보면,
알리익스프레스는 이용자 개인정보를 해외 판매자 18만 곳에 이전하면서
제대로 고지하지 않은 행위로 20억 원의 과징금을 부과받았습니다.

출처: 개인정보보호위원회 제재 결정, 2024년 7월

20억이요? 이 회사 입장에서는 껌 값입니다.
문제는, 이게 빙산의 일각이라는 겁니다."

[데이터 콜아웃 화면: ₩20억 / 개인정보 무단 이전 해외 판매자 18만 곳]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 SECTION 2: {meta['section_titles'][1] if len(meta['section_titles']) > 1 else ''}
  (5:00~10:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[화면: 국가정보법 조항 텍스트 + 지도 애니메이션]

나레이션:
"많은 분들이 '개인정보 좀 털려도 괜찮지 않나?' 생각하실 수 있습니다.
그런데 여기서 핵심적인 문제가 있습니다.

해당 플랫폼 본국의 국가정보법 제7조를 보면,
'모든 조직과 시민은 국가 정보 활동을 지지·보조·협조해야 한다'고 명시되어 있습니다.

출처: 해당국 국가정보법 제7조, 2017년 제정

이게 무슨 말이냐?
알리, 테무가 수집한 여러분의 데이터를
그 나라 정부가 요청하면 제공해야 한다는 겁니다.

여러분의 쇼핑 습관, 이름, 주소, 카드 정보가
국가 단위의 정보 자산이 될 수 있다는 이야기입니다."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎯 SECTION 3: {meta['section_titles'][2] if len(meta['section_titles']) > 2 else ''}
  (10:00~13:30)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[화면: 비대칭 구도 인포그래픽]

나레이션:
"그런데 더 충격적인 사실이 있습니다.
그 나라는 구글, 유튜브, 인스타그램, 심지어 카카오도 자국 내에서 막습니다.
자국민의 데이터는 철저히 보호하면서,
대한민국 국민의 데이터는 마음껏 수집해 가고 있습니다.

이것을 '상호주의 없는 시장 개방'이라고 합니다.
우리만 문을 열고 있는 겁니다."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🛡️ 실천 강령 & 마무리 (13:30~15:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
나레이션:
"그렇다면 우리는 무엇을 해야 할까요?

{chr(10).join([f"- {a['title']}: {a['desc'][:80]}..." for a in meta['actions']])}

마지막으로 이 말로 오늘 영상을 마무리합니다.

'{meta['pq_text']}'

오늘 영상이 도움이 되셨다면, 구독과 좋아요 부탁드립니다.
이 내용을 가족과 친구에게 꼭 공유해 주세요.
다음 에피소드에서 또 만나겠습니다. IssueLens였습니다!"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📝 유튜브 영상 설명란 (복사-붙여넣기용)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{meta['description']}

📌 이 영상의 목차:
0:00 오프닝 — 알리·테무의 진짜 비용
1:00 Section 1: {meta['section_titles'][0] if meta['section_titles'] else ''}
5:00 Section 2: {meta['section_titles'][1] if len(meta['section_titles']) > 1 else ''}
10:00 Section 3: {meta['section_titles'][2] if len(meta['section_titles']) > 2 else ''}
13:30 실천 강령 & 마무리

🔔 IssueLens 구독: https://www.youtube.com/@IssueLens
📱 Instagram: https://www.instagram.com/issuelens
🎵 TikTok: https://www.tiktok.com/@issuelens
🧵 Threads: https://www.threads.net/@issuelens
🐦 X: https://x.com/issuelens
📘 Facebook: https://www.facebook.com/issuelens

#알리익스프레스개인정보 #테무개인정보유출 #해외직구앱위험 #데이터주권 #개인정보보호 #IssueLens #이슈렌즈

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎨 썸네일 텍스트 가이드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
메인 텍스트: "알리·테무 개인정보"
서브 텍스트: "내 정보 어디로?"
배경: 빨간/검정 그라디언트
아이콘: 자물쇠 + 스마트폰 이미지
강조색: #C8001A (IssueLens 레드)
크기: 1280x720px

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🏷️ 유튜브 태그 (복사-붙여넣기용)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{', '.join(kws[:30])}
"""
    out_path = out_dir / f"issuelens-ep{ep}-youtube-longform-script.txt"
    out_path.write_text(script, encoding="utf-8")
    print(f"  ✅ 유튜브 롱폼: {out_path.name}")


def make_youtube_shorts(meta: dict, out_dir: Path):
    """유튜브 쇼츠: 60초 이내 세로형 스크립트."""
    ep = meta["ep_num"]
    script = f"""╔══════════════════════════════════════════╗
║  IssueLens EP.{ep} — YouTube Shorts 스크립트  ║
║  목표: 60초 이하 / 세로형 9:16              ║
╚══════════════════════════════════════════╝

━━━━━ SHORTS 제목 3개 (A/B 테스트) ━━━━━
A. 알리·테무 쓰면 내 개인정보 유출된다? #Shorts
B. 500원 양말의 충격적인 진실 #알리 #테무 #개인정보
C. 해외직구 앱 개인정보 유출 경로 30초 요약 #Shorts

━━━━━ 60초 스크립트 ━━━━━━━━━━━━━━━━━━━━

[0초~5초] 훅
자막: "알리·테무 쓰시나요? 충격적인 사실 알려드립니다"
나레이션: "잠깐! 알리·테무 앱 쓰시는 분, 이것만 알고 쓰세요."

[5초~20초] 핵심 팩트
[화면: 빠른 텍스트 슬라이드]
- 알리, 2024년 개인정보 과징금 → 20억 원
- 내 개인정보 → 해외 판매자 18만 곳 유출
- 국가정보법 제7조 → 언제든 정부 요청 시 제공 가능

[20초~45초] 데이터 흐름
[화면: 애니메이션 플로우]
"앱 설치 → 결제 정보 입력 → 해외 서버 전송 → 통제권 상실"
나레이션: "단 한 번의 결제로, 내 데이터는 영원히 돌아오지 않습니다."

[45초~55초] 행동 촉구
"지금 당장: 알리·테무 앱 권한 설정 확인하세요!"
자막: ACTION 01: 앱 삭제 / ACTION 02: 국내 플랫폼 이용

[55초~60초] CTA
"구독하면 매일 이런 정보 드립니다! IssueLens ↑↑↑"
자막: #알리개인정보 #테무위험 #데이터주권 #IssueLens

━━━━━ Shorts 설명란 ━━━━━━━━━━━━━━━━━━━━
알리·테무 개인정보 유출 실태 30초 요약! 자세한 내용은 IssueLens EP.{ep}에서.
#알리익스프레스 #테무 #개인정보 #해외직구 #데이터주권 #IssueLens #Shorts
"""
    out_path = out_dir / f"issuelens-ep{ep}-youtube-shorts-script.txt"
    out_path.write_text(script, encoding="utf-8")
    print(f"  ✅ 유튜브 쇼츠: {out_path.name}")


def make_instagram(meta: dict, out_dir: Path):
    """인스타그램: 10장 캐러셀 + 캡션 + 해시태그."""
    ep = meta["ep_num"]
    tags = " ".join([f"#{t.strip('#')}" for t in meta["tags"][:15]])
    extra_tags = "#인스타그램 #카드뉴스 #이슈 #뉴스 #정보 #알리 #테무 #개인정보 #데이터보안 #IssueLens #issuelens #카드뉴스 #정보공유 #지식 #알아야할것"

    carousel = f"""╔══════════════════════════════════════════╗
║  IssueLens EP.{ep} — Instagram 캐러셀 (10장)  ║
╚══════════════════════════════════════════╝

━━━━━ 슬라이드 1 (커버) ━━━━━━━━━━━━━━━━━━
제목: 알리·테무 앱
서브: 내 개인정보 어디로 가나?
배경: IssueLens 레드 (#C8001A) + 다크 그라디언트
하단: IssueLens EP.{ep} · 스와이프 →
크기: 1080x1080px (정방형) 또는 1080x1350px (세로)

━━━━━ 슬라이드 2 (핵심 통계) ━━━━━━━━━━━━
제목: 충격의 숫자들
내용:
  📊 ₩20억  → 알리 과징금 (2024년)
  👥 18만 곳 → 개인정보 이전된 해외 판매자 수
  ⚠️ 제7조  → 국가정보법 (정부 협조 의무)
배경: 흰색, 빨간 강조

━━━━━ 슬라이드 3 (문제 제기) ━━━━━━━━━━━━
제목: 500원 양말, 진짜 가격은?
내용: "앱 설치 순간, 내 이름·주소·카드 정보·구매 패턴이 수집됩니다"
시각: 스마트폰 → 데이터 유출 아이콘

━━━━━ 슬라이드 4 (데이터 플로우) ━━━━━━━━
제목: 내 정보의 여행
내용 (플로우 형태):
  앱 설치 → 구매·결제 → 해외 서버 → 국가정보법 → 통제권 상실
시각: 화살표 플로우 다이어그램

━━━━━ 슬라이드 5 (법조항) ━━━━━━━━━━━━━━
제목: 알아야 할 법조항
내용: "국가정보법 제7조 — 모든 기업은 정부 요청 시 데이터를 제공해야 한다"
시각: 법전 아이콘 + 경고 색상

━━━━━ 슬라이드 6 (리스크 평가) ━━━━━━━━━━
제목: 위험도 평가
내용:
  개인정보 수집 범위: ████████░░ 광범위
  삭제 요청 어려움:   ████████░░ 높음
  해외 서버 이전 위험: ███████░░░ 높음
  소비자 인지도:      ██░░░░░░░░ 낮음

━━━━━ 슬라이드 7 (비대칭 구도) ━━━━━━━━━━
제목: 공정한가요?
내용:
  ✗ 그 나라는: 구글·유튜브·카카오 차단
  ✓ 우리나라는: 알리·테무 자유롭게 수집
시각: 불평등 저울 이미지

━━━━━ 슬라이드 8~9 (실천 강령) ━━━━━━━━━
제목: 지금 당장 할 수 있는 것
{chr(10).join([f"  ACTION {i+1}. {a['title']}" for i, a in enumerate(meta['actions'])])}

━━━━━ 슬라이드 10 (CTA) ━━━━━━━━━━━━━━━
제목: 이 내용을 공유하세요!
내용: IssueLens — 매일 새로운 이슈 분석
CTA: "저장 + 공유로 소중한 사람을 지키세요"
하단: @IssueLens · YouTube · TikTok · Threads

━━━━━ 캡션 (2200자 이내) ━━━━━━━━━━━━━━━━

알리·테무 앱을 쓰고 계신가요? 오늘은 초저가 해외 직구 앱의 숨겨진 진실을 파헤칩니다. 🔍

💥 충격의 팩트:
• 개인정보보호위원회, 알리에 과징금 20억 원 부과 (2024년)
• 이용자 정보가 해외 판매자 18만 곳에 이전
• 국가정보법 제7조: 정부 요청 시 데이터 제공 의무

500원짜리 양말 한 켤레를 사면서, 우리는 그보다 훨씬 비싼 것을 내주고 있습니다.

{meta['pq_text']}

지금 바로 스마트폰의 앱 권한 설정을 확인하세요. 그리고 주변에 꼭 알려주세요.

👉 자세한 내용은 프로필 링크의 IssueLens EP.{ep} 블로그 포스트에서!

{tags} {extra_tags}

━━━━━ 해시태그 (별도 댓글용) ━━━━━━━━━━━━
{tags} {extra_tags}
"""
    out_path = out_dir / f"issuelens-ep{ep}-instagram-carousel.txt"
    out_path.write_text(carousel, encoding="utf-8")
    print(f"  ✅ 인스타그램: {out_path.name}")


def make_tiktok(meta: dict, out_dir: Path):
    """틱톡: 30초 + 60초 스크립트."""
    ep = meta["ep_num"]
    script = f"""╔══════════════════════════════════════════╗
║  IssueLens EP.{ep} — TikTok 스크립트          ║
╚══════════════════════════════════════════╝

━━━━━ 틱톡 영상 제목 ━━━━━━━━━━━━━━━━━━━━━━
알리·테무 쓰면 벌어지는 일 😱 #알리 #테무 #개인정보 #FYP

━━━━━ 30초 버전 스크립트 ━━━━━━━━━━━━━━━━━━

[0~3초] 훅
"알리·테무 아직도 쓰세요? 잠깐요 🚨"

[3~12초] 팩트 폭격
"개인정보보호위원회 발표 들었어요?
알리가 과징금 20억 맞았어요.
이유? 내 정보를 해외 판매자 18만 곳에 넘겼대요."

[12~22초] 핵심 위험
"그것도 모자라서, 해당국 법에 따르면
알리·테무가 수집한 내 데이터, 그 나라 정부가
요청하면 줘야 해요. 내 쇼핑 정보가 국가 정보가 되는 거예요."

[22~28초] 행동 촉구
"지금 바로 앱 권한 설정 확인하세요!
아니면 국내 플랫폼으로 갈아타는 것도 방법이에요."

[28~30초] CTA
"더 알고 싶으면 팔로우! @IssueLens 매일 올려요!"

━━━━━ 60초 버전 추가 내용 ━━━━━━━━━━━━━━━━
[30~50초] 비대칭 구도 설명
"그런데 진짜 충격적인 건요, 그 나라는 구글도 막고, 유튜브도 막고, 카카오도 막아요.
자국민 데이터는 철저히 보호하면서, 우리나라 데이터는 막 가져가는 거예요.
이걸 '상호주의 없는 시장 개방'이라고 해요."

[50~58초] 인용구
"오늘 아낀 몇천 원이, 내일 대한민국 주권을 위협하는 실탄이 됩니다."

[58~60초] CTA
"팔로우 + 저장해서 주변에 공유해주세요!"

━━━━━ 틱톡 캡션 + 해시태그 ━━━━━━━━━━━━━━
알리·테무 개인정보 유출 충격 실태 😱 500원 양말의 진짜 가격

{" ".join([f"#{t.strip('#')}" for t in meta["tags"][:8]])} #FYP #fypage #viral #틱톡 #카드뉴스 #정보 #알아야할것 #IssueLens

━━━━━ 화면 구성 가이드 ━━━━━━━━━━━━━━━━━━━
• 세로형 (9:16) 1080x1920px
• 자막: 굵은 흰색 텍스트 + 검정 외곽선 (가독성 최대화)
• 배경: 스마트폰 화면 + 개인정보 아이콘 애니메이션
• BGM: 긴박한 비트 (저작권 무료 TikTok 라이브러리)
• 효과: 빨간 경고 플래시 + 텍스트 강조 효과
"""
    out_path = out_dir / f"issuelens-ep{ep}-tiktok-script.txt"
    out_path.write_text(script, encoding="utf-8")
    print(f"  ✅ 틱톡: {out_path.name}")


def make_facebook(meta: dict, out_dir: Path):
    """페이스북 포스트."""
    ep = meta["ep_num"]
    tags_str = " ".join([f"#{t.strip('#')}" for t in meta["tags"][:12]])
    post = f"""📌 [IssueLens EP.{ep}] {meta['og_title']}

{meta['description']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 이 글의 핵심 포인트:

{"".join([f"  ▶ {t}{chr(10)}" for t in meta['section_titles']])}

📊 충격의 수치:
{"".join([f"  • {n} — {l}{chr(10)}" for n, l in zip(meta['bignums'], meta['biglbls'])])}

🛡️ 지금 바로 할 수 있는 것:
{"".join([f"  {i+1}. {a['title']}: {a['desc'][:80]}...{chr(10)}" for i, a in enumerate(meta['actions'])])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 "{meta['pq_text']}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👉 전체 기사 읽기: [블로그 URL]
🔔 IssueLens 페이지 팔로우하면 매일 새 에피소드!
📱 YouTube·Instagram·TikTok: @IssueLens

{tags_str} #IssueLens #이슈렌즈 #카드뉴스 #정보공유
"""
    out_path = out_dir / f"issuelens-ep{ep}-facebook-post.txt"
    out_path.write_text(post, encoding="utf-8")
    print(f"  ✅ 페이스북: {out_path.name}")


def make_x_twitter(meta: dict, out_dir: Path):
    """X(트위터) 스레드 — 1트윗=280자 이내."""
    ep = meta["ep_num"]
    thread = f"""╔══════════════════════════════════════════╗
║  IssueLens EP.{ep} — X(트위터) 스레드         ║
║  각 트윗: 280자 이하 유지                   ║
╚══════════════════════════════════════════╝

━━━ 트윗 1/7 (훅) ━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 알리·테무 쓰시는 분들, 이것 알고 계십니까?

2024년, 개인정보보호위원회가 알리익스프레스에 과징금 20억 원을 부과했습니다.
이유: 이용자 정보를 해외 판매자 18만 곳에 무단 이전.

이게 시작에 불과합니다. 🧵

━━━ 트윗 2/7 (데이터 플로우) ━━━━━━━━━━━━━━━━

앱을 설치하는 순간 이런 일이 일어납니다:

📱 앱 설치·회원가입
↓ 이름·연락처·위치 수집
🛒 구매·결제 행동 기록
↓ 카드번호·패턴·지인 관계 수집
🌐 해외 서버 전송
↓ 통제권 완전 상실

되돌릴 수 없습니다.

━━━ 트윗 3/7 (법조항) ━━━━━━━━━━━━━━━━━━━━━━

더 심각한 문제가 있습니다.

해당국 국가정보법 제7조:
"모든 조직과 시민은 국가 정보 활동을 지지·보조·협조해야 한다."

알리·테무가 수집한 여러분의 데이터,
그 나라 정부가 요청하면 제공해야 합니다.

━━━ 트윗 4/7 (비대칭 구도) ━━━━━━━━━━━━━━━━

아이러니한 사실:

❌ 그 나라 → 구글, 유튜브, 인스타그램, 카카오 차단
✅ 한국 → 알리, 테무, 쉬인 자유롭게 데이터 수집

우리만 문을 열고 있습니다.
이것이 공정한 거래입니까?

━━━ 트윗 5/7 (인용구) ━━━━━━━━━━━━━━━━━━━━━━

"오늘 당신이 아낀 몇천 원이,
내일 대한민국의 주권을 위협하는 실탄이 됩니다."

#데이터주권 #개인정보보호 #IssueLens

━━━ 트윗 6/7 (실천 강령) ━━━━━━━━━━━━━━━━━━━

지금 바로 할 수 있는 것:

{chr(10).join([f"  {i+1}. {a['title']}" for i, a in enumerate(meta['actions'][:3])])}

모르면 당합니다. 알아야 지킵니다.

━━━ 트윗 7/7 (CTA) ━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 전체 분석 보기: [블로그 URL]
🔔 IssueLens 팔로우: @IssueLens
📹 YouTube: https://www.youtube.com/@IssueLens

더 많은 이슈 분석은 매일 업데이트됩니다!

{" ".join([f"#{t.strip('#')}" for t in meta['tags'][:5]])} #IssueLens
"""
    out_path = out_dir / f"issuelens-ep{ep}-x-twitter-thread.txt"
    out_path.write_text(thread, encoding="utf-8")
    print(f"  ✅ X(트위터): {out_path.name}")


def make_threads(meta: dict, out_dir: Path):
    """Threads 포스트 (500자 이내 메인 + 댓글 체인)."""
    ep = meta["ep_num"]
    tags_str = " ".join([f"#{t.strip('#')}" for t in meta["tags"][:8]])
    post = f"""╔══════════════════════════════════════════╗
║  IssueLens EP.{ep} — Threads 포스트           ║
╚══════════════════════════════════════════╝

━━━ 메인 포스트 (500자 이내) ━━━━━━━━━━━━━━━

🚨 알리·테무 개인정보 유출, 이 정도인 줄 몰랐습니다.

2024년 개인정보보호위원회 발표:
→ 알리, 과징금 20억 원
→ 해외 판매자 18만 곳에 정보 무단 이전
→ 국가정보법 제7조: 정부 요청 시 제공 의무

500원 양말 한 켤레의 진짜 가격입니다.

{meta['pq_text']}

👉 IssueLens EP.{ep} 전체 분석: 프로필 링크

{tags_str} #IssueLens

━━━ 답글 체인 1 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━

데이터 흐름 요약:
앱 설치 → 결제 → 해외 서버 → 통제권 상실

이게 한 번 일어나면 되돌릴 수 없습니다.

━━━ 답글 체인 2 (실천 강령) ━━━━━━━━━━━━━━━

지금 바로 할 수 있는 것:
{chr(10).join([f"  • {a['title']}" for a in meta['actions']])}

모르면 당합니다. RT/리포스트로 주변에 알려주세요!

━━━ 답글 체인 3 (CTA) ━━━━━━━━━━━━━━━━━━━━━━

📌 전체 기사: [블로그 URL]
IssueLens 팔로우하면 매일 새로운 이슈 분석!
@IssueLens
"""
    out_path = out_dir / f"issuelens-ep{ep}-threads-post.txt"
    out_path.write_text(post, encoding="utf-8")
    print(f"  ✅ Threads: {out_path.name}")


# ─────────────────────────────────────────────
#  SEO 키워드 마스터 파일
# ─────────────────────────────────────────────

def make_seo_master(meta: dict, out_dir: Path):
    """SEO 마스터 파일: 검색 의도별 키워드 분류."""
    ep = meta["ep_num"]
    seo = f"""╔══════════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — SEO 마스터 키워드 파일              ║
║  목표: 1개월 내 100만 구독자 달성을 위한 검색어 최적화     ║
╚══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 기본 메타 태그 정보
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
타이틀: {meta['title']}
설명:   {meta['description']}
OG 제목: {meta['og_title']}
OG 설명: {meta['og_description']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2. 검색 의도별 핵심 키워드 (구글·네이버·유튜브 공통)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[정보성 검색 — 높은 검색량]
{chr(10).join([f"  • {k}" for k in meta['keywords'][:10]])}

[문제 해결 검색 — 구매 의향 높음]
  • 알리익스프레스 개인정보 삭제 방법
  • 테무 앱 권한 해제하는 법
  • 해외 직구 앱 삭제 후기
  • 개인정보 유출 신고 방법
  • 개인정보보호위원회 신고

[비교 검색 — 네이버 블로그 강세]
  • 알리 vs 쿠팡 개인정보
  • 테무 vs 아마존 보안
  • 국내 직구 앱 vs 해외 직구 앱 비교

[최신 뉴스 검색 — 속보성]
  • 알리익스프레스 과징금 2024
  • 테무 개인정보 유출 최신
  • 개인정보보호위원회 제재 2024

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3. 롱테일 키워드 (경쟁 낮음·전환율 높음)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 알리익스프레스 깔면 개인정보 털리나요
  • 테무 앱 안전한지 알고 싶어요
  • 해외직구 앱 개인정보 위험한 이유
  • 알리 탈퇴하면 개인정보 삭제되나요
  • 직구 앱 위치 정보 수집 막는 방법
  • 쉬인 개인정보 유출 사례
  • 중국 앱 개인정보 위험성 정리
  • 알리 테무 미니소 개인정보 비교

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4. 유튜브 특화 검색어
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • 알리 테무 개인정보 유출 영상
  • 해외직구 앱 위험성 실험
  • 데이터 주권 설명 영상
  • 개인정보보호 실천법 영상
  • 중국 앱 보안 위험 유튜브

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5. 인스타그램·틱톡 해시태그 전략
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[상위 해시태그 — 도달률 극대화]
  #개인정보 #개인정보보호 #데이터보안 #정보보안
  #알리익스프레스 #테무 #해외직구 #직구

[중간 해시태그 — 틈새 공략]
  #데이터주권 #개인정보유출 #해외앱보안 #직구앱위험

[IssueLens 브랜드 태그]
  #IssueLens #이슈렌즈 #issuelens

[트렌드 태그]
  #FYP #fypage #viral #카드뉴스 #정보공유 #알아야할것

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6. 플랫폼별 발행 전략
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[티스토리]
  • 타이틀에 핵심 키워드 포함 ✅
  • 메타 description 150자 이내 ✅
  • 내부 링크: 이전 EP 링크 삽입
  • 발행 시간: 오전 7시 (출근 전 독서 시간)

[네이버 블로그]
  • 제목: [알리·테무 개인정보] 형식으로 대괄호 활용
  • 태그: 30개 풀 활용
  • 이미지 3장 이상 필수 (이미지 검색 노출)
  • 발행 시간: 오전 8시

[SubStack]
  • 영문 제목도 함께 작성
  • 이메일 뉴스레터 형식 유지
  • 발행 시간: 오전 9시 (EST 기준)

[WordPress]
  • Yoast SEO 플러그인 활용
  • Schema.org 아티클 마크업 추가
  • 영문/한국어 혼용 포스트

[YouTube]
  • 제목: 감정 키워드 + 숫자 포함 (예: "충격" + "20억")
  • 썸네일: 빨간/검정 고대비 + 큰 텍스트
  • 첫 24시간 인게이지먼트 최대화 중요

[Instagram]
  • 10장 캐러셀 > 단일 이미지 (저장율 3배)
  • 스토리 → 하이라이트 저장
  • 발행: 화·목·일 오후 7~9시

[TikTok]
  • 처음 3초 훅이 전부
  • 자막 필수 (소음 없는 시청 고려)
  • 발행: 화·목·토 저녁 7~10시

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7. 100만 구독자 달성 로드맵
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Week 1: 기반 구축
  • 4대 블로그 EP01~03 발행
  • YouTube 채널 SEO 최적화
  • 모든 SNS 계정 @IssueLens 통일

Week 2: 크로스 프로모션
  • 각 플랫폼에서 다른 플랫폼 유도
  • 협업 계정 태그 (관련 인플루언서)
  • 댓글·DM 적극 응답 (알고리즘 신호)

Week 3: 바이럴 전략
  • 가장 반응 좋은 포맷 집중 확장
  • 쇼츠/릴스로 트래픽 → 블로그 유도
  • 네이버 검색 상위 목표 (이미지 검색 포함)

Week 4: 확장
  • 협업 게스트 포스트
  • 언론 보도 자료 배포
  • EP13까지 전체 발행 완료
"""
    out_path = out_dir / f"issuelens-ep{ep}-seo-master.txt"
    out_path.write_text(seo, encoding="utf-8")
    print(f"  ✅ SEO 마스터: {out_path.name}")


# ─────────────────────────────────────────────
#  이미지 생성 프롬프트
# ─────────────────────────────────────────────

def make_image_prompts(meta: dict, out_dir: Path):
    """AI 이미지 생성 프롬프트 (DALL-E / Midjourney / Stable Diffusion)."""
    ep = meta["ep_num"]
    prompts = f"""╔══════════════════════════════════════════════════════════╗
║  IssueLens EP.{ep} — AI 이미지 생성 프롬프트 가이드       ║
║  지원 도구: DALL-E 3, Midjourney v6, Adobe Firefly        ║
╚══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  섹션 1 이미지 (s1i) — 데이터 수집 개념
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[DALL-E 3 프롬프트]
A sleek smartphone screen showing a shopping app with a sinister data collection interface.
Digital data streams flowing out of the phone into dark servers labeled with lock icons.
Red warning symbols. Dark, moody atmosphere. Infographic style.
Korean text elements subtly integrated. High contrast red and dark navy color scheme.
16:9 ratio, editorial illustration style.

[Midjourney 프롬프트]
/imagine smartphone data privacy breach visualization, Korean shopping app, red danger signals,
data streams flowing to overseas servers, editorial infographic style, dark dramatic lighting,
red #C8001A and navy #1E3A8A color palette, 16:9 --ar 16:9 --v 6 --style raw

[Adobe Firefly]
사용자 스마트폰에서 빨간색 데이터 스트림이 해외 서버로 흘러가는 모습,
경고 아이콘과 자물쇠 아이콘 포함, 다크 에디토리얼 스타일, 16:9

[무료 대안 — Unsplash 검색어]
"data privacy smartphone" / "personal data security" / "digital surveillance"
추천 사진 키워드: https://unsplash.com/s/photos/data-privacy-security

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  섹션 1 영상 (s1v) — YouTube 검색어
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YouTube 검색어로 관련 영상 찾기:
  • "AliExpress personal data collection explained"
  • "알리익스프레스 개인정보 수집"
  • "Temu data privacy concerns"
  • "PIPC fine AliExpress Korea 2024"
  • "개인정보보호위원회 알리 과징금"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  섹션 2 이미지 (s2i) — 국가정보법 개념
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[DALL-E 3 프롬프트]
An ominous government building with surveillance cameras, connected by glowing red data lines
to smartphones and shopping bags. Legal document with Article 7 highlighted in red.
Map of Asia with data flow arrows. Authoritarian surveillance aesthetic.
Editorial news illustration style. Dark blue and red color scheme.

[Midjourney]
/imagine government surveillance data law article 7, Asia map, smartphones connected to
government servers, red warning lines, legal document, editorial news style,
dark atmospheric --ar 16:9 --v 6

[Unsplash 검색어]
"surveillance camera" / "government building digital" / "cybersecurity law"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  섹션 2 영상 (s2v) — YouTube 검색어
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • "China National Intelligence Law explained"
  • "중국 국가정보법 설명"
  • "Chinese tech companies data government access"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  섹션 3 이미지 (s3i) — 비대칭 구도
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[DALL-E 3 프롬프트]
An asymmetric balance scale infographic. One side: Great Firewall blocking Google, YouTube,
Instagram logos with red X marks. Other side: AliExpress and Temu logos freely flowing
data from Korea. Conceptual editorial illustration. Blue and red contrast.
Flat design infographic style, 16:9.

[Midjourney]
/imagine asymmetric trade data, great firewall vs open market, balance scale concept,
flat infographic design, editorial style, red and blue contrast --ar 16:9 --v 6

[Unsplash 검색어]
"trade imbalance infographic" / "internet censorship" / "data asymmetry"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  섹션 3 영상 (s3v) — YouTube 검색어
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • "Great Firewall China internet censorship"
  • "China app Korea data collection"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  썸네일 이미지 (YouTube / 블로그 대표 이미지)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[DALL-E 3 프롬프트 — 유튜브 썸네일]
YouTube thumbnail, ultra high contrast, red background, shocked Asian person holding phone
showing AliExpress/Temu app, large bold white Korean text overlay space on left side,
red warning icons, dark dramatic lighting, 1280x720px.
Text space for: "알리·테무 개인정보" (top) "내 정보 어디로?" (bottom)

[Canva 썸네일 가이드]
크기: 1280×720px
배경색: #C8001A (IssueLens 레드) → #0A0A0A (검정) 그라디언트
메인 텍스트: "알리·테무 개인정보" (Pretendard Black, 흰색, 90pt)
서브 텍스트: "내 정보 어디로?" (Pretendard Bold, 노란색, 60pt)
아이콘: 자물쇠 깨지는 이미지 + 스마트폰
IssueLens EP.01 뱃지: 왼쪽 상단

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  인스타그램 캐러셀 슬라이드 이미지 (10장)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
크기: 1080×1080px (정방형) 권장
디자인 도구: Canva / Adobe Express / Figma
색상 팔레트: #C8001A, #1E3A8A, #FFFFFF, #0A0A0A
폰트: Noto Sans KR (Bold, Black)
템플릿 스타일: 미니멀 뉴스 카드

Canva 검색어: "news card template Korean"
Adobe Express 검색어: "infographic dark editorial"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  무료 이미지 소스 정리
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Unsplash (unsplash.com) — 고품질 무료, 상업 사용 가능
2. Pexels (pexels.com) — 무료 스톡 사진/영상
3. Pixabay (pixabay.com) — 무료, 저작권 불필요
4. Freepik (freepik.com) — 일부 무료 (출처 표기 필요)
5. Flaticon (flaticon.com) — 아이콘
"""
    out_path = out_dir / f"issuelens-ep{ep}-image-prompts.txt"
    out_path.write_text(prompts, encoding="utf-8")
    print(f"  ✅ 이미지 프롬프트: {out_path.name}")


# ─────────────────────────────────────────────
#  메인 파이프라인 실행
# ─────────────────────────────────────────────

def run_pipeline(html_path: Path, output_base: Path):
    print(f"\n{'='*60}")
    print(f"  🚀 IssueLens 자동화 파이프라인 시작")
    print(f"  입력: {html_path.name}")
    print(f"{'='*60}")

    meta = extract_ep_meta(html_path)
    ep   = meta["ep_num"]
    print(f"  📌 EP.{ep} 메타데이터 추출 완료")

    ep_dir = output_base / f"ep{ep}"

    # 블로그
    print(f"\n  📝 블로그 버전 생성:")
    make_tistory(meta,   ep_dir / "blogs" / "tistory")
    make_naver(meta,     ep_dir / "blogs" / "naver")
    make_substack(meta,  ep_dir / "blogs" / "substack")
    make_wordpress(meta, ep_dir / "blogs" / "wordpress")

    # SNS
    print(f"\n  📱 SNS 콘텐츠 생성:")
    make_youtube_longform(meta, ep_dir / "sns" / "youtube_longform")
    make_youtube_shorts(meta,   ep_dir / "sns" / "youtube_shorts")
    make_instagram(meta,        ep_dir / "sns" / "instagram")
    make_tiktok(meta,           ep_dir / "sns" / "tiktok")
    make_facebook(meta,         ep_dir / "sns" / "facebook")
    make_x_twitter(meta,        ep_dir / "sns" / "x_twitter")
    make_threads(meta,          ep_dir / "sns" / "threads")

    # 에셋
    print(f"\n  🎨 에셋 파일 생성:")
    make_image_prompts(meta, ep_dir / "assets")
    make_seo_master(meta,    ep_dir / "seo")

    print(f"\n{'='*60}")
    print(f"  ✅ EP.{ep} 파이프라인 완료!")
    print(f"  📁 출력 위치: {ep_dir}")
    print(f"  📊 생성 파일 수: 13개")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IssueLens Automation Pipeline")
    parser.add_argument("--ep", type=str, help="단일 에피소드 HTML 경로")
    parser.add_argument("--all", type=str, help="에피소드 폴더 경로 (일괄 처리)")
    parser.add_argument("--out", type=str, default=str(OUTPUT_DIR), help="출력 기본 경로")
    args = parser.parse_args()

    output_base = Path(args.out)

    if args.ep:
        run_pipeline(Path(args.ep), output_base)
    elif args.all:
        eps_dir = Path(args.all)
        html_files = sorted(eps_dir.glob("issuelens-ep*.html"))
        print(f"  📂 {len(html_files)}개 에피소드 발견")
        for f in html_files:
            run_pipeline(f, output_base)
    else:
        print("사용법: python3 issuelens_pipeline.py --ep <HTML파일>")
        print("        python3 issuelens_pipeline.py --all <에피소드폴더>")
