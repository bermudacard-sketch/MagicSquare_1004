from src.entity.constants import BLANK_CELL

# G1 — 부분 마방진 학습 격자 SSOT (PRD §10.2 / §11)
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, BLANK_CELL, 8],
    [9, 6, 7, 12],
    [4, 15, 14, BLANK_CELL],
]
