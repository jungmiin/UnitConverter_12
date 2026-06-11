# golden-master — 기존 동작 회귀 테스트 고정

**모드**: Agent

## 목적

현재 **정상 동작**을 Golden Master로 기록·테스트에 고정한다. 이후 REFACTOR에서 깨지면 안 되는 **계약(contract)** 이 된다.

## 절차

1. 현재 통과하는 핵심 동작을 식별한다.
2. **회귀 테스트**를 추가하거나 기존 테스트를 Golden Master로 문서화한다.
3. meter, feet, yard 변환·오류 입력·CLI 출력을 고정한다.
4. 아래 표를 작성하고 테스트 파일과 연결한다.

## 고정 대상 (UnitConverter)

### 변환 (meter 기준)

- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- 입력 `meter:2.5` → 3줄 출력 (meter, feet, yard 각각)
- 입력 `feet:10`, `yard:1` 등 역방향 입력도 meter 기준으로 일관

### 오류 입력

| 입력 패턴 | 기대 동작 |
| --------- | --------- |
| `:` 없음 | `"Invalid format. Use unit:value (ex: meter:2.5)"` |
| 숫자 아님 | `"Invalid number: {value_str}"` |
| unknown unit | `"Unknown unit: {unit}"` |

### CLI 출력 형식

- `{value} {unit} = {result} {target_unit}` — 3줄
- 프롬프트: `"Insert value for converting (ex: meter:2.5): "`

## 출력 형식

| Behavior | Input | Expected Output/Error | Test File | Reason |
| -------- | ----- | --------------------- | --------- | ------ |

### Behavior 예시

- `meter_to_all_units`
- `feet_to_all_units`
- `invalid_format_no_colon`
- `invalid_number`
- `unknown_unit`

### Reason

- Mom Test: "수정 후 meter/feet/yard를 매번 직접 실행해 확인"
- REFACTOR 안전망
- README 기본 요구사항

## 원칙

- Golden Master 테스트는 **리팩토링 후에도 동일**해야 한다.
- 출력 문자열·에러 메시지 변경은 **의도적 요구 + 테스트 갱신** 없이 금지.
- P1 기능(음수, JSON 출력 등)은 Golden Master에 **아직 포함하지 않음** — 별도 RED 사이클.

## 완료 후 출력

1. Golden Master 표 (위 형식)
2. 추가·수정한 테스트 파일
3. `pytest` 실행 결과 (전부 GREEN)
4. REFACTOR에서 깨지면 안 되는 항목 요약 (3~5줄)
5. 다음 권장 명령: `/refactor-smell`
