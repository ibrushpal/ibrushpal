#!/bin/bash

# iBrushPal警告修复脚本
echo "=== 修复服务器警告 ==="

# 1. 修复TorchVision版本不兼容
echo "1. 修复TorchVision版本兼容性..."
pip uninstall torchvision -y
pip install torchvision==0.23 --index-url https://download.pytorch.org/whl/cu128

# 2. 修复Ultralytics配置目录权限
echo "2. 修复Ultralytics配置目录..."
mkdir -p ~/.config/Ultralytics
chmod 755 ~/.config/Ultralytics

# 3. 设置环境变量
echo "3. 设置环境变量..."
echo 'export YOLO_CONFIG_DIR="$HOME/.config/Ultralytics"' >> ~/.bashrc
source ~/.bashrc

# 4. 验证修复
echo "4. 验证修复结果..."
pip list | grep torch
echo "Ultralytics配置目录:"
ls -la ~/.config/ | grep Ultralytics || echo "创建Ultralytics目录"

echo "=== 警告修复完成 ==="
echo "现在可以重新启动服务器:"
echo "uvicorn main:app --reload --host 0.0.0.0 --port 8000"