from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .adapters import default_adapters
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
    input_path = Path(args.input)
    output_path = Path(args.out)

    if not input_path.exists():
        logger.error("Input FASTA not found: %s", input_path)
        return 2

    output_path.mkdir(parents=True, exist_ok=True)

    logger.info("Milestone A scaffold run")
    logger.info("Input: %s", input_path)
    logger.info("Output: %s", output_path)
    logger.info("Threads: %d", args.threads)
    logger.info("No legacy pipeline behavior has been executed in this scaffold command.")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    logger = setup_logging(args.log_level)
    config = build_app_config(legacy_config_path=args.legacy_config)

    results = [adapter.check_installation(config.tools) for adapter in default_adapters()]
    max_name_len = max(len(result.name) for result in results)

    logger.info("Checking configured tools from: %s", args.legacy_config)
    missing = 0
    for result in results:
        status = "OK" if result.exists else "MISSING"
        if not result.exists:
            missing += 1

        logger.info(
            "%-*s  %-7s  %s",
            max_name_len,
            result.name,
            status,
            result.configured_path or "<not configured>",
        )

    if missing:
        logger.warning("%d tool(s) are missing or not configured.", missing)
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
