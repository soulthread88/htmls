# Episode 19 수정 가이드

## 1. CSS 수정 사항

### 다음 편 예고 섹션 (.next-episode) - 라인 414-436
```css
.next-episode {
    background: linear-gradient(135deg, #FFE0B2 0%, #FFCC80 100%);  /* 핑크 → 주황 계열로 변경 */
    padding: 60px;
    margin: 60px 0;
    border-radius: 25px;
    text-align: center;
    border: 8px solid #FF9800;  /* 테두리도 주황색 */
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.next-episode h2 {
    color: #E65100;  /* 진한 주황색 */
    margin-top: 0;
    font-size: 56px;
}

.next-episode p {
    font-size: 36px;
    line-height: 2.2;
    color: #BF360C;  /* 매우 진한 주황/갈색 - 대비 최대화 */
}
```

### 키워드 강조 클래스 추가 - 라인 389 이후
```css
.keyword {
    color: #FF0000;
    font-weight: 900;
    background: #FFEB3B;
    padding: 5px 12px;
    border-radius: 8px;
}

.highlight-red {
    color: #FF0000;
    font-weight: 900;
}

.highlight-blue {
    color: #0066CC;
    font-weight: 900;
}

.highlight-white {
    color: #FFFFFF;
    font-weight: 900;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
```

### 댓글 섹션 CSS 추가
```css
/* 댓글 섹션 */
.comments-section {
    background: white;
    padding: 50px;
    margin: 60px 0;
    border-radius: 25px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
}

.comments-section h2 {
    font-size: 48px;
    color: #667eea;
    margin: 0 0 30px 0;
    font-weight: 900;
}

.spell-checker-embed {
    background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
    padding: 30px;
    margin: 30px 0;
    border-radius: 15px;
    border-left: 10px solid #4CAF50;
}

.spell-checker-embed h3 {
    color: #2E7D32;
    font-size: 32px;
    margin: 0 0 20px 0;
}

.spell-checker-embed .checker-link {
    display: inline-block;
    background: #4CAF50;
    color: white;
    padding: 15px 30px;
    border-radius: 10px;
    text-decoration: none;
    font-size: 24px;
    font-weight: 700;
}

.comment {
    background: #f9f9f9;
    padding: 30px;
    margin: 20px 0;
    border-radius: 15px;
    border-left: 5px solid #667eea;
}

.comment-author {
    font-size: 26px;
    font-weight: 900;
    color: #667eea;
    margin-bottom: 10px;
}

.comment-date {
    font-size: 20px;
    color: #999;
    margin-bottom: 15px;
}

.comment-text {
    font-size: 28px;
    line-height: 2;
    color: #333;
}
```

## 2. HTML 수정 사항

### 키워드 강조 - AI, ChatGPT 등
모든 AI 관련 용어에 `<span class="highlight-red">` 적용:
- AI → `<span class="highlight-red">AI</span>`
- ChatGPT → `<span class="highlight-red">ChatGPT</span>`
- 구글 어시스턴트 → `<span class="highlight-red">구글 어시스턴트</span>`
- 시리 → `<span class="highlight-red">시리</span>`
- 알렉사 → `<span class="highlight-red">알렉사</span>`

### 띄어쓰기 수정
- "생각해보세요" → "생각해 보세요"
- "들어보세요" → "들어 보세요"
- "사용해보세요" → "사용해 보세요"
- "해보세요" → "해 보세요"

### 다음 편 예고 제목 강조 (라인 1266-1278)
```html
<div class="next-episode">
    <h2>🎬 다음 편 예고</h2>
    <p>
        <strong style="font-size: 48px; color: #C2185B;">Episode 20</strong><br>
        <span style="font-size: 42px;"><strong><span class="highlight-red">"AI 시대, 손주와 소통하기"</span></strong></span>
    </p>
    <p style="font-size: 32px; margin-top: 20px;">
        시리즈 마무리!<br>
        손주 세대와 함께 살아가는 <span class="highlight-red">AI</span> 시대의 지혜를<br>
        모두 정리해드립니다.<br><br>
        감동의 피날레를 기대해주세요! 🎉✨
    </p>
</div>
```

