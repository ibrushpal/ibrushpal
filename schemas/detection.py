from pydantic import BaseModel
from typing import List, Dict

class ToothDetectionResult(BaseModel):
    """牙齿检测结果模型"""
    type: str
    confidence: float
    position: Dict[str, int]
    bbox: List[int]

class DetectionResponse(BaseModel):
    """API响应模型"""
    teeth: List[ToothDetectionResult]
    status: str = "success"