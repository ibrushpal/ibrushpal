from fastapi import APIRouter
from models.recommendation_engine import RecommendationEngine
from schemas.recommendation import RecommendationResponse
from typing import Dict

router = APIRouter()
engine = RecommendationEngine()

@router.post("/generate-recommendation", response_model=RecommendationResponse)
async def generate_recommendation(inputs: Dict) -> Dict:
    """生成个性化刷牙方案API"""
    return engine.generate_recommendation(inputs)