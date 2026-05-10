from pydantic import BaseModel
from typing import List

class AnalysisResponse(BaseModel):
    ats_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]