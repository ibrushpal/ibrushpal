import cv2
import numpy as np
from typing import List
from .image_enhancer import ImageEnhancer

class VideoProcessor:
    """刷牙视频处理器"""
    
    def __init__(self, target_fps: int = 1):
        self.target_fps = target_fps
        self.enhancer = ImageEnhancer()
        
    def extract_key_frames(self, video_path: str) -> List[np.ndarray]:
        """提取关键帧(1fps)并增强"""
        frames = []
        cap = cv2.VideoCapture(video_path)
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(original_fps / self.target_fps)
        
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if count % frame_interval == 0:
                enhanced = self.enhancer.enhance(frame)
                frames.append(enhanced)
            count += 1
            
        cap.release()
        return frames
    
    def analyze_brushing_trajectory(self, frames: List[np.ndarray]) -> dict:
        """分析刷牙动作轨迹"""
        # TODO: 实现轨迹分析算法
        return {
            "coverage": 0.0,
            "missed_areas": [],
            "movement_pattern": []
        }
    
    def check_quality(self, video_path: str) -> bool:
        """检查视频质量是否合格"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        return width >= 640 and height >= 480 and fps >= 15