"""
Tests para módulo de IA
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai.analyzer import TextAnalyzer
from src.ai.classifier import CaseClassifier, Urgency
from src.ai.processor import CaseProcessor


class TestAnalyzer:
    """Tests para TextAnalyzer."""
    
    def test_analyze_domestic_violence(self):
        """Test análisis de violencia doméstica."""
        analyzer = TextAnalyzer()
        
        text = "Mi pareja me golpeó. Tengo moretones en los brazos."
        analysis = analyzer.analyze(text)
        
        assert "violencia_fisica" in analysis["detected_categories"]
        assert analysis["urgency_score"] > 0.7
    
    def test_detect_emotions(self):
        """Test detección de emociones."""
        analyzer = TextAnalyzer()
        
        text = "Tengo mucho miedo y estoy muy triste"
        analysis = analyzer.analyze(text)
        
        emotions = [e["emotion"] for e in analysis["detected_emotions"]]
        assert "miedo" in emotions
        assert "tristeza" in emotions
    
    def test_extract_risk_factors(self):
        """Test extracción de factores de riesgo."""
        analyzer = TextAnalyzer()
        
        text = "Quiero suicidarme, tengo un arma"
        analysis = analyzer.analyze(text)
        
        risks = analysis["risk_factors"]
        assert any("suicidio" in r.lower() for r in risks)
        assert any("arma" in r.lower() for r in risks)
    
    def test_summarize(self):
        """Test generación de resumen."""
        analyzer = TextAnalyzer()
        
        text = """
        Primer párrafo con información. 
        Segundo párrafo con más detalles.
        Tercer párrafo bien largo que no debería incluirse.
        """
        
        summary = analyzer.summarize(text, max_length=50)
        assert len(summary) < 100
        assert "Primer" in summary


class TestClassifier:
    """Tests para CaseClassifier."""
    
    def test_classify_very_high_urgency(self):
        """Test clasificación urgencia muy alta."""
        classifier = CaseClassifier()
        
        analysis = {
            "urgency_score": 0.95,
            "detected_categories": ["suicidio"],
            "risk_factors": ["Riesgo suicida"],
            "keywords_found": {}
        }
        
        classification = classifier.classify(analysis)
        
        assert classification["urgency"] == "Muy Alta"
        assert classification["requires_immediate_action"] == True
    
    def test_classify_case_type(self):
        """Test clasificación de tipo de caso."""
        classifier = CaseClassifier()
        
        analysis = {
            "urgency_score": 0.5,
            "detected_categories": ["sexual"],
            "risk_factors": [],
            "keywords_found": {"sexual": ["violación"]}
        }
        
        classification = classifier.classify(analysis)
        assert classification["case_type"] == "violencia_sexual"
    
    def test_suggest_resources(self):
        """Test sugerencia de recursos."""
        classifier = CaseClassifier()
        
        analysis = {
            "urgency_score": 0.8,
            "detected_categories": ["violencia_fisica"],
            "risk_factors": ["Violencia física"],
            "keywords_found": {}
        }
        
        classification = classifier.classify(analysis)
        resources = classification["suggested_resources"]
        
        assert len(resources) > 0
        assert "refugio" in resources or "linea_ayuda" in resources


class TestProcessor:
    """Tests para CaseProcessor."""
    
    def test_process_complete_case(self):
        """Test procesamiento completo de caso."""
        processor = CaseProcessor()
        
        test_case = """
        Mi pareja me golpeó ayer. Tengo miedo.
        Mis hijos vieron todo. Quiero ayuda.
        """
        
        result = processor.process_case(test_case)
        
        assert "summary" in result
        assert "classification" in result
        assert "suggested_response" in result
        assert result["confidence"] > 0
    
    def test_confidence_calculation(self):
        """Test cálculo de confianza."""
        processor = CaseProcessor()
        
        analysis = {
            "detected_categories": ["violencia_fisica", "menores"],
            "urgency_score": 0.8,
            "keywords_found": {"violencia_fisica": ["golpe", "moretón"]}
        }
        
        confidence = processor._calculate_confidence(analysis)
        
        assert 0 <= confidence <= 1.0
        assert confidence > 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
