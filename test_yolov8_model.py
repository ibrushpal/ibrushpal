#!/usr/bin/env python3
"""
YOLOv8模型验证脚本
测试模型是否正确加载并能进行推理
"""

import torch
import cv2
import numpy as np
from ultralytics import YOLO
import time
import os

def test_gpu_environment():
    """测试GPU环境"""
    print("=== GPU环境测试 ===")
    print(f"PyTorch版本: {torch.__version__}")
    print(f"CUDA可用: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"GPU设备: {torch.cuda.get_device_name(0)}")
        print(f"CUDA版本: {torch.version.cuda}")
        print(f"GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        print("❌ CUDA不可用，请检查NVIDIA驱动和PyTorch安装")

def test_model_loading():
    """测试模型加载"""
    print("\n=== 模型加载测试 ===")
    
    model_path = "models/yolov8n-seg.pt"
    
    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在: {model_path}")
        print("请先运行 download_yolov8.py 下载模型")
        return None
    
    try:
        start_time = time.time()
        model = YOLO(model_path)
        load_time = time.time() - start_time
        
        print(f"✅ 模型加载成功: {load_time:.2f}秒")
        print(f"模型类型: {type(model)}")
        print(f"模型设备: {model.device}")
        
        return model
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return None

def test_model_inference(model):
    """测试模型推理"""
    print("\n=== 模型推理测试 ===")
    
    # 创建测试图像（简单的牙齿区域模拟）
    test_image = np.ones((640, 640, 3), dtype=np.uint8) * 255
    cv2.rectangle(test_image, (200, 200), (440, 440), (200, 200, 200), -1)  # 模拟牙齿区域
    
    try:
        start_time = time.time()
        
        # 进行推理
        results = model(test_image, verbose=False)
        inference_time = time.time() - start_time
        
        print(f"✅ 推理成功: {inference_time:.2f}秒")
        
        # 分析结果
        if results and len(results) > 0:
            result = results[0]
            print(f"检测到对象数量: {len(result.boxes) if result.boxes else 0}")
            
            if result.boxes:
                print(f"置信度: {result.boxes.conf[0].item():.3f}")
                print(f"边界框: {result.boxes.xyxy[0].cpu().numpy()}")
            
            if result.masks:
                print(f"分割掩码: {result.masks.xy[0].shape if result.masks.xy else '无'}")
        
        return inference_time
        
    except Exception as e:
        print(f"❌ 推理失败: {e}")
        return None

def test_performance(model, num_tests=5):
    """性能测试"""
    print(f"\n=== 性能测试 ({num_tests}次推理) ===")
    
    test_image = np.ones((640, 640, 3), dtype=np.uint8) * 255
    cv2.rectangle(test_image, (200, 200), (440, 440), (200, 200, 200), -1)
    
    times = []
    
    for i in range(num_tests):
        start_time = time.time()
        results = model(test_image, verbose=False)
        inference_time = time.time() - start_time
        times.append(inference_time)
        
        print(f"测试 {i+1}: {inference_time:.3f}秒")
    
    avg_time = sum(times) / len(times)
    print(f"平均推理时间: {avg_time:.3f}秒")
    print(f"最大推理时间: {max(times):.3f}秒")
    print(f"最小推理时间: {min(times):.3f}秒")
    
    # 检查是否满足30秒要求
    if avg_time <= 30:
        print("✅ 性能满足要求 (≤30秒)")
    else:
        print("❌ 性能不满足要求 (>30秒)")
    
    return times

def main():
    """主测试函数"""
    print("YOLOv8模型验证测试")
    print("=" * 50)
    
    # 测试GPU环境
    test_gpu_environment()
    
    # 测试模型加载
    model = test_model_loading()
    if model is None:
        return
    
    # 测试推理
    inference_time = test_model_inference(model)
    if inference_time is None:
        return
    
    # 性能测试
    test_performance(model)
    
    print("\n=== 测试完成 ===")
    print("模型验证状态: ✅ 通过" if inference_time <= 30 else "❌ 未通过")

if __name__ == "__main__":
    main()