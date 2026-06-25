from src.entity.find_blank_coords import find_blank_coords
from tests._approval import GOLDEN_DIR, assert_matches_golden, format_coord_list


# D-LOC-01
def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: G1 격자 (0이 2개, row-major)
    # When: find_blank_coords(grid_g1) 호출
    actual = format_coord_list(find_blank_coords(grid_g1))
    golden = GOLDEN_DIR / "d_loc_01_g1_blank_coords.approved.txt"
    # Then: golden matched
    assert_matches_golden(actual, golden)
