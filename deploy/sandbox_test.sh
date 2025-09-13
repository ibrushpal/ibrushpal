#!/bin/bash
# iBrushPal 爱伢伴 AI 沙盒测试环境
# 作者: CodeBuddy
# 日期: 2025-09-13

# 显示彩色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的信息
info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示欢迎信息
echo "=================================================="
echo "    iBrushPal 爱伢伴 AI 系统沙盒测试环境"
echo "=================================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    error "Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 获取当前目录
CURRENT_DIR=$(pwd)
PROJECT_ROOT=$(dirname $(dirname "$0"))
cd $PROJECT_ROOT

info "创建沙盒测试环境..."

# 创建沙盒Docker Compose文件
cat > docker-compose.sandbox.yml << EOL
version: '3.8'

services:
  # 模拟AI服务
  ai-service:
    image: python:3.9-slim
    volumes:
      - ./:/app
    ports:
      - "8000:8000"
    working_dir: /app
    command: >
      bash -c "pip install fastapi uvicorn && 
              uvicorn main:app --host 0.0.0.0 --port 8000"
    networks:
      - ibrushpal-network

  # 模拟数据库
  db:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    networks:
      - ibrushpal-network

  # 模拟前端服务
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./miniprogram:/usr/share/nginx/html
    networks:
      - ibrushpal-network

networks:
  ibrushpal-network:
    driver: bridge

volumes:
  mongo-data:
EOL

# 创建模拟的main.py（如果不存在）
if [ ! -f "main.py" ]; then
    info "创建模拟API服务..."
    cat > main.py << EOL
from fastapi import FastAPI
from typing import Dict

app = FastAPI(
    title="iBrushPal AI API (Sandbox)",
    description="口腔健康AI分析系统API - 沙盒环境",
    version="0.1.0-sandbox"
)

@app.get("/")
async def root():
    return {"message": "iBrushPal AI Service - Sandbox Mode"}

@app.post("/api/v1/detect-teeth")
async def detect_teeth_mock():
    return [
        {
            "type": "incisor",
            "confidence": 0.95,
            "position": {"x": 100, "y": 150},
            "bbox": [80, 130, 120, 170]
        },
        {
            "type": "molar",
            "confidence": 0.87,
            "position": {"x": 200, "y": 160},
            "bbox": [180, 140, 220, 180]
        }
    ]

@app.post("/api/v1/score-cleanliness")
async def score_cleanliness_mock():
    return {
        "overall_score": 78.5,
        "detailed_scores": {
            "incisor": 82.0,
            "molar": 75.0
        },
        "teeth_count": 28
    }

@app.post("/api/v1/generate-recommendation")
async def generate_recommendation_mock(inputs: Dict):
    return {
        "must": ["fluoride_toothpaste", "floss"],
        "suggest": ["mouthwash"],
        "avoid": ["hard_bristle"]
    }
EOL
fi

# 创建模拟的前端页面
mkdir -p miniprogram
if [ ! -f "miniprogram/index.html" ]; then
    info "创建模拟前端页面..."
    cat > miniprogram/index.html << EOL
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iBrushPal 爱伢伴 - 沙盒测试</title>
    <style>
        body {
            font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #0078d4;
            text-align: center;
        }
        .card {
            border: 1px solid #eaeaea;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .btn {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f0f8ff;
            border-radius: 5px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>iBrushPal 爱伢伴 - 沙盒测试环境</h1>
        
        <div class="card">
            <h2>牙齿检测测试</h2>
            <button class="btn" onclick="testDetection()">测试牙齿检测API</button>
            <div id="detection-result" class="result"></div>
        </div>
        
        <div class="card">
            <h2>清洁度评分测试</h2>
            <button class="btn" onclick="testCleanliness()">测试清洁度评分API</button>
            <div id="cleanliness-result" class="result"></div>
        </div>
        
        <div class="card">
            <h2>推荐系统测试</h2>
            <button class="btn" onclick="testRecommendation()">测试推荐系统API</button>
            <div id="recommendation-result" class="result"></div>
        </div>
    </div>

    <script>
        async function testDetection() {
            const resultDiv = document.getElementById('detection-result');
            resultDiv.textContent = '请求中...';
            
            try {
                const response = await fetch('/api/v1/detect-teeth', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.textContent = '请求失败: ' + error.message;
            }
        }
        
        async function testCleanliness() {
            const resultDiv = document.getElementById('cleanliness-result');
            resultDiv.textContent = '请求中...';
            
            try {
                const response = await fetch('/api/v1/score-cleanliness', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.textContent = '请求失败: ' + error.message;
            }
        }
        
        async function testRecommendation() {
            const resultDiv = document.getElementById('recommendation-result');
            resultDiv.textContent = '请求中...';
            
            try {
                const response = await fetch('/api/v1/generate-recommendation', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "cleanliness_score": 78,
                        "coverage_score": 65,
                        "caries_history": true,
                        "gingivitis": false
                    })
                });
                
                const data = await response.json();
                resultDiv.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.textContent = '请求失败: ' + error.message;
            }
        }
    </script>
</body>
</html>
EOL
fi

# 启动沙盒环境
info "启动沙盒测试环境..."
docker-compose -f docker-compose.sandbox.yml up -d

# 检查服务状态
sleep 5
if docker ps | grep -q "ai-service"; then
    info "沙盒环境已成功启动!"
    
    # 获取服务器IP
    if command -v hostname &> /dev/null; then
        SERVER_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
    else
        SERVER_IP="localhost"
    fi
    
    echo ""
    echo "=================================================="
    echo "    iBrushPal 爱伢伴 AI 沙盒环境已启动!"
    echo "=================================================="
    echo ""
    echo "前端页面: http://$SERVER_IP"
    echo "API服务: http://$SERVER_IP:8000"
    echo "API文档: http://$SERVER_IP:8000/docs"
    echo "MongoDB: mongodb://$SERVER_IP:27017"
    echo ""
    echo "测试完成后，可以使用以下命令停止沙盒环境:"
    echo "docker-compose -f docker-compose.sandbox.yml down"
else
    error "沙盒环境启动失败，请检查日志:"
    docker-compose -f docker-compose.sandbox.yml logs
fi

cd $CURRENT_DIR
echo ""
info "沙盒环境设置完成!"