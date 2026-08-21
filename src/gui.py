from __future__ import annotations

import os
import threading
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from src.validate_excel import validate


class ExcelValidatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Excel 업무 자동 검증")
        self.root.geometry("760x500")
        self.root.minsize(680, 460)

        self.employee_path = tk.StringVar()
        self.department_path = tk.StringVar()
        self.output_path = tk.StringVar(value=str(Path.cwd() / "result.xlsx"))
        self.status_text = tk.StringVar(value="파일 2개를 선택한 뒤 검증을 실행하세요.")
        self.summary_text = tk.StringVar(value="")
        self.last_output: Path | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=24)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Excel 업무 자동 검증",
            font=("Malgun Gothic", 20, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            container,
            text="직원목록과 부서마스터를 자동 매칭하고 중복·누락·미등록 코드를 찾아 결과 Excel을 만듭니다.",
            wraplength=700,
        ).pack(anchor="w", pady=(6, 22))

        self._file_row(container, "1. 직원 목록", self.employee_path, self._choose_employee)
        self._file_row(container, "2. 부서 마스터", self.department_path, self._choose_department)
        self._file_row(container, "3. 결과 저장 위치", self.output_path, self._choose_output, save=True)

        action_frame = ttk.Frame(container)
        action_frame.pack(fill="x", pady=(22, 8))

        self.run_button = ttk.Button(action_frame, text="검증 실행", command=self._start_validation)
        self.run_button.pack(side="left")

        self.open_button = ttk.Button(
            action_frame,
            text="결과 파일 열기",
            command=self._open_result,
            state="disabled",
        )
        self.open_button.pack(side="left", padx=(10, 0))

        self.progress = ttk.Progressbar(action_frame, mode="indeterminate", length=180)
        self.progress.pack(side="right")

        status_box = ttk.LabelFrame(container, text="처리 결과", padding=16)
        status_box.pack(fill="both", expand=True, pady=(16, 0))

        ttk.Label(status_box, textvariable=self.status_text, wraplength=660).pack(anchor="w")
        ttk.Label(
            status_box,
            textvariable=self.summary_text,
            font=("Malgun Gothic", 13, "bold"),
        ).pack(anchor="w", pady=(14, 0))

        ttk.Label(
            status_box,
            text=(
                "지원 컬럼 예: EmployeeID/사번, Name/이름, DepartmentCode/부서코드, "
                "Email/이메일, DepartmentName/부서명, Manager/부서장"
            ),
            wraplength=660,
        ).pack(anchor="w", pady=(18, 0))

    def _file_row(
        self,
        parent: ttk.Frame,
        label: str,
        variable: tk.StringVar,
        command,
        save: bool = False,
    ) -> None:
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=7)
        ttk.Label(frame, text=label, width=18).pack(side="left")
        ttk.Entry(frame, textvariable=variable).pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(frame, text="저장 위치" if save else "파일 선택", command=command).pack(side="right")

    def _choose_employee(self) -> None:
        path = filedialog.askopenfilename(
            title="직원 목록 Excel 선택",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )
        if path:
            self.employee_path.set(path)
            if not self.output_path.get().strip():
                self.output_path.set(str(Path(path).with_name("result.xlsx")))

    def _choose_department(self) -> None:
        path = filedialog.askopenfilename(
            title="부서 마스터 Excel 선택",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        )
        if path:
            self.department_path.set(path)

    def _choose_output(self) -> None:
        path = filedialog.asksaveasfilename(
            title="결과 Excel 저장 위치",
            defaultextension=".xlsx",
            initialfile="result.xlsx",
            filetypes=[("Excel files", "*.xlsx")],
        )
        if path:
            self.output_path.set(path)

    def _start_validation(self) -> None:
        employees = Path(self.employee_path.get().strip())
        departments = Path(self.department_path.get().strip())
        output = Path(self.output_path.get().strip())

        if not self.employee_path.get().strip() or not employees.is_file():
            messagebox.showwarning("입력 확인", "직원 목록 Excel 파일을 선택해 주세요.")
            return
        if not self.department_path.get().strip() or not departments.is_file():
            messagebox.showwarning("입력 확인", "부서 마스터 Excel 파일을 선택해 주세요.")
            return
        if not self.output_path.get().strip():
            messagebox.showwarning("입력 확인", "결과 파일 저장 위치를 지정해 주세요.")
            return

        self.run_button.configure(state="disabled")
        self.open_button.configure(state="disabled")
        self.progress.start(10)
        self.status_text.set("검증 중입니다...")
        self.summary_text.set("")

        thread = threading.Thread(
            target=self._run_validation,
            args=(employees, departments, output),
            daemon=True,
        )
        thread.start()

    def _run_validation(self, employees: Path, departments: Path, output: Path) -> None:
        try:
            summary = validate(employees, departments, output)
        except Exception as exc:  # GUI boundary: surface a readable error to the user.
            self.root.after(0, lambda: self._finish_error(str(exc)))
            return
        self.root.after(0, lambda: self._finish_success(output, summary))

    def _finish_success(self, output: Path, summary: dict[str, int]) -> None:
        self.progress.stop()
        self.run_button.configure(state="normal")
        self.open_button.configure(state="normal")
        self.last_output = output
        self.status_text.set(f"완료: {output}")
        self.summary_text.set(
            f"전체 {summary['total']:,}건  ·  정상 {summary['ok']:,}건  ·  오류 {summary['error']:,}건"
        )
        messagebox.showinfo("검증 완료", "결과 Excel 파일을 생성했습니다.")

    def _finish_error(self, message: str) -> None:
        self.progress.stop()
        self.run_button.configure(state="normal")
        self.status_text.set("처리 중 오류가 발생했습니다.")
        self.summary_text.set("")
        messagebox.showerror("검증 실패", message)

    def _open_result(self) -> None:
        if self.last_output is None or not self.last_output.exists():
            messagebox.showwarning("결과 없음", "먼저 검증을 실행해 결과 파일을 생성해 주세요.")
            return

        if os.name == "nt":
            os.startfile(self.last_output)  # type: ignore[attr-defined]
        else:
            webbrowser.open(self.last_output.resolve().as_uri())


def main() -> None:
    root = tk.Tk()
    ExcelValidatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
