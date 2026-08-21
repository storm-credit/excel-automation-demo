# ACCEPTANCE CRITERIA

## Core validation
- [x] 직원 데이터와 부서 마스터를 매칭한다.
- [x] 중복 EmployeeID를 검출한다.
- [x] 부서코드 누락을 검출한다.
- [x] 미등록 부서코드를 검출한다.
- [x] 오류 목록을 별도 시트로 보여준다.
- [x] 정상/오류 결과를 요약한다.
- [x] 모든 샘플 데이터는 더미 데이터다.

## Input flexibility
- [x] 흔한 한글/영문 컬럼 별칭을 표준 컬럼으로 자동 매핑한다.
- [x] 같은 의미의 컬럼이 중복되면 임의 선택하지 않고 오류로 중단한다.

## User experience
- [x] 비개발자가 GUI에서 파일 두 개를 선택할 수 있다.
- [x] 결과 저장 위치를 지정할 수 있다.
- [x] 한 번의 검증 실행으로 result.xlsx를 생성한다.
- [x] 완료 후 전체/정상/오류 건수를 화면에서 확인할 수 있다.
- [x] 결과 파일을 GUI에서 바로 열 수 있다.

## Quality gates
- [x] Golden Case 자동 테스트를 통과한다.
- [x] 10,000행 데이터 성능 스모크를 통과한다.
- [x] GitHub Actions Linux CI를 통과한다.
- [x] Windows CLI EXE를 실제 빌드하고 스모크 테스트한다.
- [x] Windows GUI EXE를 실제 빌드하고 스모크 테스트한다.
- [x] Windows EXE를 GitHub Actions Artifact로 업로드한다.

## Safety / portfolio
- [x] 실제 회사·고객 데이터를 저장소에 포함하지 않는다.
- [x] 외부 업로드 없이 로컬 파일만 처리한다.
- [x] 사용법과 현재 구현 범위를 README/USER_GUIDE에 문서화한다.
