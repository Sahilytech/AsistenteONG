"""
Tests para la base de datos y DAOs
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
import sys

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.schema import init_database, DB_PATH
from src.database.dao import (
    UserDAO, CaseDAO, CaseAnalysisDAO, ResourceDAO, AuditLogDAO
)


@pytest.fixture
def test_db():
    """Crea una base de datos de prueba."""
    # Usar DB temporal para tests
    with tempfile.TemporaryDirectory() as tmpdir:
        test_db_path = Path(tmpdir) / "test.db"
        
        # Crear conexión de prueba
        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()
        
        # Crear esquema
        from src.database.schema import SCHEMA
        for statement in SCHEMA.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        conn.close()
        
        # Monkeypatch DB_PATH
        import src.database.dao as dao_module
        original_get_connection = dao_module.get_connection
        
        def mock_get_connection():
            return sqlite3.connect(test_db_path)
        
        dao_module.get_connection = mock_get_connection
        
        yield test_db_path
        
        # Restore
        dao_module.get_connection = original_get_connection


class TestUserDAO:
    """Tests para UserDAO."""
    
    def test_create_user(self, test_db):
        """Test crear usuario."""
        dao = UserDAO()
        user_id = dao.create("test_user", "hashed_password", "operator")
        
        assert user_id > 0
        
        user = dao.get_by_id(user_id)
        assert user is not None
        assert user["username"] == "test_user"
        assert user["role"] == "operator"
    
    def test_get_user_by_username(self, test_db):
        """Test obtener usuario por username."""
        dao = UserDAO()
        dao.create("john_doe", "hash123", "admin")
        
        user = dao.get_by_username("john_doe")
        assert user is not None
        assert user["username"] == "john_doe"
        assert user["role"] == "admin"
    
    def test_list_all_users(self, test_db):
        """Test listar todos los usuarios."""
        dao = UserDAO()
        dao.create("user1", "hash1")
        dao.create("user2", "hash2")
        dao.create("user3", "hash3")
        
        users = dao.list_all()
        assert len(users) == 3


class TestCaseDAO:
    """Tests para CaseDAO."""
    
    @pytest.fixture
    def user_id(self, test_db):
        """Crea un usuario para los tests."""
        dao = UserDAO()
        return dao.create("test_user", "hash")
    
    def test_create_case(self, test_db, user_id):
        """Test crear caso."""
        dao = CaseDAO()
        case_id = dao.create("CASE-001", "Mi pareja me golpeó", user_id)
        
        assert case_id > 0
        
        case = dao.get_by_id(case_id)
        assert case is not None
        assert case["case_number"] == "CASE-001"
        assert case["status"] == "new"
    
    def test_update_case(self, test_db, user_id):
        """Test actualizar caso."""
        dao = CaseDAO()
        case_id = dao.create("CASE-002", "Texto", user_id)
        
        success = dao.update(case_id, urgency="Muy Alta", status="in_progress")
        assert success
        
        case = dao.get_by_id(case_id)
        assert case["urgency"] == "Muy Alta"
        assert case["status"] == "in_progress"
    
    def test_list_by_status(self, test_db, user_id):
        """Test listar casos por estado."""
        dao = CaseDAO()
        dao.create("CASE-003", "Texto 1", user_id)
        dao.create("CASE-004", "Texto 2", user_id)
        
        cases = dao.list_by_status("new")
        assert len(cases) == 2
    
    def test_list_by_urgency(self, test_db, user_id):
        """Test listar casos por urgencia."""
        dao = CaseDAO()
        case_id = dao.create("CASE-005", "Texto", user_id)
        dao.update(case_id, urgency="Alta")
        
        cases = dao.list_by_urgency("Alta")
        assert len(cases) == 1


class TestCaseAnalysisDAO:
    """Tests para CaseAnalysisDAO."""
    
    @pytest.fixture
    def case_id(self, test_db):
        """Crea un caso para los tests."""
        user_dao = UserDAO()
        user_id = user_dao.create("test_user", "hash")
        
        case_dao = CaseDAO()
        return case_dao.create("CASE-ANALYSIS", "Texto", user_id)
    
    def test_create_analysis(self, test_db, case_id):
        """Test crear análisis."""
        dao = CaseAnalysisDAO()
        analysis_id = dao.create(
            case_id=case_id,
            emotions="miedo, angustia",
            risk_factors="violencia física",
            identified_people="pareja",
            ai_score=0.95,
            analysis_data='{"key": "value"}'
        )
        
        assert analysis_id > 0
        
        analysis = dao.get_by_case_id(case_id)
        assert analysis is not None
        assert analysis["ai_score"] == 0.95


class TestResourceDAO:
    """Tests para ResourceDAO."""
    
    def test_create_resource(self, test_db):
        """Test crear recurso."""
        dao = ResourceDAO()
        resource_id = dao.create(
            name="Hospital Central",
            resource_type="hospital",
            phone="911",
            region="Buenos Aires"
        )
        
        assert resource_id > 0
        
        resource = dao.get_by_id(resource_id)
        assert resource["name"] == "Hospital Central"
    
    def test_list_by_type(self, test_db):
        """Test listar recursos por tipo."""
        dao = ResourceDAO()
        dao.create("Hospital A", "hospital")
        dao.create("Hospital B", "hospital")
        dao.create("Refugio C", "refugio")
        
        hospitals = dao.list_by_type("hospital")
        assert len(hospitals) == 2
    
    def test_search(self, test_db):
        """Test buscar recursos."""
        dao = ResourceDAO()
        dao.create("Hospital Central", "hospital", description="Centro médico")
        dao.create("Refugio María", "refugio", description="Para mujeres")
        
        results = dao.search("Central")
        assert len(results) > 0


class TestAuditLogDAO:
    """Tests para AuditLogDAO."""
    
    @pytest.fixture
    def user_id(self, test_db):
        """Crea un usuario para los tests."""
        dao = UserDAO()
        return dao.create("audit_user", "hash")
    
    def test_log_action(self, test_db, user_id):
        """Test registrar acción."""
        dao = AuditLogDAO()
        log_id = dao.log(
            user_id=user_id,
            action="CREATE_CASE",
            table_name="cases",
            record_id=1,
            details="Caso de violencia doméstica"
        )
        
        assert log_id > 0
    
    def test_get_by_user(self, test_db, user_id):
        """Test obtener auditoría de usuario."""
        dao = AuditLogDAO()
        dao.log(user_id, "CREATE_CASE", "cases", 1)
        dao.log(user_id, "UPDATE_CASE", "cases", 1)
        
        logs = dao.get_by_user(user_id)
        assert len(logs) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
