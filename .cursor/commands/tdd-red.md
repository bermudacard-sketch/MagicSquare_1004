# TDD RED — validate_lines

`validate_lines(grid)` TDD 사이클의 **RED 단계 전용** 커맨드.  
한 턴에 **실패하는 테스트 하나(또는 한 묶음)** 만 추가한다. GREEN·REFACTOR는 수행하지 않는다.

SSOT: `.cursorrules` · `docs/PRD.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: RED
```

이어서 **한국어**로 진행한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/` 하위 파일만 | `src/` 수정 (구현·시그니처·docstring 변경 포함) |
| | `pyproject.toml`, `conftest.py`, `.cursorrules` 등 **tests/ 외 전부** |
| | GREEN / REFACTOR 작업을 같은 턴에 섞기 |
| | assert 완화·삭제 (`==` → `in`, 조건 제거, `approx` 기준 완화 등) |
| | `pytest.skip`, `pytest.mark.xfail` |

---

## AAA 절차

각 테스트는 **Arrange → Act → Assert** 순서로 작성한다.

1. **Arrange** — `grid: list[list[int]]` (4×4) 준비
   - 완성 격자: `0` 없음, 값 1~16
   - 부분 격자: `0` = 빈칸 (incomplete 시나리오)
   - Test ID 주석 권장: `# T-01`, `# T-02` … (`docs/PRD.md` §4.4)
2. **Act** — `result = validate_lines(grid)`
3. **Assert** — 계약 키만 검증
   - `result["status"]` ∈ `pass` | `fail` | `incomplete`
   - `result["failed_lines"]` — `list[str]`, ID는 `R1`~`R4`, `C1`~`C4`, `D1`, `D2`
   - `failed_lines` 순서 기대 시: `R1`→`R4`→`C1`→`C4`→`D1`→`D2`

**도메인 상수:** `34` 리터럴은 테스트에 쓰지 않는다. 합 값이 아닌 `status` / `failed_lines`로 검증한다.

---

## pytest 예시

```python
from src.validate_lines import validate_lines

# T-01 — README 완성 격자 → pass
def test_t01_complete_grid_returns_pass():
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    result = validate_lines(grid)
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


# T-02 — 대각선(D1)만 틀린 격자 → fail (Mom Test 실수 패턴)
def test_t02_wrong_d1_returns_fail_with_d1():
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 2],  # (3,3) 1→2 → D1 합 깨짐
    ]
    result = validate_lines(grid)
    assert result["status"] == "fail"
    assert result["failed_lines"] == ["D1"]


# T-incomplete — 빈칸(0) 포함 → incomplete, failed_lines 빈 리스트
def test_t_incomplete_blank_returns_incomplete():
    grid = [
        [16, 3, 2, 13],
        [5, 10, 0, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    result = validate_lines(grid)
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []
```

RED 완료 시 `pytest` 실행 → **새 테스트가 실패**해야 한다 (구현 스텁 `...` 상태).

---

## 보고 형식

RED 턴 종료 시 아래 형식으로 보고한다.

```markdown
Phase: RED

## 추가 테스트
- Test ID: T-__
- 파일: tests/test_validate_lines.py
- 시나리오: (한 줄)

## Arrange
- 격자 요약: (빈칸 유무, 의도한 실패 선)

## 기대 (Assert)
- status: pass | fail | incomplete
- failed_lines: [...]

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: N failed, M passed (신규 테스트 FAIL 확인)

## 다음
- GREEN: `src/validate_lines.py` 최소 구현
```

---

## 완료 조건

- [ ] `tests/` 만 수정했는가
- [ ] 신규 테스트가 **의도적으로 FAIL** 하는가
- [ ] assert 완화·skip·xfail 없는가
- [ ] API 계약(`status`, `failed_lines`, 줄 ID)과 `.cursorrules` 10선 정의를 따르는가
