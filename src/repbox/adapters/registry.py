from __future__ import annotations

from .base import ExternalToolAdapter
from .repeatmasker import RepeatMaskerAdapter
from .repeatmodeler import RepeatModelerAdapter


def default_adapters() -> list[ExternalToolAdapter]:
    return [
        RepeatModelerAdapter(),
        RepeatMaskerAdapter(),
        ExternalToolAdapter(name="RepeatClassifier", config_key="RepeatClassifier"),
        ExternalToolAdapter(name="BuildDatabase", config_key="BuildDatabase"),
        ExternalToolAdapter(name="SINE_Scan", config_key="SineScan"),
        ExternalToolAdapter(name="miteFinder", config_key="miteFinder"),
        ExternalToolAdapter(name="HelitronScanner", config_key="HelitronScanner"),
        ExternalToolAdapter(name="VSEARCH", config_key="VSEARCH"),
    ]
