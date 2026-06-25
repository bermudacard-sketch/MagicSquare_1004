# RED Skeleton — ARRR A단계 (RED ④)

`/red-test-plan` 설계표(블록 1~3)를 기준으로 **pytest.fail 스켈레톤만** `tests/`에 작성한다.  
실제 `assert` 본문·GREEN·REFACTOR는 **하지 않는다**.

추가 인자 없이 `/red-skeleton` 만으로 동작한다.  
Test ID·파일 경로·Given/Then은 **직전 `/red-test-plan` 출력** 또는 **채팅·`docs/PRD.md`**에서 자동 추출한다.  
**추가 입력·질문 금지** — 부족하면 SSOT에서 추론하고 “추론 근거” 한 줄만 명시한다.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름** (네이밍·픽스처·Track 분리 규칙 우선).

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/red-test-plan.md` · `.cursor/commands/tdd-red.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Phase` | `red` | 고정 |
| `Layer` | `entity` \| `boundary` | Logic → **`entity`** |
| `Track` | `Logic` \| `UI` | Boundary UI → `boundary` / `UI`로 선언만 변경 |

이어서 **한국어**로 진행한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/` 하위만 (`test_*.py`, `conftest.py`, `tests/entity/` 등) | `src/` **전부** (구현·시그니처·`entity/constants.py` 생성 포함) |
| | `assert` 본문 (스켈레톤 단계) |
| | `pytest.skip`, `pytest.mark.xfail` |
| | 통과하는 더미 테스트 (`pass`, 빈 `assert True`) |
| | GREEN / REFACTOR |
| | `pyproject.toml`, `.cursorrules` 등 tests/ 외 수정 |

---

## 스켈레톤 규칙

### AAA 주석 (필수)

각 테스트 함수 안에 **Given / When / Then** 주석 3줄을 둔다.

```python
    # Given: …
    # When: …
    # Then: …
```

### Then — `pytest.fail` 한 줄만

`Then` 구간에는 **아래 한 줄만** 허용한다. `assert` 금지.

```python
    pytest.fail("RED: {Test ID} — {한 줄 기대 요약}")
```

예: `pytest.fail("RED: T-03 — D1 fail, failed_lines에 D1 포함")`

### 상수 import

`34` / `16` / `4` 리터럴을 테스트·conftest에 **직접 쓰지 않는다**.  
픽스처·격자 데이터 조립 시에만 `src.entity.constants`에서 import 한다.

```python
from src.entity.constants import BLANK_CELL, BLANK_COUNT, GRID_SIZE, MAGIC_CONSTANT, MAX_CELL_VALUE
```

> `entity/constants.py`가 아직 없으면 **본 커맨드에서 생성하지 않는다**. 픽스처는 `BLANK_CELL` 등 import 줄만 두고, GREEN 전까지 `ImportError`로 FAIL해도 RED로 간주한다. 또는 설계표에 “리터럴 격자만” 명시된 경우 Given에 리터럴 격자 허용(상수 비교 assert 없음).

### conftest — `grid_g1`

`tests/conftest.py`에 **`grid_g1` 픽스처**를 둔다 (없으면 생성, 있으면 설계와 맞게만 수정).

| 항목 | 값 |
|------|-----|
| 격자 | 4×4, `0` **정확히 2개** |
| 빈칸 위치 | row-major 스캔 순 (예: `(1,2)`, `(3,3)` 0-index) |
| SSOT | PRD §예시 부분 격자 / G1 |
| 검증 | `BLANK_COUNT`, `GRID_SIZE`, `BLANK_CELL`로 assert **금지** — 스켈레톤은 `pytest.fail`만 |

```python
import pytest

from src.entity.constants import BLANK_CELL, BLANK_COUNT, GRID_SIZE

@pytest.fixture
def grid_g1() -> list[list[int]]:
  """G1 — 빈칸 2개, row-major."""
  grid = [
      [16, 3, 2, 13],
      [5, 10, BLANK_CELL, 8],
      [9, 6, 7, 12],
      [4, 15, 14, BLANK_CELL],
  ]
  return grid
```

---

## 템플릿 예시

### Logic — `validate_lines` (세션 3)

```python
import pytest

from src.validate_lines import validate_lines


def test_t03_diagonal_only_fail_skeleton():
    # Given: README 완성 격자에서 (3,3)만 1→2, 행·열 합 유지·D1만 깨짐
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 2],
    ]
    # When: validate_lines(grid) 호출 예정
    _ = validate_lines  # Act placeholder — 스켈레톤은 호출 생략 가능
    # Then:
    pytest.fail("RED: T-03 — status=fail, failed_lines에 D1 포함")
```

### Entity — `find_blank_coords` (참고: `test_d_loc_01_blank_coords_row_major`)

```python
import pytest

from src.entity.find_blank_coords import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Given: grid_g1 — 0 두 개, row-major
    # When: find_blank_coords(grid_g1) 호출 예정
    _ = find_blank_coords
    # Then:
    pytest.fail("RED: D-LOC-01 — 1-index row-major [(2,3), (4,4)]")
```

- 함수명: `test_{test_id_snake}_…` (예: `test_d_loc_01_blank_coords_row_major`)
- Test ID 주석: 파일 상단 또는 함수 위 `# T-03` / `# D-LOC-01`

---

## 작업 순서

1. `/red-test-plan` 블록 3에서 **파일 경로·함수명·RED 묶음** 확인
2. `tests/conftest.py` — `grid_g1` 필요 시만 추가·수정
3. 해당 `test_*.py`에 스켈레톤 함수 추가 (**한 묶음**만)
4. `pytest` 실행
5. 보고 (아래 형식)

---

## 보고 형식 (필수)

```markdown
Phase: red | Layer: entity | Track: Logic

## 스켈레톤
| Test ID | FAIL 한 줄 |
|---------|------------|
| T-03 | RED: T-03 — … |

## pytest
- 명령: `pytest tests/ -v`
- 결과: N failed (pytest.fail 의도), …

## 변경 파일 (tests/ 만)
- tests/conftest.py (신규|수정)
- tests/test_validate_lines.py (수정)

## 다음
/tdd-red — assert 본문으로 RED 완성
```

---

## 완료 조건

- [ ] `/red-test-plan` 설계표의 Test ID와 **1:1** 대응하는가
- [ ] Given/When/Then 주석 + `pytest.fail` **한 줄**만 있는가
- [ ] `assert` 본문·skip·xfail·통과 더미 **없는가**
- [ ] `src/` **미수정**인가
- [ ] `pytest` 실행 후 **FAIL** 보고했는가
- [ ] `magic-square-tdd` Skill 존재 시 그 규칙을 **따랐는가**

---

## Track A (Boundary)

`Layer: boundary` \| `Track: UI`로 선언하고, 파일은 `tests/boundary/test_u_*.py` 등 설계표 경로를 따른다.  
스켈레톤 형식(Given/When/Then + `pytest.fail`)은 동일하다.
