from src.entity.find_blank_coords import find_blank_coords


def solver_step_a(grid: list[list[int]]) -> list[int]:
    """Step A — row-major 1-index blank coords then cell values (int[6] for G1)."""
    coords = find_blank_coords(grid)
    result: list[int] = []
    for row, col in coords:
        result.extend([row, col])
    for row, col in coords:
        result.append(grid[row - 1][col - 1])
    return result