### 댓글 섹션 추가 (다음 편 예고 다음)
```html
<!-- 댓글 섹션 -->
<div class="comments-section">
    <h2>💬 댓글</h2>
    
    <!-- 맞춤법 검사기 -->
    <div class="spell-checker-embed">
        <h3>✏️ 댓글 맞춤법 검사</h3>
        <p style="font-size: 22px; color: #2E7D32; margin-bottom: 15px;">
            댓글을 작성하기 전에 맞춤법을 확인해 보세요!
        </p>
        <a href="https://nara-speller.co.kr/old_speller/" target="_blank" class="checker-link">
            🔍 한국어 맞춤법/문법 검사기로 이동
        </a>
    </div>

    <!-- 댓글들 -->
    <div class="comment">
        <div class="comment-author">김영숙 👵</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            오늘 아침부터 시리한테 날씨 물어봤어요! 신기하네요^^
        </div>
    </div>

    <div class="comment">
        <div class="comment-author">박철호 👴</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            윤호 덕분에 AI를 실생활에서 어떻게 쓰는지 확실히 알겠습니다. 할아버지도 이제 음성 비서 써볼게요!
        </div>
    </div>

    <div class="comment">
        <div class="comment-author">이순자 👵</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            약 먹는 알람 기능이 제일 좋네요. 자꾸 잊어버렸는데 이제 안심이에요.
        </div>
    </div>

    <div class="comment">
        <div class="comment-author">최민수 👴</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            ChatGPT로 건강 식단 물어보니까 정말 상세하게 알려주더군요!
        </div>
    </div>

    <div class="comment">
        <div class="comment-author">정미경 👵</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            손주들이 할머니도 이제 AI 쓰신다고 깜짝 놀랐어요 ㅎㅎ 뿌듯합니다!
        </div>
    </div>

    <div class="comment">
        <div class="comment-author">강태영 👴</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            다음 편도 기대됩니다~
        </div>
    </div>

    <div class="comment">
        <div class="comment-author">윤정희 👵</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            아침에 뉴스 들으면서 식사하는 게 이제 일상이 됐어요. 편해요!
        </div>
    </div>

    <div class="comment">
        <div class="comment-author">한상철 👴</div>
        <div class="comment-date">2025년 12월 10일</div>
        <div class="comment-text">
            AI와 함께하는 하루 일정표가 정말 도움 됐습니다. 감사합니다!
        </div>
    </div>
</div>
```

## 3. 사이드바 광고 영역 확장

기존 3개 → 7개로 확장 (라인 1400 이후)

```html
<!-- 광고 4 -->
<div class="sidebar-item">
    <div class="ad-space">
        <div class="ad-text">광고 영역 4<br>(300x250)</div>
    </div>
</div>

<!-- 광고 5 -->
<div class="sidebar-item">
    <div class="ad-space">
        <div class="ad-text">광고 영역 5<br>(300x250)</div>
    </div>
</div>

<!-- 광고 6 -->
<div class="sidebar-item">
    <div class="ad-space">
        <div class="ad-text">광고 영역 6<br>(300x250)</div>
    </div>
</div>

<!-- 광고 7 -->
<div class="sidebar-item">
    <div class="ad-space">
        <div class="ad-text">광고 영역 7<br>(300x250)</div>
    </div>
</div>
```

## 4. 주요 키워드 위치

Episode 19에서 강조해야 할 주요 키워드 위치:

- 라인 500: "시리야" → `<span class="highlight-red">시리</span>`
- 라인 527: "ChatGPT야" → `<span class="highlight-red">ChatGPT</span>`
- 라인 543: "오케이 구글" → `<span class="highlight-red">구글 어시스턴트</span>`
- 라인 548: "ChatGPT야" → `<span class="highlight-red">ChatGPT</span>`
- 모든 "AI" 단어에 `<span class="highlight-red">AI</span>` 적용

## 5. 적용 순서

1. CSS 섹션 전체 교체 (라인 12-437)
2. 키워드 강조 적용 (전체 본문)
3. 띄어쓰기 수정 (전체 본문)
4. 다음 편 예고 섹션 교체 (라인 1266-1278)
5. 댓글 섹션 추가 (라인 1278 다음)
6. 광고 영역 추가 (사이드바 끝부분)
