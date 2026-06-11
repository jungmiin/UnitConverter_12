"""P1-A Formatter tests — JSON / CSV / TABLE 출력 포맷 (RED skeleton).

RED Test Plan: docs/RED-TEST-PLAN-P1.md § P1-A
  B-FMT-02, B-FMT-03, B-FMT-04
"""

from __future__ import annotations

import json

import pytest

from unit_converter.app.output_formatter import OutputFormat, OutputFormatter
from unit_converter.domain.converter import ConversionResult
from unit_converter.domain.unit_registry import METER_TO_FEET, METER_TO_YARD


def _meter_2_5_results() -> list[ConversionResult]:
    """meter:2.5 golden master fixture (P0 수치 고정)."""
    return [
        ConversionResult(2.5, "meter", 2.5, "meter"),
        ConversionResult(2.5, "meter", 2.5 * METER_TO_FEET, "feet"),
        ConversionResult(2.5, "meter", 2.5 * METER_TO_YARD, "yard"),
    ]


# --- B-FMT-02: JSON 포맷 ---


def test_b_fmt_02_json_output():
    """B-FMT-02: JSON 포맷 — meter:2.5 3건, 파싱 가능·P0 수치 일치."""
    formatter = OutputFormatter()
    results = _meter_2_5_results()

    output = formatter.format(results, OutputFormat.JSON)

    data = json.loads(output)
    assert len(data) == 3
    assert data[0] == {
        "source_value": 2.5,
        "source_unit": "meter",
        "target_value": 2.5,
        "target_unit": "meter",
    }
    assert data[1]["target_unit"] == "feet"
    assert data[1]["target_value"] == pytest.approx(8.2021)
    assert data[2]["target_unit"] == "yard"
    assert data[2]["target_value"] == pytest.approx(2.734025)


# --- B-FMT-03: CSV 포맷 ---


def test_b_fmt_03_csv_output():
    """B-FMT-03: CSV 포맷 — 헤더 + 3데이터 행, P0 수치 일치."""
    formatter = OutputFormatter()
    results = _meter_2_5_results()

    output = formatter.format(results, OutputFormat.CSV)

    lines = output.strip().split("\n")
    assert len(lines) == 4
    assert lines[0] == "source_value,source_unit,target_value,target_unit"
    assert lines[1] == "2.5,meter,2.5,meter"
    assert lines[2] == "2.5,meter,8.2021,feet"
    assert lines[3] == "2.5,meter,2.734025,yard"


# --- B-FMT-04: TABLE 포맷 ---


def test_b_fmt_04_table_output():
    """B-FMT-04: TABLE 포맷 — 헤더·구분선·3데이터 행."""
    formatter = OutputFormatter()
    results = _meter_2_5_results()

    output = formatter.format(results, OutputFormat.TABLE)

    expected = (
        "source_value | source_unit | target_value | target_unit\n"
        "-------------|-------------|--------------|-------------\n"
        "2.5          | meter       | 2.5          | meter\n"
        "2.5          | meter       | 8.2021       | feet\n"
        "2.5          | meter       | 2.734025     | yard"
    )
    assert output == expected
