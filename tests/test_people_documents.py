from pathlib import Path
from tempfile import TemporaryDirectory
from src.person_registry import PersonRegistry, PersonImporter
from src.knowledge.memory import LocalMemory

def test_person_is_unique_and_can_have_many_cases():
    with TemporaryDirectory() as tmp:
        db=Path(tmp)/"test.db"
        registry=PersonRegistry(db)
        pid,created=registry.upsert({"name":"María López","document_id":"123","birth_date":"2000-01-01"})
        same_pid,created_again=registry.upsert({"name":"Maria López","document_id":"123","contact":"contacto"})
        assert pid==same_pid
        assert created is True
        assert created_again is False

def test_memory_chunks_and_delete():
    with TemporaryDirectory() as tmp:
        memory=LocalMemory(Path(tmp)/"knowledge.db")
        source="file:///tmp/protocolo.pdf"
        count=memory.save_chunks(source,"archivo local","protocolo.pdf","violencia y orientación. "*250,chunk_size=300,overlap=50)
        assert count>1
        assert memory.search("violencia",include_content=True)
        memory.delete_file(Path("/tmp/protocolo.pdf"))
        assert memory.search("violencia",include_content=True)==[]
