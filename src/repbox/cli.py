from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .adapters import AdapterCheckResult, RepeatMaskerAdapter, RepeatModelerAdapter, default_adapters
from .config import build_app_config
from .logging import setup_logging


SMOKE_REPORT_SCHEMA_VERSION = "1"


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

    smoke_parser = subparsers.add_parser(
        "smoke",
        help="Run lightweight environment/input smoke checks",
    )
    smoke_parser.add_argument("--input", required=True, help="Input genome FASTA")
    smoke_parser.add_argument("--out", required=True, help="Output directory")
    smoke_parser.add_argument(
        "--legacy-config",
        default="repbox_config.txt",
        help="Path to legacy RepBox config file",
    )

    smoke_report_parser = subparsers.add_parser(
        "smoke-report",
        help="Read and summarize a smoke report file",
    )
    smoke_report_parser.add_argument(
        "--report",
        required=True,
        help="Path to smoke_report.txt",
    )
    smoke_report_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON summary",
    )

    subparsers.add_parser("version", help="Print RepBox version")
    return parser


def _tool_status(result: AdapterCheckResult) -> str:
    if not result.exists:
        return "MISSING"
    if not result.is_executable:
        return "BROKEN"
    if result.compatibility_mode == "unsupported":
        return "BROKEN"
    return "OK"


def _log_tool_diagnostics(logger, results: list[AdapterCheckResult], level: str = "warning") -> None:
    failing = [result for result in results if _tool_status(result) != "OK"]
    if not failing:
        return

    log_fn = logger.warning if level == "warning" else logger.error
    names = ", ".join(result.name for result in failing)
    log_fn("Tool diagnostics: %d failing tool(s): %s", len(failing), names)
    for result in failing:
        status = _tool_status(result)
        log_fn(
            "  %s [%s] path=%s",
            result.name,
            status,
            result.configured_path or "<not configured>",
        )
        if result.hint:
            log_fn("    hint: %s", result.hint)


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
    repeatmodeler_result = adapter.check_installation(config.tools)
    build_database_result = next(
        item for item in default_adapters() if item.name == "BuildDatabase"
    ).check_installation(config.tools)
    required_results = [repeatmodeler_result, build_database_result]
    required_failing = [
        result
        for result in required_results
        if (not result.exists) or (not result.is_executable)
    ]
    if required_failing:
        logger.error("Run prerequisites failed. Fix required tool configuration before retrying.")
        _log_tool_diagnostics(logger, required_results, level="error")
        logger.error("Config file: %s", args.legacy_config)
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

    repeatmasker_adapter = RepeatMaskerAdapter()
    repeatmasker_check = repeatmasker_adapter.check_installation(config.tools)
    if not repeatmasker_check.exists:
        logger.info("RepeatMasker not configured/found; skipping masking step.")
        return 0
    if not repeatmasker_check.is_executable:
        logger.warning("RepeatMasker configured but not executable; skipping masking step.")
        return 0

    logger.info("Running optional RepeatMasker step.")
    try:
        rm_result = repeatmasker_adapter.run_pipeline(
            tools=config.tools,
            genome_fasta=input_path,
            output_dir=output_path,
            threads=args.threads,
            engine=args.engine,
            timeout_seconds=float(config.runtime.timeout_seconds),
        )
    except ValueError as exc:
        logger.error(str(exc))
        return 1
    except Exception as exc:
        logger.error("RepeatMasker execution failed: %s", exc)
        return 1

    if rm_result.repeatmasker.returncode != 0:
        logger.error("RepeatMasker failed (exit=%d)", rm_result.repeatmasker.returncode)
        if rm_result.repeatmasker.stderr:
            logger.error(rm_result.repeatmasker.stderr.strip())
        return rm_result.repeatmasker.returncode

    logger.info("RepeatMasker step completed successfully.")
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
        status = _tool_status(result)

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


