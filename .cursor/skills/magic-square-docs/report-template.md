# Report Template — `Report/NN.REPORT.md`

SSOT 형식 예: `Report/05.REPORT.md`

`NN` = 2자리 (`01`~`99`). 기존 번호 **덮어쓰기 금지**.

---

```markdown
# MagicSquare_1004 — {세션 주제}

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_1004 (4×4 마방진, 10선 검증) |
| 세션 | NN |
| Phase | {red \| green \| refactor \| repeat} |
| ARRR 사이클 | {해당 시 1줄} |
| 보고서 생성일 | YYYY-MM-DD |
| Test ID | {T-__, D-__ …} |
| Command | {/red-test-plan, /tdd-red, …} |

관련 Transcript: [Prompting/NN.Export-Transcript.md](../Prompting/NN.Export-Transcript.md)

---

## 1. 요약

{3~5문장: 이번 Export 구간에서 한 일·pytest 상태·다음 1줄}

---

## 2. 입력 스냅샷 (Step A)

| 항목 | 값 |
|------|-----|
| git status | {한 줄 요약} |
| pytest | `python -m pytest tests/ -v` → {N passed, M failed} |
| Phase 선언 | `Phase: …` |
| Test ID | … |
| Command | … |

---

## 3. STEP — RED

| 항목 | 내용 |
|------|------|
| 적용 | {해당 시만 — 없으면 "해당 없음"} |
| Test ID | … |
| 변경 | `tests/` … |
| pytest | {실측 FAIL/PASS} |

---

## 4. STEP — GREEN

| 항목 | 내용 |
|------|------|
| 적용 | {해당 시만} |
| Test ID | … |
| 변경 | `src/` … |
| pytest | {실측} |
| golden | matched yes/no |

---

## 5. STEP — REFACTOR

| 항목 | 내용 |
|------|------|
| 적용 | {해당 시만} |
| 스멜 | P_ / 유형 / 위치 |
| Budget | 파일·메서드 수 |
| pytest · golden | {실측} |

---

## 6. STEP — REPEAT

| 항목 | 내용 |
|------|------|
| 적용 | {Phase: repeat 시} |
| ARRR 1사이클 | Ask → … → Refine 요약 |
| 재진입 사유 | … |

---

## 7. 생성·변경 파일

| 파일 | 작업 | 비고 |
|------|------|------|
| … | 신규 \| 수정 | … |

---

## 8. pytest 상태 (최종)

```text
{실행 명령}
→ {실제 출력 한 줄}
```

---

## 9. 다음 단계

1. …
2. …

---

*본 문서는 Report/NN.REPORT.md — {세션 주제} (YYYY-MM-DD)입니다.*
```

## Phase별 섹션 규칙

| Phase | 필수 채움 섹션 | 나머지 |
|-------|----------------|--------|
| `red` | §3 STEP-RED | §4~§6 "해당 없음" |
| `green` | §4 STEP-GREEN | … |
| `refactor` | §5 STEP-REFACTOR | … |
| `repeat` | §6 STEP-REPEAT + §3~§5 요약 | 전 구간 요약 |

여러 Phase가 한 세션에 있으면 해당 STEP **모두** 채운다.
