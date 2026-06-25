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
python -m src.boundary.app
```

## 진행 상태

- [x] Test Harness (`pyproject.toml`, `validate_lines`, pytest)
- [x] Track B — T-02 GREEN, D-LOC-01 GREEN + Golden, D-SOL-01 GREEN
- [x] Track A — U-IN-01/02 (`InputHandler`)
- [x] G1 GUI 데모 (`python -m src.boundary.app`)
- [x] REFACTOR — `/refactor-safe` 후보 #1 (G1 SSOT → `src/entity/grids.py`)

## ARRR 실습 순서

| ARRR | TDD | Command |
|------|-----|---------|
| Ask | RED 설계 | `/red-test-plan` |
| Ask | RED 스켈레톤 | `/red-skeleton` |
| Ask | RED assert | `/tdd-red` |
| Respond | GREEN | `/green-minimal` |
| Respond | Golden | `/golden-master` |
| Refine | 스멜 탐지 | `/refactor-smell` |
| Refine | Safe Refactor | `/refactor-safe` |

## REFACTOR To-Do

`/refactor-smell` (Phase: refactor · Scope: `src/` `tests/` · Track: Logic+UI) 결과.  
전제: `python -m pytest tests/ -v` → 전부 PASS.

**Change Budget:** 파일 ≤3 · 클래스 ≤1 · 메서드 ≤3

### 스멜 표

| P | 스멜 | 위치 (파일:함수) | 근거 | Budget 내 리팩터 후보 |
|---|------|------------------|------|------------------------|
| ~~P1~~ | ~~Duplicated Code~~ | ~~G1 SSOT~~ | **완료** — `src/entity/grids.py:GRID_G1` SSOT | — |
| P1 | Duplicated Code | `src/validate_lines.py:_line_totals` | 행·열·주대각·부대각 `sum` 패턴 4회 반복 | `_row_totals` / `_col_totals` / `_diagonal_totals` private 추출 (파일 1, 메서드 ≤2) |
| P1 | Long Method | `src/boundary/app.py:MagicSquareDemoApp._build_ui` | 격자 UI + 빈칸 판별 + 결과 패널 한 메서드 (~38줄) | `_build_grid_frame`, `_build_result_panel` 분리 (파일 1, 메서드 +2) |
| P2 | Mysterious Name | `src/boundary/app.py:_build_ui` — `blank_coords_0` | 1-index → 0-index 변환 의도 불명 | `blank_cells_zero_indexed` 등 rename |
| P2 | Duplicated Code | `src/entity/solver_step_a.py:solver_step_a` | `coords` 2회 순회 | 단일 루프로 좌표·값 수집 |
| P2 | Feature Envy | `src/boundary/app.py:_read_grid` | Boundary가 격자 복사·파싱 직접 수행 | `GridReader` boundary 헬퍼 추출 |
| — | Magic Number | `src/` 로직 | `34`/`4`/`16`은 `constants.py`만 — **P0 없음** | — |
| — | ECB 위반 | `src/entity/*` | Entity→Boundary import 없음, E001~E005 emit 없음 — **P0 없음** | — |

**P0:** 정적 스캔 기준 없음.

### `/refactor-safe` 후보

| # | 후보 | P | 유형 | 예상 변경 | Budget |
|---|------|---|------|-----------|--------|
| ~~1~~ | ~~G1 격자 SSOT 단일화~~ | P1 | Duplicated Code | **완료** — `src/entity/grids.py` + boundary re-export + conftest import | — |
| 2 | 10선 합산 헬퍼 추출 | P1 | Duplicated Code | `validate_lines.py` — `_line_totals` 분리, API·`failed_lines` 불변 | 파일 1 · 메서드 +2 |
| 3 | GUI `_build_ui` 분리 | P1 | Long Method | `app.py` — grid/result 패널 메서드 추출 | 파일 1 · 클래스 1 · 메서드 +2 |

### 다음

**P0 없음** → 후보 **#2 (10선 합산 헬퍼)** 부터 `/refactor-safe` 실행.

```text
/refactor-safe — #2 P1 Duplicated Code — validate_lines 10선 합산 헬퍼 추출
```

## 후속 (예정)

- [ ] D-SOL-01 `/golden-master` — `d_sol_01_g1_step_a.approved.txt`
- [ ] T-01, incomplete, T-03 등 추가 RED
- [ ] REFACTOR 후보 #2, #3 순차 처리 (후보 #1 G1 SSOT 완료)

## 문서

| NN | Report | Transcript | 주제 |
|----|--------|------------|------|
| 01 | [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | — | Mom Test·문제 정의 |
| 02 | [Report/02.REPORT.md](Report/02.REPORT.md) | [Prompting/02.Export-Transcript.md](Prompting/02.Export-Transcript.md) | 세션 3 Harness·TDD RED |
| 03 | [Report/03.REPORT.md](Report/03.REPORT.md) | [Prompting/03.Export-Transcript.md](Prompting/03.Export-Transcript.md) | Entity D-LOC-01 RED Test Plan · README 갱신 |
| 04 | [Report/04.REPORT.md](Report/04.REPORT.md) | [Prompting/04.Export-Transcript.md](Prompting/04.Export-Transcript.md) | Entity D-LOC-01 RED Skeleton |
| 05 | [Report/05.REPORT.md](Report/05.REPORT.md) | [Prompting/05.Export-Transcript.md](Prompting/05.Export-Transcript.md) | Entity D-LOC-01 GREEN |
| 06 | [Report/06.REPORT.md](Report/06.REPORT.md) | [Prompting/06.Export-Transcript.md](Prompting/06.Export-Transcript.md) | Dual-Track PASS · Golden · G1 GUI 데모 |
| 07 | [Report/07.REPORT.md](Report/07.REPORT.md) | [Prompting/07.Export-Transcript.md](Prompting/07.Export-Transcript.md) | REFACTOR Smell · README To-Do |
| 08 | [Report/08.REPORT.md](Report/08.REPORT.md) | [Prompting/08.Export-Transcript.md](Prompting/08.Export-Transcript.md) | REFACTOR Safe · G1 SSOT 단일화 |

- 요구사항 SSOT: [docs/PRD.md](docs/PRD.md)
