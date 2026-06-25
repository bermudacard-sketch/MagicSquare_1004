# GREEN Minimal — ARRR R단계 (Respond = GREEN)

**RED 1묶음**당 `src/` **최소 구현**만 수행한다.  
**1 커밋 = 1 RED 묶음** (커밋은 사용자 요청 시만).

추가 인자 없이 `/green-minimal` 만으로 동작한다.  
대상 Test ID·RED 묶음은 **직전 RED 턴**·**채팅**·**`docs/PRD.md`**에서 자동 추출한다.  
**추가 입력·질문 금지** — 부족하면 SSOT에서 추론하고 “추론 근거” 한 줄만 명시한다.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/tdd-red.md` · `.cursor/commands/red-test-plan.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Phase` | `green` | 고정 |
| `Layer` | `entity` \| `boundary` | Logic → **`entity`** |
| `Track` | `Logic` \| `UI` | Boundary → `boundary` / `UI` |

이어서 **한국어**로 진행한다.

---

## 절차 (필수 순서)

| # | 단계 | 내용 |
|---|------|------|
| 1 | **RED 재확인** | 이번 묶음 Test ID·`pytest.fail` 또는 실패 assert·기대 Then을 확인. 다른 ID는 **손대지 않음** |
| 2 | **src/ 최소 구현** | 해당 Test ID를 **PASS**시키는 최소 코드만. 계약·시그니처 불변 |
| 3 | **테스트 정리** | `pytest.fail` 제거 → 설계·RED의 **assert 본문**으로 교체 (스켈레톤만 있던 경우) |
| 4 | **PASS 확인** | pytest 실행 — **이번 묶음 + 기존 테스트** 회귀 없음 |

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| `src/` — 이번 RED 묶음에 필요한 **최소** 변경 | **이번 RED 묶음 외** Test ID를 동시에 통과시키려는 구현 |
| `tests/` — `pytest.fail` → assert 교체 (이번 묶음만) | REFACTOR (구조 정리·추출·이름 변경) |
| `src/entity/constants.py` — SSOT 상수 (없으면 생성) | assert 완화·삭제, `skip`, `xfail` |
| | `34`/`16`/`4` 등 **매직넘버·하드코딩** (`constants.py` 외) |
| | E001~E005 **raise / return** (Entity·Logic) |
| | Entity가 `boundary` / `control` **import** |
| | 범위 밖 기능 (Solver, UI, …) |
| | **git commit** (사용자 명시 요청 없이) |

---

## 상수 SSOT

`src/entity/constants.py`에만 정의하고 import 한다.

```python
MAGIC_CONSTANT = 34
GRID_SIZE = 4
MAX_CELL_VALUE = 16
BLANK_CELL = 0
BLANK_COUNT = 2
```

- `validate_lines` 및 테스트: `from src.entity.constants import …`
- 리터럴 `34`, `4`, `16` in `src/`·`tests/` **금지** (격자 데이터 리터럴 1~16은 Given 격자만 허용)

---

## ECB · 오류 코드

| 계층 | GREEN 규칙 |
|------|------------|
| **Entity / Logic** | Boundary·Control import **금지**. E001~E005 emit **금지** |
| **Boundary** | (Track UI) 입력 검증·E002/E003는 **별도 RED 묶음**에서만 |

---

## pytest 명령 (예시)

```bash
# 단일 테스트 (이번 RED 묶음)
pytest tests/test_validate_lines.py::test_t02_r2_and_c2_fail_when_intersection_cell_wrong -v

# 파일 전체 (회귀)
pytest tests/test_validate_lines.py -v
```

Entity Track 예:

```bash
pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
pytest tests/entity/ -v
```

---

## 보고 형식 (필수)

```markdown
Phase: green | Layer: entity | Track: Logic

## PASS
| Test ID | 결과 |
|---------|------|
| T-02 | PASS |

## 변경 파일
- src/validate_lines.py (수정)
- src/entity/constants.py (신규|수정)
- tests/test_validate_lines.py (pytest.fail → assert)

## pytest
- 단일: `pytest …::test_t02_… -v` → passed
- 전체: `pytest tests/test_validate_lines.py -v` → N passed

## 회귀
- (없음) 또는 실패 Test ID · **즉시 수정** 내역

## 다음
- 다음 RED 묶음: `/tdd-red` 또는 `/refactor-safe` (REFACTOR는 별도 턴)
```

**회귀 실패 시:** GREEN 범위를 넘지 않는 선에서 **즉시 수정**하고 보고에 반영한다. assert 완화로 우회 **금지**.

---

## 완료 조건

- [ ] **RED 1묶음**만 GREEN했는가
- [ ] `constants.py` SSOT, 매직넘버 **없는가**
- [ ] E001~E005 · boundary import **없는가**
- [ ] REFACTOR·다른 Test ID 선행 해결 **없는가**
- [ ] pytest **PASS** (단일 + 파일/회귀)
- [ ] git commit **하지 않았는가** (요청 없을 때)

---

## 파이프라인 위치

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /refactor-safe
     Ask ③          RED ④         RED assert    Respond(GREEN)    REFACTOR
```

---

## Track A (Boundary)

`Phase: green | Layer: boundary | Track: UI` — `src/boundary/` 최소 구현.  
Entity 계약은 건드리지 않고, UI RED 묶음 1개만 PASS.
