import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def format_coord_list(coords: list[tuple[int, int]]) -> str:
    """1-index (row,col) per line, row-major."""
    return "\n".join(f"{r},{c}" for r, c in coords) + ("\n" if coords else "")


def assert_matches_golden(actual: str, golden_path: Path) -> None:
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8", newline="\n")
        return
    expected = golden_path.read_text(encoding="utf-8")
    assert actual == expected, (
        f"Golden mismatch:\n{golden_path}\n--- diff ---\n{_diff_summary(expected, actual)}"
    )


def _diff_summary(expected: str, actual: str) -> str:
    if expected == actual:
        return "(identical)"
    return f"expected ({len(expected)} chars) vs actual ({len(actual)} chars)"
