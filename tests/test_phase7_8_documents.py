from pathlib import Path
from tempfile import TemporaryDirectory

from openpyxl import Workbook
from reportlab.pdfgen import canvas

from src.core.document_ingestion import preview_document, map_person_preview
from src.core.case_knowledge import build_case_knowledge_context
from src.knowledge.memory import LocalMemory


def test_pdf_preview_extracts_text_and_pages():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "protocolo.pdf"
        pdf = canvas.Canvas(str(path))
        pdf.drawString(50, 750, "Protocolo de orientación laboral ante despido")
        pdf.save()
        result = preview_document(path)
        assert result["type"] == "pdf"
        assert result["pages"] == 1
        assert "despido" in result["text"].lower()
        assert result["fingerprint"]


def test_xlsx_preview_and_person_mapping_do_not_persist():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "personas.xlsx"
        wb = Workbook(); ws = wb.active
        ws.append(["Nombre completo", "DNI", "Fecha de nacimiento", "Edad"])
        ws.append(["Ana Pérez", "123", "1990-01-01", 36])
        wb.save(path)
        preview = preview_document(path)
        assert preview["row_count"] == 1
        mapped = map_person_preview(preview["rows"])
        assert mapped[0]["name"] == "Ana Pérez"
        assert mapped[0]["document_id"] == "123"


def test_case_uses_local_documents_as_evidence_not_decisions():
    with TemporaryDirectory() as tmp:
        memory = LocalMemory(Path(tmp) / "knowledge.db")
        memory.save("file:///guia.pdf", "archivo local", "Guía laboral", "", "orientación ante despido y documentación")
        result = build_case_knowledge_context("Necesito orientación por despido", memory)
        assert result["documents_considered"] >= 1
        assert result["analysis"]["evidence"]
        assert result["review_required"] is True
        assert result["analysis"]["review_required"] is True
