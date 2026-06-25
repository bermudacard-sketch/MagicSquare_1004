# Phase Checklist — Export 전 검증

Export 전 **실행·기록**한다. 채팅에 없는 결과는 **기재 금지**.

## 공통 (Step A)

- [ ] `git status` 실행·요약 기록 (커밋은 사용자 요청 시만)
- [ ] `python -m pytest tests/ -v` 실행·**실제** passed/failed 수 기록
- [ ] 이번 세션 **Phase** 확정 (`red` | `green` | `refactor` | `repeat`)
- [ ] **Test ID** 목록 (예: `T-02`, `D-LOC-01`)
- [ ] 사용 **Command** 목록 (예: `/tdd-red`, `/green-minimal`)
- [ ] `UPDATE_GOLDEN` **실행 안 함** (golden 갱신은 `/golden-master`·의도적 ISS 전용)

## Phase: red

- [ ] `tests/`만 변경 (해당 Command 규칙)
- [ ] 신규/의도적 **FAIL** 또는 `pytest.fail` 스켈레톤 명시
- [ ] `src/` 미수정
- [ ] Report §STEP-RED 채움

## Phase: green

- [ ] 대상 Test ID **PASS** (pytest 실측)
- [ ] `src/` 최소 변경 범위
- [ ] 1 RED 묶음 = 1 GREEN (보고에 명시)
- [ ] Report §STEP-GREEN 채움
- [ ] golden 연결 시 **matched** 여부 (UPDATE_GOLDEN 없이)

## Phase: refactor

- [ ] `/refactor-smell`: 수정 **없음**, 스멜 표만
- [ ] `/refactor-safe`: 스멜 **1개**, Budget 준수
- [ ] pytest 전체 PASS + golden matched
- [ ] Report §STEP-REFACTOR 채움

## Phase: repeat

- [ ] ARRR **1사이클** 요약 (Ask→Respond→Refine 또는 RED→GREEN 구간)
- [ ] 동일 Test ID 재방문 사유 1줄
- [ ] Report §STEP-REPEAT 채움

## Export 산출물

- [ ] `Report/NN.REPORT.md` 생성 (덮어쓰기 금지)
- [ ] `Prompting/NN.Export-Transcript.md` 생성
- [ ] README 문서 표 갱신 (Step E)
- [ ] Step F 완료 보고 (경로 2개)

## 금지

- [ ] git commit / push **임의** 실행 안 함
- [ ] `UPDATE_GOLDEN=1` **임의** 실행 안 함
- [ ] 채팅·터미널에 **없는** pytest 결과 기재 안 함
