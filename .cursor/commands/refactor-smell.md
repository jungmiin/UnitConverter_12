# refactor-smell — 리팩토링 후보 분석

**모드**: Ask (코드 수정 금지)

## 목적

현재 `UnitConverter.py`와 테스트를 읽고 **스멜만** 분석한다. OCP/SRP 위반·테스트 공백·안전한 리팩토링 순서를 제안한다.

## 절차

1. **`UnitConverter.py`를 직접 수정하지 않는다.**
2. `main()` 및 관련 코드의 책임 혼합을 분석한다.
3. OCP/SRP 위반 가능성을 찾는다.
4. **테스트로 보호된 부분**과 **보호되지 않은 부분**을 구분한다.
5. Golden Master 테스트가 커버하는 동작을 명시한다.
6. **안전한 리팩토링 순서**를 제안한다 (한 번에 하나).

## 스멜 분류 (체크리스트)

- Parser 책임 혼합 — `split(':', 1)`, `float()` 변환이 `main()`에 있음
- Converter 책임 혼합 — 단위별 meter 환산·타 단위 계산이 `main()`에 있음
- Formatter 책임 혼합 — `print(f"...")` 3줄이 변환 로직과 인접
- Registry 부재 — meter/feet/yard가 `if/elif` 하드코딩
- Config Loader 부재 — 비율 `3.28084`, `1.09361`이 코드에 중복
- if/elif 단위 분기 증가 — 새 단위마다 elif 추가 위험
- CLI와 비즈니스 로직 결합 — `input()`/`print()`와 변환이 한 함수
- 테스트하기 어려운 함수 구조 — `main()`만 있고 순수 함수 부재

## 출력 형식

| Smell | Location | Why It Matters | Related Test | Safe Refactor Plan |
| ----- | -------- | -------------- | ------------ | ------------------ |

### 열 설명

| 열 | 설명 |
| --- | --- |
| Smell | 위 분류 중 해당 항목 |
| Location | 파일·함수·대략적 줄 |
| Why It Matters | Mom Test·OCP/SRP·회귀 위험 연결 |
| Related Test | Golden Master 또는 RED 테스트 파일/케이스 |
| Safe Refactor Plan | **한 단계** 추출 순서 (예: Parser 함수 분리만) |

## 안전한 리팩토링 순서 (권장 예)

1. 순수 함수로 변환 계산 추출 (CLI 분리 전)
2. Parser 추출 (`unit`, `value` 파싱)
3. Registry 또는 비율 dict 도입 (elif 제거)
4. Formatter 추출 (출력 3줄)
5. Config Loader (README P1 — 별도 사이클)
6. CLI `main()`은 조립만

## 금지

- 코드 수정·테스트 수정
- 한 번에 Parser+Registry+Formatter+Config 일괄 설계
- Golden Master 범위 밖 동작 변경 제안

## 완료 기준

- 표에 **우선순위**가 드러남 (테스트 커버 있는 항목 우선)
- 각 `Safe Refactor Plan`이 `/refactor-safe`에서 **한 diff**로 실행 가능
- 다음 권장 명령: `/refactor-safe` (표에서 승인할 항목 지정)
