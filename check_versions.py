#!/usr/bin/env python3
"""
版本兼容性检查脚本
"""

import torch
import torchvision
import sys

def main():
    print("=== 版本兼容性检查 ===")
    
    # 检查PyTorch和TorchVision版本
    print(f"PyTorch版本: {torch.__version__}")
    print(f"TorchVision版本: {torchvision.__version__}")
    
    # 检查CUDA支持
    print(f"CUDA可用: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU设备: {torch.cuda.get_device_name(0)}")
        print(f"CUDA版本: {torch.version.cuda}")
    
    # 检查版本兼容性
    torch_major, torch_minor = map(int, torch.__version__.split('+')[0].split('.')[:2])
    tv_major, tv_minor = map(int, torchvision.__version__.split('.')[:2])
    
    print(f"\n=== 兼容性分析 ===")
    if torch_major == 2 and tv_major == 0:
        print("⚠️ 警告: TorchVision 0.x 与 PyTorch 2.x 不完全兼容")
        print("建议: pip install torchvision==0.23")
    elif torch_major == tv_major:
        print("✅ 版本兼容性良好")
    else:
        print("⚠️ 版本可能存在兼容性问题")
    
    print("\n=== 检查完成 ===")

if __name__ == "__main__":
    main()