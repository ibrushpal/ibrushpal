#!/bin/bash

# NVIDIA驱动检查脚本
echo "=== NVIDIA驱动检查 ==="

# 检查nvidia-smi
if command -v nvidia-smi &> /dev/null; then
    echo "✓ nvidia-smi 命令可用"
    nvidia-smi
else
    echo "✗ nvidia-smi 命令不可用"
fi

# 检查驱动模块
echo -e "\n=== 驱动模块检查 ==="
if lsmod | grep -q nvidia; then
    echo "✓ NVIDIA驱动模块已加载"
    lsmod | grep nvidia
else
    echo "✗ NVIDIA驱动模块未加载"
fi

# 检查设备
echo -e "\n=== GPU设备检查 ==="
if lspci | grep -i nvidia; then
    echo "✓ 检测到NVIDIA GPU设备"
else
    echo "✗ 未检测到NVIDIA GPU设备"
fi

# 检查CUDA
echo -e "\n=== CUDA检查 ==="
if command -v nvcc &> /dev/null; then
    echo "✓ nvcc 命令可用"
    nvcc --version
else
    echo "✗ nvcc 命令不可用"
fi

echo -e "\n=== 检查完成 ==="