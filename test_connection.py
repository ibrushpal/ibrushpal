#!/usr/bin/env python3
"""
简单连接测试脚本
测试API服务是否可用
"""

import requests

def test_api_connection():
    """测试API连接"""
    base_url = "http://localhost:8000"
    
    # 测试健康检查端点
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"健康检查状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ API服务运行正常")
            print(f"响应内容: {response.json()}")
        else:
            print("❌ API服务异常")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务，请确保服务正在运行")
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")

if __name__ == "__main__":
    test_api_connection()