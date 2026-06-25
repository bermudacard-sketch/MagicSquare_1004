---
name: magic-square-tdd
description: >-
  MagicSquare_1004 Dual-Track TDD workflow (ARRR, C2C, pytest). Use when Phase is
  red, green, or refactor; when invoking Commands /red-test-plan, /red-skeleton,
  /tdd-red, /green-minimal, /golden-master, /refactor-smell, /refactor-safe; or
  when the user mentions TDD, RED, GREEN, REFACTOR, Dual-Track, C2C, or pytest.fail.
disable-model-invocation: true
---

# MagicSquare_1004 — Dual-Track TDD

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/*.md`

도메인: 4×4 격자, 빈칸 `0`, 1~16, `MAGIC_CONSTANT=34`, 10선 `R1`~`R4`·`C1`~`C4`·`D1`·`D2`.

API: `validate_lines(grid) -> {status: pass|fail|incomplete, failed_lines: list[str]}`

---

## 1. ARRR ↔ TDD 매핑

| ARRR | 단계 | TDD | Command |
|------|------|-----|---------|
| **Ask** | ③ | RED 설계 | `/red-test-plan` |
| **Ask** | ④ | RED 스켈레톤 | `/red-skeleton` |
| **Ask** | ⑤ | RED assert | `/tdd-red` |
| **Respond** | GREEN | 최소 구현 | `/green-minimal` |
| **Respond** | Golden | Approval | `/golden-master` |
| **Refine** | ⑦ | 스멜 탐지 | `/refactor-smell` (수정 금지) |
| **Refine** | ⑧ | Safe Refactor | `/refactor-safe` (스멜 1개) |

한 턴 = 한 Phase. RED·GREEN·REFACTOR **혼합 금지**.

---

## 2. Phase 선언 (응답 첫 줄)

| Phase | 첫 줄 |
|-------|--------|
| RED 설계/스켈레톤/assert | `Phase: red \| Layer: entity \| Track: Logic` |
| GREEN / Golden | `Phase: green \| Layer: entity \| Track: Logic` |
| REFACTOR smell | `Phase: refactor \| Scope: src/ tests/ \| Track: Logic+UI` |
| REFACTOR safe | `Phase: refactor \| Layer: entity \| Track: Logic` |

Track A(UI): `Layer: boundary` \| `Track: UI`로 치환.

기본 언어: **한국어**. `git commit`은 사용자 요청 시만.

---

## 3. C2C Rule 1~3 요약

| Rule | PRD | 검증 |
|------|-----|------|
| **Rule1** | R-03, C-03 — 10선 합 = `MAGIC_CONSTANT` | `status` `pass` / `fail` |
| **Rule2** | R-04 — 빈칸 `0` | `status` `incomplete`, 합 검사 생략, `failed_lines=[]` |
| **Rule3** | C-04 — 실패 선 식별 | `failed_lines` ID·순서 `R1`→`R4`→`C1`→`C4`→`D1`→`D2` |

테스트에 `34` 리터럴 **금지** — `status` / `failed_lines`로만 assert.

---

## 4. RED 절대 금지

- `src/` 수정 (스켈레톤·플랜 단계 포함)
- `pytest.skip`, `pytest.mark.xfail`
- assert 완화·삭제 (`==`→`in`, 조건 제거, `approx` 완화)
- GREEN / REFACTOR 동시 수행
- **Logic Track Domain Mock** — 실제 `grid` 리터럴·`grid_g1` 픽스처만
- `tests/` 외 파일 수정 (`pyproject.toml`, `.cursorrules` 등) — `/tdd-red` 기준

RED 스켈레톤 Then: `pytest.fail("RED: {Test ID} — …")` **한 줄만**.

---

## 5. GREEN

- **1 RED 묶음 = 1 GREEN 턴 = 1 커밋**(사용자 요청 시)
- `src/` 최소 구현 — 이번 Test ID만 PASS, 다른 ID 선행 해결 금지
- `src/entity/constants.py` SSOT: `MAGIC_CONSTANT`, `GRID_SIZE`, `MAX_CELL_VALUE`, `BLANK_CELL`, `BLANK_COUNT`
- 매직넘버·`34`/`4`/`16` 하드코딩 금지 (`constants` import)
- E001~E005 emit 금지 (Entity·Logic)
- Entity → boundary/control import 금지

---

## 6. REFACTOR

**`/refactor-smell`:** 읽기·표만. 수정·commit 금지. `pytest tests/ -v` 전부 PASS 전제.

**`/refactor-safe`:** 스멜 **1개**. Change Budget:

| 항목 | ≤ |
|------|---|
| 파일 | 3 |
| 클래스 | 1 |
| 메서드 | 3 |

- 입출력·예외·`int[6]` 1-index·golden 포맷 **불변**
- golden: `UPDATE_GOLDEN` 없이 **matched** 필수
- golden diff **의도적** → ISS 1줄 + `UPDATE_GOLDEN=1` / **비의도** → 롤백
- 기능 추가·버그 수정 → `/green-minimal`

---

## 7. Track A (UI) vs Track B (Logic)

| | Track B — Logic | Track A — UI |
|---|-----------------|--------------|
| Layer | `entity` | `boundary` |
| 경로 | `src/validate_lines.py`, `src/entity/`, `tests/`, `tests/entity/` | `src/boundary/`, `tests/boundary/` |
| 테스트 ID | `T-*`, `D-*` | `U-*` |
| Mock | Domain Mock **금지** | UI·입력만; Entity 호출 |
| 오류 | E001~E005 **금지** | E002, E003 등 Boundary |
| Golden | 좌표 1-index, `status=`/`failed_lines=` | `error_code=E00x` |

---

## 8. Command 체인

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master
                                                      ↓
                              /refactor-smell → /refactor-safe
```

| Command | 산출 |
|---------|------|
| `red-test-plan` | C2C 표·테스트 플랜 (파일 없음) |
| `red-skeleton` | `pytest.fail` 스켈레톤 (`tests/`) |
| `tdd-red` | assert 본문 RED (`tests/`만) |
| `green-minimal` | `src/` 최소 구현 |
| `golden-master` | `tests/golden/*.approved.txt` |
| `refactor-smell` | 스멜 표 + 후보 1~3 |
| `refactor-safe` | Budget 내 리팩터 1건 |

---

## 9. pytest 명령 패턴

```powershell
# 전체
python -m pytest tests/ -v

# 단일 Test ID
python -m pytest tests/test_validate_lines.py::test_t02_r2_and_c2_fail_when_intersection_cell_wrong -v

# Entity
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v

# Golden 기준 생성 (PASS 후만)
$env:UPDATE_GOLDEN = "1"
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue

# Golden matched 확인
python -m pytest tests/ -v
```

완료 판정: **전체 PASS**. RED는 신규 테스트 **FAIL** 의도.

---

## 10. 완료 보고 형식

### RED (`tdd-red`)

```markdown
Phase: red | Layer: entity | Track: Logic
## 추가 테스트 · Arrange · 기대 · pytest 결과 (N failed)
## 다음: /green-minimal
```

### GREEN (`green-minimal`)

```markdown
Phase: green | Layer: entity | Track: Logic
## PASS Test ID · 변경 파일 · pytest (단일+전체)
## 다음: /golden-master 또는 다음 RED
```

### Golden (`golden-master`)

```markdown
Phase: green | Layer: entity | Track: Logic
## golden 경로 · matched yes/no · diff 요약
```

### REFACTOR smell

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
## pytest N passed · (스멜 표) · (/refactor-safe 후보 1~3)
## 다음: P0 1개 골라 /refactor-safe
```

### REFACTOR safe

```markdown
Phase: refactor | Layer: entity | Track: Logic
## 대상 스멜 · 변경 요약 · pytest · golden matched
```

---

## 빠른 체크리스트

- [ ] Phase 첫 줄 선언
- [ ] SSOT·10선·API 계약 준수
- [ ] RED: `tests/`만 / GREEN: 최소 `src/` / REFACTOR: Budget·golden
- [ ] Dual-Track: Logic Mock 금지, UI·Logic 분리
- [ ] 해당 Command md와 충돌 시 **Command + SSOT** 우선

## 추가 리소스

- Command 상세: `.cursor/commands/red-test-plan.md` … `refactor-safe.md`
- 문제 정의: `Report/01.MagicSquare_ProblemDefinition_Report.md`
