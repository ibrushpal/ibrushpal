#!/bin/bash

# 彻底清理和重新安装PyTorch脚本
echo "=== 彻底清理和重新安装PyTorch ==="

# 1. 首先检查当前安装的PyTorch
echo "1. 检查当前PyTorch安装..."
pip list | grep torch

# 2. 完全卸载所有torch相关包
echo "2. 卸载所有torch相关包..."
pip uninstall torch torchvision torchaudio torchtext torchdata -y

# 3. 清理pip缓存
echo "3. 清理pip缓存..."
pip cache purge

# 4. 检查NVIDIA驱动版本并推荐合适的PyTorch版本
echo "4. 检查NVIDIA驱动版本..."
python check_nvidia_driver.py

# 5. 根据推荐安装合适的PyTorch版本
echo "5. 安装推荐的PyTorch版本..."
read -p "请输入推荐的PyTorch版本 (例如: cu121, cu118, cpu): " pytorch_version

if [ "$pytorch_version" = "cpu" ]; then
    echo "安装CPU版本的PyTorch..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
else
    echo "安装CUDA $pytorch_version 版本的PyTorch..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/$pytorch_version
fi

# 6. 验证安装
echo "6. 验证安装..."
python -c "
import torch
print('=== 安装验证 ===')
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU设备: {torch.cuda.get_device_name(0)}')
    print(f'CUDA版本: {torch.version.cuda}')
else:
    print('使用CPU模式')
"

echo "=== 清理安装完成 ==="