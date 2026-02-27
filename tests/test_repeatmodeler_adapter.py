from __future__ import annotations

import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from repbox.adapters.repeatmodeler import RepeatModelerAdapter, ThreadFlagProbeResult
from repbox.adapters.runner import CommandResult


class RepeatModelerAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = RepeatModelerAdapter()

    def test_probe_thread_flag_uses_threads_when_help_includes_threads(self) -> None:
        fake_result = CommandResult(
            command=["RepeatModeler", "-help"],
            returncode=0,
            stdout="Usage: RepeatModeler ... -threads N",
            stderr="",
            duration_seconds=0.1,
        )
        with mock.patch("repbox.adapters.repeatmodeler.run_command", return_value=fake_result):
            probe = self.adapter.probe_thread_flag("/tmp/RepeatModeler")
        self.assertIsNotNone(probe)
        self.assertEqual(probe.thread_flag, "-threads")

    def test_probe_thread_flag_falls_back_to_version_for_legacy(self) -> None:
        help_result = CommandResult(
            command=["RepeatModeler", "-help"],
            returncode=0,
            stdout="RepeatModeler help text without thread flags",
            stderr="",
            duration_seconds=0.1,
        )
        version_result = CommandResult(
            command=["RepeatModeler", "-version"],
            returncode=0,
            stdout="RepeatModeler version 2.0.1",
            stderr="",
            duration_seconds=0.1,
        )
        with mock.patch(
            "repbox.adapters.repeatmodeler.run_command",
            side_effect=[help_result, help_result, version_result, version_result],
        ):
            probe = self.adapter.probe_thread_flag("/tmp/RepeatModeler")
        self.assertIsNotNone(probe)
        self.assertEqual(probe.thread_flag, "-pa")
        self.assertEqual(probe.version, "2.0.1")

    def test_detect_thread_flag_raises_for_unparseable_probe(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            binary = Path(tmpdir) / "RepeatModeler"
            binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            os.chmod(binary, 0o755)
            tools = {"RepeatModeler": str(binary)}

            with mock.patch.object(self.adapter, "probe_thread_flag", return_value=None):
                with self.assertRaises(ValueError):
                    self.adapter.detect_thread_flag(tools)

    def test_build_repeatmodeler_command_uses_selected_thread_flag(self) -> None:
        tools = {"RepeatModeler": "/opt/repeatmodeler/RepeatModeler"}
        cmd = self.adapter.build_repeatmodeler_command(
            tools=tools,
            database_name="genome",
            threads=4,
            engine="ncbi",
            thread_flag="-threads",
        )
        self.assertEqual(
            cmd,
            [
                "/opt/repeatmodeler/RepeatModeler",
                "-engine",
                "ncbi",
                "-database",
                "genome",
                "-threads",
                "4",
            ],
        )

    def test_check_installation_reports_modern_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            binary = Path(tmpdir) / "RepeatModeler"
            binary.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            os.chmod(binary, 0o755)
            with mock.patch.object(
                self.adapter,
                "probe_thread_flag",
                return_value=ThreadFlagProbeResult(thread_flag="-threads", version="2.0.7"),
            ):
                result = self.adapter.check_installation({"RepeatModeler": str(binary)})
        self.assertTrue(result.exists)
        self.assertTrue(result.is_executable)
        self.assertEqual(result.compatibility_mode, "modern-threads")
        self.assertEqual(result.version, "2.0.7")


if __name__ == "__main__":
    unittest.main()
