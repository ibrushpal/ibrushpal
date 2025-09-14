#!/bin/bash

# iBrushPal PyTorch CUDA修复脚本
echo "开始修复PyTorch CUDA版本不匹配问题..."

# 检查当前CUDA版本
echo "检查CUDA版本..."
nvcc --version
nvidia-smi

# 卸载当前有问题的PyTorch
echo "卸载当前PyTorch..."
pip uninstall torch torchvision torchaudio -y

# 清理缓存
pip cache purge

# 安装正确版本的PyTorch（根据CUDA 12.1）
echo "安装正确版本的PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 验证安装
echo "验证PyTorch安装..."
python -c "import torch; print('PyTorch版本:', torch.__version__); print('CUDA可用:', torch.cuda.is_available()); print('CUDA版本:', torch.version.cuda)"

# 安装项目依赖
echo "安装项目依赖..."
pip install -r requirements.txt

echo "修复完成！请运行验证命令：python -c \"import torch; print('PyTorch版本:', torch.__version__); print('CUDA可用:', torch.cuda.is_available())\""