import abc
import google.generativeai as genai
import os

class LLMEngine(abc.ABC):
    @abc.abstractmethod
    def generate_response(self, prompt: str, document_text: str) -> str:
        pass

class GeminiLLMEngine(LLMEngine):
    def __init__(self):
        # Assumes GOOGLE_API_KEY is set in environment
        api_key = os.environ.get("GOOGLE_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        
    def generate_response(self, prompt: str, document_text: str) -> str:
        full_prompt = f"{prompt}\n\nDocument Text:\n{document_text}"
        response = self.model.generate_content(full_prompt)
        return response.text
