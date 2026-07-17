# IssueLens 완전 자동화 파이프라인 — 사용 가이드

## 📁 폴더 구조

```
issuelens/
├── scripts/
│   └── issuelens_pipeline.py     ← 마스터 자동화 스크립트
├── _templates/
│   └── issuelens-template.html   ← 마스터 템플릿
├── ep01/
│   ├── issuelens-ep1-*.html      ← 원본 파일
│   ├── blogs/
│   │   ├── tistory/              → 티스토리 발행용 HTML
│   │   ├── naver/                → 네이버 블로그용 HTML
│   │   ├── substack/             → 서브스택용 Markdown
│   │   └── wordpress/            → WordPress.org용 HTML
│   ├── sns/
│   │   ├── youtube_longform/     → 유튜브 롱폼 스크립트 (12~18분)
│   │   ├── youtube_shorts/       → 유튜브 쇼츠 스크립트 (60초)
│   │   ├── instagram/            → 인스타 캐러셀 10장 + 해시태그
│   │   ├── tiktok/               → 틱톡 30초/60초 스크립트
│   │   ├── facebook/             → 페이스북 포스트
│   │   ├── x_twitter/            → X 스레드 (7트윗)
│   │   └── threads/              → Threads 포스트 + 댓글 체인
│   ├── assets/
│   │   └── *-image-prompts.txt   → AI 이미지 생성 프롬프트
│   └── seo/
│       └── *-seo-master.txt      → SEO 키워드 마스터
└── ep02/ ... ep13/               ← EP02부터 같은 구조 자동 생성
```

---

## 🚀 새 에피소드 처리 방법

```bash
# 단일 에피소드 처리
python3 scripts/issuelens_pipeline.py --ep episodes/issuelens-ep02-xyz.html

# 여러 에피소드 일괄 처리
python3 scripts/issuelens_pipeline.py --all ./episodes/
```

---

## 📅 일일 발행 워크플로우

### Step 1: 파이프라인 실행 (5분)
```bash
python3 scripts/issuelens_pipeline.py --ep issuelens-epXX-[제목].html
```

### Step 2: 이미지 준비 (10~20분)
1. `ep{XX}/assets/image-prompts.txt` 열기
2. DALL-E 3 (https://chat.openai.com) 또는 Midjourney에 프롬프트 붙여넣기
3. 생성된 이미지 → 각 블로그 HTML의 미디어 박스에 삽입
4. 또는: Unsplash 검색어로 무료 이미지 사용

### Step 3: 블로그 발행 (20분)
| 플랫폼 | 파일 | 발행 시간 |
|--------|------|-----------|
| 티스토리 | blogs/tistory/*.html | 07:00 |
| 네이버 블로그 | blogs/naver/*.html | 08:00 |
| SubStack | blogs/substack/*.md | 09:00 |
| WordPress | blogs/wordpress/*.html | 09:30 |

### Step 4: SNS 발행 (30분)
| 플랫폼 | 파일 | 발행 시간 |
|--------|------|-----------|
| YouTube 쇼츠 | sns/youtube_shorts/*.txt | 12:00 |
| Instagram | sns/instagram/*.txt | 19:00 |
| TikTok | sns/tiktok/*.txt | 19:30 |
| Threads | sns/threads/*.txt | 20:00 |
| X (트위터) | sns/x_twitter/*.txt | 20:30 |
| Facebook | sns/facebook/*.txt | 21:00 |
| YouTube 롱폼 | sns/youtube_longform/*.txt | 다음날 09:00 |

---

## 🎨 이미지 빠른 삽입 방법

### 방법 A: Unsplash 직접 URL 삽입 (가장 빠름)
```html
<!-- 미디어 박스 대신 이 코드로 교체 -->
<img src="https://images.unsplash.com/photo-[ID]?w=800&q=80" 
     alt="[설명]" style="width:100%;border-radius:14px">
```

### 방법 B: AI 이미지 생성 (최고 품질)
1. image-prompts.txt의 DALL-E 프롬프트 복사
2. ChatGPT → DALL-E 3에 붙여넣기
3. 생성된 이미지 다운로드
4. 블로그 HTML의 미디어 박스에 업로드

### 방법 C: Canva로 직접 제작 (브랜드 일관성)
- Canva 템플릿: "뉴스 카드" 검색
- 색상: #C8001A (빨강), #1E3A8A (파랑), #0A0A0A (검정)
- 폰트: Noto Sans KR Bold

---

## ⚖️ 법률·윤리 준수 가이드

### 반드시 지킬 것
- ✅ 모든 수치는 공신력 있는 출처 명기 (개인정보보호위원회, FTC 등)
- ✅ 정치적 논란 사안: Pro/Con 양측 의견 균형 있게 제시
- ✅ 출처 표기 형식: *Source: [기관명], [날짜], [작성자]* (이탤릭, 본문보다 2pt 작게)
- ✅ YouTube 영상 인용: *Source: [URL]*
- ✅ 사실 확인 없는 내용 절대 포함 금지

### 면책 공고 포함 (자동 포함됨)
본 게시물은 공신력 있는 언론 보도 및 정부 기관 발표 자료를 바탕으로 작성된 공익적 논평입니다.

---

## 📊 성과 측정 지표

### 주간 체크
- [ ] 블로그 방문자 수 (GA4 또는 네이버 통계)
- [ ] YouTube 조회수 + 구독자 증가
- [ ] 인스타그램 도달률 + 저장 수
- [ ] 틱톡 조회수 + 팔로워 증가

### 100만 구독자 목표 (4주)
- Week 1: 계정 기반 + EP01~03 발행
- Week 2: 크로스 프로모션 + EP04~07
- Week 3: 바이럴 최적화 + EP08~11
- Week 4: 확장 + EP12~13 완료

---

*IssueLens 자동화 파이프라인 v1.0 | 질문: 각 파일 내 상단 주석 참조*
