import cv2
import numpy as np
from typing import Tuple
from ultralytics import YOLO

class CleanlinessScorer:
    """牙齿清洁度评分器（混合方法）"""
    
    def __init__(self):
        self.plaque_model = YOLO('yolov8n-seg.pt')  # 牙菌斑分割模型
        self.color_ranges = {
            'plaque': ([0, 0, 100], [50, 50, 255]),  # 牙菌斑颜色范围 (BGR)
            'healthy': ([200, 200, 200], [255, 255, 255])  # 健康牙齿颜色范围
        }
        
    def score(self, image: np.ndarray, teeth_regions: list) -> Tuple[float, dict]:
        """计算牙齿清洁度评分"""
        total_score = 0
        detailed_scores = {}
        
        for region in teeth_regions:
            x1, y1, x2, y2 = region['bbox']
            tooth_img = image[y1:y2, x1:x2]
            
            # 方法1: 基于颜色的初步评分
            color_score = self._color_based_score(tooth_img)
            
            # 方法2: 基于深度学习的精细评分
            dl_score = self._dl_based_score(tooth_img)
            
            # 混合评分 (权重: 颜色30% + 深度学习70%)
            final_score = 0.3 * color_score + 0.7 * dl_score
            total_score += final_score
            detailed_scores[region['class']] = final_score
            
        avg_score = total_score / len(teeth_regions) if teeth_regions else 0
        return avg_score, detailed_scores
    
    def _color_based_score(self, img: np.ndarray) -> float:
        """基于颜色阈值的评分"""
        healthy_mask = cv2.inRange(img, *self.color_ranges['healthy'])
        plaque_mask = cv2.inRange(img, *self.color_ranges['plaque'])
        
        healthy_pixels = cv2.countNonZero(healthy_mask)
        plaque_pixels = cv2.countNonZero(plaque_mask)
        total_pixels = img.shape[0] * img.shape[1]
        
        if total_pixels == 0:
            return 0
        return (healthy_pixels / total_pixels) * 100
    
    def _dl_based_score(self, img: np.ndarray) -> float:
        """基于深度学习的分割评分"""
        results = self.plaque_model(img)
        if not results[0].masks:
            return 100  # 未检测到牙菌斑
            
        mask = results[0].masks[0].data.cpu().numpy()
        plaque_area = np.sum(mask > 0.5)
        total_area = mask.size
        
        return 100 * (1 - plaque_area / total_area) if total_area > 0 else 100