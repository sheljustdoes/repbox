from __future__ import annotations

from dataclasses import dataclass, field
import ast
from pathlib import Path
from typing import Dict


@dataclass
class RuntimeConfig:
    threads: int = 1
    output_dir: str = "./repbox_output"
    retries: int = 1
    timeout_seconds: int = 0


@dataclass
class AppConfig:
    runtime: RuntimeConfig = field(default_factory=RuntimeConfig)
    tools: Dict[str, str] = field(default_factory=dict)


def _parse_legacy_line(line: str) -> Dict[str, str]:
    parsed = ast.literal_eval(line.strip())
    if not isinstance(parsed, dict) or len(parsed) != 1:
        raise ValueError(f"Invalid legacy config line: {line!r}")

    key, value = next(iter(parsed.items()))
    return {str(key): str(value)}


def load_legacy_repbox_config(config_path: str | Path) -> Dict[str, str]:
    path = Path(config_path)
    if not path.exists():
        return {}

    tool_paths: Dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        tool_paths.update(_parse_legacy_line(raw_line))

    return tool_paths


def build_app_config(
    legacy_config_path: str | Path = "repbox_config.txt",
    threads: int | None = None,
    output_dir: str | None = None,
) -> AppConfig:
    config = AppConfig()
    config.tools = load_legacy_repbox_config(legacy_config_path)

    if threads is not None:
        config.runtime.threads = threads
    if output_dir is not None:
        config.runtime.output_dir = output_dir

    return config
