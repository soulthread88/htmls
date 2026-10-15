UNO SYSTEM 재사용형 페이지 템플릿 (보정판, 2026-10-15)
기준 파일: products(4).html → uno_products_based_template.html

1. uno_products_based_template.html을 복사하여 새 페이지를 만듭니다.
2. title(data-ko/data-en), description, canonical, OG·Twitter 메타, JSON-LD를 페이지별로 수정합니다.
   - 주소는 모두 https://soulmaru.com/파일이름.html (템플릿의 PAGE.html 자리)
   - robots는 템플릿에서 noindex입니다. 실제 페이지에서는 index,follow… 로 바꿉니다.
   - 제품 페이지는 JSON-LD에 Product 항목을 추가하고, FAQ 문구는 화면 FAQ와 똑같이 맞춥니다.
3. #products의 .prod-card를 복제하거나 변경합니다. 섹션은 .pg / .pg.alt를 번갈아 쓰고 사이에 <div class="div-line"></div>.
4. 이미지·영상은 GitHub 외부 URL(soulthread88/imgs/homepage/uno)로만 참조하고 Base64 삽입을 피합니다.
   src는 .webp, data-orig는 원본(.png 등). 복잡한 구성도는 가로 3840px "이름 4K.webp"를 src·data-zoom에.
5. 모든 이미지·영상 아래 원작자/출처/라이선스를 실제 확인하여 기재합니다 (class="uno-credit").
6. 배포 전에 메뉴 링크, 언어 전환, Light/Dark, 모바일 및 문의 기능을 테스트합니다.
7. 머리말(<uno-header>)·꼬리말(<uno-footer>)은 손대지 않습니다. 모든 페이지가 index.html과 같아야 합니다.
   새 페이지는 머리 메뉴, products.html 카드, sitemap.xml·llms.txt에 함께 등록합니다.
8. 이미지 대원칙은 자동 적용됩니다: 오른쪽 위 '교체' 버튼(평소 숨김, 가까이 가면 표시), 그 밖을 누르면 확대.
   예외: data-ux-detail="해설 id"를 단 이미지는 누르면 해설이 펼쳐집니다.

보정 내역 (원본 대비)
- 잘못된 닫는 태그 </meta>, </img> 제거 (W3C 오류)
- <body id="artifacts-component-root-html"> 편집 환경 잔재 제거
- canonical https://www.uno-system.com/ → https://soulmaru.com/PAGE.html, og:url·Twitter 메타를 자리표시로
- 템플릿 자체는 검색 제외(noindex)
- 이미지 교체·확대 스크립트를 최신 대원칙 버전으로 교체
- 머리말·꼬리말을 현재 사이트(v15, 새 제품 메뉴 포함)와 동일하게
- 구조화 데이터(JSON-LD) 골격과 출처 표기·구성도·사양표용 공통 스타일 추가
- 대표 이미지 아래 출처 줄을 보이게 하고 '원작자 · 출처 · 라이선스' 형식으로
