#!/usr/bin/env python3
"""
iBrushPal 依赖验证脚本
检查所有关键依赖包的安装状态和版本
"""

import importlib
import sys

# 关键依赖包列表
REQUIRED_PACKAGES = [
    ("torch", "2.7.1+cu118"),
    ("torchvision", "0.22.1+cu118"),
    ("torchaudio", None),
    ("fastapi", "0.104.1"),
    ("uvicorn", "0.24.0"),
    ("python-multipart", "0.0.6"),
    ("opencv-python", "4.8.1.78"),
    ("ultralytics", "8.0.196"),
    ("numpy", "1.24.3"),
    ("pillow", "10.0.1"),
    ("scikit-learn", "1.3.2")
]

def check_package(package_name, expected_version=None):
    """检查单个包的安装状态"""
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', '未知版本')
        
        if expected_version and version != expected_version:
            status = f"⚠️  版本不匹配 (当前: {version}, 期望: {expected_version})"
        else:
            status = "✅ 安装正常"
            
        return {
            "package": package_name,
            "installed": True,
            "version": version,
            "status": status
        }
    except ImportError:
        return {
            "package": package_name,
            "installed": False,
            "version": None,
            "status": "❌ 未安装"
        }

def main():
    print("=== iBrushPal 依赖包验证 ===\n")
    
    results = []
    for package, expected_version in REQUIRED_PACKAGES:
        result = check_package(package, expected_version)
        results.append(result)
    
    # 打印结果
    for result in results:
        print(f"{result['package']}: {result['status']}")
        if result['installed']:
            print(f"  版本: {result['version']}")
        print()
    
    # 检查CUDA支持
    print("=== GPU/CUDA 支持验证 ===")
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            print("✅ CUDA 可用")
            print(f"  GPU设备: {torch.cuda.get_device_name(0)}")
            print(f"  CUDA版本: {torch.version.cuda}")
        else:
            print("❌ CUDA 不可用")
    except ImportError:
        print("❌ PyTorch 未安装，无法检查CUDA")
    
    # 统计结果
    installed_count = sum(1 for r in results if r['installed'])
    total_count = len(results)
    
    print(f"\n=== 验证完成 ===")
    print(f"已安装: {installed_count}/{total_count} 个关键包")
    
    if installed_count == total_count:
        print("✅ 所有关键依赖包都已安装！")
    else:
        missing = [r['package'] for r in results if not r['installed']]
        print(f"❌ 缺少的包: {', '.join(missing)}")
        print("请运行: pip install " + " ".join(missing))

if __name__ == "__main__":
    main()