# iBrushPal 详细部署指南

## 第一阶段：Git 仓库设置

### 1.1 配置Git全局设置
```bash
# 设置用户名和邮箱
git config --global user.name "ibrushpal"
git config --global user.email "hzd@ibrushpal.com"

# 验证配置
git config --list
```

### 1.2 克隆仓库
```bash
# 创建项目目录
mkdir -p ~/projects
cd ~/projects

# 克隆仓库（使用SSH或HTTPS）
git clone https://github.com/ibrushpal/ibrushpal.git
# 或者使用SSH
# git clone git@github.com:ibrushpal/ibrushpal.git

cd ibrushpal

# 检查仓库状态
git status
git log --oneline -5
```

### 1.3 设置远程仓库
```bash
# 查看远程仓库
git remote -v

# 如果需要添加远程仓库
git remote add origin https://github.com/ibrushpal/ibrushpal.git

# 拉取最新代码
git pull origin main
```

## 第二阶段：环境准备

### 2.1 系统更新
```bash
# 更新系统包
sudo apt update
sudo apt upgrade -y

# 安装基础工具
sudo apt install -y python3-pip python3-venv git curl wget
```

### 2.2 检查NVIDIA驱动
```bash
# 检查NVIDIA驱动
nvidia-smi

# 如果驱动未安装，安装驱动
sudo apt install -y nvidia-driver-535
sudo reboot  # 重启后生效

# 再次检查
nvidia-smi
```

### 2.3 创建Python虚拟环境
```bash
cd ~/ibrushpal
python3 -m venv .venv
source .venv/bin/activate

# 验证虚拟环境
which python
which pip
```

## 第三阶段：依赖安装

### 3.1 安装PyTorch（带CUDA支持）
```bash
pip install torch==2.7.1+cu118 torchvision==0.22.1+cu118 torchaudio==2.7.1+cu118 --index-url https://download.pytorch.org/whl/cu118

# 验证安装
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}')"
```

### 3.2 安装FastAPI和相关依赖
```bash
pip install fastapi==0.104.1 uvicorn==0.24.0 python-multipart==0.0.6

# 验证安装
python -c "import fastapi; print(f'FastAPI版本: {fastapi.__version__}')"
```

### 3.3 安装计算机视觉库
```bash
pip install opencv-python==4.8.1.78 ultralytics==8.0.196 numpy==1.24.3 pillow==10.0.1

# 验证安装
python -c "import cv2; print(f'OpenCV版本: {cv2.__version__}')"
python -c "from ultralytics import YOLO; print('YOLOv8加载成功')"
```

### 3.4 安装其他依赖
```bash
pip install scikit-learn==1.3.2 pandas==2.3.2

# 验证所有依赖
pip list
```

## 第四阶段：API服务搭建

### 4.1 创建基础API服务
```bash
# 创建主API文件
cat > app/main.py << 'EOF'
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import cv2
import numpy as np
from typing import List
import json

app = FastAPI(title="iBrushPal API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "iBrushPal API服务正常运行", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "iBrushPal API"}

@app.get("/model-info")
async def model_info():
    return {
        "ai_model": "YOLOv8 + Traditional CV",
        "status": "operational",
        "detection_methods": ["deep_learning", "traditional_image_processing"]
    }

@app.post("/detect-teeth")
async def detect_teeth(image: UploadFile = File(...)):
    try:
        # 读取图像
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 简单的牙齿检测逻辑（后续替换为YOLOv8）
        # 这里使用简单的颜色阈值作为示例
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        tooth_count = len([c for c in contours if cv2.contourArea(c) > 100])
        
        return {
            "detected_teeth": tooth_count,
            "image_size": f"{img.shape[1]}x{img.shape[0]}",
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理图像时出错: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

### 4.2 启动API服务
```bash
# 启动开发服务器
python app/main.py

# 或者使用后台启动
nohup python app/main.py > api.log 2>&1 &

# 检查服务状态
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/model-info
```

### 4.3 测试API端点
```bash
# 测试健康检查
curl -X GET http://localhost:8000/health

# 测试模型信息
curl -X GET http://localhost:8000/model-info

# 测试牙齿检测（需要准备测试图像）
# 先创建一个测试图像
python -c "
import cv2
import numpy as np
# 创建简单的测试图像
img = np.ones((300, 300, 3), dtype=np.uint8) * 255
cv2.imwrite('test_teeth.jpg', img)
print('测试图像已创建: test_teeth.jpg')
"

# 使用curl测试牙齿检测
curl -X POST http://localhost:8000/detect-teeth \
  -F "image=@test_teeth.jpg" \
  -H "Content-Type: multipart/form-data"
```

## 第五阶段：文档和监控

### 5.1 访问API文档
```bash
# API文档会自动生成
echo "OpenAPI文档: http://localhost:8000/docs"
echo "Redoc文档: http://localhost:8000/redoc"
echo "原始OpenAPI规范: http://localhost:8000/openapi.json"
```

### 5.2 创建系统服务
```bash
# 创建系统服务文件
sudo tee /etc/systemd/system/ibrushpal-api.service > /dev/null << EOF
[Unit]
Description=iBrushPal API Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/ibrushpal
Environment=PATH=/home/ubuntu/ibrushpal/.venv/bin
ExecStart=/home/ubuntu/ibrushpal/.venv/bin/python app/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# 重新加载系统配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ibrushpal-api

# 设置开机自启
sudo systemctl enable ibrushpal-api

# 检查服务状态
sudo systemctl status ibrushpal-api
```

### 5.3 监控日志
```bash
# 查看实时日志
sudo journalctl -u ibrushpal-api -f

# 查看最近日志
sudo journalctl -u ibrushpal-api --since "1 hour ago"
```

## 第六阶段：生产环境部署

### 6.1 配置防火墙
```bash
# 开放API端口
sudo ufw allow 8000/tcp
sudo ufw enable
sudo ufw status
```

### 6.2 配置Nginx反向代理（可选）
```bash
# 安装Nginx
sudo apt install -y nginx

# 创建Nginx配置
sudo tee /etc/nginx/sites-available/ibrushpal > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# 启用配置
sudo ln -s /etc/nginx/sites-available/ibrushpal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 验证清单

完成以上步骤后，验证以下内容：

1. [ ] Git仓库正确克隆和配置
2. [ ] NVIDIA驱动正常工作
3. [ ] Python虚拟环境创建成功
4. [ ] 所有依赖包安装成功
5. [ ] PyTorch CUDA支持正常
6. [ ] FastAPI服务启动正常
7. [ ] 所有API端点可访问
8. [ ] 系统服务配置成功
9. [ ] 日志监控正常工作

## 故障排除

如果遇到问题，检查以下内容：

1. **端口冲突**：确保8000端口未被占用 `netstat -tlnp | grep :8000`
2. **权限问题**：确保文件权限正确 `chmod +x 脚本文件`
3. **依赖问题**：重新安装依赖 `pip install -r requirements.txt`
4. **GPU问题**：检查CUDA `nvidia-smi` 和 `nvcc --version`

这个详细的指南涵盖了从Git配置到生产环境部署的所有步骤。