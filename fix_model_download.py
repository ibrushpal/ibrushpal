#!/usr/bin/env python3
"""
YOLOv8模型下载优化脚本
解决github下载慢的问题
"""

import os
import requests
from pathlib import Path
import urllib.request
import sys

# 模型下载配置
MODEL_URLS = {
    "yolov8n-seg.pt": [
        "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",  # 官方源
        "https://mirror.ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",  # 国内镜像1
        "https://pd.zwc365.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",  # 国内镜像2
    ]
}

MODEL_DIR = Path("models/weights")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def download_with_mirrors(model_name, target_path):
    """使用多个镜像源下载模型"""
    print(f"开始下载 {model_name}...")
    
    for i, url in enumerate(MODEL_URLS[model_name]):
        try:
            print(f"尝试镜像 {i+1}: {url}")
            
            # 使用urllib下载
            urllib.request.urlretrieve(url, target_path)
            
            # 检查文件是否完整下载
            if target_path.exists() and target_path.stat().st_size > 0:
                print(f"✅ 下载成功: {model_name}")
                return True
                
        except Exception as e:
            print(f"❌ 镜像 {i+1} 失败: {e}")
            continue
    
    return False

def main():
    print("=== YOLOv8模型下载优化 ===")
    
    model_name = "yolov8n-seg.pt"
    target_path = MODEL_DIR / model_name
    
    # 检查是否已存在
    if target_path.exists():
        print(f"✅ 模型已存在: {target_path}")
        return True
    
    # 尝试下载
    success = download_with_mirrors(model_name, target_path)
    
    if success:
        print(f"🎉 模型下载完成: {target_path}")
        print(f"文件大小: {target_path.stat().st_size / 1024/1024:.1f} MB")
    else:
        print("❌ 所有镜像下载失败")
        print("请手动下载并放置到 models/weights/ 目录")
        print("下载地址: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt")
    
    return success

if __name__ == "__main__":
    main()