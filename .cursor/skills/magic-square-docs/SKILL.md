---
name: magic-square-docs
description: >-
  Export MagicSquare_1004 session Report and Transcript (Report/NN.REPORT.md,
  Prompting/NN.Export-Transcript.md). Use for Report Export, Transcript,
  /export-session, Phase repeat, ARRR 1-cycle completion reports, or session N
  report requests.
disable-model-invocation: true
---

# MagicSquare_1004 — Docs Export

세션 **Report**·**Transcript** Export. SSOT 파일명:

- `Report/NN.REPORT.md`
- `Prompting/NN.Export-Transcript.md`

**Export 요청 시 magic-square-docs Skill 로드 후 [phase-checklist.md](phase-checklist.md) 수행.**

관련: [report-template.md](report-template.md) · [transcript-template.md](transcript-template.md)

SSOT 프로젝트: `.cursorrules` · `docs/PRD.md` · `.cursor/skills/magic-square-tdd/SKILL.md`

---

## 금지

- `git commit` / `git push` **임의** 실행
- `UPDATE_GOLDEN=1` **임의** 실행 (golden은 `/golden-master`·ISS 절차만)
- 채팅·터미널에 **없는** pytest 결과 기재
- 기존 `NN` 파일 **덮어쓰기**

---

## 워크플로

### Step A — 입력 수집

실행 후 보고서 §2에만 **실측값** 기록.

```powershell
git status
python -m pytest tests/ -v
```

| 수집 항목 | 출처 |
|-----------|------|
| git status | 터미널 |
| pytest 결과 | 터미널 (passed/failed/skipped) |
| Phase | `red` \| `green` \| `refactor` \| `repeat` — 채팅·Command |
| Test ID | `T-*`, `D-*`, `U-*` |
| Command | `/red-test-plan`, `/tdd-red`, … |
| 세션 주제 | 채팅 한 줄 |

pytest 미실행 시 Report에 **"미실행"** — 추측 금지.

### Step B — NN 할당

```
NN = max(Report/, Prompting/ 의 NN) + 1
```

- 패턴: 파일명 선두 `^\d{2}\.` (`01.…`, `02.REPORT.md` → `02`)
- `01.MagicSquare_ProblemDefinition_Report.md` → **01**
- `02.REPORT.md` + `02.Export-Transcript.md` → 다음 **03**
- 항상 **2자리** (`03`, `09`, `10`)

### Step C — Report

[report-template.md](report-template.md) 따름.

- 제목: `# MagicSquare_1004 — {세션 주제}`
- Phase별 **STEP** 섹션:
  - **RED** — `/red-test-plan`, `/red-skeleton`, `/tdd-red`
  - **GREEN** — `/green-minimal`, `/golden-master`
  - **REFACTOR** — `/refactor-smell`, `/refactor-safe`
  - **repeat** — ARRR 1사이클 완료·재진입
- 해당 없는 STEP: `해당 없음` 한 줄

### Step D — Transcript

[transcript-template.md](transcript-template.md) 따름.

- `## User` / `## Cursor` 교대
- 헤더: `_Exported on YYYY-MM-DD from Cursor_`
- `_Source: {uuid}` — transcript id 또는 `session export`
- Export 구간 대화 + 마지막 Export 턴
- 끝: 생성·변경 파일 표 + Report 링크

### Step E — README 문서 표 갱신

`README.md`에 **문서** 섹션 없으면 추가:

```markdown
## 문서

| NN | Report | Transcript | 주제 |
|----|--------|------------|------|
| 01 | [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | — | Mom Test·문제 정의 |
| NN | [Report/NN.REPORT.md](Report/NN.REPORT.md) | [Prompting/NN.Export-Transcript.md](Prompting/NN.Export-Transcript.md) | {주제} |
```

- 새 행 **추가**만 (기존 행 수정은 주제 오류 시만)
- NN 오름차순

### Step F — 완료 보고

채팅에 **경로 2개** + 한 줄 요약:

```markdown
**NN** · `{세션 주제}`
- Report: Report/NN.REPORT.md
- Transcript: Prompting/NN.Export-Transcript.md
```

---

## Phase: repeat

ARRR **1사이클** 완료 보고 시:

| 구간 | 포함 내용 |
|------|-----------|
| Ask | `red-test-plan` → `red-skeleton` → `tdd-red` |
| Respond | `green-minimal` → `golden-master` |
| Refine | `refactor-smell` → `refactor-safe` (해당 시) |

Report §STEP-REPEAT + §1 요약에 사이클 전체 압축. Phase 선언: `repeat`.

---

## /export-session 연동

`.cursor/commands/export-session.md`(또는 `/export`) 호출 시:

1. **magic-square-docs** Skill 로드
2. [phase-checklist.md](phase-checklist.md) 전항 체크
3. Step A → F 순서 실행
4. 추가 질문 **금지** (채팅·SSOT에서 추론)

별칭: `/export`, `/export-session` 동일 워크플로.

---

## ARRR 1사이클 완료 보고

트리거: "ARRR 1사이클 완료", "세션 N 보고서"

- 한 Report에 RED+GREEN+REFACTOR STEP **모두** 채움 (해당 없으면 해당 없음)
- pytest·golden은 **최종** 스냅샷만 §8
- Transcript는 사이클 구간 전체

---

## 빠른 참조 — Command → Phase

| Command | Report STEP |
|---------|-------------|
| `/red-test-plan`, `/red-skeleton`, `/tdd-red` | RED |
| `/green-minimal`, `/golden-master` | GREEN |
| `/refactor-smell`, `/refactor-safe` | REFACTOR |

---

## 완료 체크리스트

- [ ] [phase-checklist.md](phase-checklist.md) 전부
- [ ] NN 미충돌·2자리
- [ ] pytest·git **실측**
- [ ] README 표 갱신
- [ ] Step F 경로 2개 출력
- [ ] commit·UPDATE_GOLDEN **안 함**
