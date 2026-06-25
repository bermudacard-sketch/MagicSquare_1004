# Golden Master — Approval Test 구축·검증

**GREEN PASS** 직후, 대상 Test ID에 **Golden Master(Approval Test)** 를 연결·검증한다.  
구현 변경이 허용된 출력과 **바이트 단위 일치**하는지 `tests/golden/*.approved.txt`로 고정한다.

추가 인자 없이 `/golden-master` 만으로 동작한다.  
대상 Test ID는 **직전 GREEN PASS**·**채팅**·**`docs/PRD.md`**에서 자동 추출한다.  
**추가 입력·질문 금지** — 부족하면 SSOT에서 추론하고 “추론 근거” 한 줄만 명시한다.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/green-minimal.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Phase` | `green` | Golden은 GREEN 산출물 고정 단계 |
| `Layer` | `entity` \| `boundary` | Logic → **`entity`** |
| `Track` | `Logic` \| `UI` | Boundary → `boundary` / `UI` |

이어서 **한국어**로 진행한다.

---

## 전제

- 대상 Test ID가 **pytest PASS** 상태여야 한다 (`/green-minimal` 완료 후).
- PASS 없이 `UPDATE_GOLDEN=1` 실행 **금지**.
- `src/` 로직 변경은 **하지 않는다** (Golden 연결·harness만). 구현 버그는 `/green-minimal`로 되돌림.

---

## 절차 (필수 순서)

| # | 단계 | 내용 |
|---|------|------|
| 1 | **`tests/_approval.py`** | `assert_matches_golden(actual, golden_path)` 없으면 **생성** |
| 2 | **golden 경로 연결** | `tests/golden/{golden_id}.approved.txt` — Test ID와 1:1 매핑 |
| 3 | **기준 생성** | `UPDATE_GOLDEN=1 pytest …` 로 **실제 출력**을 golden에 기록 |
| 4 | **matched 확인** | `UPDATE_GOLDEN` **없이** 동일 pytest → **matched** |

### 1. `tests/_approval.py` (최소 계약)

```python
import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(actual: str, golden_path: Path) -> None:
    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(actual, encoding="utf-8", newline="\n")
        return
    expected = golden_path.read_text(encoding="utf-8")
    assert actual == expected, f"Golden mismatch:\n{golden_path}\n--- diff ---\n{_diff_summary(expected, actual)}"


def _diff_summary(expected: str, actual: str) -> str:
    if expected == actual:
        return "(identical)"
    return f"expected ({len(expected)} chars) vs actual ({len(actual)} chars)"
```

- 테스트에서 `actual`은 **고정 포맷 함수**로만 생성 (아래 §출력 포맷).
- diff 상세는 프로젝트에 `difflib` 확장 가능; 보고에 **diff 요약** 필수.

### 2. golden 파일 명명

| Test ID | golden 파일 예 |
|---------|----------------|
| `D-LOC-01` | `tests/golden/d_loc_01_g1_blank_coords.approved.txt` |
| `T-02` | `tests/golden/t_02_r2_c2_fail.approved.txt` |

- `{golden_id}` = Test ID를 snake_case·소문자 (`D-LOC-01` → `d_loc_01_…`)

### 3·4. pytest 명령 (PowerShell)

```powershell
# 3) 기준 생성 (PASS 후 1회)
$env:UPDATE_GOLDEN = "1"
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v

