# UnitConverter_12 — RED 테스트 설계 (Test Plan)

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_12 |
| 문서 버전 | 0.1 (초안) |
| 작성일 | 2026-06-11 |
| 단계 | RED — Ask (`/red-test-plan`) |
| 근거 | [PRD.md](PRD.md), Mom Test ([Report/01.REPORT.md](../Report/01.REPORT.md)) |
| 세션 보고서 | [Report/05.REPORT.md](../Report/05.REPORT.md) |

---

## 범위

| 포함 (P0) | 제외 (P1) |
| ---- | ---- |
| meter / feet / yard 변환·정확도 | JSON / YAML 설정 파일 로드 |
| `unit:value` 파싱·검증 (음수·형식·unknown) | 런타임 `1 cubit = 0.4572 meter` 등록 CLI |
| TEXT 3줄 출력 | JSON / CSV / table 출력 포맷 |
| Registry OCP (inch 추가) | ConfigLoader 연동 |
| CLI `run()` golden master | `main()` 대화형 `input()` 루프 (B-CLI-01/02로 대체) |

### 테스트 ID 규칙

| 접두사 | 대상 |
| ------ | ---- |
| `D-*` | Domain / Logic 테스트 |
| `B-*` | Boundary / CLI 테스트 |
| `D-REG-*` | Registry |
| `D-CONV-*` | Converter |
| `B-PARSE-*` | Parser |
| `B-ERR-*` | Error |
| `B-CLI-*` | CLI |

### SC 매핑

| 성공 기준 | 대표 테스트 |
| --------- | ----------- |
| SC-1 수정 지점 한 흐름 | `D-REG-02`, `D-OCP-01` |
| SC-2 입력·출력 비율 일관 | `D-CONV-02`, `D-CONV-03`, `D-CONV-04` |
| SC-3 수동 실행 없이 회귀 | `B-CLI-01`, `B-CLI-02`, `B-FMT-01` |

---

## 1. C2C 추적표

