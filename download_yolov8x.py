#!/usr/bin/env python3
"""
下载YOLOv8x-seg专业模型
"""

from ultralytics import YOLO
import os

def download_professional_model():
    """下载YOLOv8x-seg模型"""
    print("=== 下载专业牙齿检测模型 ===")
    
    # 确保模型目录存在
    os.makedirs("models", exist_ok=True)
    model_path = "models/yolov8x-seg.pt"
    
    # 检查是否已存在
    if os.path.exists(model_path):
        print(f"✅ 模型已存在: {model_path}")
        return model_path
    
    try:
        print("下载YOLOv8x-seg模型...")
        print("注意: 这将下载约68MB的模型文件")
        
        # 下载模型
        model = YOLO('yolov8x-seg.pt')
        
        # 保存到本地
        model.save(model_path)
        print(f"✅ 模型下载完成: {model_path}")
        
        # 验证模型
        print("验证模型...")
        test_model = YOLO(model_path)
        print(f"模型设备: {test_model.device}")
        print(f"模型参数: {sum(p.numel() for p in test_model.model.parameters()):,}")
        
        return model_path
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return None

def test_model_performance():
    """测试模型性能"""
    print("\n=== 测试模型性能 ===")
    
    model_path = "models/yolov8x-seg.pt"
    if not os.path.exists(model_path):
        print("❌ 模型文件不存在")
        return
    
    # 加载模型
    model = YOLO(model_path)
    print(f"模型加载成功: {model_path}")
    
    # 创建测试图像
    import cv2
    import numpy as np
    
    test_image = np.ones((640, 640, 3), dtype=np.uint8) * 255
    cv2.rectangle(test_image, (200, 200), (440, 440), (220, 220, 220), -1)
    
    # 性能测试
    import time
    times = []
    for i in range(5):
        start_time = time.time()
        results = model(test_image, verbose=False)
        inference_time = time.time() - start_time
        times.append(inference_time)
        print(f"测试 {i+1}: {inference_time:.3f}s")
    
    avg_time = sum(times) / len(times)
    print(f"平均推理时间: {avg_time:.3f}s")
    print(f"最快: {min(times):.3f}s, 最慢: {max(times):.3f}s")
    
    if avg_time <= 2.0:
        print("✅ 性能满足要求 (<2s)")
    else:
        print("⚠️ 性能可能影响用户体验")

if __name__ == "__main__":
    # 下载模型
    model_path = download_professional_model()
    
    if model_path:
        # 测试性能
        test_model_performance()
        
        print("\n=== 下一步 ===")
        print("1. 使用新模型测试牙齿图像")
        print("2. 比较与YOLOv8n-seg的性能差异")
        print("3. 根据结果决定是否部署")
    else:
        print("❌ 模型下载失败，请检查网络连接")