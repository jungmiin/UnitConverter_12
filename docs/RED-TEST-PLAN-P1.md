# UnitConverter_12 — RED 테스트 설계 (P1 Test Plan)

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_12 |
| 문서 버전 | 0.1 (초안) |
| 작성일 | 2026-06-11 |
| 단계 | RED — Ask (`/red-test-plan`) |
| 근거 | [PRD.md §5.3](PRD.md), [README.md §추가 요구사항](../README.md), Mom Test ([Report/01.REPORT.md](../Report/01.REPORT.md)) |
| 전제 | P0 완료 — pytest 22 passed, `docs/RED-TEST-PLAN.md` 범위 GREEN |

---

## 범위

| 포함 (P1) | 제외 |
| ---- | ---- |
| JSON / CSV / table 출력 포맷 선택 | P0 TEXT golden master 변경 (기본값 TEXT 유지) |
| 런타임 `1 cubit = 0.4572 meter` 단위·비율 등록 | `main()` 대화형 `input()` 루프 직접 테스트 |
| JSON / YAML 설정 파일에서 비율 로드 | 네트워크·원격 설정, GUI |
| ConfigLoader → Registry 단일 경로 연동 | 비-P1 단위 카테고리(질량·온도 등) |

### 사이클 분할 (한 RED 사이클 = 하나의 기능 흐름)

| 사이클 | 범위 | 대표 테스트 | 선행 조건 |
| ------ | ---- | ----------- | --------- |
| **P1-A** | 출력 포맷 (JSON / CSV / TABLE) | `B-FMT-02`~`04`, `B-CLI-05` | P0 GREEN (`OutputFormatter` TEXT 구현됨) |
| **P1-B** | 동적 단위 등록 | `B-REG-01`, `D-REG-04`, `D-CONV-05`, `B-CLI-06` | P0 GREEN (`UnitRegistry.register`) |
| **P1-C** | 설정 외부화 (JSON / YAML) | `I-CFG-01`~`04`, `B-CLI-07` | P1-B 권장 (등록 스키마·Registry 적용 패턴 확정 후) |

> **첫 `/red-skeleton` 권장:** **P1-A** — `cli.run()`이 이미 `output_format` 인자를 받으며, P0 TEXT 회귀와 독립적이다.

### 테스트 ID 규칙

| 접두사 | 대상 |
| ------ | ---- |
| `B-FMT-*` | Formatter 출력 포맷 |
| `B-REG-*` | 동적 등록 입력 파싱 |
| `D-REG-*` | Registry 확장 |
| `D-CONV-*` | 등록·설정 반영 후 변환 |
| `I-CFG-*` | ConfigLoader (Infrastructure) |
| `B-CLI-*` | CLI end-to-end (P1) |

### SC 매핑

| 성공 기준 | P1 대표 테스트 |
| --------- | -------------- |
| SC-1 수정 지점 한 흐름 | `D-REG-04`, `I-CFG-03` — cubit·설정 단위가 Registry 한 경로만 수정 |
| SC-2 입력·출력 비율 일관 | `D-CONV-05`, `I-CFG-04` — 등록·설정 비율이 Converter 출력과 동일 경로 |
| SC-3 수동 실행 없이 회귀 | `B-CLI-05`~`07`, `B-FMT-02`~`04` — 포맷·등록·설정 케이스 자동 고정 |

---

## 1. C2C 추적표 (P1)

