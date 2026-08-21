# Testing Rules
Golden cases:
1. 정상 직원 + 정상 부서코드 → OK
2. 중복 EmployeeID → DUPLICATE_ID
3. 빈 DepartmentCode → MISSING_DEPT_CODE
4. 존재하지 않는 DepartmentCode → UNKNOWN_DEPT

Release 전에 위 4개를 반드시 확인한다.
