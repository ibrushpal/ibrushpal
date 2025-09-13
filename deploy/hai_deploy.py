#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
iBrushPal 爱伢伴 - 腾讯云HAI部署脚本
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

# 彩色输出
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_color(text, color):
    """打印彩色文本"""
    print(f"{color}{text}{Colors.ENDC}")

def check_prerequisites():
    """检查部署前提条件"""
    print_color("检查部署前提条件...", Colors.HEADER)
    
    # 检查腾讯云CLI
    try:
        subprocess.run(["tccli", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print_color("✓ 腾讯云CLI已安装", Colors.GREEN)
    except (subprocess.SubprocessError, FileNotFoundError):
        print_color("✗ 腾讯云CLI未安装，请先安装并配置：", Colors.FAIL)
        print("   pip install tccli")
        print("   tccli configure")
        return False
    
    # 检查Docker
    try:
        subprocess.run(["docker", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print_color("✓ Docker已安装", Colors.GREEN)
    except (subprocess.SubprocessError, FileNotFoundError):
        print_color("✗ Docker未安装，请先安装Docker", Colors.FAIL)
        return False
    
    # 检查项目文件
    required_files = ["main.py", "requirements.txt"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print_color(f"✗ 缺少必要文件: {', '.join(missing_files)}", Colors.FAIL)
        return False
    else:
        print_color("✓ 项目文件检查通过", Colors.GREEN)
    
    return True

def create_dockerfile():
    """创建Dockerfile"""
    print_color("创建Dockerfile...", Colors.HEADER)
    
    dockerfile_content = """FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \\
    libgl1-mesa-glx libglib2.0-0 \\
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print_color("✓ Dockerfile创建成功", Colors.GREEN)

def create_hai_config(app_name, region="ap-guangzhou"):
    """创建HAI配置文件"""
    print_color("创建HAI配置文件...", Colors.HEADER)
    
    hai_config = {
        "appName": app_name,
        "region": region,
        "containerConfig": {
            "image": f"{app_name}:latest",
            "port": 8000,
            "envVars": {
                "PYTHONUNBUFFERED": "1"
            },
            "resources": {
                "cpu": 1,
                "memory": "2Gi",
                "gpu": {
                    "count": 1,
                    "type": "T4"
                }
            }
        },
        "scaling": {
            "minReplicas": 1,
            "maxReplicas": 5
        },
        "networking": {
            "ingress": {
                "enabled": True,
                "authEnabled": False
            }
        }
    }
    
    with open("hai-config.json", "w") as f:
        json.dump(hai_config, f, indent=2)
    
    print_color("✓ HAI配置文件创建成功", Colors.GREEN)

def build_and_push_image(app_name, registry):
    """构建并推送Docker镜像"""
    print_color("构建Docker镜像...", Colors.HEADER)
    
    image_name = f"{registry}/{app_name}:latest"
    
    # 构建镜像
    build_cmd = ["docker", "build", "-t", image_name, "."]
    result = subprocess.run(build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print_color("✗ 镜像构建失败", Colors.FAIL)
        print(result.stderr.decode())
        return False
    
    print_color("✓ 镜像构建成功", Colors.GREEN)
    
    # 登录腾讯云容器镜像服务
    print_color("登录腾讯云容器镜像服务...", Colors.HEADER)
    login_cmd = ["tccli", "tcr", "login", "--registry", registry]
    result = subprocess.run(login_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print_color("✗ 登录失败", Colors.FAIL)
        print(result.stderr.decode())
        return False
    
    # 推送镜像
    print_color("推送镜像到腾讯云...", Colors.HEADER)
    push_cmd = ["docker", "push", image_name]
    result = subprocess.run(push_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print_color("✗ 镜像推送失败", Colors.FAIL)
        print(result.stderr.decode())
        return False
    
    print_color("✓ 镜像推送成功", Colors.GREEN)
    return True

def deploy_to_hai():
    """部署到HAI平台"""
    print_color("部署到HAI平台...", Colors.HEADER)
    
    deploy_cmd = ["tccli", "hai", "deploy", "--config", "hai-config.json"]
    result = subprocess.run(deploy_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print_color("✗ 部署失败", Colors.FAIL)
        print(result.stderr.decode())
        return False
    
    print_color("✓ 部署成功", Colors.GREEN)
    return True

def get_deployment_info(app_name, region="ap-guangzhou"):
    """获取部署信息"""
    print_color("获取部署信息...", Colors.HEADER)
    
    info_cmd = ["tccli", "hai", "describe-app", "--app-name", app_name, "--region", region]
    result = subprocess.run(info_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print_color("✗ 获取部署信息失败", Colors.FAIL)
        print(result.stderr.decode())
        return
    
    try:
        app_info = json.loads(result.stdout.decode())
        url = app_info.get("url", "未获取到URL")
        status = app_info.get("status", "未知状态")
        
        print_color("\n部署信息:", Colors.BOLD)
        print(f"应用名称: {app_name}")
        print(f"状态: {status}")
        print(f"访问URL: {url}")
        print(f"区域: {region}")
        
    except json.JSONDecodeError:
        print_color("✗ 解析部署信息失败", Colors.FAIL)

def deploy_streamlit_app(app_name, region="ap-guangzhou"):
    """部署Streamlit应用到HAI"""
    print_color("准备部署Streamlit应用...", Colors.HEADER)
    
    # 创建Streamlit专用Dockerfile
    streamlit_dockerfile = """FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \\
    libgl1-mesa-glx libglib2.0-0 \\
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8501

# 启动Streamlit应用
CMD ["streamlit", "run", "deploy/sandbox_demo.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open("Dockerfile.streamlit", "w") as f:
        f.write(streamlit_dockerfile)
    
    # 创建requirements.txt（如果不存在）
    if not os.path.exists("requirements.txt"):
        with open("requirements.txt", "w") as f:
            f.write("streamlit>=1.22.0\n")
            f.write("numpy>=1.20.0\n")
            f.write("opencv-python>=4.5.0\n")
            f.write("matplotlib>=3.5.0\n")
            f.write("pillow>=9.0.0\n")
    
    # 创建HAI配置
    streamlit_config = {
        "appName": f"{app_name}-streamlit",
        "region": region,
        "containerConfig": {
            "image": f"{app_name}-streamlit:latest",
            "port": 8501,
            "envVars": {
                "PYTHONUNBUFFERED": "1"
            },
            "resources": {
                "cpu": 1,
                "memory": "2Gi"
            }
        },
        "scaling": {
            "minReplicas": 1,
            "maxReplicas": 3
        },
        "networking": {
            "ingress": {
                "enabled": True,
                "authEnabled": False
            }
        }
    }
    
    with open("hai-config-streamlit.json", "w") as f:
        json.dump(streamlit_config, f, indent=2)
    
    print_color("✓ Streamlit配置创建成功", Colors.GREEN)
    
    # 构建Streamlit镜像
    print_color("构建Streamlit镜像...", Colors.HEADER)
    registry = f"ccr.{region}.tencentcloudcr.com/ibrushpal"
    image_name = f"{registry}/{app_name}-streamlit:latest"
    
    build_cmd = ["docker", "build", "-f", "Dockerfile.streamlit", "-t", image_name, "."]
    result = subprocess.run(build_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print_color("✗ Streamlit镜像构建失败", Colors.FAIL)
        print(result.stderr.decode())
        return False
    
    # 推送镜像和部署
    login_cmd = ["tccli", "tcr", "login", "--registry", registry]
    subprocess.run(login_cmd)
    
    push_cmd = ["docker", "push", image_name]
    subprocess.run(push_cmd)
    
    deploy_cmd = ["tccli", "hai", "deploy", "--config", "hai-config-streamlit.json"]
    subprocess.run(deploy_cmd)
    
    print_color("✓ Streamlit应用部署请求已提交", Colors.GREEN)
    return True

def main():
    parser = argparse.ArgumentParser(description="iBrushPal HAI部署工具")
    parser.add_argument("--app-name", default="ibrushpal", help="应用名称")
    parser.add_argument("--region", default="ap-guangzhou", help="部署区域")
    parser.add_argument("--registry", default=None, help="容器镜像仓库地址")
    parser.add_argument("--streamlit", action="store_true", help="部署Streamlit演示应用")
    
    args = parser.parse_args()
    
    print_color("\n========== iBrushPal 爱伢伴 - HAI部署工具 ==========\n", Colors.BOLD)
    
    # 设置默认镜像仓库
    if args.registry is None:
        args.registry = f"ccr.{args.region}.tencentcloudcr.com/ibrushpal"
    
    # 检查前提条件
    if not check_prerequisites():
        sys.exit(1)
    
    # 部署Streamlit演示应用
    if args.streamlit:
        if deploy_streamlit_app(args.app_name, args.region):
            print_color("\n✓ Streamlit演示应用部署流程已启动", Colors.GREEN)
            print_color("  请等待几分钟，然后使用以下命令查看部署状态：", Colors.BLUE)
            print(f"  tccli hai describe-app --app-name {args.app_name}-streamlit --region {args.region}")
        else:
            print_color("\n✗ Streamlit演示应用部署失败", Colors.FAIL)
        return
    
    # 创建Dockerfile
    create_dockerfile()
    
    # 创建HAI配置
    create_hai_config(args.app_name, args.region)
    
    # 构建并推送镜像
    if not build_and_push_image(args.app_name, args.registry):
        sys.exit(1)
    
    # 部署到HAI
    if not deploy_to_hai():
        sys.exit(1)
    
    # 获取部署信息
    get_deployment_info(args.app_name, args.region)
    
    print_color("\n========== 部署完成 ==========\n", Colors.BOLD)
    print_color("您的iBrushPal应用已成功部署到腾讯云HAI平台！", Colors.GREEN)
    print("应用启动可能需要几分钟时间，请耐心等待。")
    print(f"您可以使用以下命令查看最新部署状态：")
    print(f"  tccli hai describe-app --app-name {args.app_name} --region {args.region}")

if __name__ == "__main__":
    main()