#!/usr/bin/env python3
"""
NVIDIA驱动版本检查脚本
用于确定正确的PyTorch版本
"""

import subprocess
import re

def get_nvidia_driver_version():
    """获取NVIDIA驱动版本"""
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, check=True)
        output = result.stdout
        
        # 查找驱动版本
        driver_match = re.search(r'Driver Version:\s+(\d+\.\d+)', output)
        if driver_match:
            return driver_match.group(1)
        
        # 如果没有找到，尝试其他方法
        try:
            result = subprocess.run(['cat', '/proc/driver/nvidia/version'], 
                                  capture_output=True, text=True, check=True)
            version_match = re.search(r'NVRM version:\s+.*?(\d+\.\d+)', result.stdout)
            if version_match:
                return version_match.group(1)
        except:
            pass
            
        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_recommended_pytorch_version(driver_version):
    """根据驱动版本推荐PyTorch版本"""
    if not driver_version:
        return "cpu"  # 没有驱动，使用CPU版本
    
    try:
        major, minor = map(float, driver_version.split('.'))
        
        # 驱动版本判断逻辑
        if major >= 535 or (major == 525 and minor >= 60.13):
            return "cu121"  # CUDA 12.1
        elif major >= 470:
            return "cu118"  # CUDA 11.8
        elif major >= 450:
            return "cu116"  # CUDA 11.6
        else:
            return "cpu"    # 太旧的驱动，使用CPU版本
            
    except ValueError:
        return "cpu"

def main():
    print("=== NVIDIA驱动版本检查 ===")
    
    # 检查nvidia-smi是否可用
    driver_version = get_nvidia_driver_version()
    
    if driver_version:
        print(f"检测到NVIDIA驱动版本: {driver_version}")
        
        # 推荐PyTorch版本
        pytorch_version = get_recommended_pytorch_version(driver_version)
        print(f"推荐的PyTorch版本: {pytorch_version}")
        
        # 生成安装命令
        if pytorch_version == "cpu":
            cmd = "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
        else:
            cmd = f"pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/{pytorch_version}"
        
        print(f"\n安装命令:")
        print(cmd)
        
    else:
        print("未检测到NVIDIA驱动或nvidia-smi不可用")
        print("建议安装CPU版本的PyTorch:")
        print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
    
    print("\n=== 检查完成 ===")

if __name__ == "__main__":
    main()