def _cmd_smoke(args: argparse.Namespace) -> int:
    logger = setup_logging(args.log_level)
    config = build_app_config(legacy_config_path=args.legacy_config)

    input_path = Path(args.input)
    output_path = Path(args.out)

    if not input_path.exists():
        logger.error("Input FASTA not found: %s", input_path)
        return 2

    output_path.mkdir(parents=True, exist_ok=True)

    results = [adapter.check_installation(config.tools) for adapter in default_adapters()]
    failing = [
        result
        for result in results
        if (not result.exists) or (not result.is_executable) or (result.compatibility_mode == "unsupported")
    ]

    report_path = output_path / "smoke_report.txt"
    report_lines = [
        f"schema_version={SMOKE_REPORT_SCHEMA_VERSION}",
        f"input={input_path}",
        f"output={output_path}",
        f"tools_total={len(results)}",
        f"tools_failing={len(failing)}",
        f"failing_tools={','.join(result.name for result in failing) if failing else '-'}",
    ]

    for result in failing:
        report_lines.append(f"{result.name}.status={_tool_status(result)}")
        report_lines.append(f"{result.name}.path={result.configured_path or '<not configured>'}")
        if result.hint:
            report_lines.append(f"{result.name}.hint={result.hint}")

    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    logger.info("Smoke report written: %s", report_path)

    if failing:
        logger.warning("Smoke check found %d tool issue(s).", len(failing))
        _log_tool_diagnostics(logger, results, level="warning")
        return 1

    logger.info("Smoke check passed.")
    return 0


def _parse_smoke_report(report_path: Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw_line in report_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip() or "=" not in raw_line:
            continue
        key, value = raw_line.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _emit_smoke_report_json_error(report_path: Path, error: str, schema_version: str | None = None) -> None:
    payload: dict[str, str] = {
        "report": str(report_path),
        "error": error,
    }
    if schema_version is not None:
        payload["schema_version"] = schema_version
    print(json.dumps(payload))


def _cmd_smoke_report(args: argparse.Namespace) -> int:
    logger = setup_logging(args.log_level)
    report_path = Path(args.report)

    if not report_path.exists():
        if args.json:
            _emit_smoke_report_json_error(report_path, error="not_found")
        logger.error("Smoke report not found: %s", report_path)
        return 2

    data = _parse_smoke_report(report_path)
    if "tools_total" not in data or "tools_failing" not in data:
        if args.json:
            _emit_smoke_report_json_error(report_path, error="malformed")
        logger.error("Smoke report is malformed: missing required fields")
        return 1

    schema_version = data.get("schema_version", "0")
    if schema_version not in {"0", SMOKE_REPORT_SCHEMA_VERSION}:
        if args.json:
            _emit_smoke_report_json_error(
                report_path,
                error="unsupported_schema",
                schema_version=schema_version,
            )
        logger.error("Smoke report schema version is unsupported: %s", schema_version)
        return 1

    tools_total = data.get("tools_total", "?")
    tools_failing = data.get("tools_failing", "?")
    failing_tools = data.get("failing_tools", "-")
    failing_count = int(tools_failing) if tools_failing.isdigit() else -1

    if args.json:
        print(
            json.dumps(
                {
                    "report": str(report_path),
                    "schema_version": schema_version,
                    "tools_total": int(tools_total) if tools_total.isdigit() else tools_total,
                    "tools_failing": failing_count,
                    "failing_tools": [] if failing_tools == "-" else failing_tools.split(","),
                    "status": "pass" if failing_count == 0 else "fail",
                }
            )
        )

    logger.info("Smoke report summary")
    logger.info("  report: %s", report_path)
    logger.info("  schema_version: %s", schema_version)
    logger.info("  tools_total: %s", tools_total)
    logger.info("  tools_failing: %s", tools_failing)
    logger.info("  failing_tools: %s", failing_tools)

    if tools_failing != "0":
        logger.warning("Smoke report indicates tool failures.")
        return 1

    logger.info("Smoke report indicates a passing environment.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        return _cmd_run(args)
    if args.command == "check":
        return _cmd_check(args)
    if args.command == "smoke":
        return _cmd_smoke(args)
    if args.command == "smoke-report":
        return _cmd_smoke_report(args)
    if args.command == "version":
        print(__version__)
        return 0

    parser.error("Unknown command")
    return 2
