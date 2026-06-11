"""Output formatter — text/json/csv/table 출력 포맷 (P1 확장 지점)."""

from __future__ import annotations

from enum import Enum
from typing import Iterable

from unit_converter.domain.converter import ConversionResult


class OutputFormat(Enum):
    """지원할 출력 포맷 종류."""

    TEXT = "text"
    JSON = "json"
    CSV = "csv"
    TABLE = "table"


class OutputFormatter:
    """변환 결과를 선택한 포맷으로 출력 문자열로 변환한다.

    P1 확장 지점: JSON / CSV / 표 형태 출력.
    """

    def format(
        self,
        results: Iterable[ConversionResult],
        output_format: OutputFormat = OutputFormat.TEXT,
    ) -> str:
        """변환 결과를 지정 포맷의 문자열로 반환한다.

        Args:
            results: 변환 결과 시퀀스.
            output_format: 출력 포맷 (기본값 TEXT).

        Returns:
            포맷팅된 출력 문자열.

        TODO: TEXT 포맷 — `{value} {unit} = {result} {target_unit}` 3줄 형식.
        TODO: JSON 포맷 구현.
        TODO: CSV 포맷 구현.
        TODO: TABLE 포맷 구현.
        """
        raise NotImplementedError
