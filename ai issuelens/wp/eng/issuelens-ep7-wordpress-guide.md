# IssueLens EP.07 — WordPress 업로드 가이드

## 파일 안내
- **`issuelens-ep7-fixed.html`** — 수정 완료된 EP.07 스탠드얼론 HTML (로컬 미리보기 / 직접 호스팅용)
- **`issuelens-ep7-wordpress.html`** — WordPress Custom HTML 블록 삽입용

---

## WordPress.org 업로드 방법

### ✅ 옵션 A — 전체 페이지 템플릿 (가장 깔끔)
1. WordPress 관리자 → **Pages → Add New**
2. **Page Attributes → Template → Full Width** (또는 Blank / No Sidebar) 선택
3. 에디터 우상단 **"⋮" → Code Editor** 전환
4. `issuelens-ep7-fixed.html`의 `<body>` 안 내용 전체 붙여넣기
5. Google Fonts `<link>` 2줄은 → **Appearance → Customize → Additional CSS** 상단에 추가

### ✅ 옵션 B — Custom HTML 블록
1. 새 페이지/포스트 → **블록 추가(+) → Custom HTML**
2. `issuelens-ep7-wordpress.html` 전체 내용 붙여넣기
3. 미리보기 확인 후 발행

> ⚠️ Wordfence 등 보안 플러그인이 `<script>` 태그를 제거할 수 있음. 해당 시 옵션 C 사용.

### ✅ 옵션 C — HTML 파일 직접 서버 업로드 (가장 안정적)
1. FTP 또는 파일 매니저로 `issuelens-ep7-fixed.html`을 서버에 업로드
2. WordPress 페이지에서 iframe으로 임베드:

```html
<iframe 
  src="https://yourdomain.com/wp-content/uploads/issuelens-ep7-fixed.html"
  width="100%"
  height="5000px"
  frameborder="0"
  style="border:none;width:100%">
</iframe>
```

---

## 포스트 메타 정보 (WordPress SEO 필드 입력용)

| 필드 | 내용 |
|------|------|
| **제목** | China's Digital Silk Road: How Huawei 5G, DeepSeek AI & SMIC Chips Threaten American Security \| IssueLens EP.07 |
| **슬러그** | issuelens-ep07-china-digital-silk-road-huawei-deepseek-smic |
| **메타 설명** | Huawei 5G backdoors, DeepSeek AI data harvesting, SMIC chip export control evasion, Alibaba Cloud surveillance risks. The definitive American guide to China's tech takeover — backed by DOJ, FCC, and Congressional reports. |
| **키워드** | China Digital Silk Road, Huawei 5G ban, DeepSeek privacy risk, SMIC 7nm chip, China AI surveillance, tech sovereignty, US China tech war, Huawei backdoor, DeepSeek ban, national security AI |
| **카테고리** | IssueLens / National Security |
| **태그** | #HuaweiBackdoor, #DeepSeekPrivacy, #ChinaTechThreat, #DigitalSilkRoad, #TechSovereignty, #SMICChips |
| **OG 이미지** | Digital Silk Road 인포그래픽 / Huawei 5G 지도 권장 |

---

## EP.07 수정 사항 요약 (템플릿 기준)

| # | 항목 | 상세 내용 |
|---|------|-----------|
| 1 | **Section 2 dcall 중복 콘텐츠 제거** | `<span class="biglbl">` + `<p class="cbody">` 블록이 동일 내용으로 2회 연속 삽입된 버그 → 중복 제거 |
| 2 | **TikTok 버튼 추가** | SNS social bar에서 TikTok 버튼 누락 → 6개 버튼 완성 |
| 3 | **SNS 버튼 순서 통일** | EP7: YT→IG→XB→FB→TH (비표준) → 템플릿 표준: YT→IG→TT→TH→XB→FB |
| 4 | **IndexedDB 표준 패턴 교체** | 단순 동기식 open → Promise 기반 `openDB()` 패턴 + `_intentionalDelete` 플래그 지원 (삭제 복원 기능 정상화) |
| 5 | **Scroll reveal stagger 적용** | 단순 `.add('on')` → 템플릿 표준 `i * 60ms` stagger delay 적용 |
| 6 | **Risk bar threshold 통일** | `0.2` → 템플릿 표준 `0.25` |
