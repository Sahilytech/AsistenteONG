"""Smoke test sin interfaz: valida imports y reglas críticas del núcleo."""
from src.config_manager import ConfigManager
from src.core.case_context import build_case_context
from src.core.genogram import create_genogram
from src.core.intervention import build_intervention
from src.core.jurisdictions import PROVINCES


def main():
    engine = ConfigManager()
    samples = {
        "quemadura": "mi hijo se quemó con la estufa mientras cocinaba",
        "laboral": "me despidieron y necesito orientación sobre mi trabajo",
        "general": "necesito información sobre una ayuda para vivienda",
    }
    results = {name: engine.analyze(text) for name, text in samples.items()}
    assert results["quemadura"]["classification"] == "Salud / accidente"
    assert results["quemadura"]["urgency"] != "Muy Alta"
    assert "hijo" in results["quemadura"]["context_keywords"]
    assert results["laboral"]["classification"] == "Situación laboral"
    assert len(PROVINCES) == 24
    context = build_case_context(samples["quemadura"], {"needs": ["salud"]})
    assert context["needs"] == ["salud"]
    assert create_genogram()["members"] == []
    assert build_intervention({}, {"needs": ["salud"]})["actions"]
    print("HEALTHCHECK OK")


if __name__ == "__main__":
    main()
