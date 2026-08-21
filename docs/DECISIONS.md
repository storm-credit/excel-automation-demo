# DECISIONS

## 2026-08-21 — 첫 외주 범위를 소형 자동화로 제한
- 이유: 본업 병행을 고려해 1~3일 내 끝낼 수 있는 작업부터 시작.
- 포함: Excel/CSV 병합, 검증, API 연동, 간단 데이터 가공.
- 제외: 대형 RAG/Agent 플랫폼 구축, 상주형, 전체 웹서비스 구축.

## 2026-08-21 — 첫 데모를 직원/부서 검증으로 선택
- 이유: 비개발자도 문제와 결과를 즉시 이해할 수 있음.
- 장점: 중복/누락/마스터 불일치 등 외주에서 흔한 문제를 보여줌.
- 위험: 실제 고객 파일의 컬럼 구조가 다를 수 있음.
- 대응: 이후 컬럼 매핑 설정을 옵션으로 확장.

## 2026-08-21 — Minimum Action Agent OS를 공통 작업 방법론 정본으로 채택
- 공통 방법론 정본: `storm-credit/minimum-action-agent-os`
- 이유: 프로젝트마다 동일한 preflight/blindspot/meta-prompting 규칙을 복제하면 Mega CLAUDE.md와 규칙 드리프트가 생김.
- 변경: 프로젝트 CLAUDE.md는 OS adoption + 프로젝트 고유 규칙만 유지.
- 변경: 프로젝트에 복제해둔 범용 `preflight`/`blindspot` skill 제거.
- 유지: Excel 고유 architecture/testing 규칙, 상태, 결정, acceptance criteria.
- Agent 정책: 현재 범위는 단순 소형 자동화이므로 별도 Agent를 늘리지 않고 direct work + 테스트/CI 검증을 사용.
- 영향: 이후 다른 외주 데모도 같은 OS를 참조하되 프로젝트별 진실은 각 저장소에 유지.
