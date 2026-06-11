# test-loop — 테스트 실행 및 실패 원인 분류

**모드**: Agent

## 목적

`pytest`를 실행하고 실패를 **분류**한 뒤, ARRR 단계에 맞는 **다음 액션**을 제안한다.

## 절차

1. 테스트 실행 — 예: `pytest tests/ -v` (프로젝트 구조에 맞게 조정)
2. 실패·에러·skip 목록 수집
3. 각 실패를 아래 **실패 원인 분류** 중 하나로 분류
4. 분류별 **Next Action** 제안
5. 전체 GREEN이면 현재 ARRR 단계와 다음 명령 권장

## 실패 원인 분류

| 분류 | 의미 | 전형적 Next Action |
| ---- | ---- | ------------------ |
| 테스트가 잘못됨 | typo, wrong import, 잘못된 기대값 | 테스트 수정 (`/red-skeleton` 재검토) |
| 구현이 없음 | RED — 기능·함수·모듈 부재 | `/green-minimal` |
| 구현 버그 | 로직 오류, 비율 계산 틀림 | 최소 수정 (범위 내) |
| 요구사항 모호함 | README·Mom Test 해석 불일치 | `/red-test-plan` 재작성 |
| 환경 문제 | venv, pytest 미설치, 경로 | 환경 수정 후 재실행 |
| Golden Master와 충돌 | 의도치 않은 출력/메시지 변경 | 롤백 또는 `/golden-master` 갱신 |
| 리팩토링 중 외부 동작 변경 | REFACTOR 범위 위반 | `/refactor-safe` 롤백·재시도 |

## 출력 형식

| Failed Test | Failure Type | Evidence | Next Action |
| ----------- | ------------ | -------- | ----------- |

- **Evidence**: assertion 메시지, traceback 한 줄, 기대 vs 실제
- **Next Action**: 구체적 명령 (`/green-minimal`, `/refactor-safe` 롤백 등)

## 전체 GREEN일 때

- 현재 추정 ARRR 단계 (RED / GREEN / REFACTOR)
- 다음 권장 명령 1개

## 완료 후 출력 (이 명령으로 rules/commands 생성 세션 시)

1. **생성한 파일 목록**
2. **각 파일 목적 한 줄 요약**
3. **ARRR 실행 순서**
4. **다음에 실행할 첫 명령 추천**

### ARRR 실행 순서 (UnitConverter)

```
/red-test-plan → /red-skeleton → /green-minimal → /golden-master
→ /refactor-smell → /refactor-safe → /traceability → /test-loop
→ (반복) /export
```

### 첫 명령 추천 (신규 프로젝트)

`/red-test-plan` — P0 회귀·입력 검증 RED 계획부터 시작
