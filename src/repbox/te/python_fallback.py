from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re


def _reverse_complement(seq: str) -> str:
    table = str.maketrans("ACGTNacgtn", "TGCANtgcan")
    return seq.translate(table)[::-1]


def _read_fasta(path: Path) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    header = ""
    sequence_parts: list[str] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header:
                records.append((header, "".join(sequence_parts).upper()))
            header = line[1:].split()[0]
            sequence_parts = []
            continue
        sequence_parts.append(line)
    if header:
        records.append((header, "".join(sequence_parts).upper()))
    return records


@dataclass
class Candidate:
    family: str
    seq_id: str
    start: int
    end: int
    strand: str
    score: float
    details: dict[str, str]
    sequence: str


def _find_mite_candidates(
    records: list[tuple[str, str]],
    min_len: int = 80,
    max_len: int = 800,
    min_tir_seed: int = 10,
    max_candidates: int = 1000,
) -> list[Candidate]:
    candidates: list[Candidate] = []
    for seq_id, seq in records:
        n = len(seq)
        if n < min_len:
            continue

        for left in range(0, n - min_len + 1):
            if len(candidates) >= max_candidates:
                return candidates

            seed = seq[left : left + min_tir_seed]
            if "N" in seed:
                continue
            rc_seed = _reverse_complement(seed)
            search_start = left + min_len - min_tir_seed
            search_end = min(n - min_tir_seed + 1, left + max_len)
            if search_start >= search_end:
                continue

            region = seq[search_start:search_end]
            offset = region.find(rc_seed)
            if offset < 0:
                continue

            right = search_start + offset
            end = right + min_tir_seed
            span = end - left
            if span < min_len or span > max_len:
                continue

            tsd = ""
            tsd_len = 0
            for k in range(2, 11):
                if left - k < 0 or end + k > n:
                    continue
                left_flank = seq[left - k : left]
                right_flank = seq[end : end + k]
                if left_flank == right_flank:
                    tsd = left_flank
                    tsd_len = k
                    break

            score = 0.5
            if tsd_len:
                score += min(0.4, tsd_len / 20)
            score += min(0.1, min_tir_seed / 20)

            candidates.append(
                Candidate(
                    family="MITE",
                    seq_id=seq_id,
                    start=left + 1,
                    end=end,
                    strand="+",
                    score=round(score, 3),
                    details={
                        "tir_seed": seed,
                        "tir_seed_rc": rc_seed,
                        "tsd": tsd,
                        "tsd_len": str(tsd_len),
                        "length": str(span),
                    },
                    sequence=seq[left:end],
                )
            )
    return candidates


def _find_sine_candidates(
    records: list[tuple[str, str]],
    min_len: int = 80,
    max_len: int = 700,
    min_poly_a: int = 8,
    max_candidates: int = 1000,
) -> list[Candidate]:
    candidates: list[Candidate] = []
    a_box = re.compile(r"TGG[CTA]..AGTGG")
    b_box = re.compile(r"GTTC[AG].{2,8}G")
    poly_a = re.compile(rf"A{{{min_poly_a},}}$")

    for seq_id, seq in records:
        if len(candidates) >= max_candidates:
            return candidates

        for tail in re.finditer(rf"A{{{min_poly_a},}}", seq):
            if len(candidates) >= max_candidates:
                return candidates

            tail_start = tail.start()
            window_start = max(0, tail_start - max_len)
            window_end = min(len(seq), tail.end())
            window = seq[window_start:window_end]

            if len(window) < min_len or not poly_a.search(window):
                continue

            a_hit = a_box.search(window)
            b_hit = b_box.search(window)
            if not a_hit or not b_hit or b_hit.start() <= a_hit.start():
                continue

            start = window_start + 1
            end = window_end
            length = end - start + 1
            if length < min_len or length > max_len:
                continue

            score = 0.45
            score += 0.2 if a_hit else 0
            score += 0.2 if b_hit else 0
            score += min(0.15, (tail.end() - tail.start()) / 100)

            candidates.append(
                Candidate(
                    family="SINE",
                    seq_id=seq_id,
                    start=start,
                    end=end,
                    strand="+",
                    score=round(score, 3),
                    details={
                        "a_box": a_hit.group(0),
                        "b_box": b_hit.group(0),
                        "poly_a_len": str(tail.end() - tail.start()),
                        "length": str(length),
                    },
                    sequence=seq[start - 1 : end],
                )
            )
    return candidates


