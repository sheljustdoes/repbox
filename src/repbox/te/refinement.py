from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class CandidateRecord:
    candidate_id: str
    family: str
    seq_id: str
    start: int
    end: int
    strand: str
    score: float
    details: dict[str, str]
    sequence: str

    @property
    def length(self) -> int:
        return self.end - self.start + 1


@dataclass
class RefinedFamily:
    family_id: str
    family: str
    representative_id: str
    member_ids: list[str]
    representative_sequence: str


def _kmer_set(sequence: str, k: int) -> set[str]:
    if len(sequence) < k:
        return {sequence} if sequence else set()
    return {sequence[i : i + k] for i in range(0, len(sequence) - k + 1)}


def _jaccard_similarity(left: str, right: str, k: int) -> float:
    left_set = _kmer_set(left, k)
    right_set = _kmer_set(right, k)
    if not left_set or not right_set:
        return 0.0
    inter = len(left_set.intersection(right_set))
    union = len(left_set.union(right_set))
    return inter / union if union else 0.0


def _boundary_compatible(left: CandidateRecord, right: CandidateRecord) -> bool:
    family = left.family.upper()
    if family != right.family.upper():
        return False

    if family == "MITE":
        left_tir = str(left.details.get("tir_seed", ""))
        right_tir = str(right.details.get("tir_seed", ""))
        if not left_tir or not right_tir:
            return True
        prefix_matches = sum(1 for a, b in zip(left_tir, right_tir) if a == b)
        required = max(4, min(len(left_tir), len(right_tir)) // 2)
        return prefix_matches >= required

    if family == "SINE":
        left_poly = int(left.details.get("poly_a_len", "0") or "0")
        right_poly = int(right.details.get("poly_a_len", "0") or "0")
        return min(left_poly, right_poly) >= 6

    if family == "HELITRON":
        left_start = str(left.details.get("start_motif", ""))
        right_start = str(right.details.get("start_motif", ""))
        return bool(left_start and right_start and left_start == right_start)

    return True


def _connectable(
    left: CandidateRecord,
    right: CandidateRecord,
    k: int,
    min_jaccard: float,
    min_length_ratio: float,
) -> bool:
    shorter = min(left.length, right.length)
    longer = max(left.length, right.length)
    if longer <= 0:
        return False

    length_ratio = shorter / longer
    if length_ratio < min_length_ratio:
        return False
    if not _boundary_compatible(left, right):
        return False

    return _jaccard_similarity(left.sequence, right.sequence, k=k) >= min_jaccard


def _connected_components(node_ids: list[str], edges: dict[str, set[str]]) -> list[list[str]]:
    seen: set[str] = set()
    components: list[list[str]] = []

    for node_id in node_ids:
        if node_id in seen:
            continue
        stack = [node_id]
        component: list[str] = []
        seen.add(node_id)
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in edges.get(current, set()):
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                stack.append(neighbor)
        components.append(sorted(component))
    return components


def _select_representative(component: list[CandidateRecord], k: int) -> CandidateRecord:
    if len(component) == 1:
        return component[0]

    best = component[0]
    best_score = -1.0
    for left in component:
        total = 0.0
        for right in component:
            if left.candidate_id == right.candidate_id:
                continue
            total += _jaccard_similarity(left.sequence, right.sequence, k=k)
        average = total / max(1, len(component) - 1)
        if average > best_score:
            best_score = average
            best = left
    return best


def _load_candidates(input_dir: Path, classes: list[str]) -> list[CandidateRecord]:
    normalized = [item.strip().lower() for item in classes if item.strip()]
    if "all" in normalized:
        normalized = ["mite", "sine", "helitron"]

    records: list[CandidateRecord] = []
    for class_name in normalized:
        source = input_dir / f"{class_name}_candidates.json"
        if not source.exists():
            continue
        loaded = json.loads(source.read_text(encoding="utf-8"))
        for idx, row in enumerate(loaded, start=1):
            family = str(row.get("family", class_name.upper())).upper()
            records.append(
                CandidateRecord(
                    candidate_id=f"{class_name}_{idx}",
                    family=family,
                    seq_id=str(row["seq_id"]),
                    start=int(row["start"]),
                    end=int(row["end"]),
                    strand=str(row.get("strand", "+")),
                    score=float(row.get("score", 0.0)),
                    details={str(key): str(value) for key, value in dict(row.get("details", {})).items()},
                    sequence=str(row.get("sequence", "")).upper(),
                )
            )
    return records


def _label_nested(records: list[CandidateRecord]) -> dict[str, dict[str, str]]:
    by_seq: dict[str, list[CandidateRecord]] = {}
    for record in records:
        by_seq.setdefault(record.seq_id, []).append(record)

    labels: dict[str, dict[str, str]] = {
        record.candidate_id: {"nested": "NO", "parent_id": "", "nested_round": "0"}
        for record in records
    }

    for seq_id_records in by_seq.values():
        ordered = sorted(seq_id_records, key=lambda item: (item.start, -(item.end - item.start)))
        for idx, record in enumerate(ordered):
            container: CandidateRecord | None = None
            for candidate in ordered:
                if candidate.candidate_id == record.candidate_id:
                    continue
                if candidate.start <= record.start and candidate.end >= record.end and candidate.length > record.length:
                    if container is None or candidate.length < container.length:
                        container = candidate
            if container is None:
                continue

            labels[record.candidate_id]["nested"] = "FULLY_NESTED"
            labels[record.candidate_id]["parent_id"] = container.candidate_id

            depth = 1
            parent_id = container.candidate_id
            visited: set[str] = {record.candidate_id}
            while parent_id and parent_id not in visited:
                visited.add(parent_id)
                parent_label = labels.get(parent_id)
                if not parent_label:
                    break
                parent_parent = parent_label.get("parent_id", "")
                if not parent_parent:
                    break
                depth += 1
                parent_id = parent_parent
            labels[record.candidate_id]["nested_round"] = str(depth)

    return labels


def _write_refinement_outputs(
    output_dir: Path,
    families: list[RefinedFamily],
    records_by_id: dict[str, CandidateRecord],
    nested_labels: dict[str, dict[str, str]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    family_lines = ["family_id\tfamily\trepresentative_id\tmember_count\trepresentative_length\tmember_ids"]
    member_lines = [
        "candidate_id\tfamily_id\tfamily\tseq_id\tstart\tend\tstrand\tscore\tnested\tnested_round\tparent_id"
    ]
    fasta_lines: list[str] = []

    for family in families:
        representative = records_by_id[family.representative_id]
        family_lines.append(
            f"{family.family_id}\t{family.family}\t{family.representative_id}\t{len(family.member_ids)}\t"
            f"{len(family.representative_sequence)}\t{','.join(family.member_ids)}"
        )

        fasta_lines.append(f">{family.family_id}|{family.family}|rep={family.representative_id}")
        fasta_lines.append(family.representative_sequence)

        for member_id in family.member_ids:
            record = records_by_id[member_id]
            nested = nested_labels[member_id]
            member_lines.append(
                f"{member_id}\t{family.family_id}\t{family.family}\t{record.seq_id}\t{record.start}\t"
                f"{record.end}\t{record.strand}\t{record.score}\t{nested['nested']}\t"
                f"{nested['nested_round']}\t{nested['parent_id']}"
            )

    summary = {
        "families": len(families),
        "members": len(records_by_id),
        "nested_members": sum(1 for data in nested_labels.values() if data["nested"] == "FULLY_NESTED"),
        "family_breakdown": {},
    }
    for family in families:
        summary["family_breakdown"].setdefault(family.family, 0)
        summary["family_breakdown"][family.family] += 1

    (output_dir / "refined_families.tsv").write_text("\n".join(family_lines) + "\n", encoding="utf-8")
    (output_dir / "refined_members.tsv").write_text("\n".join(member_lines) + "\n", encoding="utf-8")
    (output_dir / "refined_library.fa").write_text(
        "\n".join(fasta_lines) + ("\n" if fasta_lines else ""),
        encoding="utf-8",
    )
    (output_dir / "refined_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def run_graph_family_refinement(
    input_dir: Path,
    output_dir: Path,
    classes: list[str],
    kmer_size: int = 6,
    min_jaccard: float = 0.25,
    min_length_ratio: float = 0.6,
) -> dict[str, int]:
    records = _load_candidates(input_dir=input_dir, classes=classes)
    if not records:
        raise ValueError("No candidate JSON files found for requested classes.")

    records_by_id = {record.candidate_id: record for record in records}
    nested_labels = _label_nested(records)

    families: list[RefinedFamily] = []
    serial_by_class: dict[str, int] = {}

    family_groups: dict[str, list[CandidateRecord]] = {}
    for record in records:
        family_groups.setdefault(record.family, []).append(record)

    for family_name, family_records in sorted(family_groups.items()):
        node_ids = [record.candidate_id for record in family_records]
        edges: dict[str, set[str]] = {node_id: set() for node_id in node_ids}

        for left_idx in range(0, len(family_records)):
            for right_idx in range(left_idx + 1, len(family_records)):
                left = family_records[left_idx]
                right = family_records[right_idx]
                if not _connectable(
                    left=left,
                    right=right,
                    k=kmer_size,
                    min_jaccard=min_jaccard,
                    min_length_ratio=min_length_ratio,
                ):
                    continue
                edges[left.candidate_id].add(right.candidate_id)
                edges[right.candidate_id].add(left.candidate_id)

        components = _connected_components(node_ids=node_ids, edges=edges)
        for component in components:
            members = [records_by_id[item] for item in component]
            representative = _select_representative(members, k=kmer_size)

            serial_by_class.setdefault(family_name, 0)
            serial_by_class[family_name] += 1
            family_id = f"{family_name}_FAM_{serial_by_class[family_name]}"

            families.append(
                RefinedFamily(
                    family_id=family_id,
                    family=family_name,
                    representative_id=representative.candidate_id,
                    member_ids=component,
                    representative_sequence=representative.sequence,
                )
            )

    _write_refinement_outputs(
        output_dir=output_dir,
        families=families,
        records_by_id=records_by_id,
        nested_labels=nested_labels,
    )

    return {
        "input_candidates": len(records),
        "refined_families": len(families),
        "nested_candidates": sum(1 for data in nested_labels.values() if data["nested"] == "FULLY_NESTED"),
    }
