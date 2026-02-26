from __future__ import annotations

from .base import ExternalToolAdapter


def default_adapters() -> list[ExternalToolAdapter]:
    return [
        ExternalToolAdapter(name="RepeatModeler", config_key="RepeatModeler"),
        ExternalToolAdapter(name="RepeatMasker", config_key="RepeatMasker"),
        ExternalToolAdapter(name="RepeatClassifier", config_key="RepeatClassifier"),
        ExternalToolAdapter(name="BuildDatabase", config_key="BuildDatabase"),
        ExternalToolAdapter(name="SINE_Scan", config_key="SineScan"),
        ExternalToolAdapter(name="miteFinder", config_key="miteFinder"),
        ExternalToolAdapter(name="HelitronScanner", config_key="HelitronScanner"),
        ExternalToolAdapter(name="VSEARCH", config_key="VSEARCH"),
    ]
