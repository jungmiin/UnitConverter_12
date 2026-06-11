"""Unit registry — 단위 등록 및 조회 (OCP 핵심 확장 지점)."""

from __future__ import annotations

from typing import Iterable, Optional

from unit_converter.domain.length_unit import LengthUnit, RatioBasedLengthUnit

METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361


class UnitRegistry:
    """길이 단위를 등록하고 조회하는 레지스트리.

    새 단위 추가 시 기존 Converter 코드를 수정하지 않도록
    단위 정보를 데이터로 확장하는 구조의 핵심 위치이다.
    """

    def __init__(self) -> None:
        self._units: dict[str, LengthUnit] = {}

    def register(self, unit: LengthUnit) -> None:
        """단위를 레지스트리에 등록한다.

        Args:
            unit: 등록할 LengthUnit 인스턴스.

        TODO: 동일 이름 중복 등록 처리 정책 결정.
        """
        self._units[unit.name] = unit

    def get(self, name: str) -> Optional[LengthUnit]:
        """이름으로 단위를 조회한다.

        Args:
            name: 조회할 단위 이름.

        Returns:
            등록된 LengthUnit 또는 None.

        TODO: 대소문자 정규화 여부 결정.
        """
        return self._units.get(name)

    def all_units(self) -> Iterable[LengthUnit]:
        """등록된 모든 단위를 반환한다.

        TODO: 반환 순서 정책 결정 (등록 순 vs 이름 정렬).
        """
        return self._units.values()

    def register_defaults(self) -> None:
        """기본 단위(meter, feet, yard)를 등록한다.

        TODO: meter, feet, yard 등록 로직 구현.
              비율: 1 meter = 3.28084 feet, 1 meter = 1.09361 yard.
              비율은 이 메서드 또는 ConfigLoader 한 경로에서만 정의할 것.
        """
        self.register(RatioBasedLengthUnit(name="meter", meters_per_unit=1.0))
        self.register(
            RatioBasedLengthUnit(name="feet", meters_per_unit=1 / METER_TO_FEET)
        )
        self.register(
            RatioBasedLengthUnit(name="yard", meters_per_unit=1 / METER_TO_YARD)
        )
