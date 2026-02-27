from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re

from .base import AdapterCheckResult, ExternalToolAdapter
from .runner import CommandResult, run_command


@dataclass
class RepeatModelerRunResult:
    build_database: CommandResult
    repeatmodeler: CommandResult


@dataclass
class ThreadFlagProbeResult:
    thread_flag: str
    version: str = ""


class RepeatModelerAdapter(ExternalToolAdapter):
    def __init__(self) -> None:
        super().__init__(name="RepeatModeler", config_key="RepeatModeler")

    @staticmethod
    def _build_database_binary(tools: dict[str, str]) -> str:
        configured = tools.get("BuildDatabase", "")
        if not configured:
            raise ValueError("BuildDatabase is not configured. Add 'BuildDatabase' to repbox_config.txt")
        return configured

    @staticmethod
    def _extract_version(text: str) -> str:
        patterns = (
            r"RepeatModeler(?:\s+open-)?\s*v?(\d+\.\d+(?:\.\d+)*)",
            r"\bv?(\d+\.\d+(?:\.\d+)*)\b",
        )
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(1)
        return ""

    @staticmethod
    def _parse_version_tuple(version: str) -> tuple[int, ...]:
        parts = []
        for piece in version.split("."):
            if piece.isdigit():
                parts.append(int(piece))
            else:
                break
        return tuple(parts)

    @classmethod
    def _probe_thread_flag_from_text(cls, text: str) -> ThreadFlagProbeResult | None:
        version = cls._extract_version(text)
        has_threads = bool(re.search(r"(?<!\w)-threads(?!\w)", text))
        has_pa = bool(re.search(r"(?<!\w)-pa(?!\w)", text))

        if has_threads:
            return ThreadFlagProbeResult(thread_flag="-threads", version=version)
        if has_pa:
            return ThreadFlagProbeResult(thread_flag="-pa", version=version)

        if version:
            parsed = cls._parse_version_tuple(version)
            if parsed >= (2, 0, 4):
                return ThreadFlagProbeResult(thread_flag="-threads", version=version)
            return ThreadFlagProbeResult(thread_flag="-pa", version=version)
        return None

    @classmethod
    def probe_thread_flag(cls, binary: str) -> ThreadFlagProbeResult | None:
        probe_commands = [
            [binary, "-help"],
            [binary, "-h"],
            [binary, "-version"],
            [binary, "--version"],
        ]
        fallback_version = ""
        for command in probe_commands:
            try:
                result = run_command(command=command, timeout_seconds=15)
            except Exception:
                continue

            combined = "\n".join((result.stdout, result.stderr)).strip()
            if not combined:
                continue

            probed = cls._probe_thread_flag_from_text(combined)
            if probed:
                return probed

            if not fallback_version:
                fallback_version = cls._extract_version(combined)

        if fallback_version:
            parsed = cls._parse_version_tuple(fallback_version)
            if parsed >= (2, 0, 4):
                return ThreadFlagProbeResult(thread_flag="-threads", version=fallback_version)
            return ThreadFlagProbeResult(thread_flag="-pa", version=fallback_version)
        return None

    def detect_thread_flag(self, tools: dict[str, str]) -> str:
        configured = tools.get(self.config_key, "")
        if not configured:
            raise ValueError("RepeatModeler is not configured. Add 'RepeatModeler' to repbox_config.txt")
        if not Path(configured).exists():
            raise ValueError(f"RepeatModeler path does not exist: {configured}")
        if not os.access(configured, os.X_OK):
            raise ValueError(f"RepeatModeler path is not executable: {configured}")

        probe = self.probe_thread_flag(configured)
        if not probe:
            raise ValueError(
                "Unable to determine RepeatModeler threading option. "
                "Expected '-threads' (modern) or '-pa' (legacy) from help/version output."
            )
        return probe.thread_flag

    def check_installation(self, tools: dict[str, str]) -> AdapterCheckResult:
        base_result = super().check_installation(tools)
        if not base_result.exists or not base_result.is_executable:
            return base_result

        probe = self.probe_thread_flag(base_result.configured_path)
        if not probe:
            base_result.compatibility_mode = "unsupported"
            base_result.hint = (
                "Could not detect RepeatModeler threading flag from help/version output."
            )
            return base_result

        base_result.version = probe.version
        if probe.thread_flag == "-threads":
            base_result.compatibility_mode = "modern-threads"
        else:
            base_result.compatibility_mode = "legacy-pa"
            base_result.hint = (
                "Legacy mode detected; consider upgrading RepeatModeler to 2.0.4+."
            )
        return base_result

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
        thread_flag: str,
    ) -> list[str]:
        return self.build_command(
            tools=tools,
            args=[
                "-engine",
                engine,
                "-database",
                database_name,
                thread_flag,
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

        thread_flag = self.detect_thread_flag(tools)
        repeatmodeler_cmd = self.build_repeatmodeler_command(
            tools=tools,
            database_name=database_name,
            threads=threads,
            engine=engine,
            thread_flag=thread_flag,
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
