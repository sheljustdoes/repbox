from __future__ import annotations

import argparse
import os
from pathlib import Path

from . import __version__
from .adapters import RepeatModelerAdapter, default_adapters
from .config import build_app_config
from .logging import setup_logging


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


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return _cmd_run(args)
    if args.command == "check":
        return _cmd_check(args)
    if args.command == "version":
        print(__version__)
        return 0

    parser.error("Unknown command")
    return 2
