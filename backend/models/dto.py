from pydantic import BaseModel
from typing import List, Optional

class RuleDTO(BaseModel):
    id: Optional[str] = None
    title: str
    description: str

class RulesResponseDTO(BaseModel):
    rules: List[RuleDTO]
