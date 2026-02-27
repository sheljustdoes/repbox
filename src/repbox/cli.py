from __future__ import annotations

import argparse
import os
from pathlib import Path

from . import __version__
from .adapters import RepeatModelerAdapter, default_adapters
from .config import build_app_config
from .logging import setup_logging
from .te import run_graph_family_refinement, run_python_fallback_scan


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="repbox", description="RepBox Python CLI scaffold")
    parser.add_argument("--log-level", default="INFO", help="Logging level")

    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run scaffold workflow")
    run_parser.add_argument("--input", required=True, help="Input genome FASTA")
    run_parser.add_argument("--out", required=True, help="Output directory")
    run_parser.add_argument("--threads", type=int, default=1, help="Worker threads")
    run_parser.add_argument(
        "--legacy-config",
        default="repbox_config.txt",
        help="Path to legacy RepBox config file",
    )
    run_parser.add_argument("--engine", default="ncbi", help="Search engine for RepeatModeler")

    check_parser = subparsers.add_parser("check", help="Check configured tool paths")
    check_parser.add_argument(
        "--legacy-config",
        default="repbox_config.txt",
        help="Path to legacy RepBox config file",
    )

    fallback_parser = subparsers.add_parser(
        "fallback-scan",
        help="Run Python fallback TE scans for families with missing/legacy tools",
    )
    fallback_parser.add_argument("--input", required=True, help="Input genome FASTA")
    fallback_parser.add_argument("--out", required=True, help="Output directory")
    fallback_parser.add_argument(
        "--classes",
        default="mite,sine,helitron",
        help="Comma-separated classes: mite,sine,helitron or all",
    )
    fallback_parser.add_argument(
        "--max-candidates",
        type=int,
        default=1000,
        help="Maximum candidates per TE class",
    )

    refine_parser = subparsers.add_parser(
        "refine-families",
        help="Build nested-aware TE families from fallback candidate outputs",
    )
    refine_parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing <class>_candidates.json files",
    )
    refine_parser.add_argument("--out", required=True, help="Output directory")
    refine_parser.add_argument(
        "--classes",
        default="mite,sine",
        help="Comma-separated classes: mite,sine,helitron or all",
    )
    refine_parser.add_argument("--kmer", type=int, default=6, help="k-mer size for similarity graph")
    refine_parser.add_argument(
        "--min-jaccard",
        type=float,
        default=0.25,
        help="Minimum k-mer Jaccard similarity for graph edges",
    )
    refine_parser.add_argument(
        "--min-length-ratio",
        type=float,
        default=0.6,
        help="Minimum shorter/longer length ratio to connect two candidates",
    )

    subparsers.add_parser("version", help="Print RepBox version")
    return parser


