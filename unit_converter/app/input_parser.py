"""Input parser — "unit:value" 및 동적 단위 등록 입력 파싱."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedInput:
    """파싱된 입력 데이터.

    Attributes:
        unit: 단위 이름.
        value: 숫자 값.
    """

    unit: str
    value: float


@dataclass(frozen=True)
class ParsedRegistration:
    """파싱된 동적 단위 등록 입력.

    Attributes:
        unit: 등록할 단위 이름.
        base_unit: 기준 단위 이름 (예: meter).
        ratio: 1 단위당 meter 환산 비율 (meters_per_unit).
    """

    unit: str
    base_unit: str
    ratio: float


_REGISTRATION_PATTERN = re.compile(
    r"^\s*(\d+(?:\.\d+)?)\s+(\w+)\s*=\s*(\d+(?:\.\d+)?)\s+(\w+)\s*$"
)


class InputParseError(Exception):
    """입력 파싱 오류."""


NEGATIVE_VALUE_MESSAGE = "Negative value not allowed"


class InputParser:
    """`unit:value` 형식 문자열을 파싱한다.

    잘못된 형식, 음수, 없는 단위 검증은 호출 측 또는
    후속 GREEN 단계에서 구현한다.
    """

    def is_registration_input(self, raw_input: str) -> bool:
        """동적 단위 등록 입력인지 판별한다."""
        return " = " in raw_input and ":" not in raw_input

    def parse(self, raw_input: str) -> ParsedInput:
        """입력 문자열을 파싱한다.

        Args:
            raw_input: `unit:value` 형식 문자열 (예: "meter:2.5").

        Returns:
            ParsedInput 인스턴스.

        TODO: `:` 없음 → 형식 오류 처리.
        TODO: 잘못된 숫자 → 숫자 오류 처리.
        TODO: 빈 문자열·공백 처리.
        """
        if ":" not in raw_input:
            raise InputParseError(
                "Invalid format. Use unit:value (ex: meter:2.5)"
            )

        unit, value_str = raw_input.split(":", 1)

        try:
            value = float(value_str)
        except ValueError:
            raise InputParseError(f"Invalid number: {value_str}") from None

        if value < 0:
            raise ValueError(NEGATIVE_VALUE_MESSAGE)

        return ParsedInput(unit=unit, value=value)

    def parse_registration(self, raw_input: str) -> ParsedRegistration:
        """동적 단위 등록 입력을 파싱한다.

        Args:
            raw_input: `1 cubit = 0.4572 meter` 형식 문자열.

        Returns:
            ParsedRegistration 인스턴스.
        """
        match = _REGISTRATION_PATTERN.match(raw_input)
        if match is None:
            raise InputParseError(
                "Invalid registration format. Use 1 unit = ratio meter "
                "(ex: 1 cubit = 0.4572 meter)"
            )

        quantity_str, unit, ratio_str, base_unit = match.groups()
        quantity = float(quantity_str)
        ratio_value = float(ratio_str)

        if base_unit != "meter":
            raise InputParseError("Registration base unit must be meter")

        if quantity <= 0:
            raise InputParseError("Registration quantity must be positive")

        meters_per_unit = ratio_value / quantity
        return ParsedRegistration(unit=unit, base_unit=base_unit, ratio=meters_per_unit)
