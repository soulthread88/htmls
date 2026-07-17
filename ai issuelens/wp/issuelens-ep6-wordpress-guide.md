# IssueLens EP.06 — WordPress 업로드 가이드

## 파일 안내
- **`issuelens-ep6-fixed.html`** — 완성된 EP.06 스탠드얼론 HTML (로컬 미리보기 / 직접 호스팅용)
- **`issuelens-ep6-wordpress.html`** — WordPress Custom HTML 블록 삽입용

---

## WordPress.org 업로드 방법 (권장: 3가지 옵션)

### ✅ 옵션 A — 전체 페이지 템플릿으로 올리기 (가장 깔끔)
**조건:** 테마가 full-width 페이지 템플릿을 지원해야 함

1. WordPress 관리자 → **Pages → Add New**
2. 오른쪽 **Page Attributes → Template → Full Width** (또는 "Blank" / "No Sidebar") 선택
3. 에디터에서 오른쪽 상단 **"⋮" → Code Editor** 전환
4. `issuelens-ep6-fixed.html` 파일의 `<body>` 안쪽 내용 전체를 붙여넣기
5. `<head>` 안의 `<link>` 폰트 태그 2줄은 → WordPress **Appearance → Customize → Additional CSS** 또는 테마 헤더에 추가

### ✅ 옵션 B — Custom HTML 블록으로 삽입
1. 새 페이지/포스트 → **블록 추가(+) → Custom HTML** 선택
2. `issuelens-ep6-wordpress.html` 전체 내용을 붙여넣기
3. 미리보기로 확인 후 발행

> ⚠️ **주의:** WordPress의 일부 보안 플러그인(예: Wordfence)이 `<script>` 태그를 제거할 수 있습니다. 이 경우 아래 옵션 C를 사용하세요.

### ✅ 옵션 C — HTML 파일 직접 업로드 (가장 안정적)
1. **Media → Add New** 또는 FTP/파일 매니저로 서버에 `issuelens-ep6-fixed.html` 업로드
2. WordPress 페이지에서 iframe으로 임베드:
```html
<iframe 
  src="https://yourdomain.com/wp-content/uploads/issuelens-ep6-fixed.html"
  width="100%" 
  height="4000px" 
  frameborder="0"
  scrolling="no"
  style="border:none;width:100%">
</iframe>
```
3. 또는 직접 URL로 링크로 공유

---

## 포스트 메타 정보 (WordPress SEO 필드 입력용)

| 필드 | 내용 |
|------|------|
| **제목** | Western Warnings & The Fight Back \| IssueLens EP.06 |
| **슬러그** | issuelens-ep06-western-warnings-fight-back |
| **메타 설명** | Warning signals the U.S., U.K., and EU are sending to Korea — and the lessons from Australia, Lithuania, and Canada, nations that stood up to China's economic retaliation and won. |
| **키워드** | Western warnings Korea, Australia China economic retaliation, Lithuania China Taiwan, Korea democracy decline, Finlandization, CFIUS, China economic sanctions, Korea data sovereignty |
| **카테고리** | IssueLens / Economic Security |
| **태그** | #AustraliaChinaTrade, #LithuaniaChina, #WesternWarningsKorea, #FinlandizationKorea, #KoreaDemocracyWatch |

---

## EP.06 수정 사항 요약 (템플릿 기준)

| 항목 | 내용 |
|------|------|
| Pretendard 폰트 링크 제거 | 템플릿에 없는 불필요한 외부 폰트 CSS 링크 삭제 |
| SNS 버튼 방식 교체 | 정적 `<a href="#...">` → 동적 modal (`onclick="snsOpen(id)")` 방식으로 교체 |
| SNS modal CSS 추가 | `.sns-modal`, `.sns-box`, `.sns-inp`, `.sns-saved-bar` 등 누락된 스타일 추가 |
| SNS modal HTML 추가 | `#sns-modal` 전체 HTML 블록 추가 |
| SNS JS 함수 추가 | `snsOpen()`, `snsSave()`, `snsClose()`, `snsClearSaved()` 등 완전한 SNS 링크 저장 시스템 추가 |
| `snsbtn` CSS 업데이트 | `background:transparent`, `position:relative`, `.has-link::after` (✓ 뱃지) 추가 |
| Escape 핸들러 수정 | `ytClose()`만 → `ytClose(); snsClose()` 둘 다 처리 |
| `media-pair` 2칼럼 | 1fr → 1fr 1fr (템플릿 표준 2칼럼 레이아웃) + 모바일 반응형 추가 |
| 푸터 업데이트 | primary sources 링크 6개 추가, EP.07 프리뷰 링크 추가 |
