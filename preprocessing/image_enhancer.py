import cv2
import numpy as np
from typing import List

class ImageEnhancer:
    """牙齿照片增强处理器"""
    
    def __init__(self):
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        
    def enhance(self, image: np.ndarray) -> np.ndarray:
        """执行图像增强流水线"""
        # 1. 白平衡调整
        balanced = self.white_balance(image)
        # 2. 锐化处理
        sharpened = self.sharpen(balanced)
        # 3. 对比度增强
        enhanced = self.contrast_enhance(sharpened)
        return enhanced
    
    def white_balance(self, img: np.ndarray) -> np.ndarray:
        """自动白平衡处理"""
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = self.clahe.apply(l)
        lab = cv2.merge((l,a,b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    def sharpen(self, img: np.ndarray) -> np.ndarray:
        """锐化牙齿边缘"""
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        return cv2.filter2D(img, -1, kernel)
    
    def contrast_enhance(self, img: np.ndarray) -> np.ndarray:
        """CLAHE对比度增强"""
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = self.clahe.apply(l)
        lab = cv2.merge((l,a,b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)