# Refactor Smell — ARRR R단계 (Refine ⑦)

코드 **스멜 탐지만** 수행한다. **수정·commit 금지**.

추가 인자 없이 `/refactor-smell` 만으로 동작한다.  
대상 범위는 **`src/` · `tests/`** 전체(Logic + UI Track). 채팅·최근 GREEN/Golden 맥락에서 우선 파일을 좁힌다.  
**추가 입력·질문 금지** — 부족하면 코드 읽기·pytest 결과로 추론한다.

**Skill:** `magic-square-tdd` Skill이 있으면 **자동 따름**.

SSOT: `.cursorrules` · `docs/PRD.md` · `.cursor/commands/green-minimal.md`

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

이어서 **한국어**로 진행한다.

---

## 전제 (중단 조건)

```bash
python -m pytest tests/ -v
```

- **전부 PASS**가 아니면 **즉시 중단** — 스멜 보고하지 않음.
- 실패 시: “pytest 미통과 — `/green-minimal` 또는 회귀 수정 후 재실행” 한 줄만 출력.

---

## 수정 범위

| 허용 | 금지 |
|------|------|
| 코드 **읽기**·분석 | `src/` · `tests/` **어떤 파일도 수정하지 않음** |
| 채팅으로 **스멜 표** 출력 | `git commit` / `git push` |
| | `/refactor-safe` 실행 (별도 커맨드) |
| | 테스트·구현 **동작 변경** 제안을 코드에 반영 |

---

## 스멜 카탈로그 (검사 항목)

| 유형 | 설명 | MagicSquare 예시 |
|------|------|------------------|
| **Long Method** | 한 함수가 10선 검증·입출력·포맷을 모두 담음 | `validate_lines` 40줄+ |
| **Duplicated Code** | 행/열/대각 합 계산·줄 ID 문자열이 반복 | `R1`~`R4` 합산 copy-paste |
| **Mysterious Name** | `x`, `tmp`, `check` 등 의도 불명 | `failed` vs `failed_lines` 혼용 |
| **Magic Number** | `34`, `4`, `16` 리터럴 | `constants.py` 밖 하드코딩 |
| **ECB 위반** | Entity가 boundary import, UI가 합 로직 직접 수행 | `entity` → `PyQt` |
| **Feature Envy** | 다른 모듈 데이터를 과도하게 조작 | 테스트 헬퍼가 `grid` 내부만 다룸 |

---

## 우선순위 (P0 / P1 / P2)

| 등급 | 기준 | 예 |
|------|------|-----|
| **P0** | 계약·테스트 깨질 위험, ECB/SSOT 위반 | Magic Number in `src/`, Entity→Boundary import |
| **P1** | 중복·긴 메서드 — Change Budget 내 분리 가능 | 10선 합산 중복 |
| **P2** | 이름·미세 구조 — 동작 무관 | 변수명, 주석 |

---

## Change Budget (`/refactor-safe` 참고)

한 번의 REFACTOR 턴 상한 (본 커맨드에서는 **예산만 표기**, 수정 안 함):

| 항목 | 상한 |
|------|------|
| 파일 | **≤ 3** |
| 클래스 | **≤ 1** |
| 메서드 | **≤ 3** |

후보 제안 시 **Budget 안에 들어가는지** 한 줄씩 적는다.

---

## 출력 형식 (필수)

### 1. 스멜 표

| P | 유형 | 위치 (파일:줄) | 요약 | Budget 적합 |
|---|------|----------------|------|-------------|
| P0 | Magic Number | `src/validate_lines.py:…` | … | 예/아니오 |
| P1 | Duplicated Code | … | … | 예 |
| … | … | … | … | … |

- 발견 0건이면 “스멜 없음(또는 P2만)” 명시.

### 2. `/refactor-safe` 후보 (1~3개)

| # | 후보 | P | 유형 | 예상 변경 | Budget |
|---|------|---|------|-----------|--------|
| 1 | … | P0 | … | private 헬퍼 1개 추출 | 파일1·메서드1 |
| 2 | … | … | … | … | … |
| 3 | … | … | … | … | … |

- **1~3개만** — 과도한 백로그 금지.

### 3. 다음 안내 (고정 문구)

```markdown
## 다음
**P0 후보 1개**만 골라 `/refactor-safe` 실행. (본 턴은 수정·commit 없음)
```

---

## 보고 예시

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest
- `python -m pytest tests/ -v` → N passed (전제 OK)

(스멜 표)

(/refactor-safe 후보 1~3)

## 다음
**P0 후보 1개**만 골라 `/refactor-safe` 실행. (본 턴은 수정·commit 없음)
```

---

## 완료 조건

- [ ] pytest **전체 PASS** 확인 후에만 스멜 표 출력
- [ ] **코드 수정·commit 없음**
- [ ] P0/P1/P2 · 6종 유형 · Change Budget 열 포함
- [ ] `/refactor-safe` 후보 **1~3개**
- [ ] P0 1개 골라 `/refactor-safe` 안내 문구 포함

---

## 파이프라인 위치

```
… → /green-minimal → /golden-master → /refactor-smell → /refactor-safe
                              PASS          Refine ⑦          Refine ⑧
```

---

## Track 참고

| Track | 주로 보는 경로 |
|-------|----------------|
| Logic | `src/validate_lines.py`, `src/entity/`, `tests/`, `tests/entity/` |
| UI | `src/boundary/`, `tests/boundary/` |

`Track: Logic+UI` — 두 Track 모두 스캔하되, **한 표**에 통합한다.