def _find_helitron_candidates(
    records: list[tuple[str, str]],
    min_len: int = 100,
    max_len: int = 30000,
    max_candidates: int = 1000,
) -> list[Candidate]:
    candidates: list[Candidate] = []
    terminal_end = re.compile(r"CT[AG][AG]")

    for seq_id, seq in records:
        n = len(seq)
        if n < min_len:
            continue

        starts = [m.start() for m in re.finditer("TC", seq)]
        for left in starts:
            if len(candidates) >= max_candidates:
                return candidates

            search_start = left + min_len
            search_end = min(n, left + max_len)
            if search_start >= search_end:
                continue

            region = seq[search_start:search_end]
            end_match = terminal_end.search(region)
            if not end_match:
                continue

            right = search_start + end_match.end()
            length = right - left
            if length < min_len or length > max_len:
                continue

            score = 0.4
            score += 0.2 if seq[left : left + 2] == "TC" else 0
            score += 0.2 if terminal_end.fullmatch(seq[right - 4 : right]) else 0
            score += 0.2 if "AT" in seq[max(0, left - 2) : left] else 0

            candidates.append(
                Candidate(
                    family="HELITRON",
                    seq_id=seq_id,
                    start=left + 1,
                    end=right,
                    strand="+",
                    score=round(score, 3),
                    details={
                        "start_motif": seq[left : left + 2],
                        "end_motif": seq[right - 4 : right],
                        "length": str(length),
                    },
                    sequence=seq[left:right],
                )
            )
    return candidates


def _write_outputs(output_dir: Path, candidates: list[Candidate], family: str) -> None:
    family_key = family.lower()
    tsv_path = output_dir / f"{family_key}_candidates.tsv"
    fasta_path = output_dir / f"{family_key}_candidates.fa"
    json_path = output_dir / f"{family_key}_candidates.json"

    tsv_lines = ["family\tseq_id\tstart\tend\tstrand\tscore\tdetails"]
    fasta_lines: list[str] = []
    json_records = []

    for idx, candidate in enumerate(candidates, start=1):
        details_text = ";".join(f"{key}={value}" for key, value in candidate.details.items())
        tsv_lines.append(
            f"{candidate.family}\t{candidate.seq_id}\t{candidate.start}\t{candidate.end}\t"
            f"{candidate.strand}\t{candidate.score}\t{details_text}"
        )
        fasta_lines.append(
            f">{candidate.family}_{idx}|{candidate.seq_id}:{candidate.start}-{candidate.end}|score={candidate.score}"
        )
        fasta_lines.append(candidate.sequence)
        json_records.append(
            {
                "family": candidate.family,
                "seq_id": candidate.seq_id,
                "start": candidate.start,
                "end": candidate.end,
                "strand": candidate.strand,
                "score": candidate.score,
                "details": candidate.details,
                "sequence": candidate.sequence,
            }
        )

    tsv_path.write_text("\n".join(tsv_lines) + "\n", encoding="utf-8")
    fasta_path.write_text("\n".join(fasta_lines) + ("\n" if fasta_lines else ""), encoding="utf-8")
    json_path.write_text(json.dumps(json_records, indent=2) + "\n", encoding="utf-8")


def run_python_fallback_scan(
    input_fasta: Path,
    output_dir: Path,
    classes: list[str],
    max_candidates_per_class: int = 1000,
) -> dict[str, int]:
    records = _read_fasta(input_fasta)
    output_dir.mkdir(parents=True, exist_ok=True)

    normalized = {item.strip().lower() for item in classes if item.strip()}
    if "all" in normalized:
        normalized = {"mite", "sine", "helitron"}

    supported = {"mite", "sine", "helitron"}
    unsupported = normalized - supported
    if unsupported:
        ordered = ", ".join(sorted(unsupported))
        raise ValueError(f"Unsupported fallback classes: {ordered}")

    summary: dict[str, int] = {}
    for item in sorted(normalized):
        if item == "mite":
            candidates = _find_mite_candidates(records, max_candidates=max_candidates_per_class)
            family = "MITE"
        elif item == "sine":
            candidates = _find_sine_candidates(records, max_candidates=max_candidates_per_class)
            family = "SINE"
        else:
            candidates = _find_helitron_candidates(records, max_candidates=max_candidates_per_class)
            family = "HELITRON"

        _write_outputs(output_dir=output_dir, candidates=candidates, family=family)
        summary[item] = len(candidates)

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary
