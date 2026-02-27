from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable


TaskCallable = Callable[[], None]


@dataclass
class Task:
    name: str
    func: TaskCallable
    depends_on: list[str] = field(default_factory=list)

    @classmethod
    def from_dependency_iterable(
        cls,
        name: str,
        func: TaskCallable,
        depends_on: Iterable[str] | None = None,
    ) -> "Task":
        return cls(name=name, func=func, depends_on=list(depends_on or []))
