# Vercel 배포 수정 방법

현재 사이트가 **인트로/히어로 애니메이션 없이** 바로 포트폴리오만 보이는 이유:
- Vercel이 **부모 폴더**를 루트로 배포하여 `index.html`(정적 페이지)만 서빙 중입니다.

## 해결 방법 (Vercel 대시보드)

1. https://vercel.com 접속 후 로그인
2. **portfolio** 프로젝트 선택
3. **Settings** → **General**
4. **Root Directory** 항목에서 **Edit** 클릭
5. `portfolio` 입력 후 **Save**
6. **Deployments** 탭에서 최신 배포 **Redeploy** (또는 새 커밋 푸시)

## 또는: 수동 재배포

프로젝트 폴더(portfolio)에서 직접 배포:

```powershell
cd "c:\Users\USER\Downloads\개인 페이지 & 공유된 페이지\portfolio"
npx vercel --prod
```

---

수정 후 접속 시 예상 흐름:
1. **정보를 찾고 계신가요?** (2초)
2. **하지만 원하는 답이...** (2초)
3. **검색은 되지만, 답은 없습니다** (2초)
4. **그 문제, 해결할 수 있습니다** (2초) → 자동 스크롤
5. **히어로 섹션** (RAG & 데이터 엔지니어)
6. **정체성 섹션**
7. **포트폴리오 상세** (기존 index.html)