| Concept | Requirement ID | Requirement | Success Criteria | Mom Test Evidence | RED Test Idea |
| ------- | -------------- | ----------- | ---------------- | ----------------- | ------------- |
| Parser | README-5.1-01 | `단위:값` 형식 입력을 unit·value로 분리한다 | `meter:2.5` → unit=`meter`, value=`2.5` | #3: 수동으로 `meter:2.5` 입력 확인 | `B-PARSE-01`: 정상 입력 파싱 |
| Parser | README-5.2-03 | `:` 없는 잘못된 형식을 거부한다 | `meter2.5` 등 → 형식 오류 | #3: 잘못된 입력 수동 확인 | `B-ERR-01`: 형식 오류 거부 |
| Parser | README-5.2-03 | 숫자가 아닌 값을 거부한다 | `meter:abc` → 숫자 오류 | #3: 잘못된 입력 수동 확인 | `B-ERR-04`: 숫자 오류 거부 |
| Parser | README-5.2-01 | 음수 입력을 거부한다 | `meter:-1` → 음수 오류 | #3: 검증 케이스 수동 확인 | `B-ERR-02`: 음수 입력 거부 |
| Registry | README-5.1-02, SC-1 | meter/feet/yard를 등록·조회한다 | `register_defaults()` 후 3단위 조회 가능 | #1: inch 추가 시 3곳 수정 → 한 경로로 통합 | `D-REG-01`, `D-REG-02`: 등록/조회·기본 단위 |
| LengthUnit | README-5.1-04 | meter 기준 to_meter/from_meter 환산 | `1 feet = 1/3.28084 meter` | #2: 입력 분기·출력 계산 비율 일치 | `D-REG-03`: RatioBasedLengthUnit 환산 |
| Converter | README-5.1-03 | 입력값을 등록된 모든 단위로 변환 | `2.5 meter` → feet·yard 포함 전 단위 결과 | #3: `meter:2.5` 수동 확인 | `D-CONV-01`: meter 기준 전체 변환 |
| Converter | README-5.1-04, SC-2 | feet 입력도 meter 경유 후 다른 단위로 변환 | `10 feet` → meter·yard 결과가 동일 비율에서 유도 | #2: feet elif만 수정 시 출력 불일치 | `D-CONV-02`: feet → meter → 타 단위 |
| Converter | README-5.1-04, SC-2 | yard 입력도 meter 경유 변환 | `5 yard` → meter·feet 결과 일관 | #2: 한쪽 비율만 수정 시 불일치 | `D-CONV-03`: yard → meter → 타 단위 |
| Converter | README-5.2-04 | 단위 간 변환 정확도를 테스트로 검증 | 비율 상수 기준 허용 오차 내 일치 | #3: 자동 테스트 부재 | `D-CONV-04`: feet↔yard 교차 변환 정확도 |
| Registry/OCP | README-5.1-03, SC-1 | 새 단위 추가 시 Converter 코드 변경 없이 변환 | inch 등록만으로 inch 변환 가능 | #1: inch 추가 시 elif·출력·비율 3곳 수정 | `D-OCP-01`: inch 등록 후 변환 |
| Formatter | README-5.1-01 | TEXT 포맷 3줄 출력 | `{value} {unit} = {result} {target}` × 3 | #3: `meter:2.5` 출력 수동 확인 | `B-FMT-01`: TEXT 3줄 포맷 |
| CLI | README-5.1-01, SC-3 | CLI 파이프라인 end-to-end 동작 | `run("meter:2.5")` → 기존 3줄 출력 | #3: `python UnitConverter.py` 수동 실행 | `B-CLI-01`: golden master 회귀 |
| CLI | README-5.2-03 | 없는 단위 입력 거부 | `inch:1`(미등록) → unknown unit | #3: 없는 단위 수동 확인 | `B-ERR-03`: unknown unit 거부 |
| CLI | README-5.2-03, SC-3 | 오류 메시지·동작 고정 | 기존 `UnitConverter.py` 메시지와 동일 | #3: 에러 케이스 수동 확인 | `B-CLI-02`: 오류 메시지 회귀 |

---

## 2. Given-When-Then 테스트 설계표

