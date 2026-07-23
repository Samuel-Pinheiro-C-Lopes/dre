from backend.engines.document_engine import DocumentEngine

class DocumentService:
    def __init__(self, engine: DocumentEngine):
        self.engine = engine

    def extract_text(self, file_path: str) -> str:
        return self.engine.handle(file_path)
