# Findi 

<img src="https://github.com/user-attachments/assets/d8f2c2ea-5270-4541-a4d1-49eccaf0431c" width="10%" alt="findi logo"/>

🖥️ 본 프로젝트는 **SSAFY**(삼성 청년 SW 아카데미) 1학기 관통 프로젝트 결과물입니다

<br>

# TEAM:  연채 말고 송금

<br>

## 🔧 Tech Stack

### Language
<div style="display: flex; gap: 8px; align-items: center;">
<!--Python-->
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>
<!--JavaScript-->
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=JavaScript&logoColor=white"/>

<br>

### Framework

#### Front
<div style="display: flex; gap: 8px; align-items: center;">
<!--Vue.js-->
  <img src="https://img.shields.io/badge/Vue.js-4FC08D?style=flat-square&logo=Vue.js&logoColor=white&Color=white"/>
  <!-- node.js -->
<img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=Node.js&logoColor=white"/>
<!-- HTML5 -->
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white"/>
<!-- CSS3 -->
<img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white"/>
<!-- tailwind -->
<img src="https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white"/>

</div>

#### Back
<div style="display: flex; gap: 8px; align-items: center;">
  <!--Django-->
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=Django&logoColor=white"/>
  <!-- Json -->
<img src="https://img.shields.io/badge/JSON-000000?style=flat-square&logo=json&logoColor=white"/>
</div>

  <br/>

### ETC
<div style="display: flex; gap: 8px; align-items: center;">
<!--Postman-->
  <img src="https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=Postman&logoColor=white"/>
<!--SQLite-->
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white"/>
<!--Notion-->
  <img src="https://img.shields.io/badge/Notion-000000?style=flat-square&logo=Notion&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/>

</div>

<br>
<br>

### API



