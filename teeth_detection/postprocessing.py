import numpy as np
from typing import List, Dict, Any
import cv2

class TeethDetectionPostprocessor:
    """牙齿检测结果后处理类"""
    
    def __init__(self, confidence_threshold: float = 0.5, iou_threshold: float = 0.45):
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
    
    def filter_by_confidence(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """根据置信度阈值过滤检测结果"""
        return [det for det in detections if det['confidence'] >= self.confidence_threshold]
    
    def non_max_suppression(self, detections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """非极大值抑制，去除重叠的检测框"""
        if not detections:
            return []
        
        # 按置信度排序
        detections.sort(key=lambda x: x['confidence'], reverse=True)
        
        selected_detections = []
        
        while detections:
            # 选择置信度最高的检测
            best_det = detections.pop(0)
            selected_detections.append(best_det)
            
            # 计算与剩余检测的IoU
            remaining_dets = []
            for det in detections:
                iou = self._calculate_iou(best_det['bbox'], det['bbox'])
                if iou < self.iou_threshold:
                    remaining_dets.append(det)
            
            detections = remaining_dets
        
        return selected_detections
    
    def _calculate_iou(self, box1: List[float], box2: List[float]) -> float:
        """计算两个边界框的IoU"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        # 计算交集区域
        x_left = max(x1_1, x1_2)
        y_top = max(y1_1, y1_2)
        x_right = min(x2_1, x2_2)
        y_bottom = min(y2_1, y2_2)
        
        if x_right < x_left or y_bottom < y_top:
            return 0.0
        
        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        
        # 计算并集区域
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = area1 + area2 - intersection_area
        
        return intersection_area / union_area if union_area > 0 else 0.0
    
    def calculate_coverage(self, detections: List[Dict[str, Any]], image_shape: tuple) -> float:
        """计算牙齿检测覆盖率"""
        if not detections:
            return 0.0
        
        total_area = image_shape[0] * image_shape[1]
        detected_area = 0.0
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            detected_area += (x2 - x1) * (y2 - y1)
        
        return min(detected_area / total_area, 1.0) * 100  # 百分比
    
    def analyze_tooth_distribution(self, detections: List[Dict[str, Any]], image_shape: tuple) -> Dict[str, int]:
        """分析牙齿在图像中的分布"""
        height, width = image_shape[:2]
        
        # 定义图像区域
        left_third = width // 3
        right_third = 2 * width // 3
        top_third = height // 3
        bottom_third = 2 * height // 3
        
        distribution = {
            'left_side': 0,
            'center': 0,
            'right_side': 0,
            'upper_jaw': 0,
            'middle_jaw': 0,
            'lower_jaw': 0
        }
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            
            # 水平分布
            if center_x < left_third:
                distribution['left_side'] += 1
            elif center_x > right_third:
                distribution['right_side'] += 1
            else:
                distribution['center'] += 1
            
            # 垂直分布
            if center_y < top_third:
                distribution['upper_jaw'] += 1
            elif center_y > bottom_third:
                distribution['lower_jaw'] += 1
            else:
                distribution['middle_jaw'] += 1
        
        return distribution
    
    def postprocess(self, raw_detections: List[Dict[str, Any]], image_shape: tuple) -> Dict[str, Any]:
        """完整的后处理流水线"""
        # 置信度过滤
        filtered_detections = self.filter_by_confidence(raw_detections)
        
        # 非极大值抑制
        final_detections = self.non_max_suppression(filtered_detections)
        
        # 计算覆盖率
        coverage = self.calculate_coverage(final_detections, image_shape)
        
        # 分析分布
        distribution = self.analyze_tooth_distribution(final_detections, image_shape)
        
        return {
            'detections': final_detections,
            'coverage_percentage': coverage,
            'tooth_distribution': distribution,
            'total_teeth_detected': len(final_detections)
        }

# 测试后处理流程
if __name__ == "__main__":
    # 创建测试检测结果
    test_detections = [
        {'bbox': [50, 50, 150, 150], 'confidence': 0.8, 'class_id': 0, 'class_name': 'tooth'},
        {'bbox': [60, 60, 160, 160], 'confidence': 0.7, 'class_id': 0, 'class_name': 'tooth'},
        {'bbox': [200, 200, 300, 300], 'confidence': 0.9, 'class_id': 0, 'class_name': 'tooth'},
        {'bbox': [10, 10, 50, 50], 'confidence': 0.3, 'class_id': 0, 'class_name': 'tooth'}  # 低置信度
    ]
    
    postprocessor = TeethDetectionPostprocessor(confidence_threshold=0.5)
    
    # 测试后处理
    result = postprocessor.postprocess(test_detections, (400, 400))
    
    print("✅ 后处理测试结果:")
    print(f"过滤后检测数: {len(result['detections'])}")
    print(f"覆盖率: {result['coverage_percentage']:.1f}%")
    print(f"牙齿分布: {result['tooth_distribution']}")
    print(f"总检测牙齿数: {result['total_teeth_detected']}")