#!/bin/bash

# iBrushPal快速设置脚本
echo "=== iBrushPal快速环境设置 ==="

# 步骤1: 系统更新
echo "1. 更新系统..."
sudo apt update && sudo apt upgrade -y

# 步骤2: 安装基础工具
echo "2. 安装基础工具..."
sudo apt install -y build-essential python3-pip python3-venv

# 步骤3: 创建项目目录
echo "3. 创建项目环境..."
mkdir -p ~/ibrushpal
cd ~/ibrushpal
python3 -m venv .venv
source .venv/bin/activate

# 步骤4: 安装PyTorch
echo "4. 安装PyTorch..."
# 自动检测并安装合适的版本
if nvidia-smi | grep -q "Driver Version"; then
    echo "检测到NVIDIA驱动，安装CUDA版本PyTorch"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
else
    echo "未检测到NVIDIA驱动，安装CPU版本PyTorch"
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# 步骤5: 安装项目依赖
echo "5. 安装项目依赖..."
pip install fastapi uvicorn opencv-python pillow numpy pandas scikit-learn

# 步骤6: 验证环境
echo "6. 验证环境..."
python -c "
import torch
print('=== 环境验证 ===')
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU设备: {torch.cuda.get_device_name(0)}')
"

echo "=== 设置完成 ==="
echo "下一步:"
echo "1. 上传您的代码"
echo "2. 运行: source .venv/bin/activate"
echo "3. 启动: uvicorn main:app --reload"