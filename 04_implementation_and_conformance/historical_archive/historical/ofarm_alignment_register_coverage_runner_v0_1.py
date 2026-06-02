#!/usr/bin/env python3
"""OFARM alignment-register coverage review runner v0.1.

This runner machine-checks whether each canonical concept in the harmonized
Alignment Register has evidence across the current standalone OFARM package.

It does not change baseline law. It emits a conformance-side review artifact
showing where each register concept is evidenced across:
- 00_active_baseline
- 01_companion_artifacts
- 02_accepted_rfcs
- 03_machine_contracts
- 04_implementation_and_conformance
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
ALIGNMENT_REGISTER_CANDIDATES = [
    ROOT / "00_active_baseline/OFARM_Alignment_Register_v0_13.md",
]
OUTPUT_DIR = Path(__file__).resolve().parent

TEXT_SUFFIXES = {".md", ".json", ".py", ".csv", ".txt"}

MANUAL_ALIASES: Dict[str, List[str]] = {
    "PhenologyState": ["phenology stage", "cropStage", "BBCH"],
    "LocalConditionPattern": ["local condition", "condition pattern"],
    "PlannedIntervention": ["planned intervention"],
    "OperationRecord": ["operation record", "operation claim"],
    "MaterializationFreshnessState": ["freshness state", "requiredFreshness", "FRESH", "STALE", "INVALID"],
    "TraceabilityLineage": ["lot lineage", "traceability lineage", "LineageChange", "lineage"],
    "ComplianceSubmission": ["submission assembly", "submission filing", "SubmissionAssembly"],
    "InspectionCase": ["inspection case", "inspection"],
    "Variety / cultivar": ["variety", "cultivar"],
}

SELF_REFERENTIAL_NAMES = {
    "OFARM_conformance_coverage_matrix_v0_1.md",
    "OFARM_conformance_seed_set_v0_1.md",
    "OFARM_Runtime_Alignment_Register_Coverage_Fixtures_v0_1.md",
    "OFARM_alignment_register_coverage_records_v0_1.json",
    "OFARM_alignment_register_gap_records_v0_1.json",
    "OFARM_alignment_register_coverage_summary_v0_1.json",
    "OFARM_alignment_register_coverage_results_v0_1.json",
    "OFARM_wave21_alignment_register_coverage_hardening_memo_v0_1.md",
    "ofarm_alignment_register_coverage_runner_v0_1.py",
    "OFARM_post_hardening_readiness_gate_memo_v0_1.md",
    "OFARM_post_hardening_readiness_snapshot_v0_1.json",
}


def load_alignment_register_path() -> Path:
    for candidate in ALIGNMENT_REGISTER_CANDIDATES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No harmonized Alignment Register file found inside the current package.")


def parse_alignment_register(path: Path) -> List[Dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    if "## 3. Register" not in text or "## 4." not in text:
        raise ValueError("Alignment Register structure is not in the expected format.")
    section = text.split("## 3. Register", 1)[1].split("## 4.", 1)[0]
    lines = [line for line in section.splitlines() if line.strip().startswith("|")]
    rows: List[Dict[str, str]] = []
    for line in lines[2:]:
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 6:
            continue
        rows.append(
            {
                "concept": parts[0],
                "mainLayer": parts[1],
                "alignmentClass": parts[2],
                "externalAnchors": parts[3],
                "canonicalNamingChoice": parts[4],
                "reason": parts[5],
            }
        )
    if not rows:
        raise ValueError("No register rows parsed from Alignment Register.")
    return rows


def gather_workspace_files() -> List[Path]:
    files: List[Path] = []

    def include_file(path: Path) -> bool:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            return False
        if path.name in SELF_REFERENTIAL_NAMES:
            return False
        value = str(path)
        if "/historical_patches/" in value or "/historical_outputs/" in value or "/reviewed_preimplementation_thread_v0_2/" in value:
            return False
        return True

    for sub in ["00_active_baseline", "01_companion_artifacts", "02_accepted_rfcs", "03_machine_contracts", "04_implementation_and_conformance"]:
        target = ROOT / sub
        if target.exists():
            files.extend([f for f in target.rglob("*") if f.is_file() and include_file(f)])

    deduped: List[Path] = []
    seen = set()
    for path in files:
        s = str(path)
        if s not in seen:
            seen.add(s)
            deduped.append(path)
    return deduped


def file_category(path: Path) -> str:
    value = str(path)
    if "/00_active_baseline/" in value:
        return "BASELINE"
    if "/01_companion_artifacts/" in value:
        return "COMPANION"
    if "/02_accepted_rfcs/" in value:
        return "RFC"
    if "/03_machine_contracts/" in value:
        return "CONTRACT"
    if "/04_implementation_and_conformance/" in value:
        return "CONFORMANCE"
    return "OTHER"


def split_candidates(concept: str) -> List[str]:
    value = concept.replace("“", "").replace("”", "").replace("’", "'")
    parts = [part.strip() for part in re.split(r"\s*/\s*", value)]
    out: List[str] = []
    for part in parts:
        part = re.sub(r"\([^)]*\)", "", part).strip()
        if part:
            out.append(part)
    return out


def words(term: str) -> List[str]:
    value = term.replace("-", " ")
    value = re.sub(r"([a-z])([A-Z])", r"\1 \2", value)
    value = re.sub(r"[^A-Za-z0-9 ]+", " ", value)
    return [word for word in value.split() if word]


def lcfirst(value: str) -> str:
    return value[:1].lower() + value[1:] if value else value


def variants_for_term(term: str) -> List[str]:
    ws = words(term)
    out = set()
    if term:
        out.add(term)
    if ws:
        pascal = "".join(word.capitalize() if not word.isupper() else word for word in ws)
        camel = lcfirst(pascal)
        snake = "_".join(word.lower() for word in ws)
        kebab = "-".join(word.lower() for word in ws)
        spaced = " ".join(ws)
        for candidate in [pascal, camel, snake, kebab, spaced]:
            if candidate:
                out.add(candidate)
                out.add(candidate + "Ref")
                out.add(candidate + "Refs")
                out.add(candidate + "Id")
                out.add(candidate + "Ids")
    return sorted(out, key=lambda x: (len(x), x), reverse=True)


def variants_for_concept(concept: str) -> List[str]:
    out = {concept}
    for term in split_candidates(concept):
        out.update(variants_for_term(term))
    out.update(MANUAL_ALIASES.get(concept, []))
    return sorted(out, key=lambda x: (len(x), x), reverse=True)


def find_hits(concept: str, files: Iterable[Path], cache: Dict[str, str], alignment_register_path: Path) -> Dict[str, List[str]]:
    variants = variants_for_concept(concept)
    hits_by_category: Dict[str, List[str]] = defaultdict(list)

    for path in files:
        if path == alignment_register_path:
            continue
        key = str(path)
        haystack = (cache[key] + "\n" + path.name).lower()
        found = False
        for variant in variants:
            if len(variant) < 4:
                continue
            if variant.lower() in haystack:
                found = True
                break
        if found:
            category = file_category(path)
            hits_by_category[category].append(str(path.relative_to(ROOT)))

    out: Dict[str, List[str]] = {}
    for category, refs in hits_by_category.items():
        seen = set()
        ordered: List[str] = []
        for ref in refs:
            if ref not in seen:
                seen.add(ref)
                ordered.append(ref)
        out[category] = ordered
    return out


def evidence_strength(hit_counts: Dict[str, int]) -> str:
    non_register_total = sum(hit_counts.values())
    if non_register_total == 0:
        return "REGISTER_ONLY"
    if hit_counts.get("RFC", 0) + hit_counts.get("CONTRACT", 0) + hit_counts.get("CONFORMANCE", 0) >= 1:
        return "STRONG"
    if hit_counts.get("BASELINE", 0) + hit_counts.get("COMPANION", 0) >= 1:
        return "MODERATE"
    return "LOW"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    alignment_register_path = load_alignment_register_path()
    rows = parse_alignment_register(alignment_register_path)
    files = gather_workspace_files()

    cache: Dict[str, str] = {}
    for path in files:
        try:
            cache[str(path)] = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            cache[str(path)] = ""

    coverage_records: List[Dict[str, object]] = []
    gap_records: List[Dict[str, object]] = []

    for row in rows:
        hits = find_hits(row["concept"], files, cache, alignment_register_path)
        hit_counts = {category: len(refs) for category, refs in hits.items()}
        strength = evidence_strength(hit_counts)

        record: Dict[str, object] = {
            **row,
            "evidenceStrength": strength,
            "hitCounts": hit_counts,
            "sampleRefs": {category: refs[:5] for category, refs in hits.items()},
        }
        coverage_records.append(record)

        if strength in {"REGISTER_ONLY", "LOW"}:
            gap_records.append(
                {
                    "concept": row["concept"],
                    "alignmentClass": row["alignmentClass"],
                    "mainLayer": row["mainLayer"],
                    "issue": "No non-register workspace evidence found." if strength == "REGISTER_ONLY" else "Only low-strength non-register evidence found.",
                    "recommendedNextClosure": "Add at least one active-substance or conformance-side artifact that uses the concept explicitly beyond the Alignment Register.",
                }
            )

    strength_counts = Counter(record["evidenceStrength"] for record in coverage_records)
    class_counts = Counter(record["alignmentClass"] for record in coverage_records)
    by_class = defaultdict(Counter)
    for record in coverage_records:
        by_class[record["alignmentClass"]][record["evidenceStrength"]] += 1

    results: Dict[str, object] = {
        "alignmentRegisterSource": str(alignment_register_path.relative_to(ROOT)),
        "workspaceRootUsed": str(ROOT),
        "counts": {
            "registerConcepts": len(coverage_records),
            "workspaceFilesScanned": len(files),
            "strengthCounts": dict(strength_counts),
            "alignmentClassCounts": dict(class_counts),
            "strengthByAlignmentClass": {key: dict(value) for key, value in by_class.items()},
            "gapConcepts": len(gap_records),
        },
        "overall": "PASS" if not gap_records else "PASS_WITH_LIMITATIONS",
        "notes": [
            "This review checks standalone-package evidence coverage for each Alignment Register concept.",
            "It intentionally excludes self-generated alignment coverage artifacts and stale readiness snapshots that would otherwise create circular evidence.",
            "REGISTER_ONLY rows are not silent failures; they are emitted as explicit follow-on coverage targets."
        ],
    }

    summary = {
        "registerConcepts": len(coverage_records),
        "workspaceFilesScanned": len(files),
        "strengthCounts": dict(strength_counts),
        "alignmentClassCounts": dict(class_counts),
        "strengthByAlignmentClass": {key: dict(value) for key, value in by_class.items()},
        "gapConcepts": len(gap_records),
    }

    (OUTPUT_DIR / "OFARM_alignment_register_coverage_records_v0_1.json").write_text(json.dumps(coverage_records, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "OFARM_alignment_register_gap_records_v0_1.json").write_text(json.dumps(gap_records, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "OFARM_alignment_register_coverage_summary_v0_1.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "OFARM_alignment_register_coverage_results_v0_1.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