| Test ID | Track | Layer | Target | Given | When | Then | Expected Failure |
| ------- | ----- | ----- | ------ | ----- | ---- | ---- | ---------------- |
| D-REG-02 | SC-1 | Domain | `UnitRegistry.register_defaults()` | 빈 `UnitRegistry` 인스턴스 | `register_defaults()` 호출 후 `all_units()` 조회 | meter·feet·yard 3단위가 등록되어 있고, feet·yard의 `meters_per_unit`이 `1/3.28084`, `1/1.09361` | `NotImplementedError` (register_defaults 미구현) |
| D-REG-01 | SC-1 | Domain | `UnitRegistry` | 빈 레지스트리와 `RatioBasedLengthUnit("inch", 0.0254)` | `register(unit)` 후 `get("inch")` 호출 | 등록한 inch 단위 객체가 반환되고, converter 코드 변경 없이 조회 가능 | `NotImplementedError` (register/get 미구현) |
| D-REG-03 | SC-2 | Domain | `RatioBasedLengthUnit` | `RatioBasedLengthUnit("feet", 1/3.28084)` | `to_meter(10)` 및 `from_meter(3.047943)` 호출 | `to_meter(10) ≈ 3.047943`, `from_meter(3.047943) ≈ 10` (허용 오차 내) | `NotImplementedError` (to_meter/from_meter 미구현) |
| D-CONV-01 | SC-2, SC-3 | Domain | `LengthConverter.convert_to_all()` | 기본 단위가 등록된 `UnitRegistry`와 `LengthConverter` | `convert_to_all(2.5, "meter")` 호출 | meter→feet `≈ 8.2021`, meter→yard `≈ 2.734025` 결과 포함, 소스 단위 meter 제외 또는 포함 정책에 맞는 전체 결과 | `NotImplementedError` (convert_to_all 미구현) |
| D-CONV-02 | SC-2 | Domain | `LengthConverter.convert_to_all()` | 기본 단위 등록된 converter | `convert_to_all(10, "feet")` 호출 | meter `≈ 3.047943`, yard `≈ 3.333` (10÷3.28084×1.09361), feet→meter→yard가 registry 비율 단일 경로에서 유도 | `NotImplementedError` |
| D-CONV-03 | SC-2 | Domain | `LengthConverter.convert()` | 기본 단위 등록된 converter | `convert(5, "yard", "feet")` 호출 | `5 yard → feet ≈ 15.0` (5÷1.09361×3.28084), yard 입력·feet 출력 모두 registry 비율 사용 | `NotImplementedError` |
| D-CONV-04 | SC-2, SC-3 | Domain | `LengthConverter.convert()` | 기본 단위 등록된 converter | `convert(1, "feet", "yard")` 호출 | `1 feet → yard ≈ 0.3333` (1÷3.28084×1.09361), feet/yard 간 비율이 meter 기준으로 일관 | `NotImplementedError` |
| D-OCP-01 | SC-1 | Domain | `LengthConverter` + `UnitRegistry` | 기본 단위 등록 후 `inch`(0.0254 m) 추가 등록, **Converter 클래스 코드 미변경** | `convert_to_all(12, "inch")` 호출 | inch→meter `≈ 0.3048`, inch→feet·yard 결과 반환; converter 소스 diff 없음 | `NotImplementedError` 또는 inch 미등록으로 `None`/예외 |
| B-PARSE-01 | SC-3 | App | `InputParser.parse()` | `InputParser` 인스턴스 | `parse("meter:2.5")` 호출 | `ParsedInput(unit="meter", value=2.5)` 반환 | `NotImplementedError` |
| B-ERR-01 | SC-3 | App | `InputParser.parse()` | `InputParser` 인스턴스 | `parse("meter2.5")` (`:` 없음) 호출 | 형식 오류 예외 발생, 메시지 `"Invalid format. Use unit:value (ex: meter:2.5)"` | `NotImplementedError` 또는 예외 미발생 |
| B-ERR-04 | SC-3 | App | `InputParser.parse()` | `InputParser` 인스턴스 | `parse("meter:abc")` 호출 | 숫자 오류 예외 발생, 메시지 `"Invalid number: abc"` | `NotImplementedError` 또는 예외 미발생 |
| B-ERR-02 | SC-3 | App | `InputParser.parse()` | `InputParser` 인스턴스 | `parse("meter:-1")` 호출 | 음수 오류 예외 발생 (메시지 정책은 GREEN에서 고정) | `NotImplementedError` 또는 음수 허용으로 AssertionError |
| B-ERR-03 | SC-3 | App/CLI | `run()` 또는 parser+registry | 기본 단위만 등록된 파이프라인 | `run("cubit:1")` 또는 unknown unit 파싱 후 변환 시도 | unknown unit 오류, 메시지 `"Unknown unit: cubit"` | `NotImplementedError` 또는 예외 미발생 |
| B-FMT-01 | SC-3 | App | `OutputFormatter.format(TEXT)` | `ConversionResult` 3건 (meter:2.5 기준) | `format(results, OutputFormat.TEXT)` 호출 | `"2.5 meter = 2.5 meter\n2.5 meter = 8.2021 feet\n2.5 meter = 2.734025 yard"` 형태 3줄 | `NotImplementedError` |
| B-CLI-01 | SC-3 | CLI | `run()` | 기본 설정(기본 단위·TEXT 포맷) | `run("meter:2.5")` 호출 | `UnitConverter.py`와 동일한 3줄 출력 문자열 반환 | `NotImplementedError` |
| B-CLI-02 | SC-3 | CLI | `run()` | 기본 설정 | `run("meter2.5")`, `run("meter:abc")`, `run("cubit:1")` 각각 호출 | 각각 형식·숫자·unknown unit 오류 메시지가 `UnitConverter.py`와 일치 | `NotImplementedError` 또는 메시지 불일치 AssertionError |

