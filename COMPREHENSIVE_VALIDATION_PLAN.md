# iBrushPal 全面验证计划

## 第一阶段：基础环境验证

### 1.1 系统环境检查
```bash
# 检查系统信息
uname -a
lsb_release -a

# 检查NVIDIA驱动
nvidia-smi
nvidia-smi --query-gpu=driver_version,name,memory.total --format=csv

# 检查CUDA版本
nvcc --version
```

### 1.2 Python环境验证
```bash
# 检查Python版本
python3 --version
pip3 --version

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 验证虚拟环境
which python
which pip
```

## 第二阶段：依赖安装验证

### 2.1 基础依赖安装
```bash
# 安装基础包
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 验证PyTorch
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'GPU设备: {torch.cuda.get_device_name(0)}')"
```

### 2.2 项目依赖安装
```bash
# 逐个安装requirements.txt中的包
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install opencv-python==4.8.1.78
pip install ultralytics==8.0.196
pip install numpy==1.24.3
pip install pillow==10.0.1
pip install scikit-learn==1.3.2

# 验证所有包安装成功
pip list
```

## 第三阶段：API服务验证

### 3.1 启动基础API测试
```bash
# 创建最简单的测试API
python -c "
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'API服务正常运行'}

import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000)
"
```

### 3.2 验证API端点
```bash
# 测试基础端点
curl http://localhost:8000/

# 测试文档页面
curl http://localhost:8000/docs

# 测试OpenAPI文档
curl http://localhost:8000/openapi.json
```

## 第四阶段：模型功能验证

### 4.1 牙齿检测模型验证
```bash
# 下载YOLOv8模型
python download_yolov8.py

# 测试牙齿检测
python test_yolov8_model.py

# 测试真实牙齿图像
python test_real_teeth_images.py
```

### 4.2 完整API服务验证
```bash
# 启动完整API服务
python teeth_detection_api.py

# 测试所有API端点
python test_api_docs.py
python test_status_dashboard.py
```

## 验证检查清单

- [ ] NVIDIA驱动正常工作
- [ ] CUDA版本正确
- [ ] Python虚拟环境创建成功
- [ ] PyTorch GPU支持正常
- [ ] 所有依赖包安装成功
- [ ] 基础API服务启动正常
- [ ] 文档页面可访问
- [ ] 牙齿检测模型下载成功
- [ ] 牙齿检测功能正常
- [ ] 完整API服务运行正常

## 问题排查指南

1. **NVIDIA驱动问题**: 运行 `check_nvidia_driver.py`
2. **PyTorch CUDA问题**: 运行 `fix_pytorch_cuda.sh`
3. **依赖安装问题**: 检查 `requirements.txt` 版本
4. **API启动问题**: 检查端口占用和防火墙设置
5. **模型下载问题**: 使用 `download_yolov8.py` 脚本

这个计划将确保我们从零开始，逐步验证每个组件，避免之前出现的混乱情况。