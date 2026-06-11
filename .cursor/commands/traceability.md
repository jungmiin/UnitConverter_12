# traceability — Concept to Code(C2C) 추적성

**모드**: Ask 또는 Agent (표 작성·갭 분석; 코드 수정은 별도 명령)

## 목적

**Concept → Requirement → Test → Code** 연결을 한 표로 정리한다. PRD·테스트·구현 간 **갭**을 드러낸다.

## 절차

1. README.md 요구사항(P0/P1)을 나열한다.
2. `/red-test-plan`, Golden Master, 기존 테스트 파일을 확인한다.
3. `UnitConverter.py` 및 분리된 모듈의 구현 위치를 매핑한다.
4. 아래 표를 작성한다.
5. **PRD와 연결되지 않는** 테스트·코드, **테스트 없는** 구현을 별도 섹션에 표시한다.

## 출력 형식

| Concept | Requirement ID | Requirement | Acceptance Criteria | Test File | Test Case | Implementation File | Function/Class |
| ------- | -------------- | ----------- | ------------------- | --------- | --------- | ------------------- | -------------- |

### Concept 값 (UnitConverter)

- Parser, Validator, Converter, Registry, Formatter, Config Loader, CLI

### Requirement ID 예시

- `P0-BASIC-CONV` — meter/feet/yard 변환
- `P0-FMT-COLON` — `unit:value` 형식
- `P0-VAL-NUM` — 숫자 검증
- `P0-VAL-UNIT` — unknown unit
- `P1-VAL-NEG` — 음수 검증 (README 품질 요구)
- `P1-OUT-JSON` — JSON 출력
- `P1-CFG-LOAD` — 설정 파일 로드
- `P1-REG-DYN` — 동적 단위 등록

## 갭 분석 (필수 추가 출력)

### PRD 없는 테스트

| Test File | Test Case | 비고 |
| --------- | --------- | ---- |

### 테스트 없는 구현

| Implementation File | Function/Class | Requirement ID (없으면 `UNTRACKED`) |
| ------------------- | -------------- | ----------------------------------- |

### 요구사항 없는 코드

| Location | 설명 |
| -------- | ---- |

## 완료 기준

- P0 행은 **Test + Implementation** 모두 채워지거나 갭으로 명시
- OCP/SRP 분리 후 Concept 열이 **한 책임**에 대응
- 다음 액션: 갭이 RED면 `/red-test-plan`, 구현만 있으면 `/red-skeleton`
