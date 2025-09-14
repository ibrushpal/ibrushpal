#!/usr/bin/env python3
"""
API文档测试脚本
"""

import requests
import sys

def test_api_docs(host="http://localhost:8000"):
    """测试API文档端点"""
    endpoints = [
        "/docs",
        "/redoc", 
        "/openapi.json"
    ]
    
    print("=== API文档端点测试 ===")
    
    for endpoint in endpoints:
        url = f"{host}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            print(f"{endpoint}: {response.status_code} - {len(response.text)} bytes")
            
            if response.status_code == 200:
                if "swagger" in response.text.lower() or "openapi" in response.text.lower():
                    print(f"  ✅ 内容正常")
                else:
                    print(f"  ⚠️ 内容可能异常")
            else:
                print(f"  ❌ 请求失败")
                
        except requests.exceptions.RequestException as e:
            print(f"{endpoint}: 连接失败 - {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    # 允许从命令行指定主机
    host = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api_docs(host)