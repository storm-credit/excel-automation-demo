# Excel Automation Demo

> **두 개의 Excel 파일을 넣으면, 자동으로 매칭하고 오류를 찾아 결과 파일까지 만들어주는 소형 업무자동화 데모**

[![CI](https://github.com/storm-credit/excel-automation-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/storm-credit/excel-automation-demo/actions/workflows/ci.yml)
[![Windows EXE](https://github.com/storm-credit/excel-automation-demo/actions/workflows/build-windows.yml/badge.svg)](https://github.com/storm-credit/excel-automation-demo/actions/workflows/build-windows.yml)

이 프로젝트는 반복적인 Excel/CSV 대조 업무를 **버튼 한 번 수준의 자동 처리 흐름**으로 바꾸기 위한 외주 포트폴리오 샘플입니다.

현재 데모는 `직원목록`과 `부서마스터`를 예제로 사용하지만, 같은 구조를 상품·거래처·재고·주문·정산·회원 데이터 등에도 적용할 수 있습니다.

---

## 한눈에 보기

```text
employees.xlsx          departments.xlsx
      │                        │
      └──────────┬─────────────┘
                 ↓
        자동 매칭 / 데이터 검증
                 ↓
   ┌─────────────┼──────────────┐
   ↓             ↓              ↓
result.xlsx   Errors 시트    Summary 시트
정상+전체결과   오류만 정리      처리현황 요약
```

### 자동으로 하는 일

- 직원 ↔ 부서 마스터 자동 매칭
- 부서명 / 관리자 자동 조회
- **중복 사번** 검출
- **부서코드 누락** 검출
- **존재하지 않는 부서코드** 검출
- 오류 항목 별도 정리
- 정상 / 오류 건수 요약

---

## 왜 필요한가

### Before — 수작업

```text
직원목록 열기
→ 부서마스터 열기
→ 한 행씩 찾기
→ VLOOKUP/XLOOKUP 작성
→ 누락 확인
→ 중복 확인
→ 오류만 다시 복사
→ 보고용 파일 정리
```

데이터가 많아질수록 시간이 오래 걸리고, 사람이 직접 확인하는 과정에서 누락이 생길 수 있습니다.

### After — 자동화

```text
파일 2개 준비
→ 명령 1회 실행
→ 결과 Excel 생성
```

검증 규칙을 코드로 고정하기 때문에 같은 작업을 반복해도 동일한 기준으로 처리할 수 있습니다.

---

## 검출 예시

| EmployeeID | Name | DepartmentCode | 결과 |
|---|---|---|---|
| E1001 | 김민수 | D001 | `OK` |
| E1004 | 최지우 | D004 | `DUPLICATE_ID` |
| E1007 | 한유진 | D999 | `UNKNOWN_DEPT` |
| E1008 | 강도윤 | *(빈 값)* | `MISSING_DEPT_CODE` |

현재 Golden Case에서 위 유형을 자동 검증합니다.

---

## 빠른 실행

### 1. 설치

```bash
pip install -r requirements.txt
```

### 2. 더미 Excel 생성

```bash
python scripts/generate_sample.py
```

### 3. 자동 검증 실행

```bash
python src/validate_excel.py \
  sample/employees.xlsx \
  sample/departments.xlsx \
  --output result.xlsx
```

생성된 `result.xlsx`에서 전체 결과와 오류 내역을 확인할 수 있습니다.

> 실제 회사·고객 데이터는 저장소에 포함하지 않습니다. 샘플 파일은 모두 공개 가능한 더미 데이터로 재현합니다.

---

## 입력 데이터

### `employees.xlsx`

| 컬럼 | 의미 |
|---|---|
| `EmployeeID` | 직원 고유 ID |
| `Name` | 이름 |
| `DepartmentCode` | 부서 코드 |
| `Email` | 이메일 |

### `departments.xlsx`

| 컬럼 | 의미 |
|---|---|
| `DepartmentCode` | 부서 코드 |
| `DepartmentName` | 부서명 |
| `Manager` | 담당 관리자 |

---

## 결과 파일

자동화 결과에는 다음 정보가 포함됩니다.

- 원본 직원 정보
- 매칭된 부서 정보
- Validation 결과
- 오류 유형
- 오류 검토용 데이터
- 처리 건수 요약

대표 상태값:

```text
OK
DUPLICATE_ID
MISSING_DEPT_CODE
UNKNOWN_DEPT
```

---

## 실제 외주에서는 이렇게 확장할 수 있습니다

이 데모의 핵심은 특정 직원 데이터가 아니라 **두 데이터셋의 매칭 + 검증 + 결과 자동생성 패턴**입니다.

예를 들어 다음과 같은 소형 업무자동화에 적용할 수 있습니다.

| 업무 | 자동화 예시 |
|---|---|
| 인사 | 직원명부 ↔ 조직도 검증 |
| 영업 | 거래처 ↔ 담당자 매칭 |
| 쇼핑몰 | 주문 ↔ 상품마스터 검증 |
| 재고 | 입출고 데이터 ↔ 재고마스터 대조 |
| 회계 | 정산내역 ↔ 입금내역 비교 |
| 운영 | 시스템 추출 CSV ↔ 관리대장 비교 |

처음부터 대형 시스템을 만드는 대신, **반복 시간이 큰 한 가지 업무부터 작게 자동화**하는 것을 목표로 합니다.

---

## 품질 검증

### Golden Case

현재 자동 테스트는 최소 다음을 보장합니다.

- 정상 코드 → `OK`
- 중복 ID → `DUPLICATE_ID`
- 부서코드 누락 → `MISSING_DEPT_CODE`
- 미등록 부서코드 → `UNKNOWN_DEPT`
- 필수 컬럼 누락 → 오류 처리

### GitHub Actions CI

`push` 또는 Pull Request가 발생하면 자동으로 테스트합니다.

```text
Push / Pull Request
        ↓
Dependency Install
        ↓
pytest Golden Cases
        ↓
PASS / FAIL
```

### Windows 실행파일

`main`에 변경이 반영되거나 버전 태그를 만들면 Windows 실행파일도 자동 빌드합니다.

```text
main update / v* tag
        ↓
PyInstaller build
        ↓
EXE smoke test
        ↓
excel-validator.exe
        ↓
GitHub Actions Artifact
```

즉 코드 변경 후 **테스트와 실행파일 생성 여부를 GitHub Actions에서 다시 검증**합니다.

---

## 프로젝트 구조

```text
excel-automation-demo/
├─ src/
│  └─ validate_excel.py       # Excel 매칭 / 검증 핵심 로직
├─ scripts/
│  └─ generate_sample.py      # 공개 가능한 더미 Excel 생성
├─ tests/
│  └─ test_validate_excel.py  # Golden Case 테스트
├─ .github/workflows/
│  ├─ ci.yml                  # Push/PR 자동 테스트
│  └─ build-windows.yml       # Windows EXE 빌드/스모크 테스트
├─ docs/
│  ├─ ACCEPTANCE_CRITERIA.md
│  ├─ CURRENT_STATUS.md
│  ├─ DECISIONS.md
│  └─ DESIGN_OPTIONS.md
├─ CLAUDE.md
└─ README.md
```

---

## 개발 원칙

이 프로젝트는 공통 **Minimum Action Agent OS** 방식으로 작업하되, 공개 저장소에는 프로젝트 자체에 필요한 목표·제약·테스트·현재 상태만 유지합니다.

핵심 원칙:

- 필요한 Tool만 사용
- 필요한 Context만 전달
- 구현 전 맹점/함정 확인
- 설계 선택지가 실제로 있을 때만 대안 비교
- Golden Case로 결과 검증
- 계획이 바뀌면 Decision Log 기록
- 공통 Agent 운영 규칙과 프로젝트 고유 규칙을 분리

---

## 현재 상태

**Prototype v0.1**

- [x] 직원/부서 데이터 자동 매칭
- [x] 중복 ID 검출
- [x] 부서코드 누락 검출
- [x] 미등록 부서코드 검출
- [x] 오류 결과 Excel 생성
- [x] Golden Case 테스트
- [x] GitHub Actions CI
- [x] Windows EXE 빌드 + 스모크 테스트 Workflow 정의
- [ ] 컬럼명 자동 매핑
- [ ] 10,000행 이상 성능 검증
- [ ] 비개발자용 단일 실행 UX

---

## 목표

이 저장소의 목표는 복잡한 ERP를 만드는 것이 아닙니다.

> **“사람이 매번 엑셀을 열어 비교하는 반복업무 하나를 빠르고 안전하게 없애는 것.”**

작은 자동화부터 시작해 필요할 때 API 연동, DB 저장, 웹 업로드 화면 등으로 확장할 수 있습니다.
