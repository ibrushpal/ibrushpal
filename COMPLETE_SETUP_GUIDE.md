# iBrushPal 完整环境设置指南

## 第一步：服务器基础配置

```bash
# 1. 登录服务器后，首先更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装基础工具
sudo apt install -y build-essential git curl wget vim python3-pip python3-venv

# 3. 检查NVIDIA驱动状态
nvidia-smi
# 如果显示驱动信息，继续下一步
# 如果没有显示，联系云服务商安装NVIDIA驱动
```

## 第二步：Python环境设置

```bash
# 1. 创建项目目录
mkdir -p ~/ibrushpal
cd ~/ibrushpal

# 2. 创建Python虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装基础Python包
pip install --upgrade pip
```

## 第三步：安装PyTorch（关键步骤）

```bash
# 1. 首先检查NVIDIA驱动版本
nvidia-smi | grep "Driver Version"

# 2. 根据驱动版本选择PyTorch版本：
# 如果驱动版本 >= 525.60.13 (支持CUDA 12.x):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 如果驱动版本 < 525.60.13 (支持CUDA 11.x):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. 验证PyTorch安装
python -c "import torch; print('PyTorch版本:', torch.__version__); print('CUDA可用:', torch.cuda.is_available())"
```

## 第四步：安装项目依赖

```bash
# 1. 安装FastAPI和相关依赖
pip install fastapi uvicorn python-multipart

# 2. 安装图像处理依赖
pip install opencv-python pillow

# 3. 安装数据处理依赖
pip install numpy pandas scikit-learn

# 4. 安装其他工具
pip install requests python-dotenv
```

## 第五步：验证GPU环境

创建验证脚本 `verify_gpu.py`：
```python
import torch
import sys

print("=== GPU环境验证 ===")
print(f"Python版本: {sys.version}")
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU设备: {torch.cuda.get_device_name(0)}")
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU内存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    
    # 测试GPU计算
    x = torch.randn(1000, 1000).cuda()
    y = torch.randn(1000, 1000).cuda()
    z = x @ y
    print(f"GPU计算测试成功，结果形状: {z.shape}")
else:
    print("警告: CUDA不可用，将使用CPU模式运行")

print("=== 验证完成 ===")
```

运行验证：
```bash
python verify_gpu.py
```

## 第六步：启动应用程序

```bash
# 1. 确保在虚拟环境中
source .venv/bin/activate

# 2. 启动FastAPI服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 3. 访问API文档
# 浏览器打开: http://服务器IP:8000/docs
```

## 故障排除

### 如果PyTorch安装失败：
```bash
# 完全卸载重装
pip uninstall torch torchvision torchaudio -y
pip cache purge

# 尝试CPU版本（备用方案）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### 如果CUDA不可用：
1. 检查NVIDIA驱动：`nvidia-smi`
2. 检查驱动版本是否与PyTorch版本匹配
3. 如果需要，安装CPU版本的PyTorch

## 常用命令总结

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload

# 启动生产服务器
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# 检查GPU状态
nvidia-smi
```

## 下一步
1. 环境配置完成后，上传您的代码
2. 运行测试确保所有功能正常
3. 配置生产环境部署