from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ADRStatus(str, Enum):
    proposed = "proposed"
    accepted = "accepted"
    deprecated = "deprecated"

class ADROption(BaseModel):
    name: str
    description: str

class ADRRequest(BaseModel):
    title: str
    status: ADRStatus
    context: str
    options: List[ADROption]
    decision: str
    extra_instructions: Optional[str] = None

class ADRSection(BaseModel):
    context: str
    options_analysis: str
    decision_rationale: str
    consequences: str

class ADRResponse(BaseModel):
    title: str
    status: str
    markdown: str
    
    