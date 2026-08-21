# CURRENT STATUS

## Current Phase
**Client-ready MVP v0.2 / Minimum Action Agent OS adopted**

첫 외주 포트폴리오로 보여줄 수 있는 최소 제품 범위가 완료되었습니다.

## Completed
- 더미 직원/부서 데이터 작성
- 직원 ↔ 부서 자동 매칭
- 중복 사번 검출
- 부서코드 누락 검출
- 미등록 부서코드 검출
- Result / Errors / Summary Excel 출력
- 결과 상태 셀 강조 및 필터 적용
- 흔한 한글/영문 컬럼명 자동 매핑
- 중복 의미 컬럼 ambiguity guard
- 재현 가능한 샘플 생성 스크립트
- 비개발자용 Tkinter GUI
- GUI에서 파일 선택 / 결과 위치 선택 / 검증 실행 / 결과 열기
- CLI 실행 경로 유지
- Golden Case 자동 테스트 4개 통과
- 10,000행 성능 스모크 통과
- GitHub Actions Linux CI 통과
- Windows CLI EXE PyInstaller 빌드 및 스모크 성공
- Windows GUI EXE PyInstaller 빌드 및 스모크 성공
- `excel-validator-windows` Artifact 업로드 성공
- 사용자 가이드 추가
- README를 외주 포트폴리오 관점으로 개편
- `storm-credit/minimum-action-agent-os`를 공통 작업 방법론 정본으로 연결

## Verification Evidence
PR #2 기준:
- Linux CI: syntax / pytest / 10k performance smoke 성공
- Windows CI: CLI build / GUI build / CLI smoke / GUI smoke / artifact upload 성공
- Windows Artifact: `excel-validator-windows`

## OS Adoption Review
- 현재 범위는 단순 소형 자동화이므로 별도 Builder Agent를 늘리지 않고 direct work를 기본으로 사용한다.
- 독립 검증은 pytest Golden Case + Linux/Windows GitHub Actions가 담당한다.
- 공통 preflight/blindspot 절차는 프로젝트에 복제하지 않고 Minimum Action Agent OS를 참조한다.
- 프로젝트에는 Excel 도메인 고유 규칙, 상태, 결정, acceptance criteria만 유지한다.

## First MVP Boundary
현재 첫 상품의 완료 범위는 다음으로 고정한다.

`파일 2개 선택 → 자동 컬럼 인식 → 매칭/검증 → result.xlsx 생성 → 오류/요약 확인`

CSV, 사용자 정의 컬럼 매핑 UI, DB, API, 웹 업로드, 설치프로그램/코드서명은 **첫 외주를 시작하기 위한 필수 범위가 아니므로 후속 요구가 생길 때만 추가**한다.

## Next Action
기능을 더 늘리기보다 이 저장소를 실제 소형 외주 지원에 사용한다.
다음 기술 포트폴리오는 별도 저장소에서 간단한 REST API 연동/데이터 저장 자동화로 확장하는 것이 우선이다.
