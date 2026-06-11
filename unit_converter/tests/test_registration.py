"""P1-B Registration tests — 동적 단위 등록 (RED skeleton).

RED Test Plan: docs/RED-TEST-PLAN-P1.md § P1-B
  B-REG-01, D-REG-04, D-CONV-05
"""

from __future__ import annotations

import pytest

from unit_converter.app.input_parser import InputParser
from unit_converter.domain.converter import LengthConverter
from unit_converter.domain.unit_registry import (
    METER_TO_FEET,
    METER_TO_YARD,
    UnitRegistry,
)
from unit_converter.tests.test_converter import _default_registry, _result_for

CUBIT_TO_METER = 0.4572


# --- B-REG-01: 등록 입력 파싱 ---


def test_b_reg_01_parse_registration_input():
    """B-REG-01: `1 cubit = 0.4572 meter` 등록 입력 파싱."""
    parser = InputParser()

    result = parser.parse_registration("1 cubit = 0.4572 meter")

    assert result.unit == "cubit"
    assert result.base_unit == "meter"
    assert result.ratio == pytest.approx(CUBIT_TO_METER)


# --- D-REG-04: cubit registry 등록 ---


def test_d_reg_04_register_cubit_ratio():
    """D-REG-04: register_ratio로 cubit 등록·조회."""
    registry = _default_registry()

    registry.register_ratio("cubit", CUBIT_TO_METER)

    cubit = registry.get("cubit")
    assert cubit is not None
    assert cubit.meters_per_unit == pytest.approx(CUBIT_TO_METER)


# --- D-CONV-05: cubit 변환 ---


def test_d_conv_05_cubit_conversion_after_registration():
    """D-CONV-05: cubit 등록 후 meter/feet/yard 포함 전 단위 변환."""
    registry = _default_registry()
    registry.register_ratio("cubit", CUBIT_TO_METER)
    converter = LengthConverter(registry)

    results = list(converter.convert_to_all(1, "cubit"))

    assert _result_for(results, "meter").target_value == pytest.approx(CUBIT_TO_METER)
    assert _result_for(results, "feet").target_value == pytest.approx(
        CUBIT_TO_METER * METER_TO_FEET
    )
    assert _result_for(results, "yard").target_value == pytest.approx(
        CUBIT_TO_METER * METER_TO_YARD
    )
    assert _result_for(results, "cubit").target_value == pytest.approx(1)
