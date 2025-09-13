#!/bin/bash
# 云服务器初始化脚本

# 1. 安装基础工具
sudo apt-get update
sudo apt-get install -y \
    git \
    curl \
    wget \
    unzip \
    docker.io \
    docker-compose \
    nvidia-driver-470 \
    nvidia-container-toolkit

# 2. 配置Docker使用GPU
sudo groupadd docker
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker

# 3. 安装Python环境
sudo apt-get install -y python3.8 python3-pip
sudo pip3 install virtualenv

# 4. 创建项目目录
mkdir -p /opt/ibrushpal
chown $USER:$USER /opt/ibrushpal

# 5. 配置日志目录
mkdir -p /var/log/ibrushpal
chown $USER:$USER /var/log/ibrushpal

echo "云服务器初始化完成，请重新登录使配置生效"
echo "下一步：部署AI服务容器"