## ERD
![Findi_ERD](https://github.com/user-attachments/assets/ac858fcf-f434-4746-b767-4b77adecb920)

<br>

## 컴포넌트 구조

<br>

## 🤗 역할 분배

| 송명철 | 이채연 |
|--------|--------|
| 기획 및 디자인 | 기획 및 디자인 |
| 회원 커스터마이징 | 주변 은행 검색 |
| API / DB | 예/적금 상품 조회 |
| Algorithm 추천 | 주식 정보 영상 조회 |
| CHAT BOT | 회원 게시판 |
| CSS | 기능 정리 및 ppt |
| 코드 전체 Debugging |  |

<br>

## 💻 개발일지
- 2025년 5월 19-20일,
 22일-27일 (9일)😂
  
| 날짜 | 작업 목록 |
|------|------|
| 2025년 5월 19일 | 디자인 |
| 2025년 5월 20일 → 2025년 5월 21일 | 아이디어 구상 |
| 2025년 5월 22일 | ERD |
| 2025년 5월 22일 | 메인페이지 |
| 2025년 5월 22일 | 요구사항 확인 + ERD |
| 2025년 5월 23일 | 현운 상품 비교 |
| 2025년 5월 23일 | 금/은 가격 조회 |
| 2025년 5월 23일 | 자유 게시판 |
| 2025년 5월 23일 → 2025년 5월 24일 | 예/적금 상품조회 |
| 2025년 5월 24일 | Kakao OAuth |
| 2025년 5월 24일 | 로그인 & 회원 가입 + Google OAuth |
| 2025년 5월 24일 → 2025년 5월 26일 | 토대 금융 상품 & 맞춤 조회 |
| 2025년 5월 24일 → 2025년 5월 25일 | 주식정보 영상 조회 |
| 2025년 5월 26일 | 은행찾기 |
| 2025년 5월 26일 | 챗봇 |
| 2025년 5월 27일 | 발표 자료 만들기 |
| 2025년 5월 27일 | json 파일 수정 및 데이터 생성 |
| 2025년 5월 27일 | 예/적금 상품 조회 |


<br>

## 👨‍💻 서비스 대표 기능
| **No** | **요구사항 명** | **기능** |
| --- | --- | --- |
| 1 | 메인페이지 | 메인페이지 디자인 |
|  |  | Findi 의 기능 carousel (스크롤)로 소개 |
| 2 | 회원 커스터마이징 | 회원가입 및 로그인/로그아웃 |
|  |  | 비밀번호 찾기 기능 
|||→ 이메일로 인증코드 수신 후 비밀번호 전환 가능 |
|  |  | Google/ kakao Oauth 및 JWT 토큰 |
|  |  | 로그인 상태에 따른 페이지 접근 및 권한 관리 |
|  |  | 회원의 정보 추가하여 알고리즘 추천으로 연결 |
| 3 | 예적금 금리 비교 | API를 활용한 금융 상품 정보 DB저장 |
|  |  | 예/적금 상품 조회 - 금리 비교 가능 (정렬) |
|  |  | 상품 상세 정보 Modal  |
|  |  | 예/적금 관심상품 가입(등록) 가능 |
|  |  | 상품 가입 후 관리자의 금리 수정 있을 시 이메일로 변화 여부 확인 가능 |
| 4 | 현물 상품 비교 | excel 데이터 chart로 변환 |
| 5 | 관심 종목 정보 검색 | Youtube API를 활용하여 동영상 검색 |
|  |  | 동영상 iframe로 제공 및 나중에 볼 영상으로 저장 가능 |
| 6 | 근처 은행 검색 | KakaoMap API를 활용하여 지도 제공 |
|  |  | 장소 필터링으로 검색하여 상세 위치 제공 |
| 7 | 커뮤니티 | 게시글 CRUD, 댓글 CRUD 기능 |
|  |  | Quill 을 활용 하여 이미지와 텍스트 포맷 변환 가능 |
| 8 | 프로필 페이지 | 회원 상세 정보 입력 
| | | → 알고리즘으로 연결 |
|  |  | 가입한 상품들을 프로필에서 확인 가능 및 차트로 금리 비교 가능 |
| 9 | 🌟금융 상품 추천 알고리즘🌟 | 회원 정보의 데이터와 예적금 상품을 조합하여 gpt 프롬프트에 전달|
| 10 | ❤️챗봇 | FAQ 는 JSON으로 저장해 사용자에게 제공 |
|||gpt 프폼프트 연결하여 답변|

<br>

## 금융 상품 알고리즘 추천 기능
!!!

<br>

## 📺 시연 영상
> **메인페이지**
![mainpage](https://github.com/user-attachments/assets/3a027177-8e22-430a-ad51-4667c5589a3f)


> **이메일 전송**
![smtp (1)](https://github.com/user-attachments/assets/a692e417-47af-4c4b-882b-2d285142b3b0)
>사용자가 가입한 상품의 금리 정보를 관리자가 수정하면
>사용자에게 금리가 변동됐음을 알리는 이메일이 발송된다

<br>

## 생성형 AI 활용

| 활용 분야                     | 내용                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------ |
| **1. 더미 데이터 생성**          | - 게시글/댓글, 사용자 정보 등 실제 서비스 흐름을 가정한 JSON 더미 데이터 생성                                       |
| **2. ERD 설계 보조**          | 모델 연결 방식 조율하여 ERD제공 |
| **3. 챗봇 프롬프트 작성 및 로직 구현** | - FAQ 응답 자동화용 JSON 설계<br>- 사용자의 질문을 받아 GPT로 연결하여 답변 생성                               |
| **4. CSS 및 UI 구조 제안**     | - Tailwind 기반 디자인 레이아웃 구성<br>- 컴포넌트별 UI 개선 (카드 위치, 색상, 정렬 등) 조언                      |
| **5. 서비스 성능 및 구조 개선**     | - 페이지 기능 분리 <br>- 비동기 처리 흐름 정리 및 로직 단순화                           |
| **6. 전체 코드 디버깅 지원**       | -  Vue 컴포넌트 props 오류 추적 <br>- Axios 및 백엔드 API 연결 문제 해결 조언                |


<br>


## 느낀점 및 후기

- **송명철**
이번 SSAFY 관통 프로젝트를 통해 단순한 기능 구현을 넘어서, 하나의 웹 서비스를 기획하고 완성도 있게 구축하는 전체 흐름을 직접 경험할 수 있었습니다.

사용자 인증 시스템(JWT 기반), OAuth(Google/Kakao), DB 설계(ERD), 그리고 금융 상품 추천 알고리즘과 챗봇까지 다양한 기능을 구현했습니다.  
그 과정에서 Django Rest Framework(DRF)와 dj-rest-auth를 활용해 커스터마이징된 로그인/회원가입 로직을 구축하고, 토큰 기반 인증의 흐름을 명확히 이해하게 되었습니다.

챗봇 구현에서는 단순히 OpenAI를 호출하는 수준이 아니라, JSON 기반 FAQ 시스템과 유사도 분석, GPT 연동까지 다층적 로직을 설계하여 사용자 질문에 맞춤 응답을 제공하는 구조를 만들었습니다.  
또, 사용자 프로필 기반 금융 상품 추천 알고리즘도 직접 설계하고, GPT 프롬프트를 효과적으로 구성하여 AI 기반 추천의 품질을 높이는 데 집중했습니다.

Vue.js와의 연동에서도 localStorage 관리, Axios 인터셉터 설정, 상태관리 등 프론트와 백의 연결에 대한 실전 감각을 익힐 수 있었고,  
특히 팀원과의 긴밀한 커뮤니케이션과 역할 분배 일정 조율 등을 통해 복잡한 문제들을 함께 해결해 나갔던 시간이 기억에 남습니다.

이 프로젝트를 통해 저는 단순한 기능 구현자에서 한 발 더 나아가, 서비스의 흐름을 설계하고 문제를 예측하며 해결책을 제시하는 개발자로 성장할 수 있었다고 생각합니다.  
함께 해 준 팀원에게 감사하고, 앞으로 더 넓은 시야로 협업하며 더 나은 제품을 팀원과 소통하며 만들 수 있는 개발자가 되고 싶습니다.

<br>

- **이채연**
  
요구사항이 제공되기 전부터 팀원과 어떤 기능이 좋을 지 상의도 하고 기획을 시작하였습니다. 아이디어를 공유하며 서로 이야기 하는 시간을 많이 가지며 프로젝트에 대한 구상을 해나갔습니다.

프로젝트를 진행하며 프론트와 백엔드 간의 연계에 대한 이해가 높아졌습니다. 각자 맡은 기능을 구현하였고, 공통되는 부분은 중간중간 소통하면서 기능구현을 이어나갔습니다.
수업에서 다루지 못했던 JWT 인증 및 quill editor, bootstrap이 아닌 tailwind css, chart.js 라이브러리도 프로젝트를 통해 추가적으로 학습할 수 있었습니다.

저는 기획부터 기능 구현까지 다 처음이었기에 이 프로젝트를 통해 모든 과정에 참여해 볼 수 있어 좋은 경험이었습니다. 특히나 협업에 대한 경험이 크게 다가왔습니다.
협업 과정에서 git의 흐름에 대한 이해와 발생한 충돌이나 오류를 해결하는 디버깅에 대한 이해가 향상되었고, 
Notion을 통한 일정 관리와 회의 기록은 프로젝트에서 매우 중요한 부분임을 깨달았습니다.

모르는 부분을 상세히 알려주고, 코드도 디버깅해주며 언제나 격려해 주는 우리 든든한 팀원 덕에 구현 완료까지 올 수 있었던 것 같습니다. 
덕분에 처음이지만 할 수 있다는 믿음을 가지고 마무리 할 수 있었습니다.

하고 싶은 기능들이 있었지만 시간이 없거나 기능이 필요가 없어져 구현하지 못해 아쉽기도 합니다. 앞으로는 UX 향상을 위한 성능 최적화나 코드 리팩토링을 통해 더욱 완성도 높은 서비스를 제공할 수 있을 것 같습니다. 

<br>
