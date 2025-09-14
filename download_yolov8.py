#!/usr/bin/env python3
"""
YOLOv8模型下载脚本 - 解决GitHub下载慢的问题
"""

import os
import sys
from pathlib import Path
import urllib.request
import time

# 模型下载配置
MODEL_URLS = [
    # 国内镜像源（优先使用）
    "https://mirror.ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",
    "https://pd.zwc365.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",
    "https://ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt",
    
    # 官方源（备用）
    "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt"
]

MODEL_DIR = Path("models/weights")
MODEL_PATH = MODEL_DIR / "yolov8n-seg.pt"

def download_model():
    """下载YOLOv8模型文件"""
    print("🚀 开始下载 YOLOv8n-seg 模型...")
    print(f"目标路径: {MODEL_PATH}")
    
    # 创建目录
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    
    # 检查是否已存在
    if MODEL_PATH.exists():
        file_size = MODEL_PATH.stat().st_size / (1024 * 1024)
        print(f"✅ 模型已存在: {file_size:.1f} MB")
        return True
    
    # 尝试各个镜像源
    for i, url in enumerate(MODEL_URLS):
        try:
            print(f"\n🔗 尝试镜像 {i+1}/{len(MODEL_URLS)}: {url}")
            
            # 显示下载进度
            def progress_callback(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = (downloaded / total_size) * 100
                mb_downloaded = downloaded / (1024 * 1024)
                mb_total = total_size / (1024 * 1024)
                sys.stdout.write(f"\r📥 下载进度: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)")
                sys.stdout.flush()
            
            # 开始下载
            start_time = time.time()
            urllib.request.urlretrieve(url, MODEL_PATH, progress_callback)
            
            # 下载完成
            download_time = time.time() - start_time
            file_size = MODEL_PATH.stat().st_size / (1024 * 1024)
            speed = file_size / download_time
            
            print(f"\n✅ 下载成功!")
            print(f"📊 文件大小: {file_size:.1f} MB")
            print(f"⏱️ 下载时间: {download_time:.1f} 秒")
            print(f"🚀 下载速度: {speed:.1f} MB/s")
            
            return True
            
        except Exception as e:
            print(f"\n❌ 下载失败: {e}")
            # 删除可能下载失败的文件
            if MODEL_PATH.exists():
                MODEL_PATH.unlink()
            continue
    
    print("\n❌ 所有镜像源都下载失败")
    return False

def main():
    print("=" * 60)
    print("🤖 YOLOv8 模型下载工具")
    print("=" * 60)
    
    # 检查网络连接
    try:
        urllib.request.urlopen("http://www.baidu.com", timeout=5)
    except:
        print("❌ 网络连接失败，请检查网络")
        return False
    
    # 开始下载
    success = download_model()
    
    if success:
        print("\n🎉 模型下载完成！")
        print("现在可以正常运行 iBrushPal 程序了")
    else:
        print("\n💡 手动下载建议:")
        print("1. 浏览器访问: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt")
        print("2. 下载后保存到: models/weights/yolov8n-seg.pt")
        print("3. 重新运行程序")
    
    return success

if __name__ == "__main__":
    main()