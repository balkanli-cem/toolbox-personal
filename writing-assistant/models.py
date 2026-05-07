from pydantic import BaseModel
from typing import List, Optional

class StyleProfile(BaseModel):
    personality: str
    structure: str
    language: str
    narrative_style: str

class AnalyzeRequest(BaseModel):
    samples: List[str]

class GenerateRequest(BaseModel):
    content_type: str              #'linkedin_post' or 'email'
    topic: str
    extra_instructions: Optional[str] = None

class GenerateResponse(BaseModel):
    draft: str
    subject: Optional[str] = None  #only for emails

