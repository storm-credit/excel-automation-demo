# Excel Automation Demo

외주 포트폴리오용 직원/부서 데이터 자동 검증 샘플입니다.

## 문제
- 직원 목록과 부서 마스터를 매번 수작업으로 대조
- 중복 사번, 부서코드 누락, 존재하지 않는 부서코드를 사람이 확인

## 자동화 결과
1. 직원 목록과 부서 마스터 자동 매칭
2. 부서명/관리자 자동 조회
3. 중복 사번 검출
4. 부서코드 누락 검출
5. 미등록 부서코드 검출
6. 오류 목록 별도 정리
7. 요약 KPI 및 차트 생성

## 시트
- `Employees`: 입력 직원 데이터
- `Departments`: 부서 마스터
- `Result`: 자동 매칭 및 검증 결과
- `Errors`: 오류 검토용 목록
- `Summary`: 처리 결과 요약

모든 데이터는 포트폴리오용 더미 데이터입니다.

## 작업 방법론
이 프로젝트는 구현 전에 맹점/함정을 먼저 확인하고, 4개 디자인 시안을 비교한 뒤 최소 범위로 구현합니다.

- Blindspot Scan
- Trap Preflight
- 4 Design Options
- Least Tool / Least Context / Least Authority
- Independent Critique
- Decision Log
- Acceptance Criteria

자세한 기준은 `CLAUDE.md`와 `docs/`를 참고합니다.

## Python 자동화 실행
```bash
pip install -r requirements.txt
python scripts/generate_sample.py
python src/validate_excel.py sample/employees.xlsx sample/departments.xlsx --output result.xlsx
```

샘플 `.xlsx` 파일은 저장소에 바이너리로 고정하지 않고 `scripts/generate_sample.py`로 재현합니다.

## GitHub Actions
- `CI`: push / pull request 때 자동으로 Golden Case 테스트 실행
- `Build Windows EXE`: Actions에서 수동 실행하거나 `v*` 태그를 push하면 `excel-validator.exe` 빌드 후 Artifact로 제공

즉, 개발 흐름은 `push → CI 테스트 → 필요 시 Windows EXE 빌드`입니다.
