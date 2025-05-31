# 📚 Bookie – 당신만을 위한 도서 추천 플랫폼

- 프로젝트 기간 : 2025/05/22 ~ 2023/05/27 (약 6일)

- Bookie는 설문과 독서 이력을 바탕으로 인생 책을 찾아주는 AI 도서 추천 플랫폼입니다.
개인의 서재 관리와 감상글 공유를 통해 독서의 깊이와 즐거움을 함께 확장해보세요.
---

## ERD
![ERD 이미지](./README_image/ERD.png)

---

## 아키텍처
![아키텍처 이미지](./README_image/Architecture.png)

--- 

## 📂 프로젝트 구조

```plaintext
Bookie/
├── backend/
│   ├── accounts/                 
│   ├── books/                    
│   ├── media/                    
│   ├── the_greatest_book_pjt/    
│   ├── venv/                     
│   ├── db.sqlite3                
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── .vscode/
│   ├── node_modules/
│   ├── public/
│   ├── src/                     
│   ├── venv/                 
│   ├── index.html
│   ├── jsconfig.json
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── README.md
```

---

## 🛠 기술 스택

### 🔸 Frontend
- Vue 3 + Vite
- Vue Router, Pinia
- Bootstrap 5
- Axios

### 🔹 Backend
- Django 4
- Django REST Framework
- SQLite3

---

## ✨ 주요 기능

### 📊 01. 설문 기반 추천 시스템
- 사용자가 작성한 설문을 기반으로 AI가 주요 키워드를 분석하여 맞춤형 도서 추천
- 회원은 추가적인 추천 방식이 작동, 개인의 회원 독서 취향 반영

### 📚 02. 나만의 서재
- 읽고 싶은 책, 읽고 있는 책, 완독한 책 등 다양한 **독서 상태**로 도서 관리 가능
- 내가 남긴 독서 포스트 또한 한눈에 파악 가능

### 💬 03. 포스트 커뮤니티
- 사용자는 책에 대한 감상이나 의견을 자유롭게 작성하고 공유 가능
- 다른 사용자의 포스트를 조회하고 소통함으로써 **독서 취향을 확장**할 수 있음

---

## ⚙️ 실행 방법

### 1. 백엔드 실행 (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows는 venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

```bash
python manage.py loaddata books.json categories.json
python manage.py loaddata dummy_users.json  avoided_keywords.json lifestyle_keywords.json reading_styles.json
python manage.py loaddata dummy_posts.json dummy_user_preferences.json dummy_reading_state.json dummy_keyword.json dummy_post_keywod.json
python manage.py runserver
```

### 2. 프론트엔드 실행 (Vue 3)
```bash
cd frontend
npm install
npm run dev
```

---

### ✍️ 역할

| 이름             | 담당 영역                                   | 주요 구현 기능                                                                                                                 |
| ---------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **곽서현(팀장)** | `accounts (회원 / 인증)`<br>`main (메인)`   | - 회원가입, 로그인, 마이페이지, 인증 관련 API 구현<br>- 사용자의 설문 정보 및 책장 구현<br>- 설문 조사 기반 추천 알고리즘 구현 |
| **김미진**       | `book (도서)`<br>`post (포스트 / 커뮤니티)` | - 도서 모델 설계 및 CRUD 구현<br>- 사용자의 책 포스트 CRUD 구현<br>- 독서 상태 기반 추천 알고리즘 구현                         |

--- 
### 느낀점
- 곽서현

이번 프로젝트를 통해 단순히 서비스를 구현하는 것을 넘어 사용자 경험을 중심에 두고 기획과 디자인 개발을 함께 고민하는 과정이 얼마나 중요한지를 체감할 수 있었습니다. 처음에는 개인이 맡은 기능 구현에 집중했다면 팀원과 협업 속에서 디자인의 통일성과 감성적인 UI/UX의 가치도 깊이 이해하게 되었습니다.

특히 Vue와 Django를 연동하며 생긴 다양한 문제들을 해결하는 과정에서 실력을 많이 키울 수 있었습니다. User를 맡으면서 했던 회원가입, 마이페이지 등 토큰을 사용하여 사용자를 인증하는 과정에서 오류와 어려움이 있었지만 하나씩 해결하는 과정을 통해 모델을 명확하게 구성하는 것의 중요성을 알 수 있었습니다.

또한 AI를 활용하여 추천시스템을 구현하며 기존에는 단순했던 추천이 사용자 개별 추천으로 좀 더 고도화된 기능을 구현할 수 있었습니다.

물론 예외 상황에 대한 처리를 더 세심히 하지 못한 점과 계획했던 부분 중 일부는 구현하지 못한 점이 아쉬움이 남습니다. 이번 경험을 바탕으로 앞으로도 기술적인 완성도와 더불어 사용자를 고려한 서비스를 제작하고 싶습니다.

- 김미진

마지막 관통 프로젝트를 진행하면서 구체적인 서비스 기획부터 프론트엔드와 백엔드 연동, 그리고 기능 구현까지 서비스 개발의 전 과정을 직접 경험할 수 있어 매우 보람찬 시간이었습니다. 사용자 대상의 추천 기능이나 게시글 작성 기능 등 실질적인 사용자 경험을 고려한 기획부터 시작해 실제로 데이터를 처리하고 화면에 출력되도록 구현하는 과정을 거치며 많은 것을 배울 수 있었습니다.

이번 프로젝트에서는 Vue라는 프론트엔드 라이브러리를 처음 활용하게 되어 초반에는 생소한 문법과 구조로 인해 어려움을 겪기도 했습니다. 하지만 생성형 AI를 통해 오류의 원인을 빠르게 파악하고 팀원들과의 활발한 의견 교환과 협업을 통해 문제를 해결해나가면서 점차 익숙해질 수 있었습니다. 덕분에 새로운 기술을 실전에서 직접 적용해보는 값진 경험을 할 수 있었습니다.

아직 서버로의 완전한 배포나 일부 추가하고자 했던 기능들이 남아 있어 아쉬움도 있지만 프로젝트 종료 이후에도 코드 리팩토링과 사용자 피드백을 반영한 개선 작업을 계속해나가며 완성도를 높이고자 합니다. 짧은 기간 동안 많은 노력을 쏟아부었던 만큼 이 프로젝트에 대한 애정이 남다르며 앞으로도 더 나은 서비스를 만들기 위한 지속적인 시도와 학습을 이어갈 계획입니다.