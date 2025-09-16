#!/usr/bin/env python3
"""
牙齿检测端点调试脚本
用于诊断HTTP 422错误
"""

import requests
import json
import os
from pathlib import Path

def test_teeth_detection():
    """测试牙齿检测端点"""
    base_url = "http://localhost:8000"
    
    # 检查图片文件是否存在
    test_images = ["t1.jpg", "t2.jpg"]
    for img_name in test_images:
        img_path = Path.home() / "ibrushpal" / img_name
        if not img_path.exists():
            print(f"❌ 图片不存在: {img_path}")
            continue
            
        print(f"📷 测试图片: {img_name}")
        
        try:
            with open(img_path, 'rb') as f:
                files = {'file': (img_name, f, 'image/jpeg')}
                data = {
                    'use_dl_model': 'true',
                    'confidence_threshold': '0.3'
                }
                
                # 发送请求
                response = requests.post(
                    f"{base_url}/detect-teeth",
                    files=files,
                    data=data
                )
                
                print(f"HTTP状态码: {response.status_code}")
                print(f"响应头: {dict(response.headers)}")
                
                if response.status_code == 200:
                    print("✅ 请求成功")
                    print(f"响应内容: {response.json()}")
                else:
                    print("❌ 请求失败")
                    try:
                        error_data = response.json()
                        print(f"错误详情: {error_data}")
                    except:
                        print(f"原始响应: {response.text}")
                        
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        print("-" * 50)

def test_health():
    """测试健康检查"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"健康检查: HTTP {response.status_code}")
        if response.status_code == 200:
            print(f"健康状态: {response.json()}")
    except Exception as e:
        print(f"健康检查失败: {e}")

if __name__ == "__main__":
    print("🦷 牙齿检测端点调试")
    print("=" * 50)
    
    # 先测试健康状态
    test_health()
    print()
    
    # 测试牙齿检测
    test_teeth_detection()