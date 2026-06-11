"""Length converter — meter 기준 단위 간 변환 계산."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from unit_converter.domain.length_unit import LengthUnit
from unit_converter.domain.unit_registry import UnitRegistry


@dataclass(frozen=True)
class ConversionResult:
    """단일 변환 결과.

    Attributes:
        source_value: 원본 입력 값.
        source_unit: 원본 단위 이름.
        target_value: 변환된 값.
        target_unit: 대상 단위 이름.
    """

    source_value: float
    source_unit: str
    target_value: float
    target_unit: str


class LengthConverter:
    """meter 기준으로 다른 단위로 변환하는 Converter.

    입력 파싱, 출력 포맷, 설정 파일 로드는 담당하지 않는다.
    """

    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert_to_all(self, value: float, source_unit_name: str) -> Iterable[ConversionResult]:
        """주어진 값을 등록된 모든 단위로 변환한다.

        Args:
            value: 변환할 숫자 값.
            source_unit_name: 원본 단위 이름.

        Returns:
            각 대상 단위에 대한 ConversionResult 시퀀스.

        TODO: source_unit_name 조회 실패 시 예외 정책 결정.
        TODO: meter 기준 환산 후 각 대상 단위로 변환하는 계산 구현.
        """
        source_unit = self._registry.get(source_unit_name)
        if source_unit is None:
            raise ValueError(f"Unknown unit: {source_unit_name}")

        meter_value = source_unit.to_meter(value)
        for target_unit in self._registry.all_units():
            yield ConversionResult(
                source_value=value,
                source_unit=source_unit_name,
                target_value=target_unit.from_meter(meter_value),
                target_unit=target_unit.name,
            )

    def convert(self, value: float, source_unit_name: str, target_unit_name: str) -> ConversionResult:
        """주어진 값을 특정 대상 단위로 변환한다.

        Args:
            value: 변환할 숫자 값.
            source_unit_name: 원본 단위 이름.
            target_unit_name: 대상 단위 이름.

        Returns:
            단일 ConversionResult.

        TODO: 단위 조회 실패 시 예외 정책 결정.
        TODO: meter 기준 환산 계산 구현.
        """
        source_unit = self._registry.get(source_unit_name)
        if source_unit is None:
            raise ValueError(f"Unknown unit: {source_unit_name}")
        target_unit = self._registry.get(target_unit_name)
        if target_unit is None:
            raise ValueError(f"Unknown unit: {target_unit_name}")

        meter_value = source_unit.to_meter(value)
        return ConversionResult(
            source_value=value,
            source_unit=source_unit_name,
            target_value=target_unit.from_meter(meter_value),
            target_unit=target_unit_name,
        )
