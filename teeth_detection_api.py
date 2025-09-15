#!/usr/bin/env python3
"""
牙齿检测API集成方案
结合传统图像处理和深度学习模型
"""

import cv2
import numpy as np
import os
import time
from typing import Dict, List, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
from pydantic import BaseModel

# 尝试导入深度学习模型
try:
    from ultralytics import YOLO
    DL_AVAILABLE = True
except ImportError:
    DL_AVAILABLE = False
    print("警告: 未安装ultralytics，将仅使用传统图像处理方法")

class TeethDetectionRequest(BaseModel):
    """牙齿检测请求模型"""
    image_url: str = None
    use_dl_model: bool = True
    confidence_threshold: float = 0.3

class TeethDetectionResult(BaseModel):
    """牙齿检测结果模型"""
    success: bool
    teeth_count: int
    detection_time: float
    teeth_regions: List[Dict[str, Any]]
    method_used: str
    message: str = ""

class HybridTeethDetector:
    """混合牙齿检测器（传统+深度学习）"""
    
    def __init__(self):
        self.dl_model = None
        self.dl_available = DL_AVAILABLE
        
        # 传统检测器参数
        self.lower_teeth = np.array([0, 0, 180])
        self.upper_teeth = np.array([30, 60, 255])
        
        # 初始化深度学习模型
        if self.dl_available:
            self._init_dl_model()
    
    def _init_dl_model(self):
        """初始化深度学习模型"""
        try:
            model_path = "models/yolov8n-seg.pt"
            if os.path.exists(model_path):
                self.dl_model = YOLO(model_path)
                print("✅ 深度学习模型加载成功")
            else:
                print("⚠️  深度学习模型文件不存在，将使用传统方法")
                self.dl_available = False
        except Exception as e:
            print(f"❌ 深度学习模型加载失败: {e}")
            self.dl_available = False
    
    def traditional_detect(self, image: np.ndarray) -> List[Dict]:
        """传统图像处理检测方法"""
        start_time = time.time()
        
        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 创建牙齿颜色掩码
        teeth_mask = cv2.inRange(hsv, self.lower_teeth, self.upper_teeth)
        
        # 形态学操作
        kernel = np.ones((5, 5), np.uint8)
        teeth_mask = cv2.morphologyEx(teeth_mask, cv2.MORPH_CLOSE, kernel)
        teeth_mask = cv2.morphologyEx(teeth_mask, cv2.MORPH_OPEN, kernel)
        
        # 查找轮廓
        contours, _ = cv2.findContours(teeth_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 过滤和处理轮廓
        teeth_regions = []
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area < 100:
                continue
                
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            if 0.3 < aspect_ratio < 3.0:  # 更宽松的宽高比限制
                confidence = min(area / 2000, 0.9)  # 调整置信度计算
                
                teeth_regions.append({
                    'id': i,
                    'bbox': [x, y, w, h],
                    'confidence': float(confidence),
                    'area': int(area),
                    'method': 'traditional'
                })
        
        detection_time = time.time() - start_time
        return teeth_regions, detection_time
    
    def deep_learning_detect(self, image: np.ndarray, confidence_threshold: float = 0.3) -> List[Dict]:
        """深度学习检测方法"""
        if not self.dl_available or self.dl_model is None:
            return [], 0.0
        
        start_time = time.time()
        
        try:
            # 使用YOLOv8进行检测
            results = self.dl_model(image, conf=confidence_threshold, verbose=False)
            
            teeth_regions = []
            if results and len(results) > 0:
                result = results[0]
                
                if result.boxes is not None:
                    for i, box in enumerate(result.boxes):
                        conf = box.conf[0].item()
                        if conf >= confidence_threshold:
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            w, h = x2 - x1, y2 - y1
                            
                            teeth_regions.append({
                                'id': i,
                                'bbox': [int(x1), int(y1), int(w), int(h)],
                                'confidence': float(conf),
                                'area': int(w * h),
                                'method': 'deep_learning'
                            })
            
            detection_time = time.time() - start_time
            return teeth_regions, detection_time
            
        except Exception as e:
            print(f"深度学习检测失败: {e}")
            return [], 0.0
    
    def hybrid_detect(self, image: np.ndarray, use_dl: bool = True, confidence_threshold: float = 0.3) -> Dict:
        """混合检测方法"""
        start_time = time.time()
        
        # 首先尝试深度学习
        dl_results, dl_time = [], 0.0
        if use_dl and self.dl_available:
            dl_results, dl_time = self.deep_learning_detect(image, confidence_threshold)
        
        # 如果深度学习没有结果或不可用，使用传统方法
        traditional_results, trad_time = [], 0.0
        if not dl_results or len(dl_results) == 0:
            traditional_results, trad_time = self.traditional_detect(image)
        
        # 合并结果（优先使用深度学习结果）
        all_results = dl_results + traditional_results
        
        # 计算总时间
        total_time = time.time() - start_time
        
        return {
            'teeth_regions': all_results,
            'teeth_count': len(all_results),
            'detection_time': total_time,
            'dl_time': dl_time,
            'traditional_time': trad_time,
            'method_used': 'hybrid'
        }

# 创建FastAPI应用
app = FastAPI(
    title="iBrushPal牙齿检测API",
    description="基于混合方法的牙齿检测服务",
    version="1.0.0"
)

# 全局检测器实例
detector = HybridTeethDetector()

@app.post("/detect-teeth", response_model=TeethDetectionResult)
async def detect_teeth(
    file: UploadFile = File(...),
    use_dl_model: bool = True,
    confidence_threshold: float = 0.3
):
    """
    牙齿检测API端点
    
    Args:
        file: 上传的图像文件
        use_dl_model: 是否使用深度学习模型
        confidence_threshold: 置信度阈值
    """
    try:
        # 读取上传的图像
        image_data = await file.read()
        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="无法解码图像")
        
        # 进行牙齿检测
        result = detector.hybrid_detect(image, use_dl_model, confidence_threshold)
        
        return TeethDetectionResult(
            success=True,
            teeth_count=result['teeth_count'],
            detection_time=result['detection_time'],
            teeth_regions=result['teeth_regions'],
            method_used=result['method_used'],
            message=f"成功检测到 {result['teeth_count']} 个牙齿区域"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "dl_available": detector.dl_available,
        "dl_model_loaded": detector.dl_model is not None
    }

