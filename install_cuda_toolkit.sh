#!/bin/bash

# iBrushPal CUDA Toolkit安装脚本
echo "=== 开始安装CUDA Toolkit ==="

# 1. 检查当前系统信息
echo "1. 检查系统信息..."
echo "Ubuntu版本:"
lsb_release -a
echo "GPU信息:"
lspci | grep -i nvidia

# 2. 检查是否已有CUDA
echo "2. 检查现有CUDA安装..."
if command -v nvcc &> /dev/null; then
    echo "现有CUDA版本:"
    nvcc --version
    echo "是否重新安装？(y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "跳过CUDA安装"
        exit 0
    fi
fi

# 3. 安装CUDA Toolkit 12.2（适用于Ubuntu 22.04）
echo "3. 安装CUDA Toolkit 12.2..."
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit-12-2

# 4. 配置环境变量
echo "4. 配置环境变量..."
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 5. 验证安装
echo "5. 验证CUDA安装..."
nvcc --version
echo "CUDA示例位置: /usr/local/cuda/samples"

# 6. 安装cuDNN（可选但推荐）
echo "6. 安装cuDNN（需要手动下载）..."
echo "请从 NVIDIA官网下载cuDNN: https://developer.nvidia.com/cudnn"
echo "下载后运行: sudo dpkg -i libcudnn8_8.x.x-1+cuda12.0_amd64.deb"

# 7. 编译测试示例
echo "7. 编译测试示例..."
cd /usr/local/cuda/samples/1_Utilities/deviceQuery
sudo make
./deviceQuery

echo "=== CUDA Toolkit安装完成 ==="
echo "请重新登录或运行: source ~/.bashrc"
echo "然后验证: nvcc --version"