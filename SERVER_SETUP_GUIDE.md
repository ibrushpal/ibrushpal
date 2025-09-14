# iBrushPal HAI服务器环境配置指南

## 第一步：系统基础配置

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装基础工具
sudo apt install -y build-essential git curl wget vim python3-pip python3-venv

# 3. 检查NVIDIA驱动
nvidia-smi
```

## 第二步：CUDA Toolkit安装

```bash
# 1. 检查当前CUDA版本（如果有）
nvcc --version

# 2. 安装CUDA Toolkit（如果需要）
# 对于Ubuntu 22.04，推荐安装CUDA 12.2
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit-12-2

# 3. 配置环境变量
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# 4. 验证CUDA安装
nvcc --version
```

## 第三步：Python环境配置

```bash
# 1. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 2. 检查NVIDIA驱动版本并安装匹配的PyTorch
# 首先检查驱动版本
nvidia-smi

# 根据驱动版本选择PyTorch版本：
# 如果驱动版本 >= 525.60.13 (CUDA 12.x):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 如果驱动版本 < 525.60.13 (CUDA 11.x):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 如果仍有问题，安装CPU版本：
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 3. 验证安装
python -c "import torch; print('PyTorch版本:', torch.__version__); print('CUDA可用:', torch.cuda.is_available())"
```

## 第三步：验证GPU环境

```bash
# 运行验证脚本
python -c "
import torch
print('PyTorch版本:', torch.__version__)
print('CUDA可用:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU设备:', torch.cuda.get_device_name(0))
    print('CUDA版本:', torch.version.cuda)
"
```

## 第四步：安装系统依赖

```bash
# 安装图像处理依赖
sudo apt install -y libgl1-mesa-glx libglib2.0-0

# 安装视频处理依赖
sudo apt install -y ffmpeg libsm6 libxext6
```

## 第五步：项目依赖安装

```bash
# 安装requirements.txt中的依赖
pip install -r requirements.txt

# 如果没有requirements.txt，安装基础依赖
pip install fastapi uvicorn opencv-python pillow numpy pandas scikit-learn
```

## 环境验证完整脚本

创建 `verify_environment.py`：

```python
import torch
import sys
import subprocess

print("=== 环境验证 ===")
print(f"Python版本: {sys.version}")
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU设备: {torch.cuda.get_device_name(0)}")
    print(f"GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # 测试GPU计算
    x = torch.randn(1000, 1000).cuda()
    y = torch.randn(1000, 1000).cuda()
    z = x @ y
    print(f"GPU计算测试: 矩阵乘法完成，结果形状: {z.shape}")
else:
    print("警告: CUDA不可用")

print("=== 环境验证完成 ===")
```

## 常见问题解决

### 1. NVIDIA驱动问题
```bash
# 检查驱动状态
./check_nvidia_driver.sh

# 如果驱动未安装，需要联系云服务商安装驱动
```

### 2. PyTorch CUDA版本不匹配
```bash
# 完全卸载重装
pip uninstall torch torchvision torchaudio -y
pip cache purge

# 重新安装正确版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 3. 依赖冲突
```bash
# 创建全新的虚拟环境
deactivate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
```

## 下一步操作

1. 环境配置完成后，上传您的代码仓库
2. 运行测试：`python main.py` 或 `uvicorn main:app --reload`
3. 访问API文档：http://服务器IP:8000/docs

## 技术支持

如果遇到问题，请检查：
- NVIDIA驱动状态：`nvidia-smi`
- CUDA版本：`nvcc --version`
- PyTorch安装：`python -c "import torch; print(torch.__version__)"`