#!/usr/bin/env python3
"""
YOLOv8 牙齿检测模型训练脚本
用于训练和微调牙齿检测模型
"""

import os
import yaml
from ultralytics import YOLO
import torch
from datetime import datetime

def setup_training_environment():
    """设置训练环境"""
    print("=== 设置牙齿检测训练环境 ===")
    
    # 创建目录结构
    os.makedirs("teeth_detection/data", exist_ok=True)
    os.makedirs("teeth_detection/models", exist_ok=True)
    os.makedirs("teeth_detection/runs", exist_ok=True)
    os.makedirs("teeth_detection/datasets", exist_ok=True)
    
    print("✅ 目录结构创建完成")

def create_dataset_config():
    """创建数据集配置文件"""
    dataset_config = {
        'path': './teeth_detection/datasets/teeth',
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': {
            0: 'tooth'
        }
    }
    
    with open('teeth_detection/data/teeth.yaml', 'w') as f:
        yaml.dump(dataset_config, f)
    
    print("✅ 数据集配置文件创建完成")

def prepare_training_config():
    """准备训练配置"""
    config = {
        'model': 'yolov8n-seg.pt',  # 使用分割模型
        'data': 'teeth_detection/data/teeth.yaml',
        'epochs': 100,
        'imgsz': 640,
        'batch': 16,
        'workers': 4,
        'device': '0' if torch.cuda.is_available() else 'cpu',
        'project': 'teeth_detection/runs',
        'name': f'train_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'optimizer': 'auto',
        'lr0': 0.01,
        'lrf': 0.01,
        'momentum': 0.937,
        'weight_decay': 0.0005,
        'warmup_epochs': 3.0,
        'warmup_momentum': 0.8,
        'box': 7.5,
        'cls': 0.5,
        'dfl': 1.5,
        'fl_gamma': 0.0,
    }
    
    return config

def train_model():
    """训练牙齿检测模型"""
    print("=== 开始训练牙齿检测模型 ===")
    
    # 检查GPU可用性
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用设备: {device}")
    if device == "cuda":
        print(f"GPU型号: {torch.cuda.get_device_name(0)}")
        print(f"CUDA版本: {torch.version.cuda}")
    
    # 加载模型
    print("加载YOLOv8模型...")
    model = YOLO('yolov8n-seg.pt')
    
    # 训练配置
    config = prepare_training_config()
    
    # 开始训练
    print("开始模型训练...")
    results = model.train(
        data=config['data'],
        epochs=config['epochs'],
        imgsz=config['imgsz'],
        batch=config['batch'],
        workers=config['workers'],
        device=config['device'],
        project=config['project'],
        name=config['name'],
        optimizer=config['optimizer'],
        lr0=config['lr0'],
        lrf=config['lrf'],
        momentum=config['momentum'],
        weight_decay=config['weight_decay'],
        warmup_epochs=config['warmup_epochs'],
        warmup_momentum=config['warmup_momentum'],
        box=config['box'],
        cls=config['cls'],
        dfl=config['dfl'],
        fl_gamma=config['fl_gamma']
    )
    
    print("✅ 模型训练完成")
    return results

def main():
    """主函数"""
    try:
        setup_training_environment()
        create_dataset_config()
        results = train_model()
        
        print("\n=== 训练结果 ===")
        print(f"最佳模型保存位置: {results.save_dir}")
        print(f"训练耗时: {results.training_time}")
        print(f"最终mAP: {results.results.get('metrics/mAP50-95(B)', 'N/A')}")
        
    except Exception as e:
        print(f"❌ 训练过程中出错: {str(e)}")
        raise

if __name__ == "__main__":
    main()