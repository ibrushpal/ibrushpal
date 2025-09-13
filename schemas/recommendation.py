from pydantic import BaseModel
from typing import List, Dict

class RecommendationResponse(BaseModel):
    """推荐响应模型"""
    must: List[str]
    suggest: List[str]
    avoid: List[str]
    explanation: str = "基于您的口腔状况生成的个性化建议"