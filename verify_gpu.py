"""
GPU验证脚本
"""
import torch
import sys

def check_gpu():
    print("=== GPU和PyTorch验证 ===")
    print(f"Python版本: {sys.version}")
    print(f"PyTorch版本: {torch.__version__}")
    print(f"CUDA可用: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA版本: {torch.version.cuda}")
        print(f"GPU设备数量: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
            print(f"  内存: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f} GB")
    else:
        print("警告: CUDA不可用，请检查NVIDIA驱动和CUDA安装")

if __name__ == "__main__":
    check_gpu()