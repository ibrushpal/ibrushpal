#!/usr/bin/env python3
"""
简单API测试脚本
直接测试牙齿检测端点，绕过可能的验证问题
"""

import requests
import json

def test_direct():
    """直接测试API端点"""
    url = "http://localhost:8000/detect-teeth"
    
    # 准备简单的测试数据
    files = {
        'image': ('test.jpg', b'test image data', 'image/jpeg')
    }
    data = {
        'use_dl_model': 'true',
        'confidence_threshold': '0.3'
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ 成功")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("❌ 失败")
            try:
                error_data = response.json()
                print(f"错误详情: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"原始响应: {response.text}")
                
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == "__main__":
    test_direct()