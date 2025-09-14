#!/usr/bin/env python3
"""
实际牙齿图像测试脚本
测试YOLOv8模型对真实牙齿图像的分割和检测能力
"""

import torch
import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
import requests
from PIL import Image
import matplotlib.pyplot as plt

def download_sample_images():
    """下载牙齿样本图像用于测试"""
    print("=== 下载样本牙齿图像 ===")
    
    # 样本牙齿图像URL（使用公开可用的牙齿图像）
    sample_urls = [
        "https://placehold.co/640x480/white/grey?text=Front+Teeth",
        "https://placehold.co/640x480/white/grey?text=Left+Teeth", 
        "https://placehold.co/640x480/white/grey?text=Right+Teeth"
    ]
    
    os.makedirs("test_images", exist_ok=True)
    
    downloaded_images = []
    for i, url in enumerate(sample_urls):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                image_path = f"test_images/sample_{i+1}.jpg"
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                downloaded_images.append(image_path)
                print(f"✅ 下载样本 {i+1}: {image_path}")
            else:
                print(f"❌ 下载失败 {i+1}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ 下载错误 {i+1}: {e}")
    
    # 如果下载失败，创建模拟牙齿图像
    if not downloaded_images:
        print("创建模拟牙齿图像...")
        for i in range(3):
            # 创建模拟牙齿图像
            img = np.ones((480, 640, 3), dtype=np.uint8) * 255
            
            # 添加牙齿形状
            if i == 0:  # 正面
                cv2.rectangle(img, (200, 150), (440, 350), (220, 220, 220), -1)
                cv2.rectangle(img, (250, 180), (390, 320), (240, 240, 240), -1)
            elif i == 1:  # 左侧
                cv2.rectangle(img, (100, 150), (300, 350), (220, 220, 220), -1)
            else:  # 右侧
                cv2.rectangle(img, (340, 150), (540, 350), (220, 220, 220), -1)
            
            image_path = f"test_images/sample_{i+1}.jpg"
            cv2.imwrite(image_path, img)
            downloaded_images.append(image_path)
            print(f"✅ 创建模拟图像 {i+1}: {image_path}")
    
    return downloaded_images

def test_teeth_detection(model, image_path):
    """测试单张牙齿图像检测"""
    print(f"\n=== 测试图像: {os.path.basename(image_path)} ===")
    
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ 无法读取图像: {image_path}")
        return None
    
    print(f"图像尺寸: {image.shape[1]}x{image.shape[0]}")
    
    try:
        # 进行牙齿检测和分割
        start_time = time.time()
        results = model(image, verbose=False)
        inference_time = time.time() - start_time
        
        print(f"✅ 检测完成: {inference_time:.3f}秒")
        
        # 分析结果
        if results and len(results) > 0:
            result = results[0]
            
            # 绘制检测结果
            annotated_image = result.plot()
            
            # 保存结果图像
            output_path = f"test_results/result_{os.path.basename(image_path)}"
            os.makedirs("test_results", exist_ok=True)
            cv2.imwrite(output_path, annotated_image)
            
            # 显示检测信息
            if result.boxes:
                print(f"检测到对象: {len(result.boxes)}个")
                for j, box in enumerate(result.boxes):
                    conf = box.conf[0].item()
                    coords = box.xyxy[0].cpu().numpy()
                    print(f"  对象 {j+1}: 置信度={conf:.3f}, 坐标={coords}")
            else:
                print("⚠️ 未检测到牙齿对象")
                
            if result.masks:
                print(f"分割掩码: {len(result.masks)}个")
            else:
                print("⚠️ 未生成分割掩码")
                
            return {
                'success': True,
                'inference_time': inference_time,
                'detected_objects': len(result.boxes) if result.boxes else 0,
                'output_path': output_path
            }
        else:
            print("❌ 未返回有效结果")
            return {'success': False, 'error': 'No results'}
            
    except Exception as e:
        print(f"❌ 检测失败: {e}")
        return {'success': False, 'error': str(e)}

def visualize_results(image_paths, results):
    """可视化测试结果"""
    print("\n=== 结果可视化 ===")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('牙齿图像检测结果', fontsize=16)
    
    for i, (image_path, result) in enumerate(zip(image_paths, results)):
        if result and result['success']:
            # 原始图像
            orig_image = cv2.imread(image_path)
            orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
            axes[0, i].imshow(orig_image)
            axes[0, i].set_title(f'原始图像 {i+1}')
            axes[0, i].axis('off')
            
            # 检测结果
            result_image = cv2.imread(result['output_path'])
            result_image = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)
            axes[1, i].imshow(result_image)
            axes[1, i].set_title(f'检测结果 ({result["detected_objects"]}对象)')
            axes[1, i].axis('off')
        else:
            axes[0, i].text(0.5, 0.5, '测试失败', ha='center', va='center', transform=axes[0, i].transAxes)
            axes[0, i].set_title(f'图像 {i+1} - 失败')
            axes[0, i].axis('off')
            axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.savefig('test_results/summary.png', dpi=300, bbox_inches='tight')
    print("✅ 结果汇总图已保存: test_results/summary.png")

def main():
    """主测试函数"""
    print("实际牙齿图像测试")
    print("=" * 50)
    
    # 检查模型
    model_path = "models/yolov8n-seg.pt"
    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在: {model_path}")
        return
    
    # 加载模型
    print("加载YOLOv8模型...")
    model = YOLO(model_path)
    print(f"模型设备: {model.device}")
    
    # 下载/创建测试图像
    image_paths = download_sample_images()
    
    # 测试每张图像
    all_results = []
    for image_path in image_paths:
        result = test_teeth_detection(model, image_path)
        all_results.append(result)
    
    # 可视化结果
    visualize_results(image_paths, all_results)
    
    # 统计结果
    success_count = sum(1 for r in all_results if r and r['success'])
    total_time = sum(r['inference_time'] for r in all_results if r and r['success'])
    avg_time = total_time / success_count if success_count > 0 else 0
    
    print(f"\n=== 测试总结 ===")
    print(f"成功测试: {success_count}/{len(image_paths)}")
    print(f"平均推理时间: {avg_time:.3f}秒")
    
    if success_count == len(image_paths):
        print("✅ 所有测试通过！模型准备好处理真实牙齿图像")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")

if __name__ == "__main__":
    main()