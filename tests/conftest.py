import pytest

from src.entity.constants import BLANK_CELL


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1 — 빈칸 2개, row-major."""
    grid = [
        [16, 3, 2, 13],
        [5, 10, BLANK_CELL, 8],
        [9, 6, 7, 12],
        [4, 15, 14, BLANK_CELL],
    ]
    return grid
