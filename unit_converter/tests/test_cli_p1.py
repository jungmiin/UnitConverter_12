"""P1 CLI tests — 출력 포맷(P1-A), 동적 등록(P1-B), 설정(P1-C) end-to-end.

RED Test Plan: docs/RED-TEST-PLAN-P1.md
  P1-A: B-CLI-05a, B-CLI-05
  P1-B: B-CLI-06
  P1-C: B-CLI-07
"""

from __future__ import annotations

import json

import pytest

from unit_converter.app.output_formatter import OutputFormat
from unit_converter.cli import run
from unit_converter.tests.test_config_loader import _default_units_config


# --- B-CLI-05a: TEXT 기본값 회귀 (P0 golden master 보호) ---


def test_b_cli_05a_text_default_regression():
    """B-CLI-05a: run() 기본 TEXT — B-CLI-01과 동일 3줄 유지."""
    output = run("meter:2.5")

    expected = (
        "2.5 meter = 2.5 meter\n"
        "2.5 meter = 8.2021 feet\n"
        "2.5 meter = 2.734025 yard"
    )
    assert output == expected


# --- B-CLI-05: JSON end-to-end ---


def test_b_cli_05_json_end_to_end():
    """B-CLI-05: run('meter:2.5', JSON) — 유효 JSON 3건, P0 수치 일치."""
    output = run("meter:2.5", OutputFormat.JSON)

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


# --- B-CLI-06: 등록 + 변환 end-to-end (P1-B) ---


def test_b_cli_06_register_then_convert():
    """B-CLI-06: `1 cubit = 0.4572 meter` 등록 후 cubit:1 변환 성공."""
    run("1 cubit = 0.4572 meter")

    output = run("cubit:1")

    assert "1.0 cubit = 0.4572 meter" in output
    assert len(output.split("\n")) == 4


# --- B-CLI-07: config 기반 run end-to-end (P1-C) ---


def test_b_cli_07_run_with_config_file(tmp_path):
    """B-CLI-07: config 파일 로드 파이프라인 — meter:2.5 P0 golden master."""
    config_path = tmp_path / "units.json"
    config_path.write_text(json.dumps(_default_units_config()), encoding="utf-8")

    output = run("meter:2.5", config_path=config_path)

    expected = (
        "2.5 meter = 2.5 meter\n"
        "2.5 meter = 8.2021 feet\n"
        "2.5 meter = 2.734025 yard"
    )
    assert output == expected
