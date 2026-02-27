from __future__ import annotations

import json
import io
from contextlib import redirect_stdout
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

    def test_run_logs_prerequisite_diagnostics_when_builddatabase_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_fa = tmp / "genome.fa"
            input_fa.write_text(">x\nACGT\n", encoding="utf-8")
            rm = tmp / "RepeatModeler"
            _make_executable(rm)
            config_path = tmp / "repbox_config.txt"
            _write_legacy_config(config_path, {"RepeatModeler": str(rm)})

            with self.assertLogs("repbox", level="ERROR") as logs:
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
        combined = "\n".join(logs.output)
        self.assertIn("Run prerequisites failed", combined)
        self.assertIn("BuildDatabase [MISSING]", combined)

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

    def test_run_skips_repeatmasker_when_not_configured(self) -> None:
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
                        returncode=0,
                        stdout="ok",
                        stderr="",
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
        self.assertEqual(rc, 0)

    def test_smoke_fails_when_input_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            config_path = tmp / "repbox_config.txt"
            _write_legacy_config(config_path, {})

            rc = main(
                [
                    "smoke",
                    "--input",
                    str(tmp / "missing.fa"),
                    "--out",
                    str(tmp / "out"),
                    "--legacy-config",
                    str(config_path),
                ]
            )

        self.assertEqual(rc, 2)

    def test_smoke_writes_report_and_passes_when_tools_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_fa = tmp / "genome.fa"
            input_fa.write_text(">x\nACGT\n", encoding="utf-8")
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
                out_dir = tmp / "out"
                rc = main(
                    [
                        "smoke",
                        "--input",
                        str(input_fa),
                        "--out",
                        str(out_dir),
                        "--legacy-config",
                        str(config_path),
                    ]
                )

            self.assertEqual(rc, 0)
            report_path = out_dir / "smoke_report.txt"
            self.assertTrue(report_path.exists())
            report = report_path.read_text(encoding="utf-8")
            self.assertIn("schema_version=1", report)
            self.assertIn("tools_total=8", report)
            self.assertIn("tools_failing=0", report)

    def test_smoke_writes_failing_tool_details_in_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_fa = tmp / "genome.fa"
            input_fa.write_text(">x\nACGT\n", encoding="utf-8")
            config_path = tmp / "repbox_config.txt"
            _write_legacy_config(config_path, {})

            out_dir = tmp / "out"
            rc = main(
                [
                    "smoke",
                    "--input",
                    str(input_fa),
                    "--out",
                    str(out_dir),
                    "--legacy-config",
                    str(config_path),
                ]
            )

            self.assertEqual(rc, 1)
            report = (out_dir / "smoke_report.txt").read_text(encoding="utf-8")
            self.assertIn("schema_version=1", report)
            self.assertIn("failing_tools=", report)
            self.assertIn("RepeatModeler.status=MISSING", report)
            self.assertIn("BuildDatabase.status=MISSING", report)

    def test_smoke_report_returns_error_when_file_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = Path(tmpdir) / "smoke_report.txt"
            rc = main(["smoke-report", "--report", str(missing)])
        self.assertEqual(rc, 2)

    def test_smoke_report_parses_passing_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "smoke_report.txt"
            report_path.write_text(
                "\n".join(
                    [
                        "input=/tmp/in.fa",
                        "output=/tmp/out",
                        "tools_total=8",
                        "tools_failing=0",
                        "failing_tools=-",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            rc = main(["smoke-report", "--report", str(report_path)])
        self.assertEqual(rc, 0)

    def test_smoke_report_parses_failing_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "smoke_report.txt"
            report_path.write_text(
                "\n".join(
                    [
                        "input=/tmp/in.fa",
                        "output=/tmp/out",
                        "tools_total=8",
                        "tools_failing=2",
                        "failing_tools=RepeatModeler,BuildDatabase",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            rc = main(["smoke-report", "--report", str(report_path)])
        self.assertEqual(rc, 1)

    def test_smoke_report_json_pass_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "smoke_report.txt"
            report_path.write_text(
                "\n".join(
                    [
                        "input=/tmp/in.fa",
                        "output=/tmp/out",
                        "tools_total=8",
                        "tools_failing=0",
                        "failing_tools=-",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            stream = io.StringIO()
            with redirect_stdout(stream):
                rc = main(["smoke-report", "--report", str(report_path), "--json"])

        self.assertEqual(rc, 0)
        payload = json.loads(stream.getvalue().strip())
        self.assertEqual(payload["schema_version"], "0")
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["tools_failing"], 0)
        self.assertEqual(payload["failing_tools"], [])

    def test_smoke_report_json_fail_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "smoke_report.txt"
            report_path.write_text(
                "\n".join(
                    [
                        "input=/tmp/in.fa",
                        "output=/tmp/out",
                        "tools_total=8",
                        "tools_failing=2",
                        "failing_tools=RepeatModeler,BuildDatabase",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            stream = io.StringIO()
            with redirect_stdout(stream):
                rc = main(["smoke-report", "--report", str(report_path), "--json"])

        self.assertEqual(rc, 1)
        payload = json.loads(stream.getvalue().strip())
        self.assertEqual(payload["schema_version"], "0")
        self.assertEqual(payload["status"], "fail")
        self.assertEqual(payload["tools_failing"], 2)
        self.assertEqual(payload["failing_tools"], ["RepeatModeler", "BuildDatabase"])

    def test_smoke_report_rejects_unsupported_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "smoke_report.txt"
            report_path.write_text(
                "\n".join(
                    [
                        "schema_version=99",
                        "tools_total=8",
                        "tools_failing=0",
                        "failing_tools=-",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            stream = io.StringIO()
            with redirect_stdout(stream):
                rc = main(["smoke-report", "--report", str(report_path), "--json"])

        self.assertEqual(rc, 1)
        payload = json.loads(stream.getvalue().strip())
        self.assertEqual(payload["error"], "unsupported_schema")
        self.assertEqual(payload["schema_version"], "99")


if __name__ == "__main__":
    unittest.main()
