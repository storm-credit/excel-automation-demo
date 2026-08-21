# CLAUDE.md — Excel Automation Demo

## PROJECT GOAL
외주 포트폴리오용으로, 비개발자 고객도 이해하고 바로 실행할 수 있는 소형 Excel/CSV 자동화 샘플을 만든다.

현재 대표 시나리오:
`직원목록 + 부서마스터 → 자동 매칭 → 중복/누락/미등록 코드 검출 → 결과/오류/요약 엑셀 생성`

## NON-NEGOTIABLE RULES
1. 회사 코드, 회사 문서, 고객사 데이터, 실데이터를 사용하지 않는다.
2. 모든 샘플 데이터는 공개 가능하거나 더미 데이터여야 한다.
3. 구현 전 반드시 `Blindspot Scan → Trap Check → 4안 비교`를 수행한다.
4. 사용자의 의도, 주사용자, 기대 출력, 사용 환경이 불명확하면 질문한다.
5. 본보기 코드는 공개 GitHub/공식 문서에서 구조와 작동 원리만 참고하고 그대로 복제하지 않는다.
6. 막히거나 원래 계획과 달라지면 `docs/DECISIONS.md`에 이유와 영향 범위를 기록한다.
7. 필요 없는 Tool, Context, 권한은 주지 않는다.
8. Critic은 Builder의 reasoning/정당화를 보지 않고 결과물·요구사항·테스트·수용기준만 본다.
9. 자동화의 핵심 계산과 검증은 재현 가능해야 한다.
10. 포트폴리오에서는 구현된 것과 기획 중인 것을 명확히 구분한다.

## SOURCE OF TRUTH
우선순위:
1. 이 `CLAUDE.md`
2. `docs/CURRENT_STATUS.md`
3. `docs/DECISIONS.md`
4. `docs/ACCEPTANCE_CRITERIA.md`
5. 실제 코드/테스트/샘플 산출물

대화 전체를 기억으로 사용하지 않는다.
정본 문서에 기록된 Goal / Current State / Decisions / Constraints / Open Issues / Next Action만 재주입한다.

## WORKFLOW
USER INTENT
→ Blindspot Scan
→ Anti-pattern / Trap Preflight
→ 사용자 인터뷰가 필요한지 판정
→ 디자인 시안 4개 비교
→ Task Decomposition
→ Tool Budget / Context Budget
→ 구현
→ 독립 Critic
→ 테스트 / Golden Case
→ Release Gate
→ Decision Log
→ Current Status 업데이트

## DESIGN OPTIONS
새 기능이나 UX를 만들 때 한 가지 안만 바로 구현하지 않는다.
가능하면 한눈에 비교되는 4개 안을 만든다.

예시:
- A. 가장 단순한 엑셀 단독형
- B. Python 실행형
- C. 드래그앤드롭 웹형
- D. 폴더 감시 자동처리형

평가 기준:
- 고객 이해 난이도
- 설치 난이도
- 작업시간
- 오류 위험
- 유지보수성
- 외주 상품화 가능성

## META PROMPTING
AI에게 작업 프롬프트를 만들게 할 때:

1. Context Dump
   - 현재 목표, 입력, 제약, 정본, 실패사례를 제공한다.
2. Prompt Distillation
   - 불필요한 문맥을 제거하고 목표·제약·성공조건·중지조건만 남긴다.
3. Result Verification
   - 산출물이 요구사항과 Acceptance Criteria를 충족했는지 독립적으로 검사한다.

프롬프트 작성 전:
"지금까지 제공된 컨텍스트를 기준으로 좋은 작업 프롬프트를 만들기 위해 부족한 정보가 있다면 질문하라."

## SUCCESS CONDITIONS
- 비개발자가 README만 보고 목적을 이해할 수 있다.
- 샘플 입력 → 결과 파일 생성 흐름이 재현된다.
- 중복 ID, 코드 누락, 미등록 코드가 검출된다.
- 정상/오류 수가 요약된다.
- 모든 데이터는 더미 데이터다.
- 오류가 나면 원인을 확인할 수 있다.
- 외주 설명에 사용할 수 있는 Before/After가 명확하다.

## STOP CONDITIONS
다음 중 하나면 구현을 멈추고 보고한다.
- 요구사항이 현재 범위를 넘어 대형 업무시스템 구축으로 변함
- 실제 회사/고객 데이터가 필요해짐
- 외부 서비스 약관/권한 우회가 필요함
- 테스트로 핵심 동작을 검증할 수 없음
- 설계 4안 비교 후 구현 가치가 낮다고 판정됨
- 원래 계획과 큰 차이가 생겼는데 결정 기록이 없음

## MINIMUM NECESSARY AGENCY
1. Least Tool
2. Least Context
3. Least Authority
4. Isolate by Default
5. Independent Critique
6. Programmatic Control

숫자 '도구 5개'를 절대 규칙으로 사용하지 않는다.
필요 없는 도구를 제거하고 실패 경계가 실제로 분리될 때만 Agent를 분리한다.

## DEFINITION OF DONE
- 샘플 입력 포함
- 실행 또는 사용 방법 문서화
- 기대 결과 확인
- 오류 사례 포함
- 민감정보 없음
- README 최신화
- CURRENT_STATUS / DECISIONS 동기화
