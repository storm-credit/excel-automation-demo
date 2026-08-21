# CLAUDE.md — Excel Automation Demo

## PROJECT GOAL
외주 포트폴리오용으로, 비개발자 고객도 이해하고 바로 실행할 수 있는 소형 Excel/CSV 자동화 샘플을 만든다.

현재 대표 시나리오:
`직원목록 + 부서마스터 → 자동 매칭 → 중복/누락/미등록 코드 검출 → 결과/오류/요약 엑셀 생성`

## MINIMUM ACTION AGENT OS ADOPTION
이 프로젝트는 `storm-credit/minimum-action-agent-os`를 공통 작업 방법론의 정본으로 사용한다.

비단순 작업 전에 GitHub에서 다음을 우선 읽는다.
1. `minimum-action-agent-os/CLAUDE.md`
2. `minimum-action-agent-os/AGENT_OS_SPEC.md`
3. `minimum-action-agent-os/rules/local-action-space.md`
4. `minimum-action-agent-os/rules/agent-vs-skill.md`
5. `minimum-action-agent-os/rules/anti-patterns.md`
6. 현재 프로젝트의 `docs/CURRENT_STATUS.md`
7. 현재 프로젝트의 `docs/DECISIONS.md`
8. 현재 프로젝트의 `docs/ACCEPTANCE_CRITERIA.md`

공통 OS는 **어떻게 일할지**를 규정하고, 이 저장소는 **무엇을 만들지**를 규정한다.
도메인 내용은 이 프로젝트 정본이 우선하며, 작업 방법은 OS를 따른다.

중요:
- `<= 5`는 전체 Agent 수 제한이 아니라 한 reasoning node의 직접 선택 가능한 action에 대한 기본 설계 목표다.
- 단순 작업에는 불필요한 Agent/Skill/단계를 기계적으로 추가하지 않는다.
- 구현 전 맹점/함정 확인은 작업 위험이 있을 때 사용한다.
- 4안 비교는 실제 디자인 선택지가 열려 있을 때만 한다.
- Builder와 Critic은 필요한 경우 독립적으로 분리한다.
- 계획이 달라지면 `docs/DECISIONS.md`에 이유와 영향 범위를 기록한다.

## PROJECT-SPECIFIC NON-NEGOTIABLES
1. 회사 코드, 회사 문서, 고객사 데이터, 실데이터를 사용하지 않는다.
2. 모든 샘플 데이터는 공개 가능하거나 더미 데이터여야 한다.
3. 자동화의 핵심 계산과 검증은 재현 가능해야 한다.
4. 포트폴리오에서는 구현된 것과 기획 중인 것을 명확히 구분한다.
5. 입력 파일을 덮어쓰지 않는다.
6. 필수 컬럼 누락이나 잘못된 데이터는 조용히 무시하지 말고 오류로 드러낸다.

## PROJECT SOURCE OF TRUTH
우선순위:
1. 이 `CLAUDE.md`의 프로젝트 고유 규칙
2. `docs/CURRENT_STATUS.md`
3. `docs/DECISIONS.md`
4. `docs/ACCEPTANCE_CRITERIA.md`
5. 실제 코드 / 테스트 / GitHub Actions 결과

대화 전체를 정본으로 사용하지 않는다.

## SUCCESS CONDITIONS
- 비개발자가 README만 보고 목적을 이해할 수 있다.
- 샘플 입력 → 결과 파일 생성 흐름이 재현된다.
- 중복 ID, 코드 누락, 미등록 코드가 검출된다.
- 정상/오류 수가 요약된다.
- 모든 샘플 데이터는 더미 데이터다.
- 오류 원인을 확인할 수 있다.
- 외주 설명에 사용할 수 있는 Before/After가 명확하다.

## STOP CONDITIONS
다음 중 하나면 구현을 멈추고 상태를 기록한다.
- 범위가 소형 자동화를 넘어 대형 업무시스템 구축으로 변함
- 실제 회사/고객 데이터가 필요해짐
- 외부 서비스 약관/권한 우회가 필요함
- 테스트로 핵심 동작을 검증할 수 없음
- 원래 계획과 큰 차이가 생겼는데 결정 기록이 없음

## DEFINITION OF DONE
- 실행 또는 사용 방법 문서화
- Golden Case 테스트 통과
- GitHub Actions CI 통과
- 오류 사례 포함
- 민감정보 없음
- README 최신화
- CURRENT_STATUS / DECISIONS 동기화
