from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class CategoryBreakdown(BaseModel):
    category: str
    matched: int
    missing: int
    extra: int
    total: int


class CoverageSummary(BaseModel):
    matched: int
    missing: int
    extra: int


class AnalysisResponse(BaseModel):
    ats_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    extra_skills: List[str]
    coverage: CoverageSummary
    suggestions: List[str]
    strengths: List[str]
    weaknesses: List[str]
    chart_data: List[CategoryBreakdown]
    semantic_score: Optional[int] = 0