### 필수 8건 매핑

| 필수 ID | 설계표 위치 |
| ------- | ----------- |
| B-PARSE-01 | §2 행 9 |
| D-CONV-01 | §2 행 4 |
| D-CONV-02 | §2 행 5 |
| B-ERR-01 | §2 행 10 |
| B-ERR-02 | §2 행 12 |
| B-ERR-03 | §2 행 13 |
| D-OCP-01 | §2 행 8 |
| D-REG-01 | §2 행 2 |

---

## 3. 테스트 플랜

| Test ID | Test Name | Test Type | Priority | Why First |
| ------- | --------- | --------- | -------- | --------- |
| D-REG-02 | 기본 단위 register_defaults 등록 | Unit | P0-1 | Converter·OCP 테스트의 전제; 비율 정의 단일 경로(SC-1) 확보 |
| D-REG-03 | RatioBasedLengthUnit meter 환산 | Unit | P0-2 | Registry 데이터의 to_meter/from_meter가 SC-2 비율 일관성 기반 |
| D-REG-01 | 단위 register/get 분리 동작 | Unit | P0-3 | Converter와 registry 책임 분리(SRP) 검증; D-OCP-01 전제 |
| D-CONV-01 | meter 입력 전체 단위 변환 | Unit | P0-4 | 핵심 변환 happy path; README 기본 요구·SC-3 회귀 핵심 |
| D-CONV-02 | feet 입력 meter 경유 변환 | Unit | P0-5 | SC-2 핵심 — 입력 분기·출력이 registry 단일 비율에서 유도 |
| D-CONV-03 | yard → feet 교차 변환 | Unit | P0-6 | SC-2 보완 — yard 입력 경로도 동일 비율 체계 |
| D-CONV-04 | feet ↔ yard 교차 변환 정확도 | Unit | P0-7 | README "각 단위 간 변환 정확도" 요구 |
| D-OCP-01 | inch 추가 시 converter 무수정 변환 | Unit/Design | P0-8 | SC-1 직접 검증 — Mom Test #1 (3곳 수정) 회피 |
| B-PARSE-01 | meter:2.5 정상 파싱 | Unit | P0-9 | CLI·검증 테스트 입력 전제 |
| B-ERR-01 | 콜론 없는 형식 거부 | Unit | P0-10 | README 품질 요구; B-CLI-02와 연결 |
| B-ERR-04 | 비숫자 값 거부 | Unit | P0-11 | README 품질 요구; 기존 baseline 메시지 고정 |
| B-ERR-02 | 음수 입력 거부 | Unit | P0-12 | README 품질 요구 (baseline 미구현 → RED에서 실패 예상) |
| B-ERR-03 | unknown unit 거부 | Integration | P0-13 | README 품질 요구; registry 조회 실패 경로 |
| B-FMT-01 | TEXT 3줄 출력 포맷 | Unit | P0-14 | CLI golden master 전 formatter 계약 고정 |
| B-CLI-01 | run meter:2.5 golden master | Integration | P0-15 | SC-3 — 수동 실행 대체 회귀 고정 |
| B-CLI-02 | run 오류 메시지 golden master | Integration | P0-16 | SC-3 — 에러 케이스 수동 확인 대체 |

**실행 순서:** Domain 기반 (`D-REG` → `D-CONV` → `D-OCP`) → App 경계 (`B-PARSE` → `B-ERR` → `B-FMT`) → CLI 통합 (`B-CLI`).

---

## 4. ECB·Mock 점검

