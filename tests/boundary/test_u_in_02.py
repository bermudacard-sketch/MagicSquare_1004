from src.boundary.input_handler import ERROR_INVALID_VALUE, InputHandler


# U-IN-02
def test_u_in_02_cell_value_17_returns_e002():
    handler = InputHandler()
    grid = [
        [17, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    result = handler.validate(grid)
    assert result["error_code"] == ERROR_INVALID_VALUE
