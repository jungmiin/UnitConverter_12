"""Length unit types and protocols."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class LengthUnit(Protocol):
    """길이 단위 인터페이스.

    단위는 name과 meter 기준 변환 비율 또는 to_meter/from_meter 메서드를 가질 수 있다.
    """

    @property
    def name(self) -> str:
        """단위 이름 (예: meter, feet, yard)."""
        ...

    def to_meter(self, value: float) -> float:
        """주어진 값을 meter 기준으로 변환한다."""
        ...

    def from_meter(self, meter_value: float) -> float:
        """meter 기준 값을 이 단위로 변환한다."""
        ...


@dataclass(frozen=True)
class RatioBasedLengthUnit:
    """meter 기준 변환 비율을 가진 길이 단위.

    Attributes:
        name: 단위 이름.
        meters_per_unit: 1 단위가 몇 meter에 해당하는지 나타내는 비율.
    """

    name: str
    meters_per_unit: float

    def to_meter(self, value: float) -> float:
        """주어진 값을 meter 기준으로 변환한다.

        TODO: value * meters_per_unit 계산 구현.
        """
        raise NotImplementedError

    def from_meter(self, meter_value: float) -> float:
        """meter 기준 값을 이 단위로 변환한다.

        TODO: meter_value / meters_per_unit 계산 구현.
        """
        raise NotImplementedError
