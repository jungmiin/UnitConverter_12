"""CLI entry point — 컴포넌트 조립 및 실행."""

from __future__ import annotations

from unit_converter.app.input_parser import InputParser
from unit_converter.app.output_formatter import OutputFormat, OutputFormatter
from unit_converter.domain.converter import LengthConverter
from unit_converter.domain.unit_registry import UnitRegistry


def run(
    raw_input: str,
    output_format: OutputFormat = OutputFormat.TEXT,
) -> str:
    """단위 변환 CLI 파이프라인을 실행한다.

    조립 위치:
        InputParser → UnitRegistry → LengthConverter → OutputFormatter

    Args:
        raw_input: `unit:value` 형식 입력 문자열.
        output_format: 출력 포맷.

    Returns:
        포맷팅된 변환 결과 문자열.

    TODO: InputParser로 입력 파싱.
    TODO: UnitRegistry 생성 및 기본 단위 등록.
    TODO: LengthConverter로 변환 수행.
    TODO: OutputFormatter로 결과 포맷팅.
    TODO: 없는 단위·음수·형식 오류 예외 처리 및 메시지 정책.
    """
    parser = InputParser()
    parsed = parser.parse(raw_input)

    registry = UnitRegistry()
    registry.register_defaults()

    if registry.get(parsed.unit) is None:
        raise ValueError(f"Unknown unit: {parsed.unit}")

    converter = LengthConverter(registry)
    results = converter.convert_to_all(parsed.value, parsed.unit)

    formatter = OutputFormatter()
    return formatter.format(results, output_format)


def main() -> None:
    """CLI 진입점.

    TODO: 사용자 입력 수신 (input 프롬프트).
    TODO: run() 호출 및 결과 stdout 출력.
    TODO: 오류 시 메시지 출력 및 종료 코드 정책.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
