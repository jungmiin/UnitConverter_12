"""CLI entry point — 컴포넌트 조립 및 실행."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from unit_converter.app.input_parser import InputParser
from unit_converter.app.output_formatter import OutputFormat, OutputFormatter
from unit_converter.domain.converter import LengthConverter
from unit_converter.domain.unit_registry import UnitRegistry
from unit_converter.infrastructure.config_loader import ConfigLoader

@dataclass(frozen=True)
class PipelineContext:
    """세션 단위 Registry를 보유하는 파이프라인 컨텍스트."""

    registry: UnitRegistry

    @classmethod
    def create_with_defaults(cls) -> PipelineContext:
        registry = UnitRegistry()
        registry.register_defaults()
        return cls(registry=registry)


_default_context: PipelineContext | None = None


def _get_default_context() -> PipelineContext:
    """세션 간 동적 등록을 유지하는 기본 컨텍스트를 반환한다."""
    global _default_context
    if _default_context is None:
        _default_context = PipelineContext.create_with_defaults()
    return _default_context


@dataclass(frozen=True)
class ConversionPipeline:
    """기본 단위 변환 파이프라인 컴포넌트."""

    parser: InputParser
    converter: LengthConverter
    formatter: OutputFormatter


def create_default_pipeline(
    context: PipelineContext | None = None,
) -> ConversionPipeline:
    """기본 Registry·Converter·Formatter를 조립한 파이프라인을 생성한다."""
    ctx = context or _get_default_context()
    return _build_pipeline(ctx.registry)


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


def _dispatch(
    raw_input: str,
    pipeline: ConversionPipeline,
    output_format: OutputFormat = OutputFormat.TEXT,
) -> str:
    """조립된 파이프라인으로 입력을 등록 또는 변환 처리한다."""
    if pipeline.parser.is_registration_input(raw_input):
        registration = pipeline.parser.parse_registration(raw_input)
        pipeline.converter.register_ratio(registration.unit, registration.ratio)
        return ""

    parsed = pipeline.parser.parse(raw_input)
    results = pipeline.converter.convert_to_all(parsed.value, parsed.unit)
    return pipeline.formatter.format(results, output_format)


def run(
    raw_input: str,
    output_format: OutputFormat = OutputFormat.TEXT,
    config_path: Path | None = None,
    context: PipelineContext | None = None,
) -> str:
    """단위 변환 CLI 파이프라인을 실행한다.

    Args:
        raw_input: `unit:value` 형식 입력 문자열.
        output_format: 출력 포맷.
        config_path: JSON/YAML 설정 파일 경로 (선택).
        context: 공유 Registry 컨텍스트 (선택, 기본값은 세션 lazy init).

    Returns:
        포맷팅된 변환 결과 문자열.
    """
    if config_path is not None:
        pipeline = _pipeline_from_config(config_path)
    else:
        pipeline = create_default_pipeline(context)

    return _dispatch(raw_input, pipeline, output_format)


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
