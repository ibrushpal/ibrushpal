#!/bin/bash
echo "=== 安装所有iBrushPal依赖包 ==="
echo "开始时间: $(date)"

# 激活虚拟环境（如果存在）
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "已激活虚拟环境"
fi

# 安装所有依赖包
echo -e "\n1. 安装PyTorch和相关包..."
pip install torch==2.7.1+cu118 torchvision==0.22.1+cu118 torchaudio==2.7.1+cu118 --index-url https://download.pytorch.org/whl/cu118

echo -e "\n2. 安装FastAPI和相关web包..."
pip install fastapi==0.104.1 uvicorn==0.24.0 python-multipart==0.0.6

echo -e "\n3. 安装计算机视觉包..."
pip install opencv-python==4.8.1.78 ultralytics==8.0.196

echo -e "\n4. 安装数据处理包..."
pip install numpy==1.24.3 pillow==10.0.1 scikit-learn==1.3.2 pandas==2.3.2

echo -e "\n5. 验证安装..."
python -c "
import torch
print(f'PyTorch版本: {torch.__version__}')
print(f'CUDA可用: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU设备: {torch.cuda.get_device_name(0)}')
"

echo -e "\n6. 检查所有包..."
pip list | grep -E '(torch|fastapi|uvicorn|opencv|ultralytics|numpy|pillow|sklearn|pandas)'

echo -e "\n=== 安装完成 ==="
echo "完成时间: $(date)"
echo "运行 'python verify_dependencies.py' 验证所有依赖"