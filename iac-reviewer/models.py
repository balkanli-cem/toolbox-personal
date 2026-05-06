from pydantic import BaseModel
from typing import List
from enum import Enum

class Severity(str, Enum):
    critical = "critical"
    warning = "warning"
    info = "info"
    good = "good"

class ReviewRequest(BaseModel):
    code: str
    cloud: str = "azure"
    focus: str = "all"

class Finding(BaseModel):
    severity: Severity
    category: str
    title: str
    description: str
    fix: str

class ReviewResponse(BaseModel):
    score: int
    summary: str
    findings: List[Finding]