# RED Test Plan — ARRR A단계 (Ask = RED ③)

`validate_lines` / 세션 3 Test Loop TDD 사이클의 **ARRR A단계(Ask)** 전용 커맨드.  
**C2C 설계표·테스트 플랜만** 작성한다. 테스트·구현 **파일은 생성하지 않는다**.

추가 인자 없이 `/red-test-plan` 만으로 동작한다.  
세션 주제·Test ID·대상 FR은 **현재 채팅 맥락**과 **`docs/PRD.md`**(없으면 `.cursorrules`)에서 자동 추출한다.  
**추가 입력·질문 금지** — 정보가 부족하면 SSOT·채팅에서 추론하고 “추론 근거” 한 줄만 명시한다.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/tdd-red.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (값은 세션에 맞게 채움):

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 기본 (세션 3 Command) |
|------|-----|------------------------|
| `Phase` | `red` | 고정 |
| `Layer` | `entity` \| `boundary` | Logic Track → **`entity`** (Command·순수 검증) |
| `Track` | `Logic` \| `UI` | `validate_lines` → **`Logic`** |

**Track A (Boundary/UI):** 동일 본문을 재사용하되 선언만 `Layer: boundary` \| `Track: UI`로 바꾼다. C2C·플랜의 대상 함수·파일 경로를 Boundary 컴포넌트로 치환한다.

이어서 **한국어**로 진행한다.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| 채팅 응답으로 **설계표·플랜 문서** 출력 | `tests/` · `src/` **파일 생성·수정** |
| | `src/` 구현, GREEN, REFACTOR |
| | `pytest.skip`, `pytest.mark.xfail` |
| | assert 완화 전략을 플랜에 넣는 것 |

---

## 출력 4블록 (표 형식, 필수)

아래 **4개 블록을 순서대로** 표로 출력한다. 코드 파일은 만들지 않는다.

### 블록 1 — C2C (Rule1~3)

PRD FR(§4.1 Rule / §4.2 Command / §4.4 Test Loop)을 **Contract-to-Check** 3행으로 매핑한다.

| Rule | PRD FR 인용 | To-Do (1개) | Test ID | Given | When | Then |
|------|-------------|-------------|---------|-------|------|------|
| Rule1 | (예: R-03, C-03) | … | T-__ | … | `validate_lines(grid)` | `status` / `failed_lines` |
| Rule2 | … | … | T-__ | … | … | … |
| Rule3 | … | … | T-__ | … | … | … |

- **Rule1** — 10선 합 = `MAGIC_CONSTANT` (`pass` / `fail`)
- **Rule2** — 빈칸 `0` → `incomplete`, 합 검사 생략
- **Rule3** — 실패 선 ID (`R1`~`R4`, `C1`~`C4`, `D1`, `D2`) 및 순서

### 블록 2 — Track B 표 (Logic)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| T-01 | `validate_lines` | README 완성 격자 → `pass`, `[]` | API 키·status 값 불변 | `TypeError` / `AssertionError` (스텁) |
| T-02 | `validate_lines` | R2·C2 교차 셀 fail → `fail`, `R2`·`C2` ∈ `failed_lines` | 10선 ID 규칙 | 동상 |
| T-03 | `validate_lines` | 대각선만 fail 격자 → `fail`, `D1` 또는 `D2` | Mom Test 패턴 | 동상 |
| … | … | … | … | … |

- **Invariant:** `.cursorrules` 계약·10선 정의·`failed_lines` 순서
- **Expected RED Failure:** 스텁 `...` 또는 미구현 시 예상 오류 유형

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|------|------|
| 파일 경로 | `tests/test_validate_lines.py` (Logic Track B) |
| 함수명 | `test_t01_…`, `test_t02_…` (Test ID와 1:1) |
| conftest 픽스처 | (없음) 또는 `grid_complete`, `grid_g1` — **본 커맨드에서 파일 생성 안 함** |
| pytest 명령 | `pytest tests/test_validate_lines.py -v` |
| RED 묶음 범위 | 이번 플랜에 포함할 Test ID 목록 (예: `T-01`만 / `T-01`~`T-03`) |
| AAA | Arrange(grid) → Act(`validate_lines`) → Assert(`status`, `failed_lines`) |
| 상수 | `34` 리터럴 테스트 금지 — `.cursorrules` |

### 블록 4 — ECB · Mock 점검

| 항목 | Logic Track (B) | Boundary Track (A) |
|------|-----------------|---------------------|
| 계층 | Command `validate_lines` — Entity 상수만 의존 (세션 4+ `entity/`) | `GridUI`, `InputHandler`, `ResultDisplay` |
| Domain Mock | **금지** — 실제 `grid` 리터럴·픽스처만 | UI Mock은 Boundary 테스트에서만 |
| Entity 규칙 | Boundary/Control import **금지** | — |
| E001~E005 emit | **금지** (Entity·Logic 테스트) | Boundary 입력 오류 코드만 해당 시 |
| Out of Scope | Solver, `find_blank_coords`, PyQt — 플랜에 넣지 않음 | 세션 3 미해당 시 표기 |

---

## 보고 형식 (응답 끝)

```markdown
Phase: red | Layer: entity | Track: Logic

(블록 1~4 표)

## 추론 근거 (해당 시)
- …

## 다음
/red-skeleton 으로 넘길 준비됐다
```

---

## 완료 조건

- [ ] **4블록 표**가 모두 채워졌는가
- [ ] PRD FR · `.cursorrules` API와 **용어 일치** (`pass`/`fail`/`incomplete`, 10선 ID)
- [ ] `tests/` · `src/` **파일을 만들지 않았는가**
- [ ] GREEN / REFACTOR / skip / xfail 을 **포함하지 않았는가**
- [ ] 마지막 줄: **`/red-skeleton 으로 넘길 준비됐다`**

---

## 참고 — 세션 3 기본 매핑

| PRD | SSOT 계약 |
|-----|-----------|
| T-01 완성 격자 | `status="pass"`, `failed_lines=[]` |
| T-02 / Mom Test | `status="fail"`, 대각선 또는 R2·C2 등 |
| T-03 대각선만 | `status="fail"`, `D1` 또는 `D2` |
| R-04 / 빈칸 | `status="incomplete"`, `failed_lines=[]` |

RED 구현 단계는 `.cursor/commands/tdd-red.md` → 이후 GREEN은 별도 커맨드.
