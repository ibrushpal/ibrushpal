#!/usr/bin/env python3
"""
简易牙齿检测器 - 临时解决方案
基于颜色和形状特征进行牙齿检测
"""

import cv2
import numpy as np
import os
from typing import List, Tuple

class SimpleTeethDetector:
    """基于传统图像处理的牙齿检测器"""
    
    def __init__(self):
        # 牙齿颜色范围（HSV空间）
        self.lower_teeth = np.array([0, 0, 180])    # 较暗的牙齿
        self.upper_teeth = np.array([30, 60, 255])  # 较亮的牙齿
        
        # 牙龈颜色范围
        self.lower_gum = np.array([0, 30, 100])
        self.upper_gum = np.array([15, 150, 200])
    
    def detect_teeth(self, image_path: str) -> List[Tuple]:
        """
        检测图像中的牙齿
        返回: [(x, y, w, h, confidence), ...]
        """
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图像: {image_path}")
            return []
        
        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 创建牙齿颜色掩码
        teeth_mask = cv2.inRange(hsv, self.lower_teeth, self.upper_teeth)
        
        # 形态学操作（去噪）
        kernel = np.ones((5, 5), np.uint8)
        teeth_mask = cv2.morphologyEx(teeth_mask, cv2.MORPH_CLOSE, kernel)
        teeth_mask = cv2.morphologyEx(teeth_mask, cv2.MORPH_OPEN, kernel)
        
        # 查找轮廓
        contours, _ = cv2.findContours(teeth_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 过滤轮廓
        teeth_regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 100:  # 过滤太小的区域
                continue
                
            x, y, w, h = cv2.boundingRect(contour)
            
            # 计算置信度（基于区域面积和宽高比）
            aspect_ratio = w / h
            confidence = min(area / 1000, 1.0)  # 归一化到0-1
            
            # 牙齿通常有特定的宽高比
            if 0.5 < aspect_ratio < 2.0:
                teeth_regions.append((x, y, w, h, confidence))
        
        return teeth_regions
    
    def visualize_detection(self, image_path: str, output_path: str = None):
        """可视化检测结果"""
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        teeth_regions = self.detect_teeth(image_path)
        
        # 绘制检测结果
        for i, (x, y, w, h, confidence) in enumerate(teeth_regions):
            # 绘制边界框
            color = (0, 255, 0)  # 绿色
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            
            # 显示置信度
            label = f"Tooth {i+1}: {confidence:.2f}"
            cv2.putText(image, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # 保存或显示结果
        if output_path:
            cv2.imwrite(output_path, image)
            print(f"结果保存到: {output_path}")
        
        return image, teeth_regions
    
    def batch_test(self, test_dir: str = "professional_test"):
        """批量测试"""
        if not os.path.exists(test_dir):
            print(f"测试目录不存在: {test_dir}")
            return
        
        results = []
        for filename in os.listdir(test_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(test_dir, filename)
                print(f"\n测试图像: {filename}")
                
                teeth_regions = self.detect_teeth(image_path)
                print(f"检测到 {len(teeth_regions)} 个牙齿区域")
                
                # 保存可视化结果
                output_dir = "simple_detection_results"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"detected_{filename}")
                
                self.visualize_detection(image_path, output_path)
                
                results.append({
                    'image': filename,
                    'detections': len(teeth_regions),
                    'regions': teeth_regions
                })
        
        return results

def main():
    """主函数"""
    print("简易牙齿检测器测试")
    print("=" * 40)
    
    detector = SimpleTeethDetector()
    
    # 测试单张图像
    test_image = "professional_test/front_teeth.jpg"
    if os.path.exists(test_image):
        print(f"测试图像: {test_image}")
        result_image, regions = detector.visualize_detection(
            test_image, 
            "simple_detection_results/detected_front_teeth.jpg"
        )
        print(f"检测到 {len(regions)} 个牙齿区域")
    else:
        print("测试图像不存在，运行批量测试...")
        detector.batch_test()

if __name__ == "__main__":
    main()