from src.entity.solver_step_a import solver_step_a


# D-SOL-01
def test_d_sol_01_step_a_success(grid_g1):
    # Given: G1 격자 (빈칸 2개)
    # When: solver_step_a(grid_g1) 호출
    result = solver_step_a(grid_g1)
    # Then: int[6] — 1-index coords row-major + 현재 셀 값
    assert result == [2, 3, 4, 4, 0, 0]
