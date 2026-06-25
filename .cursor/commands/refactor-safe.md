# Refactor Safe — ARRR R단계 (Refine ⑧)

`/refactor-smell` 표에서 **선택한 스멜 1개만** Safe Refactor 실행한다.  
**구조 정리만** — 동작·계약·Golden 출력은 불변.

추가 인자 없이 `/refactor-safe` 만으로 동작한다.  
대상 스멜은 **직전 `/refactor-smell` 후보 표**·**채팅 지정**·**P0 1개**에서 자동 추출한다.  
여러 스멜 동시 해결 **금지**. 추가 입력·질문 금지.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/refactor-smell.md` · `.cursor/commands/golden-master.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: refactor | Layer: entity | Track: Logic
```

| 필드 | 값 | 비고 |
|------|-----|------|
| `Phase` | `refactor` | 고정 |
| `Layer` | `entity` \| `boundary` | Logic → **`entity`** |
| `Track` | `Logic` \| `UI` | UI 스멜 → `boundary` / `UI` |

이어서 **한국어**로 진행한다.

---

## 전제

1. `/refactor-smell` **직후** — pytest 전체 PASS 상태.
2. **스멜 1개**만 선택 (표의 `#` 번호 또는 P·유형·위치 명시).
3. 선택 스멜이 **Change Budget** 안에 들어감.

```bash
python -m pytest tests/ -v
```

시작 전 FAIL이면 **중단** — “pytest 미통과” 한 줄만.

---

## Safe Refactor 원칙 (불변)

| 항목 | 금지 |
|------|------|
| **공개 API** | `validate_lines` 시그니처·반환 키·`status` 값·줄 ID 규칙 변경 |
| **입출력** | 관찰 가능한 반환값·stdout·파일 출력 변경 |
| **예외** | 새 예외·삼킨 예외·예외 타입 변경 |
| **좌표·포맷** | **`int[6]` 1-index** · 좌표 golden · `error_code=E00x` 문자열 포맷 변경 |
| **오류 코드** | E001~E005 **raise / return / emit** (Entity·Logic) |
| **ECB** | Entity → boundary/control import 추가 |
| **기능** | 새 Test ID 통과·버그 수정·Solver/UI — **별도 GREEN** |
| **테스트** | assert 완화·skip·xfail |

허용: private 헬퍼 추출, 이름 개선(동작 동일), 중복 제거, `constants.py`로 매직넘버 **이동**(값 불변).

---

## Change Budget (필수 준수)

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드 (신규·추출·시그니처 변경 포함) | **≤ 3** |

초과 시: **이번 턴 중단** — 스멜을 더 쪼개 `/refactor-smell` 재실행.

---

## 절차

| # | 단계 |
|---|------|
| 1 | 선택 스멜 1개·위치·예상 변경을 한 줄로 고정 |
| 2 | Budget 내에서 **최소 diff** 리팩터 (기능 추가 없음) |
| 3 | `python -m pytest tests/ -v` — **전부 PASS** |
| 4 | Golden **matched** (`UPDATE_GOLDEN` **없이**) |
| 5 | golden diff 발생 시 → 아래 §Golden 처리 |

---

## Golden 검증

```powershell
# matched 확인 (UPDATE_GOLDEN 없음)
python -m pytest tests/ -v
```

Golden 연결 테스트가 있으면 반드시 **matched**.

### golden diff 처리

| 구분 | 조치 |
|------|------|
| **의도적** (포맷터·이름만, 계약 동일) | ISS(이슈) 문서 1줄 기록 → `UPDATE_GOLDEN=1 pytest …` → 재검증 |
| **비의도** (동작·출력 변경) | **롤백** → `/green-minimal` 또는 원인 수정. golden 수동 편집 **금지** |

ISS 문서 예: `Report/` 또는 채팅 보고에 “ISS: REF-… golden 갱신 사유” 한 줄.

```powershell
# 의도적 golden 갱신만
$env:UPDATE_GOLDEN = "1"
python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
python -m pytest tests/ -v
```

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| 선택 스멜 1개 해소에 필요한 `src/` · `tests/` **구조** 변경 | 스멜 2개 이상 동시 해결 |
| `src/entity/constants.py` — 리터럴→상수 **이동** | 상수 **값** 변경 |
| | RED / GREEN / 새 테스트 추가 |
| | `git commit` (사용자 요청 없이) |

---

## 보고 형식 (필수)

```markdown
Phase: refactor | Layer: entity | Track: Logic

## 대상 스멜
- #1 from /refactor-smell — P1 Duplicated Code — `src/validate_lines.py`

## 변경 요약
- (파일 N, private 헬퍼 M — Budget: 파일1·메서드1)
- 동작·API·golden 포맷: **불변**

## pytest
- `python -m pytest tests/ -v` → N passed

## golden
- matched: yes / no
- (diff 시) 의도적 ISS + UPDATE_GOLDEN / 비의도 롤백

## 다음
- 추가 스멜 → `/refactor-smell` 재실행
- 없음 → 다음 RED 묶음 또는 Track A
```

---

## 완료 조건

- [ ] **스멜 1개**만 처리
- [ ] Change Budget **준수**
- [ ] 입출력·예외·`int[6]` 1-index·E001~E005 **불변**
- [ ] 기능 추가·버그 수정 **없음**
- [ ] `pytest tests/ -v` **전부 PASS**
- [ ] golden **matched** (또는 의도적 diff → ISS + UPDATE_GOLDEN 후 matched)
- [ ] git commit **없음** (요청 없을 때)

---

## 파이프라인 위치

```
… → /refactor-smell (⑦ 탐지) → /refactor-safe (⑧ 1스멜) → /refactor-smell …
```

---

## Track A (Boundary)

`Phase: refactor | Layer: boundary | Track: UI` — `src/boundary/`만.  
Entity·`validate_lines` 계약은 **건드리지 않음**.

---

## 예시 (Duplicated Code → 헬퍼 1개)

- **Before:** 행·열 합산 루프가 `validate_lines` 내 2회 반복
- **After:** `_line_sum(cells) -> int` private 1개 (메서드 +1, 파일 1)
- **금지:** 10선 검증 순서·`failed_lines` ID·반환 dict 변경
