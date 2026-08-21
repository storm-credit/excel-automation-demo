# DECISIONS

## 2026-08-21 — 첫 외주 범위를 소형 자동화로 제한
- 이유: 본업 병행을 고려해 1~3일 내 끝낼 수 있는 작업부터 시작.
- 포함: Excel/CSV 병합, 검증, API 연동, 간단 데이터 가공.
- 제외: 대형 RAG/Agent 플랫폼 구축, 상주형, 전체 웹서비스 구축.

## 2026-08-21 — 첫 데모를 직원/부서 검증으로 선택
- 이유: 비개발자도 문제와 결과를 즉시 이해할 수 있음.
- 장점: 중복/누락/마스터 불일치 등 외주에서 흔한 문제를 보여줌.
- 위험: 실제 고객 파일의 컬럼 구조가 다를 수 있음.
- 대응: 흔한 한글/영문 컬럼 별칭을 자동 매핑하고, 그 범위를 넘는 고객별 매핑은 후속 요구로 처리.

## 2026-08-21 — Minimum Action Agent OS를 공통 작업 방법론 정본으로 채택
- 공통 방법론 정본: `storm-credit/minimum-action-agent-os`
- 이유: 프로젝트마다 동일한 preflight/blindspot/meta-prompting 규칙을 복제하면 Mega CLAUDE.md와 규칙 드리프트가 생김.
- 변경: 프로젝트 CLAUDE.md는 OS adoption + 프로젝트 고유 규칙만 유지.
- 변경: 프로젝트에 복제해둔 범용 preflight/blindspot skill 제거.
- 유지: Excel 고유 architecture/testing 규칙, 상태, 결정, acceptance criteria.
- Agent 정책: 현재 범위는 단순 소형 자동화이므로 별도 Agent를 늘리지 않고 direct work + 테스트/CI 검증을 사용.

## 2026-08-21 — 첫 상품 UX를 GUI + CLI 이중 진입점으로 확정
- 원래 추천안: Python 실행형(B안)을 중심으로 시작.
- 발견: 외주 고객이 Python 명령행을 직접 사용하는 것은 첫 상품의 진입장벽이 큼.
- 변경: 핵심 로직은 Python 모듈로 유지하고, 비개발자용 Tkinter GUI를 얇게 추가.
- 결과: `excel-validator-gui.exe`는 일반 사용자용, `excel-validator-cli.exe`는 개발/배치 연계용.
- 영향: 웹앱까지 확장하지 않고도 '파일 2개 선택 → 실행' 경험을 제공.

## 2026-08-21 — 컬럼 자동 매핑 범위를 흔한 Alias로 제한
- 이유: 고객마다 모든 임의 컬럼명을 자동 추론하면 오매핑 위험이 커짐.
- 선택: 사번/직원ID, 이름/성명, 부서코드/조직코드 등 흔한 별칭만 deterministic mapping.
- 안전장치: 같은 의미 컬럼이 둘 이상 있으면 임의 선택하지 않고 실패 처리.
- 후속: 고객별 특수 컬럼은 실제 외주 요구가 들어왔을 때 설정형 매핑으로 확장.

## 2026-08-21 — 10,000행을 첫 성능 스모크 기준으로 채택
- 이유: 소형 외주 Excel 자동화에서 체감 가능한 규모를 최소한 검증하기 위함.
- 방식: 100개 부서 + 10,000명 직원 더미 데이터를 생성해 전체 검증 및 결과 Excel 생성을 수행.
- CI 기준: 20초 이내 완료 + 총건수/정상건수/오류건수 일치.
- 결과: GitHub Actions Linux runner에서 통과.

## 2026-08-21 — Windows EXE는 PR 단계에서 실제 빌드/실행 검증
- 이유: 머지 후에만 EXE 오류를 발견하는 것을 방지.
- 방식: Windows runner에서 CLI/GUI 두 EXE를 PyInstaller로 빌드 후 각각 스모크 테스트.
- 결과: 두 EXE 빌드 및 스모크 성공, Artifact 업로드 성공.

## 2026-08-21 — Plan Drift 기록: CI import path
- 발생 지점: 10,000행 performance smoke 최초 CI 실행.
- 문제: `python scripts/performance_smoke.py` 실행 시 repository root가 module path에 없어 `src` import 실패.
- 변경: `python -m scripts.performance_smoke` 방식으로 실행.
- 영향: 기능/설계 변경 없음. CI 실행 방식만 수정.

## 2026-08-21 — Plan Drift 기록: Windows CLI console encoding
- 발생 지점: Windows EXE 최초 CLI `--help` 스모크.
- 문제: GitHub Windows runner의 cp1252 콘솔이 한글 argparse 설명을 출력하지 못해 UnicodeEncodeError 발생.
- 판단: EXE 빌드는 정상이며 콘솔 출력 경계 문제.
- 변경: CLI 도움말/완료 메시지는 ASCII-safe English로 유지하고, 사용자용 GUI/결과 Excel의 한국어 UX는 그대로 유지.
- 영향: 일반 사용자 GUI에는 변화 없음. CLI의 이식성이 좋아짐.

## 2026-08-21 — 첫 MVP의 확장 중지선 확정
- 현재 완료 범위: 파일 선택 → 자동 컬럼 인식 → 매칭/검증 → 결과 Excel → GUI/CLI EXE.
- 지금 추가하지 않음: CSV 범용화, 사용자 정의 컬럼 매핑 UI, DB, API, 웹앱, 설치프로그램, 코드서명.
- 이유: 첫 외주를 받기 전에 기능을 무한 확장하면 작은 상품이라는 목표를 잃음.
- 원칙: 실제 고객 요구가 확인된 기능만 후속으로 추가.
