from pathlib import Path

from openpyxl import Workbook, load_workbook

from src.validate_excel import validate


def _make_book(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    for row in rows:
        ws.append(row)
    wb.save(path)


def test_golden_cases(tmp_path: Path) -> None:
    employees = tmp_path / "employees.xlsx"
    departments = tmp_path / "departments.xlsx"
    output = tmp_path / "result.xlsx"

    _make_book(
        employees,
        ["EmployeeID", "Name", "DepartmentCode", "Email"],
        [
            ["E1", "정상", "D1", "ok@example.com"],
            ["E2", "미등록", "D9", "bad@example.com"],
            ["E3", "누락", "", "missing@example.com"],
            ["E4", "중복1", "D1", "dup1@example.com"],
            ["E4", "중복2", "D1", "dup2@example.com"],
        ],
    )
    _make_book(
        departments,
        ["DepartmentCode", "DepartmentName", "Manager"],
        [["D1", "개발", "김팀장"]],
    )

    summary = validate(employees, departments, output)
    assert summary == {"total": 5, "ok": 1, "error": 4}

    wb = load_workbook(output, data_only=True)
    result = wb["Result"]
    statuses = [result.cell(row=i, column=7).value for i in range(2, 7)]
    assert statuses == ["OK", "UNKNOWN_DEPT", "MISSING_DEPT_CODE", "DUPLICATE_ID", "DUPLICATE_ID"]


def test_korean_column_aliases(tmp_path: Path) -> None:
    employees = tmp_path / "employees-ko.xlsx"
    departments = tmp_path / "departments-ko.xlsx"
    output = tmp_path / "result-ko.xlsx"

    _make_book(
        employees,
        ["사번", "이름", "부서코드", "이메일"],
        [["E1", "홍길동", "D1", "hong@example.com"]],
    )
    _make_book(
        departments,
        ["부서 코드", "부서명", "부서장"],
        [["D1", "개발팀", "김팀장"]],
    )

    summary = validate(employees, departments, output)
    assert summary == {"total": 1, "ok": 1, "error": 0}

    wb = load_workbook(output, data_only=True)
    row = [wb["Result"].cell(row=2, column=i).value for i in range(1, 8)]
    assert row == ["E1", "홍길동", "D1", "개발팀", "김팀장", "hong@example.com", "OK"]


def test_required_column_validation(tmp_path: Path) -> None:
    employees = tmp_path / "employees.xlsx"
    departments = tmp_path / "departments.xlsx"
    _make_book(employees, ["Name"], [["홍길동"]])
    _make_book(departments, ["DepartmentCode", "DepartmentName", "Manager"], [["D1", "개발", "김팀장"]])

    try:
        validate(employees, departments, tmp_path / "out.xlsx")
    except ValueError as exc:
        assert "Missing required columns" in str(exc)
    else:
        raise AssertionError("Expected missing-column validation to fail")


def test_duplicate_alias_mapping_is_rejected(tmp_path: Path) -> None:
    employees = tmp_path / "employees.xlsx"
    departments = tmp_path / "departments.xlsx"
    _make_book(
        employees,
        ["EmployeeID", "사번", "Name", "DepartmentCode", "Email"],
        [["E1", "E1", "홍길동", "D1", "hong@example.com"]],
    )
    _make_book(
        departments,
        ["DepartmentCode", "DepartmentName", "Manager"],
        [["D1", "개발", "김팀장"]],
    )

    try:
        validate(employees, departments, tmp_path / "out.xlsx")
    except ValueError as exc:
        assert "Duplicate mapped column: EmployeeID" in str(exc)
    else:
        raise AssertionError("Expected duplicate alias mapping to fail")
