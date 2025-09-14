#!/usr/bin/env python3
"""
简化牙齿图像测试脚本
直接创建模拟牙齿图像测试YOLOv8模型
"""

import torch
import cv2
import numpy as np
from ultralytics import YOLO
import time
import os

def create_teeth_images():
    """创建模拟牙齿图像"""
    print("=== 创建模拟牙齿图像 ===")
    
    os.makedirs("test_images", exist_ok=True)
    
    images = []
    for i in range(3):
        # 创建白色背景
        img = np.ones((480, 640, 3), dtype=np.uint8) * 255
        
        if i == 0:  # 正面牙齿
            # 牙齿区域
            cv2.rectangle(img, (200, 150), (440, 350), (220, 220, 220), -1)
            # 牙齿分隔线
            for x in range(240, 400, 40):
                cv2.line(img, (x, 150), (x, 350), (180, 180, 180), 2)
            # 牙龈
            cv2.rectangle(img, (180, 140), (460, 150), (150, 100, 100), -1)
            
        elif i == 1:  # 左侧牙齿
            # 牙齿轮廓
            points = np.array([[400, 150], [300, 200], [250, 250], [220, 300], [200, 350], 
                              [300, 350], [350, 300], [380, 250], [400, 200]], np.int32)
            cv2.fillPoly(img, [points], (220, 220, 220))
            # 牙龈
            cv2.polylines(img, [points[:5]], False, (150, 100, 100), 3)
            
        else:  # 右侧牙齿
            # 牙齿轮廓
            points = np.array([[240, 150], [340, 200], [390, 250], [420, 300], [440, 350],
                              [340, 350], [290, 300], [260, 250], [240, 200]], np.int32)
            cv2.fillPoly(img, [points], (220, 220, 220))
            # 牙龈
            cv2.polylines(img, [points[:5]], False, (150, 100, 100), 3)
        
        image_path = f"test_images/teeth_{i+1}.jpg"
        cv2.imwrite(image_path, img)
        images.append(image_path)
        print(f"✅ 创建图像 {i+1}: {image_path}")
    
    return images

def test_model():
    """测试模型"""
    print("\n=== 测试YOLOv8模型 ===")
    
    # 检查模型
    model_path = "models/yolov8n-seg.pt"
    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在: {model_path}")
        return
    
    # 加载模型
    print("加载模型...")
    model = YOLO(model_path)
    print(f"模型设备: {model.device}")
    
    # 创建测试图像
    image_paths = create_teeth_images()
    
    # 测试每张图像
    results = []
    for image_path in image_paths:
        print(f"\n--- 测试 {os.path.basename(image_path)} ---")
        
        # 读取图像
        img = cv2.imread(image_path)
        if img is None:
            print("❌ 无法读取图像")
            continue
        
        # 推理
        start_time = time.time()
        try:
            result = model(img, verbose=False)
            inference_time = time.time() - start_time
            
            if result and len(result) > 0:
                r = result[0]
                detected = len(r.boxes) if r.boxes else 0
                masks = len(r.masks) if r.masks else 0
                
                print(f"✅ 推理成功: {inference_time:.3f}s")
                print(f"检测对象: {detected}, 分割掩码: {masks}")
                
                # 保存结果图像
                os.makedirs("test_results", exist_ok=True)
                output_path = f"test_results/result_{os.path.basename(image_path)}"
                annotated = r.plot()
                cv2.imwrite(output_path, annotated)
                print(f"结果保存: {output_path}")
                
                results.append({
                    'success': True,
                    'time': inference_time,
                    'detected': detected,
                    'output': output_path
                })
            else:
                print("⚠️ 无检测结果")
                results.append({'success': False})
                
        except Exception as e:
            print(f"❌ 推理错误: {e}")
            results.append({'success': False})
    
    # 输出总结
    print("\n=== 测试总结 ===")
    success = sum(1 for r in results if r['success'])
    times = [r['time'] for r in results if r['success']]
    
    print(f"成功测试: {success}/{len(image_paths)}")
    if times:
        print(f"平均推理时间: {sum(times)/len(times):.3f}s")
        print(f"最快: {min(times):.3f}s, 最慢: {max(times):.3f}s")
    
    if success == len(image_paths):
        print("🎉 所有测试通过！模型准备就绪")
    else:
        print("⚠️ 部分测试失败")

if __name__ == "__main__":
    test_model()