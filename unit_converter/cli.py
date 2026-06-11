"""CLI entry point — 컴포넌트 조립 및 실행."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from unit_converter.app.input_parser import InputParser
from unit_converter.app.output_formatter import OutputFormat, OutputFormatter
from unit_converter.domain.converter import LengthConverter
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import ConfigLoader

_shared_registry: UnitRegistry | None = None


def _get_registry() -> UnitRegistry:
    """세션 간 동적 등록을 유지하는 공유 Registry를 반환한다."""
    global _shared_registry
    if _shared_registry is None:
        _shared_registry = UnitRegistry()
        _shared_registry.register_defaults()
    return _shared_registry


def _is_registration_input(raw_input: str) -> bool:
    return " = " in raw_input and ":" not in raw_input


@dataclass(frozen=True)
class ConversionPipeline:
    """기본 단위 변환 파이프라인 컴포넌트."""

    parser: InputParser
    converter: LengthConverter
    formatter: OutputFormatter


def create_default_pipeline() -> ConversionPipeline:
    """기본 Registry·Converter·Formatter를 조립한 파이프라인을 생성한다."""
    registry = _get_registry()
    return _build_pipeline(registry)


def _build_pipeline(registry: UnitRegistry) -> ConversionPipeline:
    return ConversionPipeline(
        parser=InputParser(),
        converter=LengthConverter(registry),
        formatter=OutputFormatter(),
    )


def _pipeline_from_config(config_path: Path) -> ConversionPipeline:
    registry = UnitRegistry()
    loader = ConfigLoader()
    config = loader.load_from_file(config_path)
    loader.apply_to_registry(config, registry)
    return _build_pipeline(registry)


def run(
    raw_input: str,
    output_format: OutputFormat = OutputFormat.TEXT,
    config_path: Path | None = None,
) -> str:
    """단위 변환 CLI 파이프라인을 실행한다.

    Args:
        raw_input: `unit:value` 형식 입력 문자열.
        output_format: 출력 포맷.
        config_path: JSON/YAML 설정 파일 경로 (선택).

    Returns:
        포맷팅된 변환 결과 문자열.
    """
    if config_path is not None:
        pipeline = _pipeline_from_config(config_path)
    else:
        pipeline = create_default_pipeline()

    if _is_registration_input(raw_input):
        registration = pipeline.parser.parse_registration(raw_input)
        if config_path is not None:
            pipeline.converter._registry.register_ratio(
                registration.unit, registration.ratio
            )
        else:
            _get_registry().register_ratio(registration.unit, registration.ratio)
        return ""

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
