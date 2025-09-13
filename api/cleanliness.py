from fastapi import APIRouter, UploadFile, File
from models.cleanliness_scorer import CleanlinessScorer
from models.tooth_detection import ToothDetector
import cv2
import numpy as np
from typing import Dict
from schemas.cleanliness import CleanlinessResponse

router = APIRouter()
scorer = CleanlinessScorer()
detector = ToothDetector()

@router.post("/score-cleanliness", response_model=CleanlinessResponse)
async def score_cleanliness(file: UploadFile = File(...)) -> Dict:
    """牙齿清洁度评分API"""
    contents = await file.read()
    image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    
    # 1. 检测牙齿区域
    teeth_regions = detector.detect(image)
    
    # 2. 计算清洁度评分
    overall_score, detailed_scores = scorer.score(image, teeth_regions)
    
    return {
        "overall_score": round(overall_score, 1),
        "detailed_scores": detailed_scores,
        "teeth_count": len(teeth_regions)
    }