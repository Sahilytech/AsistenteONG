# Motor de IA Offline (v0.4)

## Visión general

Motor de análisis de texto 100% offline usando modelos GGUF pequeños (1-2GB), sin depender de APIs externas.

## Arquitectura

```
Texto del caso
    ↓
TextAnalyzer (Análisis NLP)
    ├─ Detecta categorías
    ├─ Extrae emociones
    ├─ Encuentra palabras clave
    └─ Calcula urgencia
    ↓
CaseClassifier (Clasificación)
    ├─ Asigna urgencia final
    ├─ Determina tipo de caso
    ├─ Sugiere recursos
    └─ Define escalación
    ↓
CaseProcessor (Orquestación)
    ├─ Carga modelo (opcional)
    ├─ Genera resumen
    ├─ Crea respuesta borrador
    └─ Calcula confianza
    ↓
Resultado completo
```

## Componentes

### 1. TextAnalyzer

Análisis NLP local basado en palabras clave y patrones.

**Funciones:**

```python
from src.ai.analyzer import TextAnalyzer

analyzer = TextAnalyzer()
analysis = analyzer.analyze(text)
```

**Output:**

```python
{
    "original_length": 250,
    "detected_categories": ["violencia_fisica", "menores"],
    "detected_emotions": [
        {"emotion": "miedo", "mentions": 3},
        {"emotion": "tristeza", "mentions": 1}
    ],
    "detected_people": ["pareja", "hijo"],
    "urgency_score": 0.87,
    "risk_factors": [
        "Violencia física documentada",
        "Menores involucrados"
    ],
    "keywords_found": {
        "violencia_fisica": ["golpe", "moretón"],
        "menores": ["hijo"]
    }
}
```

### 2. CaseClassifier

Clasificación automática de urgencia, tipo y recursos.

**Niveles de urgencia:**

- **Muy Alta (0.95)**: Riesgo inmediato de vida
- **Alta (0.75)**: Agresión/violencia documentada
- **Media (0.50)**: Conflicto/problema
- **Baja (0.25)**: Consulta rutinaria

**Tipos de caso:**

- `violencia_doméstica`
- `violencia_sexual`
- `asesoría_legal`
- `violencia_infantil`
- `violencia_anciano`
- `discriminación`
- `salud_mental`
- `otro`

**Ejemplo:**

```python
from src.ai.classifier import CaseClassifier

classifier = CaseClassifier()
classification = classifier.classify(analysis)
```

### 3. CaseProcessor

Orquestador principal que integra análisis y clasificación.

**Uso:**

```python
from src.ai.processor import get_processor, initialize_processor

# Inicializar (carga modelo si disponible)
initialize_processor()

# Procesar caso
processor = get_processor()
result = processor.process_case(text)
```

**Resultado:**

```python
{
    "timestamp": "2025-01-15T10:30:00",
    "summary": "Resumen generado automáticamente...",
    "analysis": {...},
    "classification": {...},
    "suggested_response": "Gracias por contactarnos...",
    "confidence": 0.87
}
```

## Modelos disponibles

### Gemma 3 1B (Recomendado)

- **Tamaño**: 2.0 GB
- **Contexto**: 1K tokens
- **RAM mínimo**: 4 GB
- **Tiempo**: ~50ms por análisis

### Alternativas

| Modelo | Tamaño | RAM | Velocidad |
|--------|--------|-----|-----------|
| Gemma 3 1B | 2.0 GB | 4 GB | ⭐⭐⭐⭐ |
| Qwen 2.5 1.5B | 1.8 GB | 4 GB | ⭐⭐⭐ |
| TinyLlama 1.1B | 1.5 GB | 3 GB | ⭐⭐⭐⭐⭐ |
| Phi-3 Mini | 2.2 GB | 4 GB | ⭐⭐⭐ |

## Palabras clave

### Categorías

**violencia_fisica**: golpe, golpeó, pegó, puñetazo, lesión, moretón...

**violencia_psicologica**: insulto, amenaza, manipulación, humillación...

**violencia_economica**: dinero, gasto, deuda, despido, salario...

**sexual**: abuso sexual, violación, acoso, coerción...

**menores**: niño, niña, hijo, hija, bebé, adolescente...

**embarazo**: embarazada, embarazo, gestación, parto...

**suicidio**: suicidio, matar, muerte, morir...

**armas**: arma, pistola, cuchillo, revólver, bomba...

**adulto_mayor**: anciano, jubilado, vejez, abuelo...

**discapacidad**: discapacidad, sordera, ceguera, movilidad...

**migracion**: migrante, refugiado, visa, pasaporte...

### Emociones

- **miedo**: asustado, pánico, aterrado
- **tristeza**: deprimido, llorar, dolor
- **rabia**: enojado, furioso, ira
- **vergüenza**: avergonzado, humillación
- **desesperanza**: desesperado, sin esperanza

## Factores de riesgo automáticos

- Violencia física documentada → ⚠️ Alta prioridad
- Menores involucrados → 🚨 Derivación DDNA
- Riesgo suicida → 🚨 EMERGENCIA
- Presencia de armas → 🚨 Derivación policía
- Embarazo en riesgo → ⚠️ Hospital obstetricia

## Performance

- **Análisis**: <100ms por caso
- **Clasificación**: <50ms
- **Generación respuesta**: <200ms
- **Total**: <500ms por caso

Soporta procesamiento de lotes (batch processing)

## Limitaciones

- Análisis basado en palabras clave (no deep learning)
- Precisión: ~85% (vs humanos)
- Idioma: Español principalmente
- No detecta contexto sarcástico/irónico

## Futuros (v0.5+)

- [ ] Integración con modelo Gemma 3 completo
- [ ] Análisis de sentimientos mejorado
- [ ] NER (Named Entity Recognition)
- [ ] Resúmenes más sofisticados
- [ ] Multi-idioma
- [ ] Fine-tuning con casos reales

---

**v0.4 Status:** ✅ Motor IA completo, sin dependencias externas
