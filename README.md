# 포트폴리오 - 현실을 넘어선, 가상공간을 향하여

노션에서 내보낸 이력서/포트폴리오를 GitHub Pages로 게시하는 프로젝트입니다.

## GitHub Pages 배포 방법

### 1. GitHub 저장소 생성

1. [GitHub](https://github.com)에 로그인
2. **New repository** 클릭
3. 저장소 이름 입력 (예: `portfolio`, `notion-resume`)
4. **Create repository** 클릭

### 2. 프로젝트를 GitHub에 푸시

터미널에서 다음 명령어를 실행하세요:

```bash
cd "c:\Users\USER\Downloads\개인 페이지 & 공유된 페이지"
git init
git add .
git commit -m "Initial commit: Notion portfolio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

> `YOUR_USERNAME`을 GitHub 사용자명으로, `YOUR_REPO_NAME`을 생성한 저장소 이름으로 바꾸세요.

### 3. GitHub Pages 활성화

1. GitHub 저장소 페이지에서 **Settings** 탭 클릭
2. 왼쪽 메뉴에서 **Pages** 선택
3. **Source**에서 **Deploy from a branch** 선택
4. **Branch**에서 `main` 선택, 폴더는 **/ (root)** 선택
5. **Save** 클릭

### 4. 배포 완료

몇 분 후 다음 주소에서 이력서를 확인할 수 있습니다:

- **프로젝트 사이트**: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`
- **사용자 사이트** (저장소 이름이 `username.github.io`인 경우): `https://YOUR_USERNAME.github.io/`

## 로컬에서 미리보기

브라우저에서 `index.html` 파일을 직접 열어 확인할 수 있습니다.