| Concept | Requirement ID | Requirement | Acceptance Criteria | RED Test Idea | Expected Failure | Evidence |
| ------- | -------------- | ----------- | ------------------- | ------------- | ---------------- | -------- |
| Formatter | P1-OUT-JSON | 변환 결과를 JSON으로 출력한다 | `meter:2.5` 결과가 파싱 가능한 JSON 배열; 각 항목에 source/target unit·value 포함; P0 수치와 일치 | `B-FMT-02`: `format(results, JSON)` — meter:2.5 3건 | `NotImplementedError` (JSON 분기 미구현) | README 추가-출력포맷; Mom Test Q10: `print` 하드코딩 → Formatter 경계 필요 |
| Formatter | P1-OUT-CSV | 변환 결과를 CSV로 출력한다 | 헤더 행 + 데이터 행; `meter:2.5` 3건; 쉼표 구분·수치 P0와 일치 | `B-FMT-03`: `format(results, CSV)` | `NotImplementedError` (CSV 분기 미구현) | README 추가-출력포맷; PRD §5.3 |
| Formatter | P1-OUT-TABLE | 변환 결과를 표(table) 형태로 출력한다 | 정렬된 열 헤더·구분선·3 데이터 행; 가독 가능한 고정 폭 또는 탭 구분 | `B-FMT-04`: `format(results, TABLE)` | `NotImplementedError` (TABLE 분기 미구현) | README 추가-출력포맷; Mom Test Q10 |
| Formatter | P0-FMT-TEXT (회귀) | 기본 TEXT 포맷은 P0 golden master 유지 | `run("meter:2.5")` 기본 호출 시 P0 3줄 문자열 불변 | `B-CLI-05a`: `run("meter:2.5")` — P0 출력 동일 | (회귀 실패 시) AssertionError — P1 구현이 TEXT 기본값 깨뜨림 | SC-3; `B-CLI-01` golden master |
| CLI | P1-OUT-JSON | CLI에서 JSON 포맷 end-to-end | `run("meter:2.5", OutputFormat.JSON)` → 유효 JSON, 3건, 수치 P0 일치 | `B-CLI-05`: JSON end-to-end | `NotImplementedError` 또는 JSON 파싱 실패 | SC-3; Mom Test #3: 수동 확인 대체 |
| Parser | P1-REG-DYN | `1 cubit = 0.4572 meter` 등록 입력을 파싱한다 | 단위명 `cubit`, 기준 `meter`, 비율 `0.4572` 추출; 공백·소수 허용 범위는 GREEN에서 고정 | `B-REG-01`: `parse_registration("1 cubit = 0.4572 meter")` | `NotImplementedError` / `AttributeError` (등록 파서 없음) | README 추가-동적등록; Mom Test Q12: cubit 런타임 등록 불가 |
| Registry | P1-REG-DYN | 파싱된 비율로 단위를 등록한다 | `register_ratio("cubit", 0.4572)` 후 `get("cubit")` 반환; Converter 코드 변경 없음 | `D-REG-04`: cubit 등록·조회 | cubit `None` 또는 `NotImplementedError` | SC-1; Mom Test #1: 단위 추가 다발 수정 회피 |
| Converter | P1-REG-DYN | 등록된 cubit으로 변환한다 | `cubit:1` → meter `≈ 0.4572`, feet·yard 포함 전 단위; meter 기준 단일 경로 | `D-CONV-05`: `convert_to_all(1, "cubit")` (사전 등록) | `Unknown unit: cubit` 또는 `NotImplementedError` | SC-2; README `1 cubit = 0.4572 meter` |
| CLI | P1-REG-DYN | 등록 후 변환 end-to-end | `1 cubit = 0.4572 meter` 입력 → 등록 성공; 이어 `cubit:1` 변환 성공 (TEXT 3줄+) | `B-CLI-06`: 등록 + `cubit:1` 파이프라인 | `Unknown unit: cubit` (등록 미반영) | README 추가-동적등록; SC-3 |
| Config Loader | P1-CFG-LOAD | JSON 설정 파일을 로드한다 | 유효 JSON 경로 → `dict` 반환; `units` 항목에 meter/feet/yard 비율 포함 | `I-CFG-01`: `load_from_file(units.json)` | `NotImplementedError` | README 추가-설정외부화; Mom Test: 비율 함수 본문 박힘 |
| Config Loader | P1-CFG-LOAD | YAML 설정 파일을 로드한다 | 유효 YAML 경로 → JSON과 동등한 구조 `dict` 반환 | `I-CFG-02`: `load_from_file(units.yaml)` | `NotImplementedError` | README 추가-설정외부화 |
| Config Loader | P1-CFG-LOAD | 설정을 Registry에 반영한다 | `apply_to_registry(config, registry)` 후 `all_units()`에 3기본 단위; 비율 P0 상수와 일치 | `I-CFG-03`: apply 후 registry 조회 | `NotImplementedError` 또는 feet/yard 비율 불일치 | SC-1; 비율 단일 경로 (ConfigLoader 또는 register_defaults) |
| Config Loader | P1-CFG-LOAD | 설정 비율 변경이 변환 결과에 반영된다 | config에서 feet 비율 변경 시 `feet:10` 출력이 변경된 비율에서 유도; Converter 미수정 | `I-CFG-04`: 커스텀 feet 비율 config → `convert_to_all(10,"feet")` | 기본 비율 결과 반환 (설정 미반영) AssertionError | SC-2; Mom Test #2 |
| CLI | P1-CFG-LOAD | 설정 기반 파이프라인 end-to-end | 기본 config 로드 후 `run("meter:2.5")` → P0 golden master와 동일 TEXT 출력 | `B-CLI-07`: config 경로 주입 파이프라인 | P0와 다른 출력 또는 `NotImplementedError` | SC-3; README 설정 외부화 |

---

## 2. Given-When-Then 테스트 설계표

