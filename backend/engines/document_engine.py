import abc
import pdfplumber
import docx
import os

class DocumentEngine(abc.ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abc.abstractmethod
    def handle(self, file_path: str) -> str:
        pass

class PDFDocumentEngine(DocumentEngine):
    def handle(self, file_path: str) -> str:
        if file_path.lower().endswith('.pdf'):
            text = ""
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"Error reading PDF: {e}")
            return text
        elif self.next_handler:
            return self.next_handler.handle(file_path)
        return ""

class DocxDocumentEngine(DocumentEngine):
    def handle(self, file_path: str) -> str:
        if file_path.lower().endswith('.docx'):
            try:
                doc = docx.Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            except Exception as e:
                print(f"Error reading DOCX: {e}")
                return ""
        elif self.next_handler:
            return self.next_handler.handle(file_path)
        return ""

class TxtDocumentEngine(DocumentEngine):
    def handle(self, file_path: str) -> str:
        if file_path.lower().endswith('.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading TXT: {e}")
                return ""
        elif self.next_handler:
            return self.next_handler.handle(file_path)
        return ""

# Setup Chain of Responsibility
def get_document_engine_chain() -> DocumentEngine:
    txt_engine = TxtDocumentEngine()
    docx_engine = DocxDocumentEngine(next_handler=txt_engine)
    pdf_engine = PDFDocumentEngine(next_handler=docx_engine)
    return pdf_engine
