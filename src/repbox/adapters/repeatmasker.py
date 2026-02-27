from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .base import ExternalToolAdapter
from .runner import CommandResult


@dataclass
class RepeatMaskerRunResult:
    repeatmasker: CommandResult


class RepeatMaskerAdapter(ExternalToolAdapter):
    def __init__(self) -> None:
        super().__init__(name="RepeatMasker", config_key="RepeatMasker")

    def build_repeatmasker_command(
        self,
        tools: dict[str, str],
        genome_fasta: Path,
        output_dir: Path,
        threads: int,
        engine: str = "ncbi",
        library: Path | None = None,
    ) -> list[str]:
        args: list[str] = [
            "-pa",
            str(threads),
            "-engine",
            engine,
            "-dir",
            str(output_dir),
            "-qq",
        ]

        if library is not None:
            args.extend(["-lib", str(library)])

        args.append(str(genome_fasta))
        return self.build_command(tools=tools, args=args)

    def run_pipeline(
        self,
        tools: dict[str, str],
        genome_fasta: Path,
        output_dir: Path,
        threads: int,
        engine: str = "ncbi",
        library: Path | None = None,
        timeout_seconds: float = 0,
    ) -> RepeatMaskerRunResult:
        repeatmasker_cmd = self.build_repeatmasker_command(
            tools=tools,
            genome_fasta=genome_fasta,
            output_dir=output_dir,
            threads=threads,
            engine=engine,
            library=library,
        )
        repeatmasker_result = self.run(
            tools=tools,
            args=repeatmasker_cmd[1:],
            timeout_seconds=timeout_seconds,
            cwd=str(output_dir),
        )

        return RepeatMaskerRunResult(repeatmasker=repeatmasker_result)
