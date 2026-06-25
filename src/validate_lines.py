from src.entity.constants import BLANK_CELL, GRID_SIZE, MAGIC_CONSTANT

_LINE_IDS = (
    "R1",
    "R2",
    "R3",
    "R4",
    "C1",
    "C2",
    "C3",
    "C4",
    "D1",
    "D2",
)


def _collect_failed_line_ids(grid: list[list[int]]) -> list[str]:
    totals: list[int] = []
    for row in range(GRID_SIZE):
        totals.append(sum(grid[row][col] for col in range(GRID_SIZE)))
    for col in range(GRID_SIZE):
        totals.append(sum(grid[row][col] for row in range(GRID_SIZE)))
    totals.append(sum(grid[i][i] for i in range(GRID_SIZE)))
    totals.append(sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)))
    return [
        line_id
        for line_id, total in zip(_LINE_IDS, totals, strict=True)
        if total != MAGIC_CONSTANT
    ]


def validate_lines(grid: list[list[int]]) -> dict[str, str | list[str]]:
    for row in grid:
        for cell in row:
            if cell == BLANK_CELL:
                return {"status": "incomplete", "failed_lines": []}

    failed_lines = _collect_failed_line_ids(grid)
    if failed_lines:
        return {"status": "fail", "failed_lines": failed_lines}
    return {"status": "pass", "failed_lines": []}
