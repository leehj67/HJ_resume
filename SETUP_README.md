# public 폴더 설정 및 배포

## 1. public 폴더 복사

아래 중 하나를 실행하세요.

**방법 A – 배치 파일 실행**
- `setup-public.bat` 더블클릭

**방법 B – 터미널**
```powershell
cd "c:\Users\USER\Downloads\개인 페이지 & 공유된 페이지"
npm run copy-public
```

## 2. 의존성 설치

```powershell
npm install
```

## 3. 로컬 실행

```powershell
npm run dev
```

브라우저에서 http://localhost:3000 접속  
→ 인트로 → 히어로 → 정체성 → 포트폴리오 순서로 표시됩니다.

## 4. Vercel 배포

```powershell
npx vercel --prod
```

`build` 시 자동으로 `prebuild`에서 public 폴더가 복사됩니다.
