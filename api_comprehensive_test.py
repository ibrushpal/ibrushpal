#!/usr/bin/env python3
"""
iBrushPal API 全面测试脚本
测试所有API端点的功能和性能
"""

import requests
import json
import time
import cv2
import numpy as np
from pathlib import Path
import base64

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = {}
    
    def create_test_image(self, width=640, height=480):
        """创建测试牙齿图像"""
        # 创建白色背景
        image = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # 添加模拟牙齿形状
        for i in range(5):
            center_x = 100 + i * 100
            center_y = height // 2
            
            # 绘制牙齿形状（椭圆）
            cv2.ellipse(image, (center_x, center_y), (30, 40), 0, 0, 360, 
                       (220, 220, 220), -1)
            cv2.ellipse(image, (center_x, center_y), (30, 40), 0, 0, 360, 
                       (150, 150, 150), 2)
        
        # 编码为JPEG
        success, encoded_image = cv2.imencode('.jpg', image)
        return encoded_image.tobytes()
    
    def test_health_endpoint(self):
        """测试健康检查端点"""
        print("🧪 测试健康检查端点...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            result = {
                "status": response.status_code,
                "data": response.json(),
                "success": response.status_code == 200
            }
            print(f"✅ 健康检查: {result}")
            return result
        except Exception as e:
            print(f"❌ 健康检查失败: {e}")
            return {"success": False, "error": str(e)}
    
    def test_model_info_endpoint(self):
        """测试模型信息端点"""
        print("🧪 测试模型信息端点...")
        try:
            response = self.session.get(f"{self.base_url}/model-info")
            result = {
                "status": response.status_code,
                "data": response.json(),
                "success": response.status_code == 200
            }
            print(f"✅ 模型信息: {result}")
            return result
        except Exception as e:
            print(f"❌ 模型信息失败: {e}")
            return {"success": False, "error": str(e)}
    
    def test_status_dashboard(self):
        """测试状态面板"""
        print("🧪 测试状态面板...")
        try:
            response = self.session.get(f"{self.base_url}/status-dashboard")
            result = {
                "status": response.status_code,
                "content_type": response.headers.get('content-type'),
                "data": response.json() if response.status_code != 200 else {},
                "success": response.status_code == 200
            }
            print(f"✅ 状态面板: HTTP {response.status_code}, Content-Type: {response.headers.get('content-type')}")
            return result
        except Exception as e:
            print(f"❌ 状态面板失败: {e}")
            return {"success": False, "error": str(e)}
    
    def test_detect_teeth_endpoint(self, use_real_images=True):
        """测试牙齿检测端点"""
        print("🧪 测试牙齿检测端点...")
        try:
            if use_real_images:
                # 使用用户提供的真实牙齿照片
                test_images = ["t1.jpg", "t2.jpg"]
                results = []
                
                for img_name in test_images:
                    img_path = Path.home() / "ibrushpal" / img_name
                    if img_path.exists():
                        print(f"📷 使用真实牙齿照片: {img_name}")
                        with open(img_path, 'rb') as f:
                            image_data = f.read()
                        
                        # 准备请求
                        files = {'file': (img_name, image_data, 'image/jpeg')}
                        data = {
                            'use_dl_model': 'true',
                            'confidence_threshold': '0.3'
                        }
                        
                        start_time = time.time()
                        response = self.session.post(
                            f"{self.base_url}/detect-teeth",
                            files=files,
                            data=data
                        )
                        response_time = time.time() - start_time
                        
                        result = {
                            "image": img_name,
                            "status": response.status_code,
                            "response_time": f"{response_time:.3f}s",
                            "data": response.json() if response.status_code == 200 else {},
                            "success": response.status_code == 200
                        }
                        
                        if response.status_code == 200:
                            data = response.json()
                            print(f"✅ {img_name}: 检测到 {data.get('teeth_count', 0)} 个牙齿, 耗时 {response_time:.3f}s")
                        else:
                            print(f"❌ {img_name}: HTTP {response.status_code}")
                            
                        results.append(result)
                        time.sleep(1)  # 请求间延迟
                    else:
                        print(f"⚠️  图片不存在: {img_path}")
                        results.append({
                            "image": img_name,
                            "success": False,
                            "error": "文件不存在"
                        })
                
                return {"results": results, "success": any(r.get('success', False) for r in results)}
            else:
                # 使用模拟图像（备用方案）
                image_data = self.create_test_image()
                
                # 准备请求
                files = {'file': ('test_teeth.jpg', image_data, 'image/jpeg')}
                data = {
                    'use_dl_model': 'true',
                    'confidence_threshold': '0.3'
                }
                
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/detect-teeth",
                    files=files,
                    data=data
                )
                response_time = time.time() - start_time
                
                result = {
                    "status": response.status_code,
                    "response_time": f"{response_time:.3f}s",
                    "data": response.json(),
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ 牙齿检测成功: 检测到 {data.get('teeth_count', 0)} 个牙齿, 耗时 {response_time:.3f}s")
                else:
                    print(f"❌ 牙齿检测失败: HTTP {response.status_code}")
                    
                return result
            
        except Exception as e:
            print(f"❌ 牙齿检测失败: {e}")
            return {"success": False, "error": str(e)}
    
    def test_docs_endpoint(self):
        """测试API文档端点"""
        print("🧪 测试API文档端点...")
        try:
            response = self.session.get(f"{self.base_url}/docs")
            result = {
                "status": response.status_code,
                "content_type": response.headers.get('content-type'),
                "success": response.status_code == 200 and 'text/html' in response.headers.get('content-type', '')
            }
            print(f"✅ API文档: HTTP {response.status_code}")
            return result
        except Exception as e:
            print(f"❌ API文档失败: {e}")
            return {"success": False, "error": str(e)}
    
    def test_root_endpoint(self):
        """测试根端点"""
        print("🧪 测试根端点...")
        try:
            response = self.session.get(f"{self.base_url}/")
            result = {
                "status": response.status_code,
                "content_type": response.headers.get('content-type'),
                "success": response.status_code == 200
            }
            print(f"✅ 根端点: HTTP {response.status_code}")
            return result
        except Exception as e:
            print(f"❌ 根端点失败: {e}")
            return {"success": False, "error": str(e)}
    
    def run_comprehensive_test(self):
        """运行全面测试"""
        print("=" * 60)
        print("🦷 iBrushPal API 全面测试")
        print("=" * 60)
        
        tests = [
            ("健康检查", self.test_health_endpoint),
            ("模型信息", self.test_model_info_endpoint),
            ("状态面板", self.test_status_dashboard),
            ("牙齿检测", self.test_detect_teeth_endpoint),
            ("API文档", self.test_docs_endpoint),
            ("根端点", self.test_root_endpoint)
        ]
        
        all_results = {}
        for test_name, test_func in tests:
            result = test_func()
            all_results[test_name] = result
            time.sleep(0.5)  # 短暂延迟
        
        # 生成测试报告
        self.generate_test_report(all_results)
        
        return all_results
    
    def generate_test_report(self, results):
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 测试报告摘要")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result.get('success', False))
        
        print(f"总测试数: {total_tests}")
        print(f"通过测试: {passed_tests}")
        print(f"失败测试: {total_tests - passed_tests}")
        print(f"通过率: {(passed_tests/total_tests)*100:.1f}%")
        
        print("\n详细结果:")
        for test_name, result in results.items():
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            print(f"{status} {test_name}")
            
            if not result.get('success', False) and 'error' in result:
                print(f"   错误: {result['error']}")
        
        # 保存详细报告
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "base_url": self.base_url,
            "results": results,
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": f"{(passed_tests/total_tests)*100:.1f}%"
            }
        }
        
        with open('api_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 详细报告已保存到: api_test_report.json")

def main():
    """主函数"""
    # 可以指定不同的URL进行测试
    tester = APITester("http://localhost:8000")
    
    # 运行全面测试
    results = tester.run_comprehensive_test()
    
    # 检查整体状态
    all_passed = all(result.get('success', False) for result in results.values())
    
    if all_passed:
        print("\n🎉 所有API测试通过！服务运行正常。")
    else:
        print("\n⚠️  部分API测试失败，请检查服务状态。")
    
    return all_passed

if __name__ == "__main__":
    main()