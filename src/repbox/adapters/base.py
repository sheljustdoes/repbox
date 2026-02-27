from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .runner import CommandResult, run_command


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

    def build_command(self, tools: dict[str, str], args: list[str]) -> list[str]:
        configured = tools.get(self.config_key, "")
        if not configured:
            raise ValueError(
                f"{self.name} is not configured. Add '{self.config_key}' to repbox_config.txt"
            )
        return [configured, *args]

    def run(
        self,
        tools: dict[str, str],
        args: list[str],
        timeout_seconds: float = 0,
        cwd: str | None = None,
        env: Mapping[str, str] | None = None,
    ) -> CommandResult:
        command = self.build_command(tools=tools, args=args)
        return run_command(
            command=command,
            timeout_seconds=timeout_seconds,
            cwd=cwd,
            env=env,
        )
