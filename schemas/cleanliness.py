from pydantic import BaseModel
from typing import Dict

class CleanlinessResponse(BaseModel):
    """清洁度评分响应模型"""
    overall_score: float
    detailed_scores: Dict[str, float]
    teeth_count: int