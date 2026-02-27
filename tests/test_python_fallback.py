from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from repbox.cli import main
from repbox.te.python_fallback import run_python_fallback_scan


def _toy_genome() -> str:
    mite_left = "AAGGTTCCAA"
    mite_right = "TTGGAACCTT"
    mite_body = "G" * 90

    sine_fragment = "TGGCTTAGTGG" + "C" * 30 + "GTTCAAAAG" + "T" * 20 + "AAAAAAAAAA"
    helitron_fragment = "TC" + "C" * 120 + "CTAG"

    sequence = "NNNN" + mite_left + mite_body + mite_right + "NNNN" + sine_fragment + "NNNN" + helitron_fragment
    return f">chr1\n{sequence}\n"


class PythonFallbackTests(unittest.TestCase):
    def test_run_python_fallback_scan_writes_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fasta = tmp / "genome.fa"
            fasta.write_text(_toy_genome(), encoding="utf-8")

            out = tmp / "fallback"
            summary = run_python_fallback_scan(
                input_fasta=fasta,
                output_dir=out,
                classes=["mite", "sine", "helitron"],
                max_candidates_per_class=100,
            )

            self.assertIn("mite", summary)
            self.assertIn("sine", summary)
            self.assertIn("helitron", summary)
            self.assertTrue((out / "summary.json").exists())
            self.assertTrue((out / "mite_candidates.tsv").exists())
            self.assertTrue((out / "sine_candidates.tsv").exists())
            self.assertTrue((out / "helitron_candidates.tsv").exists())

    def test_cli_fallback_scan_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            fasta = tmp / "genome.fa"
            fasta.write_text(_toy_genome(), encoding="utf-8")

            out = tmp / "scan_out"
            rc = main(
                [
                    "fallback-scan",
                    "--input",
                    str(fasta),
                    "--out",
                    str(out),
                    "--classes",
                    "all",
                    "--max-candidates",
                    "50",
                ]
            )

            self.assertEqual(rc, 0)
            self.assertTrue((out / "summary.json").exists())


if __name__ == "__main__":
    unittest.main()
