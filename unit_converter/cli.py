"""CLI entry point — 컴포넌트 조립 및 실행."""

from __future__ import annotations

from dataclasses import dataclass

from unit_converter.app.input_parser import InputParser
from unit_converter.app.output_formatter import OutputFormat, OutputFormatter
from unit_converter.domain.converter import LengthConverter
from unit_converter.domain.unit_registry import UnitRegistry


@dataclass(frozen=True)
class ConversionPipeline:
    """기본 단위 변환 파이프라인 컴포넌트."""

    parser: InputParser
    converter: LengthConverter
    formatter: OutputFormatter


def create_default_pipeline() -> ConversionPipeline:
    """기본 Registry·Converter·Formatter를 조립한 파이프라인을 생성한다."""
    registry = UnitRegistry()
    registry.register_defaults()
    return ConversionPipeline(
        parser=InputParser(),
        converter=LengthConverter(registry),
        formatter=OutputFormatter(),
    )


def run(
    raw_input: str,
    output_format: OutputFormat = OutputFormat.TEXT,
) -> str:
    """단위 변환 CLI 파이프라인을 실행한다.

    Args:
        raw_input: `unit:value` 형식 입력 문자열.
        output_format: 출력 포맷.

    Returns:
        포맷팅된 변환 결과 문자열.
    """
    pipeline = create_default_pipeline()
    parsed = pipeline.parser.parse(raw_input)
    results = pipeline.converter.convert_to_all(parsed.value, parsed.unit)
    return pipeline.formatter.format(results, output_format)


def main() -> None:
    """CLI 진입점 — input() 수신, run() 호출, stdout 출력."""
    input_str = input("Insert value for converting (ex: meter:2.5): ")
    try:
        output = run(input_str)
    except Exception as exc:
        print(str(exc))
        return
    print(output)


if __name__ == "__main__":
    main()
