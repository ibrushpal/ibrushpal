#!/bin/bash
echo "=== iBrushPal 第一步验证脚本 ==="
echo "开始时间: $(date)"

# 1. 系统环境检查
echo -e "\n1. 检查系统环境..."
echo "系统信息: $(uname -a)"
echo "发行版信息:"
lsb_release -a 2>/dev/null || echo "lsb_release不可用"

# 2. NVIDIA驱动检查
echo -e "\n2. 检查NVIDIA驱动..."
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=driver_version,name,memory.total --format=csv
else
    echo "nvidia-smi不可用，请安装NVIDIA驱动"
fi

# 3. Python环境检查
echo -e "\n3. 检查Python环境..."
echo "Python版本: $(python3 --version 2>&1)"
echo "Pip版本: $(pip3 --version 2>&1)"

# 4. 创建虚拟环境
echo -e "\n4. 创建Python虚拟环境..."
python3 -m venv .venv
source .venv/bin/activate
echo "虚拟环境Python: $(which python)"
echo "虚拟环境Pip: $(which pip)"

# 5. 验证PyTorch基础安装
echo -e "\n5. 安装和验证PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 6. 验证GPU支持
echo -e "\n6. 验证GPU支持..."
python3 -c "
import torch
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU数量: {torch.cuda.device_count()}')
    print(f'当前GPU: {torch.cuda.current_device()}')
    print(f'GPU名称: {torch.cuda.get_device_name(0)}')
    print(f'CUDA版本: {torch.version.cuda}')
else:
    print('CUDA不可用，请检查NVIDIA驱动')
"

echo -e "\n=== 第一步验证完成 ==="
echo "完成时间: $(date)"