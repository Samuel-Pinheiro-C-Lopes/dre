from backend.engines.llm_engine import LLMEngine

class LLMService:
    def __init__(self, engine: LLMEngine):
        self.engine = engine

    def extract_rules(self, prompt: str, document_text: str) -> str:
        return self.engine.generate_response(prompt, document_text)
