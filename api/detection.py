from fastapi import APIRouter, UploadFile, File
from models.tooth_detection import ToothDetector
import cv2
import numpy as np
from typing import List, Dict
import io

router = APIRouter()
detector = ToothDetector()

@router.post("/detect-teeth")
async def detect_teeth(file: UploadFile = File(...)) -> List[Dict]:
    """牙齿检测API端点"""
    contents = await file.read()
    image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    detections = detector.detect(image)
    return [
        {
            "type": det["class"],
            "confidence": det["confidence"],
            "position": {
                "x": det["center"][0],
                "y": det["center"][1]
            },
            "bbox": det["bbox"]
        }
        for det in detections
    ]