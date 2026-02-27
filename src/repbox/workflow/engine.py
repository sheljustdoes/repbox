from __future__ import annotations

from typing import Iterable

from .task import Task


class WorkflowEngine:
    """Minimal sequential workflow engine for v0.3.0 Milestone A."""

    def __init__(self) -> None:
        self._completed: set[str] = set()

    def run(self, tasks: Iterable[Task]) -> None:
        ordered = list(tasks)
        for task in ordered:
            missing = [name for name in task.depends_on if name not in self._completed]
            if missing:
                missing_list = ", ".join(missing)
                raise RuntimeError(
                    f"Task '{task.name}' has unmet dependencies: {missing_list}"
                )
            task.func()
            self._completed.add(task.name)
