from src.core.case_context import build_case_context, merge_case_context
from src.core.genogram import create_genogram, add_member, add_relationship
from src.core.intervention import build_intervention, add_action
from src.core.referral import create_referral, STATUSES
from src.core.followup import create_followup, pending
from src.core.jurisdictions import PROVINCES, is_argentine_province, normalize_jurisdiction
from src.core.knowledge import document, search
from src.core.privacy import redact_personal
from src.core.analysis_report import build_analysis


def test_case_context_combines_report_and_location():
    ctx = build_case_context("Consulta", {"needs": ["vivienda"]}, {"province": "Córdoba"})
    assert ctx["summary"] == "Consulta"
    assert ctx["needs"] == ["vivienda"]
    assert ctx["location"]["province"] == "Córdoba"


def test_case_context_merge_does_not_overwrite_with_none():
    ctx = {"a": 1, "b": 2}
    assert merge_case_context(ctx, {"a": None, "b": 3}) == {"a": 1, "b": 3}


def test_genogram_members_and_relationships():
    g = create_genogram()
    add_member(g, "Persona", 30, "referencia", "empleo")
    add_member(g, "Familiar", 10, "hijo")
    add_relationship(g, "member-1", "member-2", "hijo", "apoyo")
    assert len(g["members"]) == 2
    assert g["relationships"][0]["quality"] == "apoyo"


def test_intervention_has_safe_fallback():
    plan = build_intervention({}, {"needs": []})
    assert plan["actions"]
    assert plan["actions"][0]["status"] == "pendiente"
    add_action(plan, "educación", "Relevar situación escolar")
    assert len(plan["actions"]) == 2


def test_referral_accepts_only_known_status():
    item = create_referral("CASE-1", "legal", status="inventado")
    assert item["status"] == "pendiente"
    assert "derivado" in STATUSES


def test_followup_pending_filters_resolved():
    items = [create_followup("CASE-1", "Llamar"), {"status": "resuelto"}]
    assert len(pending(items)) == 1


def test_argentina_jurisdictions():
    assert len(PROVINCES) == 24
    assert is_argentine_province("Córdoba")
    assert is_argentine_province("ciudad autónoma de buenos aires")
    assert not is_argentine_province("Madrid")
    assert normalize_jurisdiction("Salta", "Salta")['country'] == "Argentina"


def test_knowledge_search_uses_source_metadata():
    docs = [document("Guía vivienda", "alquiler y vivienda", "fuente oficial", "Buenos Aires", "vivienda")]
    result = search(docs, "vivienda")
    assert result and result[0]["source"] == "fuente oficial"


def test_privacy_redacts_sensitive_fields():
    result = redact_personal({"name": "Persona", "dni": "123", "category": "vivienda"})
    assert result["name"] == "[OCULTO]"
    assert result["dni"] == "[OCULTO]"
    assert result["category"] == "vivienda"


def test_analysis_always_requires_professional_review():
    result = build_analysis("relato", signals=["necesidad"])
    assert result["professional_review_required"] is True
