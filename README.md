# Excel Automation Demo

> **두 개의 Excel 파일을 선택하면 자동으로 매칭하고, 중복·누락·미등록 데이터를 찾아 `result.xlsx`까지 만들어주는 Windows 업무자동화 데모**

[![CI](https://github.com/storm-credit/excel-automation-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/storm-credit/excel-automation-demo/actions/workflows/ci.yml)
[![Windows EXE](https://github.com/storm-credit/excel-automation-demo/actions/workflows/build-windows.yml/badge.svg)](https://github.com/storm-credit/excel-automation-demo/actions/workflows/build-windows.yml)

이 저장소는 **작은 Excel/CSV 반복업무부터 빠르게 자동화하는 외주 포트폴리오**입니다.

현재 예시는 `직원목록 ↔ 부서마스터` 대조지만, 핵심은 특정 인사 데이터가 아니라 **두 데이터셋의 매칭 + 검증 + 오류 분리 + 결과 자동생성** 패턴입니다.

---

## 30초 요약

```text
직원목록.xlsx       부서마스터.xlsx
      │                    │
      └────────┬───────────┘
               ↓
      [ Windows GUI 실행 ]
               ↓
       자동 매칭 / 검증
               ↓
     ┌─────────┼─────────┐
     ↓         ↓         ↓
   Result    Errors    Summary
   전체결과    오류만      건수요약
```

**개발 지식이 없는 사용자는 GUI EXE에서 파일 두 개를 선택하고 `검증 실행`만 누르면 됩니다.**

---

## Windows에서 사용하는 방법

### 1. 실행파일 받기

GitHub의 **Actions → Build Windows EXE → 성공한 실행 → Artifacts**에서 `excel-validator-windows`를 받습니다.

압축 파일에는 두 실행파일이 들어 있습니다.

| 파일 | 용도 |
|---|---|
| `excel-validator-gui.exe` | 일반 사용자용. 화면에서 파일 선택 후 실행 |
| `excel-validator-cli.exe` | 개발자/배치/스크립트 연계용 |

### 2. GUI 실행

`excel-validator-gui.exe`를 실행한 뒤:

1. **직원 목록** Excel 선택
2. **부서 마스터** Excel 선택
3. 결과 저장 위치 확인
4. **검증 실행** 클릭
5. 완료 후 **결과 파일 열기** 클릭

처리가 끝나면 화면에 `전체 / 정상 / 오류` 건수가 표시됩니다.

자세한 사용법은 [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)를 참고하세요.

---

## 자동으로 하는 일

- 직원 ↔ 부서 마스터 자동 매칭
- 부서명 / 관리자 자동 조회
- **중복 ID** 검출
- **부서코드 누락** 검출
- **부서 마스터에 없는 코드** 검출
- 오류 항목만 `Errors` 시트에 별도 정리
- 정상 / 오류 건수 `Summary` 시트 생성
- 결과 상태에 따라 Excel 셀 강조
- 한글/영문 컬럼명 자동 인식

---

## Before / After

### Before — 사람이 직접

```text
파일 2개 열기
→ VLOOKUP/XLOOKUP 작성
→ 한 행씩 대조
→ 누락 확인
→ 중복 확인
→ 잘못된 코드 확인
→ 오류만 다시 복사
→ 보고용 파일 정리
```

### After — 자동화

```text
파일 2개 선택
→ 검증 실행
→ result.xlsx 생성
```

검증 규칙을 코드로 고정하기 때문에 반복할 때마다 같은 기준으로 처리합니다.

---

## 검출 예시

| EmployeeID | Name | DepartmentCode | 결과 |
|---|---|---|---|
| E1001 | 김민수 | D001 | `OK` |
| E1004 | 최지우 | D004 | `DUPLICATE_ID` |
| E1007 | 한유진 | D999 | `UNKNOWN_DEPT` |
| E1008 | 강도윤 | *(빈 값)* | `MISSING_DEPT_CODE` |

대표 상태값:

```text
OK
DUPLICATE_ID
MISSING_DEPT_CODE
UNKNOWN_DEPT
```

---

## 한글/영문 컬럼 자동 인식

컬럼 순서는 달라도 됩니다. 다음처럼 흔한 이름을 자동으로 같은 의미로 인식합니다.

| 표준 의미 | 인식 예시 |
|---|---|
| 직원 ID | `EmployeeID`, `employee_id`, `사번`, `직원ID`, `직원번호` |
| 이름 | `Name`, `이름`, `성명`, `직원명` |
| 부서 코드 | `DepartmentCode`, `department_code`, `부서코드`, `조직코드` |
| 이메일 | `Email`, `E-mail`, `이메일`, `메일` |
| 부서명 | `DepartmentName`, `부서명`, `조직명` |
| 관리자 | `Manager`, `관리자`, `담당자`, `부서장`, `조직장` |

같은 의미의 컬럼이 두 개 동시에 있으면 임의로 선택하지 않고 오류로 중단합니다.

---

## 결과 Excel

생성되는 `result.xlsx`에는 세 시트가 있습니다.

### `Result`
전체 데이터와 매칭된 부서 정보, 검증 상태를 보여줍니다.

### `Errors`
오류 데이터만 따로 모으고 권장 조치를 함께 표시합니다.

### `Summary`
전체/정상/오류 및 오류 유형별 건수를 보여줍니다.

---

## 실제 외주에서는 이렇게 바꿀 수 있습니다

이 데모의 핵심 구조는 다양한 소형 업무에 그대로 적용할 수 있습니다.

| 업무 | 자동화 예시 |
|---|---|
| 인사 | 직원명부 ↔ 조직도 검증 |
| 영업 | 거래처 ↔ 담당자 매칭 |
| 쇼핑몰 | 주문 ↔ 상품마스터 검증 |
| 재고 | 입출고 데이터 ↔ 재고마스터 대조 |
| 회계 | 정산내역 ↔ 입금내역 비교 |
| 운영 | 시스템 추출 CSV ↔ 관리대장 비교 |

처음부터 대형 시스템을 만드는 대신 **반복 시간이 큰 한 가지 업무부터 작게 자동화**하는 것이 목표입니다.

---

## 검증된 품질 게이트

PR 단계에서 Linux와 Windows를 각각 검증합니다.

### Linux CI

```text
Syntax Check
    ↓
Golden Case 4종
    ↓
한글 컬럼 Alias 검증
    ↓
10,000행 Performance Smoke
```

현재 PR 검증에서 위 단계가 모두 통과했습니다.

### Windows EXE CI

```text
PyInstaller
   ├─ excel-validator-cli.exe
   └─ excel-validator-gui.exe
            ↓
CLI Smoke Test
GUI Smoke Test
            ↓
Artifact Upload
```

현재 실제 Windows GitHub Actions에서 **CLI/GUI 두 EXE 빌드·스모크 테스트·Artifact 업로드까지 성공**했습니다.

---

## 개발자로 실행하기

```bash
pip install -r requirements.txt
python scripts/generate_sample.py
python src/validate_excel.py sample/employees.xlsx sample/departments.xlsx --output result.xlsx
```

GUI는 다음처럼 실행할 수 있습니다.

```bash
python -m src.gui
```

1만 행 성능 스모크:

```bash
python -m scripts.performance_smoke --rows 10000 --max-seconds 20
```

---

## 프로젝트 구조

```text
excel-automation-demo/
├─ src/
│  ├─ validate_excel.py       # 매칭 / 검증 / 결과 Excel 생성
│  └─ gui.py                  # 비개발자용 Windows GUI
├─ scripts/
│  ├─ generate_sample.py      # 더미 Excel 생성
│  └─ performance_smoke.py    # 10,000행 성능 스모크
├─ tests/
│  └─ test_validate_excel.py  # Golden Case + 컬럼 Alias 테스트
├─ .github/workflows/
│  ├─ ci.yml                  # Linux 기능/성능 검증
│  └─ build-windows.yml       # GUI/CLI EXE 빌드 및 스모크
├─ docs/
│  ├─ USER_GUIDE.md
│  ├─ ACCEPTANCE_CRITERIA.md
│  ├─ CURRENT_STATUS.md
│  ├─ DECISIONS.md
│  └─ DESIGN_OPTIONS.md
├─ CLAUDE.md
└─ README.md
```

---

## 데이터 안전

- 저장소에는 실제 회사·고객 데이터를 넣지 않습니다.
- 샘플 데이터는 모두 더미 데이터입니다.
- 현재 프로그램은 선택한 로컬 파일을 로컬에서 처리합니다.
- 외부 서버 업로드나 고객 데이터 전송 기능은 없습니다.

---

## 개발 원칙

이 프로젝트는 공통 **Minimum Action Agent OS** 방식으로 작업하되, 프로젝트 저장소에는 Excel 자동화에 필요한 목표·제약·상태·테스트만 유지합니다.

- 필요한 Tool / Context / 권한만 사용
- 구현 전 맹점·함정 확인
- 설계 선택지가 있을 때 대안 비교
- Golden Case와 CI로 결과 검증
- 계획이 달라지면 Decision Log 기록
- 단순 작업에 불필요한 Agent를 늘리지 않음

---

## 현재 상태

**Client-ready MVP v0.2**

- [x] 직원/부서 데이터 자동 매칭
- [x] 중복 ID / 누락 / 미등록 코드 검출
- [x] 오류/요약 Excel 자동 생성
- [x] 한글/영문 컬럼명 자동 매핑
- [x] 비개발자용 Windows GUI
- [x] CLI 실행 방식
- [x] Golden Case 테스트
- [x] 10,000행 성능 스모크
- [x] GitHub Actions CI
- [x] Windows GUI/CLI EXE 빌드
- [x] Windows EXE 스모크 테스트
- [x] Artifact 자동 업로드
- [x] 사용자 가이드

---

## 목표

> **사람이 매번 Excel을 열어 비교하는 반복업무 하나를 빠르고 안전하게 없애는 것.**

필요해질 때만 CSV, 사용자별 컬럼 매핑, API, DB, 웹 업로드 같은 기능으로 확장합니다.
