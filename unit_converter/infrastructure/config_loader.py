"""Config loader — JSON/YAML 설정 파일에서 단위·비율 로드 (P1 확장 지점)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from unit_converter.domain.unit_registry import (
    FEET_TO_METER,
    YARD_TO_METER,
    UnitRegistry,
)


def default_units_config() -> dict[str, Any]:
    """기본 단위 비율 설정 — register_defaults와 config 파일의 단일 소스."""
    return {
        "units": [
            {"name": "meter", "meters_per_unit": 1.0},
            {"name": "feet", "meters_per_unit": FEET_TO_METER},
            {"name": "yard", "meters_per_unit": YARD_TO_METER},
        ]
    }


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

        """
        suffix = path.suffix.lower()
        text = path.read_text(encoding="utf-8")

        if suffix == ".json":
            return json.loads(text)
        if suffix in (".yaml", ".yml"):
            data = yaml.safe_load(text)
            if not isinstance(data, dict):
                raise ValueError("YAML config must be a mapping")
            return data

        raise ValueError(f"Unsupported config file extension: {suffix}")

    def apply_to_registry(self, config: dict[str, Any], registry: UnitRegistry) -> None:
        """설정 데이터를 UnitRegistry에 반영한다.

        Args:
            config: load_from_file()이 반환한 설정 데이터.
            registry: 단위를 등록할 레지스트리.

        """
        units = config.get("units", [])
        for unit_def in units:
            registry.register_ratio(
                unit_def["name"],
                float(unit_def["meters_per_unit"]),
            )
