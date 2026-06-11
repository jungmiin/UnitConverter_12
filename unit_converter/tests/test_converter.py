"""Domain-level tests — 변환 로직 검증."""

from __future__ import annotations

import pytest

from unit_converter.domain.converter import ConversionResult, LengthConverter
from unit_converter.domain.length_unit import RatioBasedLengthUnit
from unit_converter.domain.unit_registry import UnitRegistry

FEET_TO_METER = 1 / 3.28084
YARD_TO_METER = 1 / 1.09361
METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361


def _default_registry() -> UnitRegistry:
    registry = UnitRegistry()
    registry.register_defaults()
    return registry


def _result_for(results: list[ConversionResult], target_unit: str) -> ConversionResult:
    for result in results:
        if result.target_unit == target_unit:
            return result
    raise AssertionError(f"No result for target unit: {target_unit}")


# --- D-REG-02: 기본 단위 register_defaults 등록 ---


def test_d_reg_02_register_defaults():
    """D-REG-02: register_defaults() 후 meter/feet/yard 3단위 등록."""
    registry = UnitRegistry()
    registry.register_defaults()

    units = {unit.name: unit for unit in registry.all_units()}
    assert set(units) == {"meter", "feet", "yard"}
    assert units["meter"].meters_per_unit == pytest.approx(1.0)
    assert units["feet"].meters_per_unit == pytest.approx(FEET_TO_METER)
    assert units["yard"].meters_per_unit == pytest.approx(YARD_TO_METER)


# --- D-REG-01: 단위 register/get 분리 동작 ---


def test_d_reg_01_register_and_get():
    """D-REG-01: register/get으로 단위 등록·조회가 converter와 분리되어 동작."""
    registry = UnitRegistry()
    inch = RatioBasedLengthUnit(name="inch", meters_per_unit=0.0254)

    registry.register(inch)
    retrieved = registry.get("inch")

    assert retrieved is inch
    assert retrieved.name == "inch"


# --- D-REG-03: RatioBasedLengthUnit meter 환산 ---


def test_d_reg_03_ratio_based_length_unit_conversion():
    """D-REG-03: RatioBasedLengthUnit to_meter/from_meter 환산."""
    feet = RatioBasedLengthUnit(name="feet", meters_per_unit=FEET_TO_METER)

    assert feet.to_meter(10) == pytest.approx(10 * FEET_TO_METER)
    assert feet.from_meter(10 * FEET_TO_METER) == pytest.approx(10)


# --- D-CONV-01: meter 입력 전체 단위 변환 ---


def test_d_conv_01_meter_to_all_units():
    """D-CONV-01: 2.5 meter를 feet/yard 등 모든 등록 단위로 변환."""
    converter = LengthConverter(_default_registry())

    results = list(converter.convert_to_all(2.5, "meter"))

    assert _result_for(results, "meter").target_value == pytest.approx(2.5)
    assert _result_for(results, "feet").target_value == pytest.approx(2.5 * METER_TO_FEET)
    assert _result_for(results, "yard").target_value == pytest.approx(2.5 * METER_TO_YARD)


# --- D-CONV-02: feet 입력 meter 경유 변환 ---


def test_d_conv_02_feet_via_meter_to_other_units():
    """D-CONV-02: 10 feet를 meter 기준으로 변환 후 다른 단위로 변환."""
    converter = LengthConverter(_default_registry())

    results = list(converter.convert_to_all(10, "feet"))

    assert _result_for(results, "meter").target_value == pytest.approx(10 * FEET_TO_METER)
    assert _result_for(results, "feet").target_value == pytest.approx(10)
    assert _result_for(results, "yard").target_value == pytest.approx(
        10 * FEET_TO_METER * METER_TO_YARD
    )


# --- D-CONV-03: yard → feet 교차 변환 ---


def test_d_conv_03_yard_to_feet():
    """D-CONV-03: 5 yard를 feet로 변환 (meter 경유)."""
    converter = LengthConverter(_default_registry())

    result = converter.convert(5, "yard", "feet")

    assert result.target_unit == "feet"
    assert result.target_value == pytest.approx(5 * YARD_TO_METER * METER_TO_FEET)


# --- D-CONV-04: feet ↔ yard 교차 변환 정확도 ---


def test_d_conv_04_feet_to_yard_accuracy():
    """D-CONV-04: 1 feet → yard, meter 기준 비율 일관성."""
    converter = LengthConverter(_default_registry())

    result = converter.convert(1, "feet", "yard")

    assert result.target_unit == "yard"
    assert result.target_value == pytest.approx(1 * FEET_TO_METER * METER_TO_YARD)


# --- D-OCP-01: inch 추가 시 converter 무수정 변환 ---


def test_d_ocp_01_new_unit_without_converter_change():
    """D-OCP-01: registry에 inch 등록만으로 converter 코드 변경 없이 변환."""
    registry = _default_registry()
    registry.register(RatioBasedLengthUnit(name="inch", meters_per_unit=0.0254))
    converter = LengthConverter(registry)

    results = list(converter.convert_to_all(12, "inch"))

    assert _result_for(results, "meter").target_value == pytest.approx(12 * 0.0254)
    assert _result_for(results, "feet").target_value == pytest.approx(12 * 0.0254 * METER_TO_FEET)
    assert _result_for(results, "yard").target_value == pytest.approx(12 * 0.0254 * METER_TO_YARD)
    assert _result_for(results, "inch").target_value == pytest.approx(12)
