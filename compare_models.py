#!/usr/bin/env python3
"""
模型性能对比测试
比较YOLOv8n-seg vs YOLOv8x-seg的性能差异
"""

from ultralytics import YOLO
import cv2
import numpy as np
import time
import os

def create_test_image():
    """创建标准测试图像"""
    img = np.ones((640, 640, 3), dtype=np.uint8) * 255
    # 添加多个牙齿状区域
    cv2.rectangle(img, (150, 150), (250, 300), (220, 220, 220), -1)  # 左侧牙齿
    cv2.rectangle(img, (270, 150), (370, 300), (220, 220, 220), -1)  # 中间牙齿  
    cv2.rectangle(img, (390, 150), (490, 300), (220, 220, 220), -1)  # 右侧牙齿
    return img

def test_model(model_path, test_image, model_name):
    """测试单个模型性能"""
    print(f"\n=== 测试 {model_name} ===")
    
    if not os.path.exists(model_path):
        print(f"❌ 模型不存在: {model_path}")
        return None
    
    try:
        # 加载模型
        model = YOLO(model_path)
        
        # 预热
        model(test_image, verbose=False)
        
        # 性能测试
        times = []
        detections = []
        
        for i in range(10):
            start_time = time.time()
            results = model(test_image, verbose=False)
            inference_time = time.time() - start_time
            times.append(inference_time)
            
            # 记录检测结果
            if results and len(results) > 0:
                result = results[0]
                detected = len(result.boxes) if result.boxes else 0
                detections.append(detected)
            else:
                detections.append(0)
            
            print(f"  测试 {i+1}: {inference_time:.3f}s, 检测: {detections[-1]}对象")
        
        # 计算统计
        avg_time = sum(times) / len(times)
        avg_detection = sum(detections) / len(detections)
        success_rate = sum(1 for d in detections if d > 0) / len(detections)
        
        return {
            'model': model_name,
            'avg_time': avg_time,
            'avg_detection': avg_detection,
            'success_rate': success_rate,
            'times': times,
            'detections': detections
        }
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return None

def main():
    """主测试函数"""
    print("YOLOv8模型性能对比测试")
    print("=" * 50)
    
    # 创建测试图像
    test_image = create_test_image()
    
    # 测试的模型列表
    models_to_test = [
        {'path': 'models/yolov8n-seg.pt', 'name': 'YOLOv8n-seg (当前)'},
        {'path': 'models/yolov8s-seg.pt', 'name': 'YOLOv8s-seg'},
        {'path': 'models/yolov8m-seg.pt', 'name': 'YOLOv8m-seg'},
        {'path': 'models/yolov8l-seg.pt', 'name': 'YOLOv8l-seg'},
        {'path': 'models/yolov8x-seg.pt', 'name': 'YOLOv8x-seg (专业)'}
    ]
    
    results = []
    
    # 测试所有模型
    for model_info in models_to_test:
        result = test_model(model_info['path'], test_image, model_info['name'])
        if result:
            results.append(result)
    
    # 输出对比结果
    print("\n" + "="*60)
    print("模型性能对比结果")
    print("="*60)
    
    print(f"{'模型名称':<25} {'平均时间':<10} {'检测数':<8} {'成功率':<8} {'推荐度':<10}")
    print("-"*60)
    
    for result in results:
        # 计算推荐度 (时间权重0.4 + 检测数权重0.3 + 成功率权重0.3)
        time_score = 1 / (result['avg_time'] + 0.1)  # 避免除零
        detection_score = result['avg_detection'] / 3.0  # 最大3个检测对象
        success_score = result['success_rate']
        
        recommendation = time_score * 0.4 + detection_score * 0.3 + success_score * 0.3
        recommendation_level = "⭐" * int(recommendation * 5)
        
        print(f"{result['model']:<25} {result['avg_time']:.3f}s     "
              f"{result['avg_detection']:.1f}      {result['success_rate']:.1%}     "
              f"{recommendation_level}")
    
    # 给出建议
    print("\n=== 部署建议 ===")
    best_model = max(results, key=lambda x: (1/x['avg_time'])*0.4 + x['avg_detection']*0.3 + x['success_rate']*0.3)
    print(f"推荐使用: {best_model['model']}")
    print(f"理由: 平均推理时间 {best_model['avg_time']:.3f}s, "
          f"检测对象 {best_model['avg_detection']:.1f}, "
          f"成功率 {best_model['success_rate']:.1%}")

if __name__ == "__main__":
    main()