| Test ID | Track | Layer | Target | Given | When | Then | Expected Failure |
| ------- | ----- | ----- | ------ | ----- | ---- | ---- | ---------------- |
| B-FMT-02 | SC-3 | App | `OutputFormatter.format(JSON)` | `ConversionResult` 3건 (meter:2.5, P0 수치) | `format(results, OutputFormat.JSON)` 호출 | `json.loads(output)` 성공; 길이 3; 각 항목 source/target 필드·수치 P0 일치 | `NotImplementedError` |
| B-FMT-03 | SC-3 | App | `OutputFormatter.format(CSV)` | 동일 3건 fixture | `format(results, OutputFormat.CSV)` 호출 | 1행 헤더 + 3데이터 행; `2.5,meter,...` 형태; 수치 P0 일치 | `NotImplementedError` |
| B-FMT-04 | SC-3 | App | `OutputFormatter.format(TABLE)` | 동일 3건 fixture | `format(results, OutputFormat.TABLE)` 호출 | 헤더·구분선·3행 포함; 3건 변환 내용 가독 가능 | `NotImplementedError` |
| B-CLI-05a | SC-3 | CLI | `run()` 기본 TEXT 회귀 | P0 GREEN 파이프라인 | `run("meter:2.5")` (기본 포맷) | `B-CLI-01`과 동일 3줄 문자열 | AssertionError (P1이 기본값 깨뜨림) |
| B-CLI-05 | SC-3 | CLI | `run(..., JSON)` | 기본 파이프라인 | `run("meter:2.5", OutputFormat.JSON)` | 유효 JSON; 3건; meter/feet/yard 수치 P0 일치 | `NotImplementedError` |
| B-REG-01 | SC-1 | App | 등록 입력 파서 | `InputParser` 또는 전용 `RegistrationParser` | `parse("1 cubit = 0.4572 meter")` | `unit="cubit"`, `base_unit="meter"`, `ratio=0.4572` (또는 동등 DTO) | `NotImplementedError` / `AttributeError` |
| D-REG-04 | SC-1 | Domain | `UnitRegistry` + cubit | 빈 registry 또는 기본 등록 후 | `register_ratio("cubit", 0.4572)` (또는 `register(RatioBasedLengthUnit(...))`) | `get("cubit")` non-None; `meters_per_unit == 0.4572` | cubit 미등록 / `NotImplementedError` |
| D-CONV-05 | SC-2 | Domain | `LengthConverter` + cubit | cubit(0.4572 m) 등록된 registry | `convert_to_all(1, "cubit")` | meter `≈ 0.4572`; feet·yard가 registry 단일 비율에서 유도 | `Unknown unit: cubit` |
| B-CLI-06 | SC-1, SC-3 | CLI | 등록 + 변환 파이프라인 | 기본 파이프라인 | `run("1 cubit = 0.4572 meter")` 후 `run("cubit:1")` (또는 단일 세션 API) | 등록 성공; `cubit:1` TEXT 출력에 meter `≈ 0.4572` 포함 | `Unknown unit: cubit` |
| I-CFG-01 | SC-1 | Infra | `ConfigLoader.load_from_file` | `units.json` fixture (meter/feet/yard 비율) | `load_from_file(path)` | `dict` 반환; `units` 키에 3단위 정의 | `NotImplementedError` |
| I-CFG-02 | SC-1 | Infra | `ConfigLoader.load_from_file` | `units.yaml` 동등 fixture | `load_from_file(path)` | `I-CFG-01`과 동등 구조 | `NotImplementedError` |
| I-CFG-03 | SC-1 | Infra | `ConfigLoader.apply_to_registry` | `I-CFG-01` 반환 config, 빈 `UnitRegistry` | `apply_to_registry(config, registry)` | `all_units()` 3건; feet `meters_per_unit ≈ 1/3.28084` | `NotImplementedError` |
| I-CFG-04 | SC-2 | Infra+Domain | config 비율 → 변환 | feet 비율을 기본과 다른 config | apply 후 `convert_to_all(10, "feet")` | meter 결과가 **변경된** config 비율에서 유도 (기본값과 다름) | 기본 P0 비율 결과 → AssertionError |
| B-CLI-07 | SC-3 | CLI | config 기반 `run()` | `units.json` 기본 비율 fixture | config 로드 파이프라인으로 `run("meter:2.5")` | `B-CLI-01`과 동일 TEXT 출력 | 출력 불일치 / `NotImplementedError` |

---

## 3. 테스트 플랜 (우선순위)

