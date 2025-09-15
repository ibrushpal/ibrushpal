#!/usr/bin/env python3
"""
牙齿检测API欢迎页面
为http://42.194.142.158:8000 提供友好的用户界面
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(
    title="iBrushPal牙齿检测API",
    description="基于AI的智能牙齿检测服务",
    version="2.0.0"
)

# 创建静态文件目录
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 设置模板目录
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """API欢迎页面"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "iBrushPal牙齿检测API",
            "api_docs_url": "/docs",
            "health_check_url": "/health",
            "model_info_url": "/model-info"
        }
    )

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "iBrushPal Teeth Detection API",
        "version": "2.0.0",
        "docs": "/docs"
    }

@app.get("/model-info")
async def model_info():
    """模型信息端点"""
    return {
        "ai_model": "YOLOv8 + Traditional CV",
        "status": "operational",
        "detection_methods": ["deep_learning", "traditional_image_processing"],
        "supported_formats": ["jpg", "jpeg", "png"]
    }

# 创建HTML模板
html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-top: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .header p {
            color: #7f8c8d;
            font-size: 18px;
        }
        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
        }
        .endpoints {
            margin-top: 30px;
        }
        .endpoint {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #3498db;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            margin: 10px 5px;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: #5a6fd8;
            transform: translateY(-2px);
        }
        .btn-docs {
            background: #27ae60;
        }
        .btn-docs:hover {
            background: #219653;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            background: #27ae60;
            color: white;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🦷 iBrushPal牙齿检测API</h1>
            <p>基于AI技术的智能牙齿健康分析服务</p>
        </div>

        <div class="card">
            <h2>✨ 服务介绍</h2>
            <p>本API提供基于深度学习和传统图像处理的牙齿检测服务，支持牙齿区域识别、健康状态分析等功能。</p>
        </div>

        <div class="card">
            <h2>✅ 服务状态 <span class="status-badge">运行中</span></h2>
            <p>API服务正常运行，深度学习模型已加载完成。</p>
        </div>

        <div class="endpoints">
            <h2>🔗 API端点</h2>
            
            <div class="endpoint">
                <h3>📊 交互式文档</h3>
                <p>查看完整的API文档和测试界面</p>
                <a href="{{ api_docs_url }}" class="btn btn-docs">查看API文档</a>
            </div>

            <div class="endpoint">
                <h3>❤️ 健康检查</h3>
                <p>检查服务运行状态和模型加载情况</p>
                <a href="{{ health_check_url }}" class="btn">健康状态</a>
            </div>

            <div class="endpoint">
                <h3>🤖 模型信息</h3>
                <p>查看AI模型详情和技术规格</p>
                <a href="{{ model_info_url }}" class="btn">模型信息</a>
            </div>
        </div>

        <div class="card">
            <h2>🚀 快速开始</h2>
            <p>使用以下代码测试牙齿检测功能：</p>
            <pre style="background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px;">
import requests

url = "http://42.194.142.158:8000/detect-teeth"
files = {"file": open("teeth_image.jpg", "rb")}
response = requests.post(url, files=files)

print(response.json())
</pre>
        </div>

        <div class="card">
            <h2>📞 技术支持</h2>
            <p>如有技术问题或合作需求，请联系：</p>
            <p>📧 邮箱: support@ibrushpal.com</p>
            <p>🌐 官网: https://ibrushpal.com</p>
        </div>
    </div>
</body>
</html>
"""

# 创建模板目录和文件
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

if __name__ == "__main__":
    import uvicorn
    print("启动iBrushPal API欢迎页面服务...")
    print("访问: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)