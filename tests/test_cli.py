from __future__ import annotations

from pathlib import Path
import tempfile
import unittest
from unittest import mock

from repbox.adapters.repeatmodeler import RepeatModelerRunResult, ThreadFlagProbeResult
from repbox.adapters.runner import CommandResult
from repbox.cli import main


def _write_legacy_config(path: Path, values: dict[str, str]) -> None:
    lines = [repr({key: value}) for key, value in values.items()]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _make_executable(path: Path) -> None:
    path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    path.chmod(0o755)


class CliTests(unittest.TestCase):
    def test_check_reports_missing_binary_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "repbox_config.txt"
            _write_legacy_config(config_path, {"RepeatModeler": "/no/such/repeatmodeler"})
            rc = main(["check", "--legacy-config", str(config_path)])
        self.assertEqual(rc, 1)

    def test_check_reports_compatibility_mode_when_probe_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            exe = tmp / "tool"
            _make_executable(exe)

            config_path = tmp / "repbox_config.txt"
            _write_legacy_config(
                config_path,
                {
                    "RepeatModeler": str(exe),
                    "RepeatMasker": str(exe),
                    "RepeatClassifier": str(exe),
                    "BuildDatabase": str(exe),
                    "SineScan": str(exe),
                    "miteFinder": str(exe),
                    "HelitronScanner": str(exe),
                    "VSEARCH": str(exe),
                },
            )
            with mock.patch(
                "repbox.adapters.repeatmodeler.RepeatModelerAdapter.probe_thread_flag",
                return_value=ThreadFlagProbeResult(thread_flag="-threads", version="2.0.7"),
            ):
                rc = main(["check", "--legacy-config", str(config_path)])
        self.assertEqual(rc, 0)

    def test_run_exits_when_builddatabase_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_fa = tmp / "genome.fa"
            input_fa.write_text(">x\nACGT\n", encoding="utf-8")
            rm = tmp / "RepeatModeler"
            _make_executable(rm)
            config_path = tmp / "repbox_config.txt"
            _write_legacy_config(config_path, {"RepeatModeler": str(rm)})

            rc = main(
                [
                    "run",
                    "--input",
                    str(input_fa),
                    "--out",
                    str(tmp / "out"),
                    "--legacy-config",
                    str(config_path),
                ]
            )
        self.assertEqual(rc, 1)

    def test_run_propagates_repeatmodeler_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_fa = tmp / "genome.fa"
            input_fa.write_text(">x\nACGT\n", encoding="utf-8")
            exe = tmp / "tool"
            _make_executable(exe)
            config_path = tmp / "repbox_config.txt"
            _write_legacy_config(
                config_path,
                {"RepeatModeler": str(exe), "BuildDatabase": str(exe)},
            )

            with mock.patch(
                "repbox.adapters.repeatmodeler.RepeatModelerAdapter.detect_thread_flag",
                return_value="-threads",
            ), mock.patch(
                "repbox.adapters.repeatmodeler.RepeatModelerAdapter.run_pipeline",
                return_value=RepeatModelerRunResult(
                    build_database=CommandResult(
                        command=["BuildDatabase"],
                        returncode=0,
                        stdout="",
                        stderr="",
                        duration_seconds=0.1,
                    ),
                    repeatmodeler=CommandResult(
                        command=["RepeatModeler"],
                        returncode=7,
                        stdout="",
                        stderr="failure",
                        duration_seconds=0.2,
                    ),
                ),
            ):
                rc = main(
                    [
                        "run",
                        "--input",
                        str(input_fa),
                        "--out",
                        str(tmp / "out"),
                        "--legacy-config",
                        str(config_path),
                    ]
                )
        self.assertEqual(rc, 7)


if __name__ == "__main__":
    unittest.main()
