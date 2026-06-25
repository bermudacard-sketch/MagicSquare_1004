from src.validate_lines import validate_lines


# T-02 — R2·C2 교차 셀 grid[1][1] 10→11 → 두 선 합 35
def test_t02_r2_and_c2_fail_when_intersection_cell_wrong():
    grid = [
        [16, 3, 2, 13],
        [5, 11, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    result = validate_lines(grid)
    assert result["status"] == "fail"
    assert "R2" in result["failed_lines"]
    assert "C2" in result["failed_lines"]