| Test ID | Entity | Control | Boundary | Mock Needed | Reason |
| ------- | ------ | ------- | -------- | ----------- | ------ |
| D-REG-02 | `UnitRegistry` | `register_defaults()`, `all_units()` | 없음 (순수 Domain) | No | 실제 registry·비율 등록 동작 검증 |
| D-REG-01 | `UnitRegistry` | `register()`, `get()` | 없음 | No | 등록/조회 분리는 실 객체로 검증 |
| D-REG-03 | `RatioBasedLengthUnit` | `to_meter()`, `from_meter()` | 없음 | No | 비율 계산 단위 테스트, mock 불필요 |
| D-CONV-01 | `LengthConverter` | `convert_to_all()` | `UnitRegistry`(실제) | No | converter+registry 통합; mock 시 SC-2 검증 무력화 |
| D-CONV-02 | `LengthConverter` | `convert_to_all(10,"feet")` | `UnitRegistry`(실제) | No | feet 입력 경로는 registry 실비율로만 검증 가능 |
| D-CONV-03 | `LengthConverter` | `convert(5,"yard","feet")` | `UnitRegistry`(실제) | No | 교차 변환 정확도는 실제 비율 필요 |
| D-CONV-04 | `LengthConverter` | `convert(1,"feet","yard")` | `UnitRegistry`(실제) | No | meter 기준 간접 비율 일관성 검증 |
| D-OCP-01 | `LengthConverter`, `UnitRegistry` | inch 등록 후 `convert_to_all()` | 없음 | No | OCP는 registry 확장만으로 동작해야 함; mock registry는 의미 상실 |
| B-PARSE-01 | `InputParser` | `parse("meter:2.5")` | 없음 | No | 순수 문자열 파싱, I/O 없음 |
| B-ERR-01 | `InputParser` | `parse("meter2.5")` | 없음 | No | 형식 검증은 parser 단독 책임 |
| B-ERR-04 | `InputParser` | `parse("meter:abc")` | 없음 | No | 숫자 검증은 parser 단독 |
| B-ERR-02 | `InputParser` | `parse("meter:-1")` | 없음 | No | 음수 검증은 parser 단독 (또는 validator 위임 시 해당 클래스) |
| B-ERR-03 | `run()` 파이프라인 | unknown unit 입력 | `UnitRegistry`(실제, cubit 미등록) | No | unknown unit은 registry 실조회 실패로 검증 |
| B-FMT-01 | `OutputFormatter` | `format(results, TEXT)` | `ConversionResult` 리스트(고정 fixture) | No | formatter는 결과 객체만 받음; stdout mock 불필요 |
| B-CLI-01 | `run()` | `run("meter:2.5")` | Parser·Registry·Converter·Formatter (실제 조립) | No | golden master는 전체 파이프라인 실동작 고정; `input()`/`print()` mock 불필요 (`run(raw_input)` 시그니처) |
| B-CLI-02 | `run()` | 오류 입력 3종 | 동일 파이프라인 | No | 오류 메시지 회귀는 실제 예외/반환 정책으로 검증 |

**Mock 정책 요약:** P0 RED 범위 전체에서 **Mock 불필요**. Domain은 실 `UnitRegistry`·실 비율로, CLI는 `run(raw_input: str) -> str` 진입점으로 `input()`/`stdout` 경계를 피한다.

---

## 다음 단계

1. **`/red-skeleton`**: 설계표 16개 테스트 ID 기준으로 실패하는 pytest 스켈레톤 작성
2. **`/green-minimal`**: P0-1~P0-4부터 최소 구현 (Registry → LengthUnit → Converter)
3. **`/golden-master`**: `UnitConverter.py` baseline 출력·에러 메시지 회귀 고정

---

*본 문서는 docs/RED-TEST-PLAN.md — UnitConverter_12 RED 테스트 설계 문서입니다.*
