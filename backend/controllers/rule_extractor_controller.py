from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import shutil
import os
from uuid import uuid4
from backend.models.dto import RulesResponseDTO, RuleDTO
from backend.services.extraction_service import ExtractionService
from backend.services.document_service import DocumentService
from backend.services.llm_service import LLMService
from backend.engines.document_engine import get_document_engine_chain
from backend.engines.llm_engine import GeminiLLMEngine
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# Basic security placeholder
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def verify_token(token: str = Depends(oauth2_scheme)):
    # Placeholder for actual verification
    if token != "supersecrettoken":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

def get_extraction_service() -> ExtractionService:
    doc_engine = get_document_engine_chain()
    llm_engine = GeminiLLMEngine()
    
    doc_service = DocumentService(doc_engine)
    llm_service = LLMService(llm_engine)
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    prompt_path = os.path.join(current_dir, '..', 'resources', 'prompt.txt')
    
    return ExtractionService(doc_service, llm_service, prompt_path)

@router.post("/extract-rules", response_model=RulesResponseDTO)
async def extract_rules(
    document: UploadFile = File(...),
    # token: str = Depends(verify_token), # Disabled for easier testing locally
    service: ExtractionService = Depends(get_extraction_service)
):
    temp_dir = "/tmp/rule_extractor"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, f"{uuid4()}_{document.filename}")
    
    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(document.file, buffer)
            
        rules_data = service.extract_rules_from_file(temp_file_path)
        
        rules = []
        for r in rules_data:
            rules.append(RuleDTO(
                id=str(uuid4()),
                title=r.get("title", "Untitled"),
                description=r.get("description", "")
            ))
            
        return RulesResponseDTO(rules=rules)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
