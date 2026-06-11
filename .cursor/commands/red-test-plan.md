# red-test-plan — RED 테스트 계획 작성

**모드**: Ask (코드·테스트 파일 생성 금지)

## 목적

Mom Test 증거와 PRD(README) 요구사항을 바탕으로, 이번 TDD 사이클에서 **실패해야 할 동작**만 정의한다.

## 절차

1. **Mom Test 증거**와 **README.md 요구사항**을 읽는다.
2. 현재 `UnitConverter.py` 기준선을 확인한다.
   - 입력: `unit:value` (예: `meter:2.5`)
   - 단위: meter, feet, yard
   - 비율: `1 meter = 3.28084 feet`, `1 meter = 1.09361 yard`
   - 출력: 3줄 `{value} {unit} = {result} {target_unit}`
3. **이번 사이클의 범위를 하나로 제한**한다.
4. **아직 테스트 파일을 만들지 않는다.**
5. **아직 구현하지 않는다.**

## 필수 지시

- **P0 요구사항**부터 다룬다.
  - P0 예: 기존 meter/feet/yard 변환 회귀, `:` 형식 검증, 잘못된 숫자, unknown unit
  - P1 예: 음수 검증, JSON/CSV/table 출력, 설정 파일 로드, 동적 단위 등록
- **한 사이클에 너무 많은 요구사항을 넣지 않는다.**
- **구현 방법이 아니라** 실패해야 할 **동작·입력·기대 결과**를 정의한다.
- 각 행은 Mom Test 증거 또는 README 조항과 연결한다.

## 출력 형식

아래 표를 채워 출력한다.

| Concept | Requirement ID | Requirement | Acceptance Criteria | RED Test Idea | Expected Failure | Evidence |
| ------- | -------------- | ----------- | ------------------- | ------------- | ---------------- | -------- |

### 열 설명

| 열 | 설명 |
| --- | --- |
| Concept | Parser, Validator, Converter, Registry, Formatter, Config Loader, CLI 등 |
| Requirement ID | README 섹션 또는 P0/P1 식별자 |
| Requirement | 요구사항 한 줄 요약 |
| Acceptance Criteria | 통과 조건 (측정 가능) |
| RED Test Idea | pytest 관점의 테스트 아이디어 (파일명·케이스명 수준) |
| Expected Failure | RED 단계에서 예상되는 실패 (미구현 / AssertionError / ImportError 등) |
| Evidence | Mom Test 인용 또는 README 근거 |

## 금지

- `UnitConverter.py` 수정
- 테스트 파일 작성
- 리팩토링·클래스 설계 상세 제안 (REFACTOR 단계로 미룸)
- 한 사이클에 P0·P1·추가 요구사항 전부 포함

## 완료 기준

- 표에 **이번 사이클 범위**만 포함
- 각 행에 **Expected Failure**가 구체적
- 다음 단계 `/red-skeleton` 실행 가능
