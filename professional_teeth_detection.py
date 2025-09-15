#!/usr/bin/env python3
"""
专业牙齿检测测试
使用更真实的牙齿图像特征测试模型
"""

from ultralytics import YOLO
import cv2
import numpy as np
import time
import os

def create_realistic_teeth_images():
    """创建更真实的牙齿测试图像"""
    print("=== 创建真实牙齿模拟图像 ===")
    
    os.makedirs("professional_test", exist_ok=True)
    images = []
    
    # 1. 正面牙齿图像
    img1 = np.ones((640, 640, 3), dtype=np.uint8) * 240  # 浅色背景
    
    # 添加牙齿特征
    for i in range(8):  # 8颗前牙
        x_start = 200 + i * 30
        x_end = x_start + 25
        # 牙齿形状（梯形）
        pts = np.array([[x_start, 300], [x_start+5, 250], [x_end-5, 250], [x_end, 300]], np.int32)
        cv2.fillPoly(img1, [pts], (255, 255, 240))  # 牙齿颜色
        
        # 牙齿分隔线
        cv2.line(img1, (x_start+12, 250), (x_start+12, 300), (220, 220, 220), 1)
    
    # 牙龈线
    cv2.rectangle(img1, (190, 245), (450, 250), (200, 150, 150), -1)
    
    image1_path = "professional_test/front_teeth.jpg"
    cv2.imwrite(image1_path, img1)
    images.append(image1_path)
    
    # 2. 侧方牙齿图像
    img2 = np.ones((480, 640, 3), dtype=np.uint8) * 240
    
    # 侧方牙齿（臼齿形状）
    for i in range(3):
        center_x = 320 + i * 80 - 80
        center_y = 240
        # 绘制臼齿形状（更复杂的几何形状）
        cv2.ellipse(img2, (center_x, center_y), (25, 20), 0, 0, 360, (250, 250, 235), -1)
        cv2.ellipse(img2, (center_x, center_y), (20, 15), 0, 0, 360, (240, 240, 220), -1)
        # 牙齿沟壑
        cv2.line(img2, (center_x-15, center_y-5), (center_x+15, center_y-5), (230, 230, 210), 2)
        cv2.line(img2, (center_x, center_y-10), (center_x, center_y+10), (230, 230, 210), 2)
    
    image2_path = "professional_test/side_teeth.jpg"
    cv2.imwrite(image2_path, img2)
    images.append(image2_path)
    
    # 3. 带有牙菌斑的牙齿
    img3 = np.ones((640, 640, 3), dtype=np.uint8) * 240
    
    # 牙齿
    for i in range(6):
        x_start = 220 + i * 35
        x_end = x_start + 30
        pts = np.array([[x_start, 320], [x_start+5, 270], [x_end-5, 270], [x_end, 320]], np.int32)
        cv2.fillPoly(img3, [pts], (250, 250, 235))
        
        # 添加牙菌斑（黄色斑点）
        if i in [1, 3, 5]:  # 每隔一颗牙齿
            for j in range(3):
                spot_x = x_start + 10 + j * 5
                spot_y = 290 + j * 3
                cv2.circle(img3, (spot_x, spot_y), 3, (220, 220, 150), -1)
    
    image3_path = "professional_test/teeth_with_plaque.jpg"
    cv2.imwrite(image3_path, img3)
    images.append(image3_path)
    
    print("✅ 专业牙齿图像创建完成")
    return images

def test_teeth_detection(model_path, image_paths, model_name):
    """测试牙齿检测性能"""
    print(f"\n=== 测试 {model_name} 牙齿检测 ===")
    
    if not os.path.exists(model_path):
        print(f"❌ 模型不存在: {model_path}")
        return None
    
    try:
        model = YOLO(model_path)
        results = []
        
        for i, image_path in enumerate(image_paths):
            print(f"\n  测试图像 {i+1}: {os.path.basename(image_path)}")
            
            img = cv2.imread(image_path)
            if img is None:
                print("    ❌ 无法读取图像")
                continue
            
            # 推理
            start_time = time.time()
            inference_results = model(img, verbose=False)
            inference_time = time.time() - start_time
            
            if inference_results and len(inference_results) > 0:
                result = inference_results[0]
                detected = len(result.boxes) if result.boxes else 0
                
                print(f"    推理时间: {inference_time:.3f}s")
                print(f"    检测到: {detected}个对象")
                
                if detected > 0:
                    # 显示检测置信度
                    for j, box in enumerate(result.boxes):
                        conf = box.conf[0].item()
                        print(f"    对象 {j+1}: 置信度={conf:.3f}")
                
                # 保存结果图像
                output_dir = f"professional_test/results_{model_name.replace(' ', '_').replace('(', '').replace(')', '')}"
                os.makedirs(output_dir, exist_ok=True)
                output_path = f"{output_dir}/result_{os.path.basename(image_path)}"
                annotated = result.plot()
                cv2.imwrite(output_path, annotated)
                
                results.append({
                    'image': image_path,
                    'time': inference_time,
                    'detected': detected,
                    'output_path': output_path
                })
            else:
                print("    ⚠️ 无检测结果")
                results.append({'detected': 0})
        
        # 统计结果
        total_detected = sum(r['detected'] for r in results)
        avg_time = sum(r['time'] for r in results if 'time' in r) / len(results)
        success_rate = sum(1 for r in results if r['detected'] > 0) / len(results)
        
        print(f"\n  {model_name} 总结:")
        print(f"  总检测对象: {total_detected}")
        print(f"  平均推理时间: {avg_time:.3f}s")
        print(f"  成功率: {success_rate:.1%}")
        
        return {
            'model': model_name,
            'total_detected': total_detected,
            'avg_time': avg_time,
            'success_rate': success_rate
        }
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return None

def main():
    """主测试函数"""
    print("专业牙齿检测能力测试")
    print("=" * 50)
    
    # 创建专业测试图像
    test_images = create_realistic_teeth_images()
    
    # 测试模型
    models = [
        {'path': 'models/yolov8n-seg.pt', 'name': 'YOLOv8n-seg'},
        {'path': 'models/yolov8x-seg.pt', 'name': 'YOLOv8x-seg'}
    ]
    
    results = []
    
    for model_info in models:
        result = test_teeth_detection(model_info['path'], test_images, model_info['name'])
        if result:
            results.append(result)
    
    # 输出对比结果
    print("\n" + "="*60)
    print("专业牙齿检测能力对比")
    print("="*60)
    
    print(f"{'模型':<15} {'检测对象':<10} {'平均时间':<12} {'成功率':<10}")
    print("-"*60)
    
    for result in results:
        print(f"{result['model']:<15} {result['total_detected']:<10} {result['avg_time']:.3f}s     {result['success_rate']:.1%}")
    
    # 给出建议
    print("\n=== 专业建议 ===")
    if results:
        best_model = max(results, key=lambda x: x['total_detected'])
        print(f"推荐使用: {best_model['model']}")
        print(f"检测能力: {best_model['total_detected']}个牙齿对象")
        print(f"推理性能: {best_model['avg_time']:.3f}秒")
        
        if best_model['total_detected'] == 0:
            print("\n⚠️ 警告: 所有模型都未能检测到牙齿")
            print("建议: 需要专门针对牙齿检测训练的模型")
    else:
        print("❌ 所有测试失败")

if __name__ == "__main__":
    main()