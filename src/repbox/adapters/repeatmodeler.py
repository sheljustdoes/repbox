from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .base import ExternalToolAdapter
from .runner import CommandResult, run_command


@dataclass
class RepeatModelerRunResult:
    build_database: CommandResult
    repeatmodeler: CommandResult


class RepeatModelerAdapter(ExternalToolAdapter):
    def __init__(self) -> None:
        super().__init__(name="RepeatModeler", config_key="RepeatModeler")

    @staticmethod
    def _build_database_binary(tools: dict[str, str]) -> str:
        configured = tools.get("BuildDatabase", "")
        if not configured:
            raise ValueError("BuildDatabase is not configured. Add 'BuildDatabase' to repbox_config.txt")
        return configured

    def build_database_command(
        self,
        tools: dict[str, str],
        input_fasta: Path,
        database_name: str,
        engine: str,
        output_dir: Path,
    ) -> list[str]:
        build_database = self._build_database_binary(tools)
        return [
            build_database,
            str(input_fasta),
            "-name",
            database_name,
            "-engine",
            engine,
            "-dir",
            str(output_dir),
        ]

    def build_repeatmodeler_command(
        self,
        tools: dict[str, str],
        database_name: str,
        threads: int,
        engine: str,
    ) -> list[str]:
        return self.build_command(
            tools=tools,
            args=[
                "-engine",
                engine,
                "-database",
                database_name,
                "-pa",
                str(threads),
            ],
        )

    def run_pipeline(
        self,
        tools: dict[str, str],
        input_fasta: Path,
        output_dir: Path,
        threads: int,
        engine: str = "ncbi",
        timeout_seconds: float = 0,
    ) -> RepeatModelerRunResult:
        database_name = input_fasta.stem
        build_database_cmd = self.build_database_command(
            tools=tools,
            input_fasta=input_fasta,
            database_name=database_name,
            engine=engine,
            output_dir=output_dir,
        )
        build_database_result = run_command(
            command=build_database_cmd,
            timeout_seconds=timeout_seconds,
            cwd=str(output_dir),
        )

        repeatmodeler_cmd = self.build_repeatmodeler_command(
            tools=tools,
            database_name=database_name,
            threads=threads,
            engine=engine,
        )
        repeatmodeler_result = run_command(
            command=repeatmodeler_cmd,
            timeout_seconds=timeout_seconds,
            cwd=str(output_dir),
        )

        return RepeatModelerRunResult(
            build_database=build_database_result,
            repeatmodeler=repeatmodeler_result,
        )
