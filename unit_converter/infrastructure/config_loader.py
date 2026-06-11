"""Config loader — JSON/YAML 설정 파일에서 단위·비율 로드 (P1 확장 지점)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from unit_converter.domain.unit_registry import UnitRegistry


class ConfigLoader:
    """외부 설정 파일(JSON/YAML)에서 단위 정보를 로드한다.

    P1 확장 지점: 변환 비율 외부화, 동적 단위 등록.
    """

    def load_from_file(self, path: Path) -> dict[str, Any]:
        """설정 파일을 읽어 파싱된 데이터를 반환한다.

        Args:
            path: JSON 또는 YAML 설정 파일 경로.

        Returns:
            파싱된 설정 딕셔너리.

        TODO: JSON/YAML 파일 파싱 구현.
        TODO: 지원하지 않는 확장자 처리 정책 결정.
        """
        raise NotImplementedError

    def apply_to_registry(self, config: dict[str, Any], registry: UnitRegistry) -> None:
        """설정 데이터를 UnitRegistry에 반영한다.

        Args:
            config: load_from_file()이 반환한 설정 데이터.
            registry: 단위를 등록할 레지스트리.

        TODO: 설정 스키마 정의 및 registry.register() 호출 구현.
        TODO: 동적 단위 등록 (예: 1 cubit = 0.4572 meter) 지원.
        """
        raise NotImplementedError
