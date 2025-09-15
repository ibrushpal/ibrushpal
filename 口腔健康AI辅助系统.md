# 口腔健康AI辅助系统

## Core Features

- 多模态数据采集

- 牙齿区域检测

- 清洁度自动评分

- 个性化方案生成

- 后台管理功能

## Tech Stack

{
  "Backend": {
    "language": "Python",
    "framework": "FastAPI",
    "cv": "PyTorch",
    "cloud": "Tencent CloudBase"
  },
  "Web": {
    "arch": "react",
    "component": "tdesign"
  },
  "MiniProgram": {
    "framework": "WePY",
    "component": "tdesign"
  }
}

## Design

Glassmorphism风格牙科专业UI

## Plan

Note: 

- [ ] is holding
- [/] is doing
- [X] is done

---

[X] 开发媒体文件上传预处理模块

[X] 实现牙齿检测与分割模型API

[X] 构建清洁度评分算法模块

[X] 开发个性化推荐规则引擎

[X] 实现小程序数据采集界面

[X] 构建分析结果可视化组件

[X] 部署云端推理服务

[X] 实现后台管理功能

89B1-21AC
Ubuntu 20.04.6

  docker pull nvidia/cuda:12.2.0-base-ubuntu22.04
ubuntu@VM-0-16-ubuntu:~$ nvidia-smi
Sun Sep 14 15:10:30 2025       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.261.03             Driver Version: 535.261.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       Off | 00000000:00:08.0 Off |                    0 |
| N/A   31C    P8               9W /  70W |      2MiB / 15360MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
ubuntu@VM-0-16-ubuntu:~$ nvidia-smi
Sun Sep 14 15:11:08 2025       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.261.03             Driver Version: 535.261.03   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       Off | 00000000:00:08.0 Off |                    0 |
| N/A   31C    P8               9W /  70W |      2MiB / 15360MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
ubuntu@VM-0-16-ubuntu:~$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Fri_Jan__6_16:45:21_PST_2023
Cuda compilation tools, release 12.0, V12.0.140
Build cuda_12.0.r12.0/compiler.32267302_0

ssh bitnami@server_ip_address -p

ubuntu@VM-0-16-ubuntu:~/ibrushpal$ python3 testpyt.py
=== 安装验证 ===
PyTorch版本: 2.8.0+cu128
CUDA可用: True
GPU设备: Tesla T4
CUDA版本: 12.8
echo "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
python test_api_docs.py http://42.194.142.158:8000
Python版本:3.10.12 (main, Aug 15 202
PyTorch版本:2.8.0+cu128
CUDA可用:True
CUDA版本:12.8
GPU设备数量:1
GPU 0: Tesla T4
内存:14.6 GB
PyTorch 2.8.0+cu128-GPU加速支持
FastAPI 0.116.1-高性能API框架
OpenCV 4.12.0-图像处理能力
Tesla T4 GPU-计算资源就绪
CUDA 12.8-深度学习环境完整
torch 2.8.0
torchaudio 2.5.1+cu121
torchvision 0.23.0+cu128
