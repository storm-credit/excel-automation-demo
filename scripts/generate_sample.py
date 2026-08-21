from pathlib import Path
from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample"
SAMPLE.mkdir(exist_ok=True)


def save_book(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    for row in rows:
        ws.append(row)
    wb.save(path)


save_book(
    SAMPLE / "employees.xlsx",
    ["EmployeeID", "Name", "DepartmentCode", "Email"],
    [
        ["E1001", "김민수", "D001", "minsu@example.com"],
        ["E1002", "이서연", "D002", "seoyeon@example.com"],
        ["E1003", "한유진", "D999", "yujin@example.com"],
        ["E1004", "강도윤", "", "doyoon@example.com"],
        ["E1005", "최지우", "D001", "jiwoo@example.com"],
        ["E1005", "최지우(중복)", "D001", "jiwoo2@example.com"],
    ],
)

save_book(
    SAMPLE / "departments.xlsx",
    ["DepartmentCode", "DepartmentName", "Manager"],
    [
        ["D001", "플랫폼개발", "김팀장"],
        ["D002", "서비스개발", "이팀장"],
    ],
)

print(f"샘플 생성 완료: {SAMPLE}")
