import unittest
from src.core.case_profile import build_case_profile
from src.core.reasoning import analyze_profile

class CoreReasoningTests(unittest.TestCase):
    def test_extra_no_matches_ex(self):
        p = build_case_profile("tuve una experiencia extraña con mi familia")
        self.assertNotIn("ex pareja", p.relationships)

    def test_ex_pareja_matches_as_phrase(self):
        p = build_case_profile("mi ex pareja me llamó")
        self.assertIn("ex pareja", p.relationships)

    def test_context_does_not_raise_urgency(self):
        p = build_case_profile("mi hijo necesita orientación")
        result = analyze_profile(p)
        self.assertEqual(result["urgency"], "no determinada")

    def test_burn_is_health_not_violence(self):
        p = build_case_profile("mi hijo se quemó con la estufa mientras cocinaba")
        result = analyze_profile(p)
        self.assertEqual(result["category"], "Salud / accidente")
        self.assertNotIn("violencia", result["category"].lower())

    def test_job_dismissal_is_labor(self):
        p = build_case_profile("me despidieron del trabajo y necesito orientación")
        result = analyze_profile(p)
        self.assertEqual(result["category"], "Situacion laboral")
        self.assertNotEqual(result["urgency"], "muy alta")

    def test_negated_violence(self):
        p = build_case_profile("no hubo violencia, necesito orientación social")
        self.assertNotIn("violencia", p.indicators)

if __name__ == "__main__":
    unittest.main()
