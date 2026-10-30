# Conference Info (14 conferences)

GitHub Pages 정적 웹사이트 + 매월 1일 오전 9시(KST) 공식 CFP 링크 점검.

## 배포
1. ZIP을 풀어서 **내용물**(`index.html`, `conferences.json`, `scripts/`, `.github/`)을 `unggix/conference-info` 저장소 루트에 업로드/교체.
2. Settings → Pages → Deploy from a branch, `main` / `(root)`.
3. Settings → Actions → General 에서 workflow 실행이 허용되는지 확인.
4. Actions → Check conference CFPs monthly → Run workflow 로 수동 테스트.
5. Issues 탭에 생성된 월간 점검 결과를 보고, 변경 확인 후 `conferences.json`을 수정하면 Pages에 반영됨.

**주의:** 이 버전은 월간 공식 페이지 접속·상태 점검 및 GitHub Issue 생성까지 자동화합니다. 공식 CFP는 문서 구조가 제각각이고 날짜 오류가 위험하기 때문에 Deadline/장소를 자동으로 덮어쓰지 않습니다. 2027/2028 회차는 검토 후 갱신합니다.

GitHub Actions `cron`은 UTC 기준이며 예약 실행이 지연될 수 있습니다.
