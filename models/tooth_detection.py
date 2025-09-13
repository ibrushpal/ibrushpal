import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict

class ToothDetector:
    """基于YOLOv8的牙齿检测器"""
    
    def __init__(self, model_path: str = 'yolov8n.pt'):
        self.model = YOLO(model_path)
        self.class_names = {
            0: 'incisor',   # 切牙
            1: 'canine',    # 尖牙
            2: 'premolar',  # 前磨牙
            3: 'molar'      # 磨牙
        }
        
    def detect(self, image: np.ndarray) -> List[Dict]:
        """检测牙齿并返回结构化结果"""
        results = self.model(image)
        detections = []
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                detections.append({
                    'class': self.class_names[int(box.cls)],
                    'confidence': float(box.conf),
                    'bbox': [x1, y1, x2, y2],
                    'center': [(x1+x2)//2, (y1+y2)//2]
                })
                
        return detections
    
    def visualize(self, image: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """可视化检测结果"""
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(image, 
                       f"{det['class']} {det['confidence']:.2f}",
                       (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (0,255,0), 1)
        return image