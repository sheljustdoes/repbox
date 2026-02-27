from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Mapping

from .runner import CommandResult, run_command


@dataclass
class AdapterCheckResult:
    name: str
    configured_path: str
    exists: bool
    is_executable: bool = False
    version: str = ""
    compatibility_mode: str = ""
    hint: str = ""


@dataclass
class ExternalToolAdapter:
    name: str
    config_key: str

    def check_installation(self, tools: dict[str, str]) -> AdapterCheckResult:
        configured = tools.get(self.config_key, "")
        exists = bool(configured and Path(configured).exists())
        is_executable = bool(exists and os.access(configured, os.X_OK))

        hint = ""
        if not configured:
            hint = f"Set '{self.config_key}' in repbox_config.txt."
        elif not exists:
            hint = "Configured path does not exist."
        elif not is_executable:
            hint = "Configured path is not executable."

        return AdapterCheckResult(
            name=self.name,
            configured_path=configured,
            exists=exists,
            is_executable=is_executable,
            hint=hint,
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
