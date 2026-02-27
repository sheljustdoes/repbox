from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RunContext:
    input_path: Path
    output_path: Path
    metadata: dict[str, Any] = field(default_factory=dict)
