"""Output formatter — text/json/csv/table 출력 포맷 (P1 확장 지점)."""

from __future__ import annotations

import json
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

        """
        items = list(results)

        if output_format == OutputFormat.TEXT:
            lines = [
                f"{r.source_value} {r.source_unit} = {r.target_value} {r.target_unit}"
                for r in items
            ]
            return "\n".join(lines)

        if output_format == OutputFormat.JSON:
            payload = [
                {
                    "source_value": r.source_value,
                    "source_unit": r.source_unit,
                    "target_value": r.target_value,
                    "target_unit": r.target_unit,
                }
                for r in items
            ]
            return json.dumps(payload)

        if output_format == OutputFormat.CSV:
            lines = ["source_value,source_unit,target_value,target_unit"]
            for r in items:
                lines.append(
                    f"{r.source_value},{r.source_unit},{r.target_value},{r.target_unit}"
                )
            return "\n".join(lines)

        if output_format == OutputFormat.TABLE:
            header = "source_value | source_unit | target_value | target_unit"
            separator = "-------------|-------------|--------------|-------------"
            rows = [
                f"{r.source_value:<13}| {r.source_unit:<12}| {r.target_value:<13}| {r.target_unit}"
                for r in items
            ]
            return "\n".join([header, separator, *rows])

        raise NotImplementedError
