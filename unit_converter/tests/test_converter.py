"""Domain-level tests — 변환 로직 검증."""

from __future__ import annotations

import pytest

# TODO: GREEN 단계에서 아래 import 활성화
# from unit_converter.domain.converter import LengthConverter
# from unit_converter.domain.unit_registry import UnitRegistry


class TestLengthConverter:
    """LengthConverter 변환 로직 테스트."""

    def test_meter_to_feet_conversion(self) -> None:
        """meter 입력을 feet로 정확히 변환한다.

        TODO: 1 meter = 3.28084 feet 비율 검증.
        """
        pytest.skip("skeleton only")

    def test_meter_to_yard_conversion(self) -> None:
        """meter 입력을 yard로 정확히 변환한다.

        TODO: 1 meter = 1.09361 yard 비율 검증.
        """
        pytest.skip("skeleton only")

    def test_feet_to_meter_conversion(self) -> None:
        """feet 입력을 meter 기준으로 정확히 변환한다.

        TODO: feet → meter 역변환 검증.
        """
        pytest.skip("skeleton only")

    def test_yard_to_meter_conversion(self) -> None:
        """yard 입력을 meter 기준으로 정확히 변환한다.

        TODO: yard → meter 역변환 검증.
        """
        pytest.skip("skeleton only")

    def test_convert_to_all_returns_all_registered_units(self) -> None:
        """등록된 모든 단위에 대한 변환 결과를 반환한다.

        TODO: meter, feet, yard 3개 결과 반환 검증.
        """
        pytest.skip("skeleton only")

    def test_unknown_source_unit_raises_error(self) -> None:
        """존재하지 않는 원본 단위 입력 시 오류를 발생시킨다.

        TODO: 예외 타입 및 메시지 정책 확정 후 assertion 작성.
        """
        pytest.skip("skeleton only")


class TestUnitRegistry:
    """UnitRegistry 등록·조회 테스트."""

    def test_register_and_get_unit(self) -> None:
        """단위 등록 후 이름으로 조회할 수 있다.

        TODO: register() → get() round-trip 검증.
        """
        pytest.skip("skeleton only")

    def test_register_defaults_includes_meter_feet_yard(self) -> None:
        """기본 단위 등록 시 meter, feet, yard가 포함된다.

        TODO: register_defaults() 후 all_units() 검증.
        """
        pytest.skip("skeleton only")
