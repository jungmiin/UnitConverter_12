# refactor-safe — 테스트 유지 안전 리팩토링

**모드**: Agent

## 목적

`/refactor-smell` 표에서 **승인된 항목만** 수행한다. 외부 동작·CLI 계약은 Golden Master 테스트로 보호한다.

## 절차

1. `/refactor-smell` 표에서 **이번에 수행할 한 항목**만 선택한다.
2. **리팩토링 전** `pytest` 전체 실행 → 결과 기록.
3. **구조만** 변경한다 (이름 추출, 모듈 분리, elif → registry 등).
4. **리팩토링 후** `pytest` 전체 실행 → 결과 기록.
5. 외부 동작 변경 여부를 명시적으로 판단한다.

## 필수 원칙

- **한 번에 하나의 Smell**만 처리한다.
- **외부 동작, 출력 문자열, 에러 메시지, exit code를 바꾸지 않는다.**
- 기능 추가(P1: JSON 출력, 설정 로드, 동적 등록)는 **금지** — REFACTOR가 아님.
- 테스트 실패 시 **즉시 중단**하고 원인 분류 (`/test-loop` 참고).

## 필수 출력

1. **리팩토링 전 테스트 결과** — passed/failed/skipped
2. **변경한 파일** — 경로 목록
3. **변경한 구조** — 추출한 함수/클래스/모듈 한 줄 설명
4. **리팩토링 후 테스트 결과** — passed/failed/skipped
5. **외부 동작 변경 여부** — `없음` 또는 `있음 (중단·롤백 필요)`

## 실패 시 원인 분류

| 분류 | 조치 |
| ---- | ---- |
| Golden Master 깨짐 | 롤백 또는 출력/메시지 의도 확인 — REFACTOR 범위 위반 |
| 테스트 import 깨짐 | import 경로만 수정 (동작 동일) |
| 구조 변경 과다 | 한 Smell만 남기고 나머지 되돌림 |
| 커버 부족 | `/golden-master` 보강 후 재시도 |

## UnitConverter REFACTOR 예시 (승인 시에만)

- `parse_input(s) -> (unit, value)` 추출
- `to_meters(unit, value)` / `from_meters(meter_value)` 추출
- `UNITS` dict 또는 Registry 클래스로 elif 제거
- `format_lines(value, unit, results) -> list[str]` 추출
- `main()`은 parse → convert → format → print 조립만

## 금지

- smell 표에 없는 대규모 재작성
- 테스트 삭제·skip·기대값 약화
- 비율 상수 변경
- README P1 기능 선구현

## 완료 기준

- 리팩토링 전후 테스트 **동일하게 전부 GREEN**
- 외부 동작 변경 **없음**
- 다음 권장: `/traceability` 또는 `/refactor-smell` (다음 Smell)
