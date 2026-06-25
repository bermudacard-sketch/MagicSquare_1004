from src.entity.constants import BLANK_CELL


def find_blank_coords(grid: list[list[int]]) -> list[tuple[int, int]]:
    coords: list[tuple[int, int]] = []
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == BLANK_CELL:
                coords.append((row_idx + 1, col_idx + 1))
    return coords
