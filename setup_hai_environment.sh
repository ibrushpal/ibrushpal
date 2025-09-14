#!/bin/bash

# iBrushPal HAI服务器环境配置脚本
echo "=== 开始配置HAI服务器环境 ==="

# 1. 系统更新
echo "1. 更新系统包..."
sudo apt update
sudo apt upgrade -y

# 2. 安装基础开发工具
echo "2. 安装基础开发工具..."
sudo apt install -y build-essential git curl wget vim python3-pip python3-venv

# 3. 检查NVIDIA驱动
echo "3. 检查NVIDIA驱动..."
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA驱动已安装:"
    nvidia-smi
else
    echo "警告: NVIDIA驱动未安装，请先安装NVIDIA驱动"
    exit 1
fi

# 4. 检查CUDA
echo "4. 检查CUDA环境..."
if command -v nvcc &> /dev/null; then
    echo "CUDA版本:"
    nvcc --version
else
    echo "CUDA未安装，但NVIDIA驱动已存在"
fi

# 5. 创建Python虚拟环境
echo "5. 设置Python虚拟环境..."
python3 -m venv .venv
source .venv/bin/activate

# 6. 安装正确版本的PyTorch（根据CUDA版本）
echo "6. 安装PyTorch..."
# 自动检测CUDA版本并安装对应的PyTorch
if nvcc --version | grep -q "release 12"; then
    echo "检测到CUDA 12.x，安装对应版本PyTorch"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
elif nvcc --version | grep -q "release 11"; then
    echo "检测到CUDA 11.x，安装对应版本PyTorch"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
    echo "无法确定CUDA版本，安装CPU版本PyTorch"
    pip install torch torchvision torchaudio
fi

# 7. 安装项目依赖
echo "7. 安装项目依赖..."
pip install -r requirements.txt

# 8. 验证环境
echo "8. 验证环境配置..."
python -c "
import torch
print('=== 环境验证结果 ===')
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA版本: {torch.version.cuda}')
    print(f'GPU设备: {torch.cuda.get_device_name(0)}')
    print(f'GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB')
else:
    print('警告: CUDA不可用，请检查驱动安装')
"

# 9. 安装其他必要的系统依赖
echo "9. 安装系统依赖..."
sudo apt install -y libgl1-mesa-glx libglib2.0-0

echo "=== HAI服务器环境配置完成 ==="
echo "请运行以下命令激活环境: source .venv/bin/activate"
echo "然后运行验证脚本: python verify_gpu.py"