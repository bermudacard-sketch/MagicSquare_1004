from src.boundary.input_handler import ERROR_NONE_GRID, InputHandler


# U-IN-01
def test_u_in_01_none_grid_returns_e003():
    handler = InputHandler()
    result = handler.validate(None)
    assert result["error_code"] == ERROR_NONE_GRID
