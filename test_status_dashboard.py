import requests

def test_status_dashboard():
    """测试状态面板路由"""
    try:
        # 测试服务器状态面板
        response = requests.get("http://42.194.142.158:8000/status-dashboard", timeout=10)
        print(f"状态: {response.status_code}")
        print(f"内容类型: {response.headers.get('content-type')}")
        
        if response.status_code == 200:
            print("✅ 状态面板路由正常工作")
            # 检查返回内容是否是HTML
            if "text/html" in response.headers.get('content-type', ''):
                print("✅ 返回内容为HTML格式")
                # 检查HTML内容是否包含预期的元素
                content = response.text
                if "iBrushPal" in content and "服务状态面板" in content:
                    print("✅ HTML内容包含正确的标题和品牌信息")
                else:
                    print("⚠️  HTML内容可能不完整")
            else:
                print("❌ 返回内容不是HTML格式")
        else:
            print(f"❌ 状态面板路由返回错误: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接失败: {e}")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

def test_other_endpoints():
    """测试其他API端点"""
    endpoints = [
        ("/", "主页"),
        ("/health", "健康检查"),
        ("/model-info", "模型信息"),
        ("/docs", "API文档")
    ]
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"http://42.194.142.158:8000{endpoint}", timeout=5)
            print(f"{name} ({endpoint}): {response.status_code}")
        except Exception as e:
            print(f"{name} ({endpoint}): 错误 - {e}")

if __name__ == "__main__":
    print("测试iBrushPal API服务状态...")
    print("=" * 50)
    
    test_status_dashboard()
    print("\n" + "-" * 50)
    print("其他端点状态:")
    test_other_endpoints()