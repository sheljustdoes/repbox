from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from repbox.adapters.repeatmasker import RepeatMaskerAdapter


class RepeatMaskerAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = RepeatMaskerAdapter()

    def test_build_repeatmasker_command_without_library(self) -> None:
        tools = {"RepeatMasker": "/opt/repeatmasker/RepeatMasker"}
        cmd = self.adapter.build_repeatmasker_command(
            tools=tools,
            genome_fasta=Path("/tmp/genome.fa"),
            output_dir=Path("/tmp/out"),
            threads=8,
            engine="ncbi",
        )
        self.assertEqual(
            cmd,
            [
                "/opt/repeatmasker/RepeatMasker",
                "-pa",
                "8",
                "-engine",
                "ncbi",
                "-dir",
                "/tmp/out",
                "-qq",
                "/tmp/genome.fa",
            ],
        )

    def test_build_repeatmasker_command_with_library(self) -> None:
        tools = {"RepeatMasker": "/opt/repeatmasker/RepeatMasker"}
        cmd = self.adapter.build_repeatmasker_command(
            tools=tools,
            genome_fasta=Path("/tmp/genome.fa"),
            output_dir=Path("/tmp/out"),
            threads=4,
            engine="rmblast",
            library=Path("/tmp/lib.fa"),
        )
        self.assertEqual(
            cmd,
            [
                "/opt/repeatmasker/RepeatMasker",
                "-pa",
                "4",
                "-engine",
                "rmblast",
                "-dir",
                "/tmp/out",
                "-qq",
                "-lib",
                "/tmp/lib.fa",
                "/tmp/genome.fa",
            ],
        )

    def test_run_pipeline_raises_when_tool_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError):
                self.adapter.run_pipeline(
                    tools={},
                    genome_fasta=Path(tmpdir) / "genome.fa",
                    output_dir=Path(tmpdir) / "out",
                    threads=2,
                )


if __name__ == "__main__":
    unittest.main()
