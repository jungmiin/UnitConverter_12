"""Boundary/CLI-level tests — 입력 문자열, 오류 처리, CLI 출력 검증."""

from __future__ import annotations

import pytest

from unit_converter.app.input_parser import InputParser, ParsedInput
from unit_converter.app.output_formatter import OutputFormat, OutputFormatter
from unit_converter.cli import run
from unit_converter.domain.converter import ConversionResult

METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361


# --- B-PARSE-01: meter:2.5 정상 파싱 ---


def test_b_parse_01_valid_input():
    """B-PARSE-01: meter:2.5 입력 파싱."""
    parser = InputParser()

    result = parser.parse("meter:2.5")

    assert result == ParsedInput(unit="meter", value=2.5)


# --- B-ERR-01: 콜론 없는 형식 거부 ---


def test_b_err_01_invalid_format_no_colon():
    """B-ERR-01: 잘못된 형식(콜론 없음) 입력 거부."""
    parser = InputParser()

    with pytest.raises(Exception, match=r"Invalid format\. Use unit:value \(ex: meter:2\.5\)"):
        parser.parse("meter2.5")


# --- B-ERR-04: 비숫자 값 거부 ---


def test_b_err_04_invalid_number():
    """B-ERR-04: 숫자가 아닌 값 거부."""
    parser = InputParser()

    with pytest.raises(Exception, match=r"Invalid number: abc"):
        parser.parse("meter:abc")


# --- B-ERR-02: 음수 입력 거부 ---


def test_b_err_02_negative_value():
    """B-ERR-02: 음수 입력 거부."""
    parser = InputParser()

    with pytest.raises(Exception) as exc_info:
        parser.parse("meter:-1")
    assert type(exc_info.value) is not NotImplementedError


# --- B-ERR-03: unknown unit 거부 ---


def test_b_err_03_unknown_unit():
    """B-ERR-03: 없는 단위 입력 거부."""
    with pytest.raises(Exception, match=r"Unknown unit: cubit"):
        run("cubit:1")


# --- B-FMT-01: TEXT 3줄 출력 포맷 ---


def test_b_fmt_01_text_three_line_output():
    """B-FMT-01: TEXT 포맷 3줄 출력 (UnitConverter.py golden master)."""
    formatter = OutputFormatter()
    results = [
        ConversionResult(2.5, "meter", 2.5, "meter"),
        ConversionResult(2.5, "meter", 2.5 * METER_TO_FEET, "feet"),
        ConversionResult(2.5, "meter", 2.5 * METER_TO_YARD, "yard"),
    ]

    output = formatter.format(results, OutputFormat.TEXT)

    expected = (
        "2.5 meter = 2.5 meter\n"
        "2.5 meter = 8.2021 feet\n"
        "2.5 meter = 2.734025 yard"
    )
    assert output == expected


# --- B-CLI-01: run meter:2.5 golden master ---


def test_b_cli_01_run_meter_golden_master():
    """B-CLI-01: run('meter:2.5') end-to-end golden master."""
    output = run("meter:2.5")

    expected = (
        "2.5 meter = 2.5 meter\n"
        "2.5 meter = 8.2021 feet\n"
        "2.5 meter = 2.734025 yard"
    )
    assert output == expected


# --- B-CLI-02: run 오류 메시지 golden master ---


@pytest.mark.parametrize(
    ("raw_input", "expected_pattern"),
    [
        ("meter2.5", r"Invalid format\. Use unit:value \(ex: meter:2\.5\)"),
        ("meter:abc", r"Invalid number: abc"),
        ("cubit:1", r"Unknown unit: cubit"),
    ],
)
def test_b_cli_02_run_error_messages(raw_input: str, expected_pattern: str):
    """B-CLI-02: run() 오류 메시지가 UnitConverter.py와 일치."""
    with pytest.raises(Exception, match=expected_pattern):
        run(raw_input)
