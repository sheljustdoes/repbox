import logging


def setup_logging(level: str = "INFO") -> logging.Logger:
    normalized = level.upper()
    if normalized not in {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}:
        normalized = "INFO"

    logging.basicConfig(
        level=getattr(logging, normalized),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger("repbox")
