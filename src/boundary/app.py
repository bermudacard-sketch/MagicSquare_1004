"""MagicSquare_1004 — G1 격자 최소 GUI 데모 (tkinter)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.boundary.grid_g1 import GRID_G1
from src.boundary.input_handler import (
    ERROR_INVALID_VALUE,
    ERROR_NONE_GRID,
    InputHandler,
)
from src.entity.constants import BLANK_CELL, GRID_SIZE
from src.entity.find_blank_coords import find_blank_coords
from src.validate_lines import validate_lines

_ERROR_MESSAGES = {
    ERROR_NONE_GRID: "입력 오류 (E003): 격자가 없습니다.",
    ERROR_INVALID_VALUE: "입력 오류 (E002): 1~16 또는 빈칸(0)만 허용됩니다.",
}


class MagicSquareDemoApp:
    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._root.title("MagicSquare_1004 — G1 검증 데모")
        self._input_handler = InputHandler()
        self._blank_entries: dict[tuple[int, int], ttk.Entry] = {}
        self._status_var = tk.StringVar(value="status: —")
        self._failed_var = tk.StringVar(value="failed_lines: —")

        self._build_ui()

    def _build_ui(self) -> None:
        main = ttk.Frame(self._root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        ttk.Label(main, text="G1 부분 마방진 — 빈칸 2칸만 입력 후 [검증]", font=("Segoe UI", 11, "bold")).grid(
            row=0, column=0, columnspan=4, pady=(0, 8)
        )

        grid_frame = ttk.Frame(main)
        grid_frame.grid(row=1, column=0, columnspan=4, pady=4)

        blank_coords_0 = {(r - 1, c - 1) for r, c in find_blank_coords(GRID_G1)}

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = GRID_G1[row][col]
                if (row, col) in blank_coords_0:
                    entry = ttk.Entry(grid_frame, width=4, justify="center")
                    entry.grid(row=row, column=col, padx=2, pady=2)
                    self._blank_entries[(row, col)] = entry
                else:
                    ttk.Label(
                        grid_frame,
                        text=str(value),
                        width=4,
                        anchor="center",
                        relief="groove",
                        padding=4,
                    ).grid(row=row, column=col, padx=2, pady=2)

        ttk.Button(main, text="검증", command=self._on_validate).grid(row=2, column=0, columnspan=4, pady=12)

        ttk.Label(main, textvariable=self._status_var, font=("Segoe UI", 10)).grid(
            row=3, column=0, columnspan=4, sticky="w"
        )
        ttk.Label(main, textvariable=self._failed_var, font=("Segoe UI", 10), wraplength=320).grid(
            row=4, column=0, columnspan=4, sticky="w", pady=(4, 0)
        )

    def _read_grid(self) -> list[list[int]] | None:
        grid = [row[:] for row in GRID_G1]
        for (row, col), entry in self._blank_entries.items():
            text = entry.get().strip()
            if not text:
                grid[row][col] = BLANK_CELL
                continue
            try:
                grid[row][col] = int(text)
            except ValueError:
                return None
        return grid

    def _on_validate(self) -> None:
        grid = self._read_grid()
        if grid is None:
            self._status_var.set("status: input_error")
            self._failed_var.set(_ERROR_MESSAGES[ERROR_INVALID_VALUE])
            return

        input_result = self._input_handler.validate(grid)
        if input_result["error_code"] is not None:
            code = input_result["error_code"]
            self._status_var.set(f"status: input_error ({code})")
            self._failed_var.set(_ERROR_MESSAGES.get(code, f"error_code={code}"))
            return

        result = validate_lines(grid)
        status = result["status"]
        failed = result["failed_lines"]
        self._status_var.set(f"status: {status}")
        if failed:
            self._failed_var.set(f"failed_lines: {', '.join(failed)}")
        else:
            self._failed_var.set("failed_lines: (없음)")


def main() -> None:
    root = tk.Tk()
    MagicSquareDemoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