| Test ID | Test Name | Test Type | Priority | Cycle | Why First |
| ------- | --------- | --------- | -------- | ----- | --------- |
| B-FMT-02 | JSON 포맷 formatter | Unit | P1-A-1 | A | 포맷 계약 고정; CLI 통합 전 Formatter 단독 검증 |
| B-FMT-03 | CSV 포맷 formatter | Unit | P1-A-2 | A | 동일 fixture로 포맷 분기만 추가 |
| B-FMT-04 | TABLE 포맷 formatter | Unit | P1-A-3 | A | README 3포맷 완성 |
| B-CLI-05a | TEXT 기본값 회귀 | Integration | P1-A-4 | A | P0 golden master 보호 (P1 구현 전 선행 RED 가능) |
| B-CLI-05 | JSON end-to-end | Integration | P1-A-5 | A | SC-3 — 포맷 선택 CLI 검증 |
| B-REG-01 | 등록 입력 파싱 | Unit | P1-B-1 | B | 동적 등록 입력 계약 |
| D-REG-04 | cubit registry 등록 | Unit | P1-B-2 | B | SC-1 — Registry 한 경로 확장 |
| D-CONV-05 | cubit 변환 | Unit | P1-B-3 | B | SC-2 — 등록 비율 → 변환 일관 |
| B-CLI-06 | 등록+변환 end-to-end | Integration | P1-B-4 | B | README 동적 등록 시나리오 완성 |
| I-CFG-01 | JSON config 로드 | Unit | P1-C-1 | C | 설정 외부화 진입점 |
| I-CFG-02 | YAML config 로드 | Unit | P1-C-2 | C | README YAML 요구 |
| I-CFG-03 | config → registry | Unit | P1-C-3 | C | SC-1 — 비율 단일 경로를 파일로 이전 |
| I-CFG-04 | 커스텀 비율 변환 반영 | Integration | P1-C-4 | C | SC-2 — 설정 변경이 출력에 반영 |
| B-CLI-07 | config 파이프라인 E2E | Integration | P1-C-5 | C | SC-3 — 설정 로드 회귀 고정 |

**실행 순서 (사이클별):**

- **P1-A:** `B-FMT-02` → `03` → `04` → `B-CLI-05a` → `B-CLI-05`
- **P1-B:** `B-REG-01` → `D-REG-04` → `D-CONV-05` → `B-CLI-06`
- **P1-C:** `I-CFG-01` → `02` → `03` → `04` → `B-CLI-07`

---

## 4. ECB·Mock 점검

| Test ID | Entity | Control | Boundary | Mock Needed | Reason |
| ------- | ------ | ------- | -------- | ----------- | ------ |
| B-FMT-02~04 | `OutputFormatter` | `format(results, fmt)` | `ConversionResult` fixture | No | 포맷 문자열만 검증; stdout 불필요 |
| B-CLI-05a, 05 | `run()` | `output_format` 인자 | 전체 파이프라인 (실제) | No | golden master는 실조립 고정 |
| B-REG-01 | Parser | 등록 문자열 | 없음 | No | 순수 문자열 파싱 |
| D-REG-04 | `UnitRegistry` | `register` / ratio API | 없음 | No | OCP는 실 registry로 검증 |
| D-CONV-05 | `LengthConverter` | `convert_to_all` | 실제 cubit 등록 registry | No | SC-2 mock 시 비율 일관성 무력화 |
| B-CLI-06 | `run()` | 등록·변환 2단계 | 실제 파이프라인 | No | 동적 등록은 통합에서만 의미 |
| I-CFG-01~02 | `ConfigLoader` | `load_from_file` | `tmp_path` fixture 파일 | No | 실제 파일 I/O; mock 파일 시 스키마 검증 약화 |
| I-CFG-03~04 | `ConfigLoader` + `UnitRegistry` | `apply_to_registry` | 실제 config dict | No | Registry 반영은 실객체 필요 |
| B-CLI-07 | config 파이프라인 | config 경로 주입 `run` | 실제 JSON fixture | No | 설정 E2E는 실로드 고정 |

**Mock 정책 요약:** P1 RED 범위 전체에서 **Mock 불필요**. 설정 파일은 pytest `tmp_path` fixture로 실파일 생성.

---

## 5. 설정 fixture 스키마 (RED 계약 — GREEN에서 구현)

테스트 작성 시 아래 최소 스키마를 fixture로 고정한다. (구현 상세는 GREEN 단계)

```json
{
  "units": [
    { "name": "meter", "meters_per_unit": 1.0 },
    { "name": "feet", "meters_per_unit": 0.3048 },
    { "name": "yard", "meters_per_unit": 0.9144 }
  ]
}
```

> `I-CFG-04` 전용: feet `meters_per_unit`을 기본(`1/3.28084`)과 **다른 값**으로 둔 별도 fixture 사용.

---

## 다음 단계

1. **`/red-skeleton` (P1-A)**: `B-FMT-02`~`04`, `B-CLI-05a`, `B-CLI-05` 실패 pytest 스켈레톤 (`test_formatter.py` 신규 또는 `test_cli.py` 확장)
2. **`/green-minimal` (P1-A)**: `OutputFormatter` JSON/CSV/TABLE 최소 구현
3. **P1-B → P1-C**: 동일 ARRR 루프 반복

---

*본 문서는 docs/RED-TEST-PLAN-P1.md — UnitConverter_12 P1 RED 테스트 설계 문서입니다.*
