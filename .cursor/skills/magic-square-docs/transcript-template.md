# Transcript Template — `Prompting/NN.Export-Transcript.md`

SSOT 형식 예: `Prompting/05.Export-Transcript.md`

`Report/NN.REPORT.md`와 **동일 NN**.

---

```markdown
# Export Transcript — {세션 주제}

_Exported on YYYY-MM-DD from Cursor_
_Source: {chat-uuid 또는 "session export"}_

---

## User

{사용자 메시지 전문 또는 요약 — Command 포함 시 명시}

---

## Cursor

{어시스턴트 응답 요약 — Phase 선언·핵심 산출}

---

## User

…

---

## Cursor

…

---

(대화 턴 반복 — Export 구간 **전체**. `/export-session` 직전까지)

---

## User

{Export 요청 메시지}

---

## Cursor

{Export 수행 요약 — NN 할당·파일 생성}

---

**생성·변경 파일 (본 Export)**

| 파일 | 작업 |
|------|------|
| `Report/NN.REPORT.md` | 신규 생성 |
| `Prompting/NN.Export-Transcript.md` | 신규 생성 |
| `README.md` | 문서 표 갱신 |

관련 보고서: [Report/NN.REPORT.md](../Report/NN.REPORT.md)

*본 문서는 Prompting/NN.Export-Transcript.md — {세션 주제} (YYYY-MM-DD)입니다.*
```

## 작성 규칙

| 규칙 | 내용 |
|------|------|
| 구분자 | `## User` / `## Cursor` 교대 |
| 메타 | `_Exported on` · `_Source` **필수** |
| 전문 | 가능하면 User/Cursor **핵심 전문**; 장문은 요약 + "…" |
| Command | `/tdd-red` 등 **백틱** 표기 |
| 금지 | 채팅에 없는 턴 **창작** 금지 |
| pytest | 터미널 실측만; 없으면 "미실행" |

## _Source uuid

- Cursor agent transcript id 있으면 기록 (예: `b3d09023-9a0b-4e13-b0cc-27e297a548c8`)
- 없으면 `session export` + 날짜