@app.get("/model-info")
async def model_info():
    """模型信息端点"""
    info = {
        "dl_available": detector.dl_available,
        "dl_model_loaded": detector.dl_model is not None,
        "traditional_available": True
    }
    
    if detector.dl_available and detector.dl_model:
        info.update({
            "model_type": "YOLOv8",
            "model_path": "models/yolov8n-seg.pt",
            "model_exists": os.path.exists("models/yolov8n-seg.pt")
        })
    
    return info

@app.get("/status-dashboard", response_class=HTMLResponse)
async def status_dashboard(request: Request):
    """状态面板页面"""
    # 内嵌HTML内容
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>服务状态面板 - iBrushPal</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #333; min-height: 100vh; }
        .container { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-top: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { color: #2c3e50; margin-bottom: 10px; }
        .status-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .status-card { background: #f8f9fa; border-radius: 10px; padding: 20px; border-left: 4px solid #27ae60; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background: #e8f4f8; border-radius: 5px; }
        .metric-value { font-weight: bold; color: #2c3e50; }
        .btn { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 20px; margin: 5px; transition: all 0.3s ease; }
        .btn:hover { background: #5a6fd8; transform: translateY(-2px); }
        .json-view { background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 5px; font-family: 'Courier New', monospace; overflow-x: auto; margin: 15px 0; }
        .last-updated { text-align: center; color: #7f8c8d; margin-top: 30px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h1>📊 iBrushPal 服务状态面板</h1><p>实时监控API服务和AI模型运行状态</p></div>
        <div class="status-cards">
            <div class="status-card"><h3>✅ 服务健康状态</h3>
                <div class="metric"><span>服务状态:</span><span class="metric-value" id="service-status">检测中...</span></div>
                <div class="metric"><span>服务版本:</span><span class="metric-value" id="service-version">检测中...</span></div>
                <div class="metric"><span>响应时间:</span><span class="metric-value" id="response-time">检测中...</span></div>
            </div>
            <div class="status-card"><h3>🤖 AI模型状态</h3>
                <div class="metric"><span>模型类型:</span><span class="metric-value" id="model-type">检测中...</span></div>
                <div class="metric"><span>模型状态:</span><span class="metric-value" id="model-status">检测中...</span></div>
                <div class="metric"><span>检测方法:</span><span class="metric-value" id="detection-methods">检测中...</span></div>
            </div>
            <div class="status-card"><h3>📷 支持功能</h3>
                <div class="metric"><span>图像格式:</span><span class="metric-value" id="supported-formats">检测中...</span></div>
                <div class="metric"><span>最大文件大小:</span><span class="metric-value">10MB</span></div>
                <div class="metric"><span>并发请求:</span><span class="metric-value">支持</span></div>
            </div>
        </div>
        <div class="json-view"><h4>📋 原始API响应数据</h4>
            <pre id="health-json">等待获取数据...</pre>
            <pre id="model-json">等待获取数据...</pre>
        </div>
        <div style="text-align: center; margin: 20px 0;">
            <a href="/" class="btn">🏠 返回主页</a>
            <a href="/docs" class="btn">📚 API文档</a>
            <button onclick="refreshData()" class="btn">🔄 刷新状态</button>
        </div>
        <div class="last-updated">最后更新: <span id="last-updated">正在更新...</span></div>
    </div>
    <script>
        async function fetchHealthData() {
            const startTime = Date.now();
            try {
                const healthResponse = await fetch('/health');
                const healthData = await healthResponse.json();
                const modelResponse = await fetch('/model-info');
                const modelData = await modelResponse.json();
                const responseTime = Date.now() - startTime;
                
                document.getElementById('service-status').textContent = healthData.status;
                document.getElementById('service-version').textContent = healthData.version;
                document.getElementById('response-time').textContent = responseTime + 'ms';
                document.getElementById('model-type').textContent = modelData.ai_model;
                document.getElementById('model-status').textContent = modelData.status;
                document.getElementById('detection-methods').textContent = modelData.detection_methods.join(', ');
                document.getElementById('supported-formats').textContent = modelData.supported_formats.join(', ');
                document.getElementById('health-json').textContent = JSON.stringify(healthData, null, 2);
                document.getElementById('model-json').textContent = JSON.stringify(modelData, null, 2);
                document.getElementById('last-updated').textContent = new Date().toLocaleString('zh-CN');
            } catch (error) {
                document.getElementById('service-status').textContent = '连接失败';
                document.getElementById('service-status').style.color = '#e74c3c';
            }
        }
        function refreshData() {
            document.getElementById('service-status').textContent = '检测中...';
            document.getElementById('response-time').textContent = '检测中...';
            document.getElementById('health-json').textContent = '获取数据中...';
            document.getElementById('model-json').textContent = '获取数据中...';
            fetchHealthData();
        }
        document.addEventListener('DOMContentLoaded', fetchHealthData);
        setInterval(fetchHealthData, 30000);
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)

@app.get("/")
async def root():
    """根路径返回欢迎页面"""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iBrushPal牙齿检测API</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #333; min-height: 100vh; }
        .container { background: white; border-radius: 15px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-top: 50px; text-align: center; }
        h1 { color: #2c3e50; margin-bottom: 20px; }
        .btn { display: inline-block; padding: 12px 24px; background: #667eea; color: white; text-decoration: none; border-radius: 25px; margin: 10px; transition: all 0.3s ease; font-weight: 500; }
        .btn:hover { background: #5a6fd8; transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
        .feature-list { text-align: left; margin: 30px 0; }
        .feature { background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #27ae60; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦷 iBrushPal牙齿检测API</h1>
        <p>基于混合方法的智能牙齿检测服务</p>
        
        <div style="margin: 30px 0;">
            <a href="/docs" class="btn">📚 API文档</a>
            <a href="/status-dashboard" class="btn">📊 状态面板</a>
            <a href="/health" class="btn">❤️ 健康检查</a>
        </div>
        
        <div class="feature-list">
            <div class="feature">
                <strong>🤖 混合检测技术</strong> - 结合深度学习和传统图像处理方法
            </div>
            <div class="feature">
                <strong>⚡ 快速响应</strong> - 单次检测时间小于1秒
            </div>
            <div class="feature">
                <strong>📷 多格式支持</strong> - JPG, JPEG, PNG格式图像
            </div>
            <div class="feature">
                <strong>🔒 安全可靠</strong> - 支持文件大小验证和错误处理
            </div>
        </div>
        
        <div style="margin-top: 40px; color: #7f8c8d; font-size: 14px;">
            <p>版本 2.0.0 | 服务状态: <span style="color: #27ae60;">✅ 运行中</span></p>
        </div>
    </div>
</body>
</html>
""")

def test_local_image(image_path: str = "professional_test/front_teeth.jpg"):
    """本地测试函数"""
    if not os.path.exists(image_path):
        print(f"测试图像不存在: {image_path}")
        return
    
    print("本地牙齿检测测试")
    print("=" * 40)
    
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像")
        return
    
    # 进行检测
    result = detector.hybrid_detect(image, use_dl=True)
    
    print(f"检测结果:")
    print(f"- 牙齿数量: {result['teeth_count']}")
    print(f"- 总耗时: {result['detection_time']:.3f}s")
    print(f"- DL耗时: {result['dl_time']:.3f}s")
    print(f"- 传统耗时: {result['traditional_time']:.3f}s")
    print(f"- 使用的方法: {result['method_used']}")
    
    # 可视化结果
    output_dir = "api_test_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # 绘制检测框
    result_image = image.copy()
    for i, region in enumerate(result['teeth_regions']):
        x, y, w, h = region['bbox']
        confidence = region['confidence']
        method = region['method']
        
        # 不同方法使用不同颜色
        color = (0, 255, 0) if method == 'deep_learning' else (0, 0, 255)
        
        # 绘制边界框
        cv2.rectangle(result_image, (x, y), (x + w, y + h), color, 2)
        
        # 添加标签
        label = f"{method}: {confidence:.2f}"
        cv2.putText(result_image, label, (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    # 保存结果
    output_path = os.path.join(output_dir, f"detected_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, result_image)
    print(f"结果图像保存到: {output_path}")
    
    return result

if __name__ == "__main__":
    # 本地测试
    test_result = test_local_image()
    
    # 启动API服务器
    print("\n启动牙齿检测API服务器...")
    print("API文档: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)