def _cmd_run(args: argparse.Namespace) -> int:
    logger = setup_logging(args.log_level)
    config = build_app_config(
        legacy_config_path=args.legacy_config,
        threads=args.threads,
        output_dir=args.out,
    )
    input_path = Path(args.input)
    output_path = Path(args.out)

    if not input_path.exists():
        logger.error("Input FASTA not found: %s", input_path)
        return 2

    output_path.mkdir(parents=True, exist_ok=True)

    logger.info("Milestone B run path: RepeatModeler adapter")
    logger.info("Input: %s", input_path)
    logger.info("Output: %s", output_path)
    logger.info("Threads: %d", args.threads)

    adapter = RepeatModelerAdapter()
    check_result = adapter.check_installation(config.tools)
    if not check_result.exists:
        logger.error(
            "RepeatModeler not available at configured path: %s",
            check_result.configured_path or "<not configured>",
        )
        logger.error(check_result.hint or "Update 'RepeatModeler' in legacy config.")
        logger.error("Update 'RepeatModeler' in %s", args.legacy_config)
        return 1

    if not check_result.is_executable:
        logger.error("RepeatModeler path is not executable: %s", check_result.configured_path)
        logger.error("Fix executable permissions or update 'RepeatModeler' in %s", args.legacy_config)
        return 1

    build_database = config.tools.get("BuildDatabase", "")
    if not build_database:
        logger.error("BuildDatabase is not configured in %s", args.legacy_config)
        return 1
    if not Path(build_database).exists():
        logger.error("BuildDatabase path does not exist: %s", build_database)
        return 1
    if not os.access(build_database, os.X_OK):
        logger.error("BuildDatabase path is not executable: %s", build_database)
        return 1

    try:
        thread_flag = adapter.detect_thread_flag(config.tools)
    except ValueError as exc:
        logger.error(str(exc))
        return 1

    mode = "modern-threads" if thread_flag == "-threads" else "legacy-pa"
    logger.info("RepeatModeler compatibility profile: %s", mode)
    if thread_flag == "-pa":
        logger.warning("Using legacy RepeatModeler thread flag '-pa'. Consider upgrading to 2.0.4+.")

    try:
        run_result = adapter.run_pipeline(
            tools=config.tools,
            input_fasta=input_path,
            output_dir=output_path,
            threads=args.threads,
            engine=args.engine,
            timeout_seconds=float(config.runtime.timeout_seconds),
        )
    except ValueError as exc:
        logger.error(str(exc))
        return 1
    except Exception as exc:
        logger.error("RepeatModeler execution failed: %s", exc)
        return 1

    if run_result.build_database.returncode != 0:
        logger.error("BuildDatabase failed (exit=%d)", run_result.build_database.returncode)
        if run_result.build_database.stderr:
            logger.error(run_result.build_database.stderr.strip())
        return run_result.build_database.returncode

    if run_result.repeatmodeler.returncode != 0:
        logger.error("RepeatModeler failed (exit=%d)", run_result.repeatmodeler.returncode)
        if run_result.repeatmodeler.stderr:
            logger.error(run_result.repeatmodeler.stderr.strip())
        return run_result.repeatmodeler.returncode

    logger.info("RepeatModeler pipeline step completed successfully.")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    logger = setup_logging(args.log_level)
    config = build_app_config(legacy_config_path=args.legacy_config)

    results = [adapter.check_installation(config.tools) for adapter in default_adapters()]
    max_name_len = max(len(result.name) for result in results)
    max_mode_len = max(len(result.compatibility_mode or "-") for result in results)
    max_version_len = max(len(result.version or "-") for result in results)

    logger.info("Checking configured tools from: %s", args.legacy_config)
    missing_or_broken = 0
    for result in results:
        status = "OK"
        if not result.exists:
            status = "MISSING"
        elif not result.is_executable:
            status = "BROKEN"
        elif result.compatibility_mode == "unsupported":
            status = "BROKEN"

        if status != "OK":
            missing_or_broken += 1

        logger.info(
            "%-*s  %-7s  %-*s  %-*s  %s",
            max_name_len,
            result.name,
            status,
            max_version_len,
            result.version or "-",
            max_mode_len,
            result.compatibility_mode or "-",
            result.configured_path or "<not configured>",
        )
        if result.hint:
            logger.info("  hint: %s", result.hint)

    if missing_or_broken:
        logger.warning("%d tool(s) are missing, non-executable, or incompatible.", missing_or_broken)
        return 1

    logger.info("All configured tools are available.")
    return 0


def _cmd_fallback_scan(args: argparse.Namespace) -> int:
    logger = setup_logging(args.log_level)
    input_path = Path(args.input)
    output_path = Path(args.out)

    if not input_path.exists():
        logger.error("Input FASTA not found: %s", input_path)
        return 2

    classes = [item.strip() for item in args.classes.split(",") if item.strip()]
    if not classes:
        logger.error("No TE classes selected. Use --classes mite,sine,helitron or all")
        return 2

    try:
        summary = run_python_fallback_scan(
            input_fasta=input_path,
            output_dir=output_path,
            classes=classes,
            max_candidates_per_class=args.max_candidates,
        )
    except ValueError as exc:
        logger.error(str(exc))
        return 2
    except Exception as exc:
        logger.error("Fallback scan failed: %s", exc)
        return 1

    logger.info("Python fallback scan completed.")
    for family, count in sorted(summary.items()):
        logger.info("%s candidates: %d", family.upper(), count)
    logger.info("Outputs: %s", output_path)
    return 0


def _cmd_refine_families(args: argparse.Namespace) -> int:
    logger = setup_logging(args.log_level)
    input_dir = Path(args.input_dir)
    output_path = Path(args.out)

    if not input_dir.exists() or not input_dir.is_dir():
        logger.error("Input directory not found: %s", input_dir)
        return 2

    classes = [item.strip() for item in args.classes.split(",") if item.strip()]
    if not classes:
        logger.error("No TE classes selected. Use --classes mite,sine,helitron or all")
        return 2

    try:
        summary = run_graph_family_refinement(
            input_dir=input_dir,
            output_dir=output_path,
            classes=classes,
            kmer_size=args.kmer,
            min_jaccard=args.min_jaccard,
            min_length_ratio=args.min_length_ratio,
        )
    except ValueError as exc:
        logger.error(str(exc))
        return 2
    except Exception as exc:
        logger.error("Family refinement failed: %s", exc)
        return 1

    logger.info("Graph refinement completed.")
    logger.info("Input candidates: %d", summary["input_candidates"])
    logger.info("Refined families: %d", summary["refined_families"])
    logger.info("Nested candidates: %d", summary["nested_candidates"])
    logger.info("Outputs: %s", output_path)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return _cmd_run(args)
    if args.command == "check":
        return _cmd_check(args)
    if args.command == "fallback-scan":
        return _cmd_fallback_scan(args)
    if args.command == "refine-families":
        return _cmd_refine_families(args)
    if args.command == "version":
        print(__version__)
        return 0

    parser.error("Unknown command")
    return 2
