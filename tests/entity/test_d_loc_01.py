import pytest

from src.entity.find_blank_coords import find_blank_coords


# D-LOC-01
def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개, row-major)
    # When: find_blank_coords(grid_g1) 호출 예정
    _ = find_blank_coords
    # Then:
    pytest.fail("RED: D-LOC-01 — 1-index row-major [(2,3), (4,4)]")
