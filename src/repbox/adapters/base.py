from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class AdapterCheckResult:
    name: str
    configured_path: str
    exists: bool


@dataclass
class ExternalToolAdapter:
    name: str
    config_key: str

    def check_installation(self, tools: dict[str, str]) -> AdapterCheckResult:
        configured = tools.get(self.config_key, "")
        return AdapterCheckResult(
            name=self.name,
            configured_path=configured,
            exists=bool(configured and Path(configured).exists()),
        )
