# KIND 2026-10-26 블로그 배포 키트

모든 원고는 같은 사실·출처·PRO/CON을 씁니다. 이미지는 `soulthread88/imgs/news/102626/`, 영상은 `soulthread88/videos/news/102626/`에서 불러옵니다.

## GEO 적용 사항
- 첫 화면에 결론(TL;DR)을 먼저 둡니다. 날짜(보도 기준일), 수치, 출처 링크를 문장 안에 직접 씁니다.
- 각 기사는 FACTS → CONTEXT → CONNECTIONS → JUDGMENT 순서입니다. 쟁점에는 PRO/CON을 붙였습니다.
- 끝에 FAQ를 넣었습니다(AI 검색 답변에 그대로 인용되기 쉬운 형식).
- HTML판(WordPress·Blogger·Tistory·Ghost)에는 JSON-LD `NewsArticle` + `FAQPage`를 포함했습니다.
- 반복 키워드를 해시태그로 붙였습니다: #김정은단둥 #왕후닝 #태풍참피 #가상자산과세 등.

## 파일 ↔ 플랫폼
| 파일 | 플랫폼 | 붙여넣는 방법 |
|---|---|---|
| velog.md | Velog | 마크다운 그대로 붙여넣기(머리말에 태그·썸네일 포함) |
| wordpress.html | WordPress | 블록 편집기 → 사용자 정의 HTML 블록 |
| blogger_adsense.html | Blogger | HTML 보기에 붙여넣기. `ca-pub-XXXX`·`data-ad-slot` 값을 본인 애드센스 값으로 교체 |
| tistory.html | 티스토리 | 기본 모드 → HTML. 광고는 관리 › 수익에서 자동 삽입 |
| substack.md | Substack | 에디터에 붙여넣기(마크다운 자동 변환) |
| stibee_email.html | 스티비 | 새 이메일 › HTML 직접 입력. `$%unsubscribe%$`는 스티비 수신거부 치환자 |
| ghost_paid.html | Ghost(유료 구독) | HTML 카드로 붙여넣기. `<!--members-only-->` 위는 무료 미리보기, 아래는 유료 멤버 전용 |
| naver_blog.txt / naver_post.txt | 네이버 블로그·포스트 | 텍스트 붙여넣기 후 [이미지] URL 자리에 사진 삽입 |
| naver_cafe.txt | 네이버 카페 | 공지/뉴스 게시판용 |
| brunch_story.txt | 브런치스토리(카카오 브런치) | 텍스트 붙여넣기 후 이미지 삽입 |
| kakao_view_board.txt | 카카오톡 채널 소식(구 카카오 뷰 보드) | 목록형 요약 + 출처 링크 |
| linkedin_article.md | LinkedIn 아티클 | 요약판(전문 링크 유도) |
| discord.txt / telegram.txt | Discord·Telegram 채널 | 2,000자 이내 공지 |
| medium_en.md | Medium(영어) | 마크다운 붙여넣기 |
| note_jp.md | note.com(일본어) | 마크다운 붙여넣기 |

## 추가로 추천하는 플랫폼
- **Google 뉴스(Publisher Center)**: 뉴스레터 HTML이 GitHub Pages에 공개되면 등록할 수 있습니다. GEO와 가장 직접적으로 연결됩니다.
- **네이버 인플루언서 / 네이버 프리미엄콘텐츠**: 유료 구독을 네이버 안에서 받을 수 있습니다.
- **Threads·Bluesky**: 영상(피드 4:5)과 TL;DR 3줄을 함께 올리는 용도.
- **Beehiiv**: 무료 플랜이 넉넉하고 추천(리퍼럴) 기능이 있는 뉴스레터 플랫폼(Substack 대안).
- **Hashnode / dev.to**: 영어권 개발자 대상 기술·AI 기사가 있을 때.
- **daum 카페, 오픈채팅방 공지**: 시니어 독자층 확산용.
- **Pinterest**: 4:5 이미지 카드에 출처 링크를 달아 장기 유입.