# 4) matched 확인
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
```

`validate_lines` 예:

```powershell
$env:UPDATE_GOLDEN = "1"
python -m pytest tests/test_validate_lines.py::test_t02_r2_and_c2_fail_when_intersection_cell_wrong -v

Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/test_validate_lines.py::test_t02_r2_and_c2_fail_when_intersection_cell_wrong -v
```

---

## 출력 포맷 (고정 · 수동 편집 금지)

Golden 통과는 **코드 출력 == golden 파일**만 인정한다.  
`.approved.txt`를 **손으로 수정**해 matched 만들기 **금지** (우회). 불일치 시 구현·포맷터 수정 후 `UPDATE_GOLDEN=1`로 **재생성**.

### 좌표 · `int` 목록 (1-index, row-major)

- 빈칸 2개 등: **`(row, col)` 1-index**, row-major 순.
- 한 줄당 `row,col` (쉼표, 공백 없음) 또는 프로젝트 `format_coord_list` SSOT.
- **`int[6]`** 형식이 명시된 Test ID: **6개 정수**, 1-index, 쉼표 구분 한 줄  
  예: `2,3,4,4,0,0` — 의미는 Test ID 주석·PRD에 고정 (임의 변경 금지).

```python
def format_coord_list(coords: list[tuple[int, int]]) -> str:
    """1-index (row,col) per line, row-major."""
    return "\n".join(f"{r},{c}" for r, c in coords) + ("\n" if coords else "")
```

### `validate_lines` 결과

```text
status=fail
failed_lines=R2,C2
```

- `failed_lines` 순서: `R1`→`R4`→`C1`→`C4`→`D1`→`D2` 중 **실패분만**, 쉼표 구분.
- `status=pass` 일 때 `failed_lines=` (빈 값).

### 에러 코드 문자열 (Boundary)

- **고정 대문자** + 숫자 3자리: `E002`, `E003` … `E005`
- golden 한 줄 예: `error_code=E003`
- Entity·Logic Golden에 **E001~E005 포함 금지** (`.cursorrules`)

---

## 테스트 연결 예시

```python
from pathlib import Path

from tests._approval import GOLDEN_DIR, assert_matches_golden


def test_d_loc_01_blank_coords_row_major(grid_g1):
    from src.entity.find_blank_coords import find_blank_coords
    from tests._approval import format_coord_list  # 또는 entity 포맷터

    actual = format_coord_list(find_blank_coords(grid_g1))
    golden = GOLDEN_DIR / "d_loc_01_g1_blank_coords.approved.txt"
    assert_matches_golden(actual, golden)
```

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/_approval.py` 생성·수정 | `src/` 구현 변경 (버그는 GREEN으로) |
| `tests/golden/*.approved.txt` — **UPDATE_GOLDEN=1로만** 생성·갱신 | golden **수동 편집**으로 matched 우회 |
| 대상 Test ID 테스트에 golden assert **추가** | PASS 안 된 Test ID에 golden 연결 |
| | `UPDATE_GOLDEN=1` 없이 golden 파일 덮어쓰기 |
| | assert 완화·skip·xfail |

---

## 보고 형식 (필수)

```markdown
Phase: green | Layer: entity | Track: Logic

## Golden
| 항목 | 값 |
|------|-----|
| Test ID | D-LOC-01 |
| golden 경로 | tests/golden/d_loc_01_g1_blank_coords.approved.txt |
| matched | yes / no |

## diff 요약 (no일 때)
- (한 줄: 어느 줄·필드 불일치)

## pytest
- UPDATE_GOLDEN=1: passed, golden written
- matched run: passed

## 변경 파일
- tests/_approval.py (신규|수정)
- tests/golden/….approved.txt (생성)
- tests/entity/test_d_loc_01.py (golden assert 추가)
```

---

## 완료 조건

- [ ] 대상 Test ID **pytest PASS** 전제 충족
- [ ] `assert_matches_golden` 연결됨
- [ ] `UPDATE_GOLDEN=1` → golden 생성 후, **없이** matched **PASS**
- [ ] golden **수동 편집 없음**
- [ ] 1-index / `int[6]` / 에러 코드 **포맷 SSOT** 준수
- [ ] 보고에 golden 경로 · matched · diff 요약 포함

---

## 파이프라인 위치

```
… → /green-minimal (PASS) → /golden-master → /refactor-safe
```

Track B(Entity/Logic) 우선. Track A(Boundary)는 `error_code=E00x` golden 별도.
