"""Salida estructurada del análisis integral."""

def build_analysis(case_text, profile=None, signals=None, missing=None, sources=None):
    return {'case_text':case_text or '', 'profile':profile or {}, 'signals':signals or [], 'missing_information':missing or [], 'sources':sources or [], 'professional_review_required':True}
