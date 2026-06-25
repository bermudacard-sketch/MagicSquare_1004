# MagicSquare_1004

4×4 마방진(Magic Square) **검증** 프로젝트입니다.  
1차 목표는 빈칸을 자동으로 푸는 것이 아니라, 후보 격자가 10줄(행 4 + 열 4 + 대각선 2) 합 **34**를 만족하는지 확인하는 것입니다.

## 도메인

| 항목 | 값 |
|------|-----|
| 격자 | 4×4 |
| 숫자 범위 | 1 ~ 16 (완성 격자에서 각 1회) |
| 빈칸 | `0` (부분 마방진, 2개) |
| 마법 상수 | 34 |
| 검증 대상 | 10선 — `R1`~`R4`, `C1`~`C4`, `D1`, `D2` |

## 예시 (완성 격자)

```
16   3   2  13
 5  10  11   8
 9   6   7  12
 4  15  14   1
```

## API — `validate_lines`

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": list[str],  # 예: ["R2", "C2"]
}
```

- `pass` — 빈칸 없음, 10선 합 모두 34
- `fail` — 빈칸 없으나 하나 이상의 선 합 ≠ 34
- `incomplete` — 격자에 `0` 포함 (`failed_lines`는 `[]`)

## 테스트

```powershell
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## 진행 상태

- [x] Test Harness (`pyproject.toml`, `src/validate_lines.py` 스텁)
- [x] TDD RED — T-02 (`validate_lines` R2·C2 fail)
- [ ] GREEN — `validate_lines` 구현
- [ ] Entity — `find_blank_coords` (D-LOC-01)
- [ ] Solver / UI — Out of Scope (세션 3)

## 문서

| NN | Report | Transcript | 주제 |
|----|--------|------------|------|
| 01 | [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | — | Mom Test·문제 정의 |
| 02 | [Report/02.REPORT.md](Report/02.REPORT.md) | [Prompting/02.Export-Transcript.md](Prompting/02.Export-Transcript.md) | 세션 3 Harness·TDD RED |
| 03 | [Report/03.REPORT.md](Report/03.REPORT.md) | [Prompting/03.Export-Transcript.md](Prompting/03.Export-Transcript.md) | Entity D-LOC-01 RED Test Plan · README 갱신 |
| 04 | [Report/04.REPORT.md](Report/04.REPORT.md) | [Prompting/04.Export-Transcript.md](Prompting/04.Export-Transcript.md) | Entity D-LOC-01 RED Skeleton |
| 05 | [Report/05.REPORT.md](Report/05.REPORT.md) | [Prompting/05.Export-Transcript.md](Prompting/05.Export-Transcript.md) | Entity D-LOC-01 GREEN |

- 요구사항 SSOT: [docs/PRD.md](docs/PRD.md)
