"""Boundary/CLI-level tests — 입력 문자열, 오류 처리, CLI 출력 검증."""

from __future__ import annotations

import pytest

# TODO: GREEN 단계에서 아래 import 활성화
# from unit_converter.cli import run, main
# from unit_converter.app.input_parser import InputParser


class TestInputParser:
    """InputParser 경계 테스트."""

    def test_parse_valid_meter_input(self) -> None:
        """유효한 meter:2.5 입력을 파싱한다.

        TODO: ParsedInput(unit="meter", value=2.5) 검증.
        """
        pytest.skip("skeleton only")

    def test_parse_rejects_missing_colon(self) -> None:
        """콜론이 없는 입력을 거부한다.

        TODO: "Invalid format. Use unit:value (ex: meter:2.5)" 메시지 검증.
        """
        pytest.skip("skeleton only")

    def test_parse_rejects_invalid_number(self) -> None:
        """잘못된 숫자 입력을 거부한다.

        TODO: "Invalid number: {value_str}" 메시지 검증.
        """
        pytest.skip("skeleton only")

    def test_parse_rejects_negative_value(self) -> None:
        """음수 입력을 거부한다.

        TODO: 음수 검증 오류 메시지 및 정책 확정.
        """
        pytest.skip("skeleton only")


class TestCliRun:
    """CLI run() 파이프라인 테스트."""

    def test_run_meter_input_produces_text_output(self) -> None:
        """meter:2.5 입력 시 3줄 텍스트 출력을 반환한다.

        TODO: 기존 UnitConverter.py Golden Master 출력과 일치 검증.
        """
        pytest.skip("skeleton only")

    def test_run_unknown_unit_reports_error(self) -> None:
        """없는 단위 입력 시 오류를 반환한다.

        TODO: "Unknown unit: {unit}" 메시지 검증.
        """
        pytest.skip("skeleton only")


class TestCliMain:
    """CLI main() 진입점 테스트."""

    def test_main_accepts_valid_input_via_stdin(self) -> None:
        """유효한 stdin 입력으로 정상 실행된다.

        TODO: subprocess 또는 capsys로 stdin/stdout 검증.
        """
        pytest.skip("skeleton only")

    def test_main_exits_gracefully_on_invalid_format(self) -> None:
        """잘못된 형식 입력 시 오류 메시지를 출력하고 종료한다.

        TODO: exit code 및 stderr/stdout 검증.
        """
        pytest.skip("skeleton only")
