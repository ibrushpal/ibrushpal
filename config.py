"""
iBrushPal配置文件 - 模型下载优化版
"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 数据目录
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# 模型目录
MODEL_DIR = BASE_DIR / "models" / "weights"
TOOTH_DETECTION_MODEL = MODEL_DIR / "yolov8n-seg.pt"  # 使用预训练模型
CLEANLINESS_MODEL = MODEL_DIR / "cleanliness_scorer.pt"
RECOMMENDATION_MODEL = MODEL_DIR / "recommendation_model.pkl"

# 创建必要的目录
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# API配置
API_HOST = "0.0.0.0"
API_PORT = 8000
API_WORKERS = 4

# 安全配置
ALLOWED_ORIGINS = ["*"]

# 模型参数
TOOTH_DETECTION_CONF = 0.25
IMAGE_SIZE = 640
VIDEO_FPS = 1

# 模型下载配置
MODEL_DOWNLOAD_URLS = {
    "yolov8n-seg.pt": [
        "https://mirror.ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",
        "https://pd.zwc365.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",
    ]
}

# 检查模型是否存在
def check_models():
    """检查模型文件是否存在"""
    models_status = {}
    for model_name, model_path in [
        ("tooth_detection", TOOTH_DETECTION_MODEL),
        ("cleanliness", CLEANLINESS_MODEL),
        ("recommendation", RECOMMENDATION_MODEL)
    ]:
        models_status[model_name] = model_path.exists()
    
    return models_status