"""P1-C ConfigLoader tests — 설정 외부화 (RED skeleton).

RED Test Plan: docs/RED-TEST-PLAN-P1.md § P1-C
  I-CFG-01, I-CFG-02, I-CFG-03, I-CFG-04
"""

from __future__ import annotations

import json

import pytest

from unit_converter.domain.converter import LengthConverter
from unit_converter.domain.unit_registry import (
    FEET_TO_METER,
    YARD_TO_METER,
    UnitRegistry,
)
from unit_converter.infrastructure.config_loader import ConfigLoader, default_units_config
from unit_converter.tests.test_converter import _result_for

CUSTOM_FEET_METERS_PER_UNIT = 0.35


def _default_units_yaml() -> str:
    return (
        "units:\n"
        "  - name: meter\n"
        "    meters_per_unit: 1.0\n"
        f"  - name: feet\n"
        f"    meters_per_unit: {FEET_TO_METER}\n"
        f"  - name: yard\n"
        f"    meters_per_unit: {YARD_TO_METER}\n"
    )


def _custom_feet_config() -> dict:
    """I-CFG-04: feet 비율만 기본과 다르게 설정."""
    return {
        "units": [
            {"name": "meter", "meters_per_unit": 1.0},
            {"name": "feet", "meters_per_unit": CUSTOM_FEET_METERS_PER_UNIT},
            {"name": "yard", "meters_per_unit": YARD_TO_METER},
        ]
    }


# --- I-CFG-01: JSON config 로드 ---


def test_i_cfg_01_load_json_config(tmp_path):
    """I-CFG-01: JSON 설정 파일 로드 — units 3건 반환."""
    config_path = tmp_path / "units.json"
    config_path.write_text(json.dumps(default_units_config()), encoding="utf-8")
    loader = ConfigLoader()

    config = loader.load_from_file(config_path)

    assert isinstance(config, dict)
    assert "units" in config
    assert len(config["units"]) == 3
    names = {unit["name"] for unit in config["units"]}
    assert names == {"meter", "feet", "yard"}


# --- I-CFG-02: YAML config 로드 ---


def test_i_cfg_02_load_yaml_config(tmp_path):
    """I-CFG-02: YAML 설정 파일 로드 — JSON과 동등 구조."""
    config_path = tmp_path / "units.yaml"
    config_path.write_text(_default_units_yaml(), encoding="utf-8")
    loader = ConfigLoader()

    config = loader.load_from_file(config_path)

    assert isinstance(config, dict)
    assert "units" in config
    assert len(config["units"]) == 3
    names = {unit["name"] for unit in config["units"]}
    assert names == {"meter", "feet", "yard"}
    feet = next(u for u in config["units"] if u["name"] == "feet")
    assert feet["meters_per_unit"] == pytest.approx(FEET_TO_METER)


# --- I-CFG-03: config → registry ---


def test_i_cfg_03_apply_to_registry():
    """I-CFG-03: 설정을 Registry에 반영 — 3기본 단위, P0 feet 비율."""
    loader = ConfigLoader()
    registry = UnitRegistry()

    loader.apply_to_registry(default_units_config(), registry)

    units = {unit.name: unit for unit in registry.all_units()}
    assert set(units) == {"meter", "feet", "yard"}
    assert units["meter"].meters_per_unit == pytest.approx(1.0)
    assert units["feet"].meters_per_unit == pytest.approx(FEET_TO_METER)
    assert units["yard"].meters_per_unit == pytest.approx(YARD_TO_METER)


# --- I-CFG-04: 커스텀 비율이 변환에 반영 ---


def test_i_cfg_04_custom_feet_ratio_affects_conversion():
    """I-CFG-04: config feet 비율 변경 → convert_to_all(10, feet) meter 결과 변경."""
    loader = ConfigLoader()
    registry = UnitRegistry()
    loader.apply_to_registry(_custom_feet_config(), registry)
    converter = LengthConverter(registry)

    results = list(converter.convert_to_all(10, "feet"))
    meter_result = _result_for(results, "meter")

    assert meter_result.target_value == pytest.approx(10 * CUSTOM_FEET_METERS_PER_UNIT)
    assert meter_result.target_value != pytest.approx(10 * FEET_TO_METER)
