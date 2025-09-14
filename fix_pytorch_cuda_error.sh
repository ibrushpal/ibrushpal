#!/bin/bash

# PyTorch CUDA版本不匹配修复脚本
echo "=== 修复PyTorch CUDA版本不匹配问题 ==="

# 1. 检查当前环境
echo "1. 检查当前环境..."
source .venv/bin/activate
python -c "import sys; print('Python版本:', sys.version)" 2>/dev/null || echo "Python环境检查失败"

# 2. 检查NVIDIA驱动版本
echo "2. 检查NVIDIA驱动版本..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi | grep "Driver Version"
    driver_version=$(nvidia-smi --query-gpu=driver_version --format=csv,noheader | head -n1)
    echo "驱动版本: $driver_version"
else
    echo "警告: nvidia-smi不可用"
fi

# 3. 完全卸载当前PyTorch
echo "3. 卸载当前PyTorch..."
pip uninstall torch torchvision torchaudio -y
pip cache purge

# 4. 根据驱动版本安装合适的PyTorch
echo "4. 安装合适的PyTorch版本..."
if [[ "$driver_version" > "525.60.13" ]] || [[ "$driver_version" == "525.60.13" ]]; then
    echo "检测到较新驱动，安装CUDA 12.1版本PyTorch"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
else
    echo "检测到较旧驱动，安装CUDA 11.8版本PyTorch"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
fi

# 5. 如果仍有问题，安装CPU版本作为后备
echo "5. 验证安装..."
if ! python -c "import torch; print('PyTorch版本:', torch.__version__)" 2>/dev/null; then
    echo "CUDA版本安装失败，回退到CPU版本"
    pip uninstall torch torchvision torchaudio -y
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# 6. 最终验证
echo "6. 最终验证..."
python -c "
import torch
print('=== 修复结果 ===')
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU设备: {torch.cuda.get_device_name(0)}')
    print(f'CUDA版本: {torch.version.cuda}')
else:
    print('使用CPU模式运行')
"

echo "=== 修复完成 ==="
echo "如果仍有问题，请检查NVIDIA驱动版本并手动安装匹配的PyTorch版本"