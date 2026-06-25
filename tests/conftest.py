import pytest

from src.entity.grids import GRID_G1


@pytest.fixture
def grid_g1() -> list[list[int]]:
    """G1 — 빈칸 2개, row-major."""
    return [row[:] for row in GRID_G1]
