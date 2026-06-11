"""Input parser — "unit:value" 형식 입력 파싱."""

from __future__ import annotations

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


class InputParser:
    """`unit:value` 형식 문자열을 파싱한다.

    잘못된 형식, 음수, 없는 단위 검증은 호출 측 또는
    후속 GREEN 단계에서 구현한다.
    """

    def parse(self, raw_input: str) -> ParsedInput:
        """입력 문자열을 파싱한다.

        Args:
            raw_input: `unit:value` 형식 문자열 (예: "meter:2.5").

        Returns:
            ParsedInput 인스턴스.

        TODO: `:` 없음 → 형식 오류 처리.
        TODO: 잘못된 숫자 → 숫자 오류 처리.
        TODO: 음수 값 검증.
        TODO: 빈 문자열·공백 처리.
        """
        raise NotImplementedError
