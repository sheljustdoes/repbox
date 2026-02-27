from __future__ import annotations

from dataclasses import dataclass
import os
import shlex
import subprocess
import time
from typing import Mapping, Sequence


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float

    @property
    def succeeded(self) -> bool:
        return self.returncode == 0


class CommandTimeoutError(RuntimeError):
    def __init__(self, command: Sequence[str], timeout_seconds: float) -> None:
        joined = " ".join(shlex.quote(part) for part in command)
        super().__init__(f"Command timed out after {timeout_seconds}s: {joined}")
        self.command = list(command)
        self.timeout_seconds = timeout_seconds


def run_command(
    command: Sequence[str],
    timeout_seconds: float = 0,
    cwd: str | None = None,
    env: Mapping[str, str] | None = None,
) -> CommandResult:
    started = time.monotonic()
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    try:
        completed = subprocess.run(
            list(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            env=merged_env,
            timeout=timeout_seconds if timeout_seconds > 0 else None,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CommandTimeoutError(command=command, timeout_seconds=timeout_seconds) from exc

    duration = time.monotonic() - started
    return CommandResult(
        command=list(command),
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        duration_seconds=duration,
    )
