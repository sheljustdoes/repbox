from __future__ import annotations

from pathlib import Path
import json
import tempfile
import unittest

from repbox.cli import main
from repbox.te.refinement import run_graph_family_refinement


def _write_candidates(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


class RefinementTests(unittest.TestCase):
    def test_graph_refinement_outputs_family_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_dir = tmp / "fallback"
            input_dir.mkdir(parents=True, exist_ok=True)

            _write_candidates(
                input_dir / "mite_candidates.json",
                [
                    {
                        "family": "MITE",
                        "seq_id": "chr1",
                        "start": 100,
                        "end": 220,
                        "strand": "+",
                        "score": 0.8,
                        "details": {"tir_seed": "AAGGTTCCAA", "tsd_len": "3"},
                        "sequence": "AAGGTTCCAAGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGTTGGAACCTT",
                    },
                    {
                        "family": "MITE",
                        "seq_id": "chr1",
                        "start": 130,
                        "end": 200,
                        "strand": "+",
                        "score": 0.77,
                        "details": {"tir_seed": "AAGGTTCCAA", "tsd_len": "2"},
                        "sequence": "AAGGTTCCAAGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGTTGGAACCTT",
                    },
                    {
                        "family": "MITE",
                        "seq_id": "chr1",
                        "start": 2000,
                        "end": 2140,
                        "strand": "+",
                        "score": 0.74,
                        "details": {"tir_seed": "CCGGAATTCC", "tsd_len": "4"},
                        "sequence": "CCGGAATTCC" + "T" * 120 + "GGAATTCCGG",
                    },
                ],
            )

            summary = run_graph_family_refinement(
                input_dir=input_dir,
                output_dir=tmp / "refined",
                classes=["mite"],
                kmer_size=5,
                min_jaccard=0.2,
                min_length_ratio=0.5,
            )

            self.assertEqual(summary["input_candidates"], 3)
            self.assertTrue((tmp / "refined" / "refined_families.tsv").exists())
            self.assertTrue((tmp / "refined" / "refined_members.tsv").exists())
            self.assertTrue((tmp / "refined" / "refined_library.fa").exists())
            self.assertTrue((tmp / "refined" / "refined_summary.json").exists())

            members = (tmp / "refined" / "refined_members.tsv").read_text(encoding="utf-8")
            self.assertIn("FULLY_NESTED", members)

    def test_cli_refine_families_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            input_dir = tmp / "fallback"
            input_dir.mkdir(parents=True, exist_ok=True)

            _write_candidates(
                input_dir / "sine_candidates.json",
                [
                    {
                        "family": "SINE",
                        "seq_id": "chr2",
                        "start": 100,
                        "end": 260,
                        "strand": "+",
                        "score": 0.73,
                        "details": {"poly_a_len": "12", "a_box": "TGGCTTAGTGG", "b_box": "GTTCAAAAG"},
                        "sequence": "TGGCTTAGTGG" + "C" * 80 + "GTTCAAAAG" + "A" * 12,
                    }
                ],
            )

            rc = main(
                [
                    "refine-families",
                    "--input-dir",
                    str(input_dir),
                    "--out",
                    str(tmp / "refined"),
                    "--classes",
                    "sine",
                ]
            )
            self.assertEqual(rc, 0)
            self.assertTrue((tmp / "refined" / "refined_summary.json").exists())


if __name__ == "__main__":
    unittest.main()
