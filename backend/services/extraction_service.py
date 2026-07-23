import os
import json
from backend.services.document_service import DocumentService
from backend.services.llm_service import LLMService

class ExtractionService:
    def __init__(self, document_service: DocumentService, llm_service: LLMService, prompt_path: str):
        self.document_service = document_service
        self.llm_service = llm_service
        self.prompt_path = prompt_path
        self._cached_prompt = None
        self._last_modified = None

    def _get_prompt(self) -> str:
        if not os.path.exists(self.prompt_path):
            raise FileNotFoundError(f"Prompt file not found at {self.prompt_path}")
        
        current_mtime = os.path.getmtime(self.prompt_path)
        if self._cached_prompt is None or self._last_modified != current_mtime:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                self._cached_prompt = f.read()
            self._last_modified = current_mtime
            
        return self._cached_prompt

    def extract_rules_from_file(self, file_path: str) -> list:
        document_text = self.document_service.extract_text(file_path)
        if not document_text:
            raise ValueError("Could not extract text from document or document is empty.")
            
        prompt = self._get_prompt()
        prompt += "\n\nCRITICAL INSTRUCTION: Regardless of the prompt above, you MUST output ONLY valid JSON. The output MUST be a JSON array of objects, where each object has exactly two string fields: 'title' and 'description'. Do not include any conversational text or markdown other than the JSON block."
        llm_response = self.llm_service.extract_rules(prompt, document_text)
        
        try:
            clean_response = llm_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:-3].strip()
            elif clean_response.startswith("```"):
                clean_response = clean_response[3:-3].strip()
            return json.loads(clean_response)
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM response as JSON: {llm_response}")
            raise Exception("LLM returned malformed data.") from e
