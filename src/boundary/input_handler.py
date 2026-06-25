from typing import TypedDict

from src.entity.constants import BLANK_CELL, MAX_CELL_VALUE

ERROR_INVALID_VALUE = "E002"
ERROR_NONE_GRID = "E003"


class InputResult(TypedDict):
    error_code: str | None


class InputHandler:
    def validate(self, grid: list[list[int]] | None) -> InputResult:
        if grid is None:
            return {"error_code": ERROR_NONE_GRID}
        for row in grid:
            for cell in row:
                if cell != BLANK_CELL and not 1 <= cell <= MAX_CELL_VALUE:
                    return {"error_code": ERROR_INVALID_VALUE}
        return {"error_code": None}
