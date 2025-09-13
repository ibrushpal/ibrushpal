#!/bin/bash
# iBrushPal 爱伢伴 AI 一键部署脚本
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

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
  error "请使用root权限运行此脚本: sudo bash one_click_deploy.sh"
  exit 1
fi

# 显示欢迎信息
echo "=================================================="
echo "    iBrushPal 爱伢伴 AI 系统一键部署工具"
echo "=================================================="
echo ""

# 步骤1: 检查系统环境
info "步骤1: 检查系统环境..."
OS_NAME=$(grep -oP '(?<=^NAME=).+' /etc/os-release | tr -d '"')
OS_VERSION=$(grep -oP '(?<=^VERSION_ID=).+' /etc/os-release | tr -d '"')

info "检测到操作系统: $OS_NAME $OS_VERSION"

# 检查GPU
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader)
    info "检测到GPU: $GPU_INFO"
else
    warn "未检测到NVIDIA GPU，AI推理性能可能受限"
    read -p "是否继续安装? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        error "安装已取消"
        exit 1
    fi
fi

# 步骤2: 安装依赖
info "步骤2: 安装系统依赖..."
apt-get update
apt-get install -y \
    git \
    curl \
    wget \
    unzip \
    docker.io \
    docker-compose \
    python3 \
    python3-pip

# 安装NVIDIA容器工具包(如果有GPU)
if command -v nvidia-smi &> /dev/null; then
    info "安装NVIDIA容器工具包..."
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
    apt-get update
    apt-get install -y nvidia-container-toolkit
    systemctl restart docker
fi

# 步骤3: 配置Docker
info "步骤3: 配置Docker环境..."
systemctl enable docker
systemctl start docker
groupadd -f docker
usermod -aG docker $USER
info "Docker配置完成"

# 步骤4: 创建项目目录
info "步骤4: 创建项目目录..."
PROJECT_DIR="/opt/ibrushpal"
LOG_DIR="/var/log/ibrushpal"

mkdir -p $PROJECT_DIR
mkdir -p $LOG_DIR

# 步骤5: 部署代码
info "步骤5: 部署代码..."
CURRENT_DIR=$(pwd)
PARENT_DIR=$(dirname "$CURRENT_DIR")

# 复制代码到项目目录
cp -r $PARENT_DIR/* $PROJECT_DIR/
chown -R $USER:$USER $PROJECT_DIR
chown -R $USER:$USER $LOG_DIR

# 步骤6: 启动服务
info "步骤6: 启动AI服务..."
cd $PROJECT_DIR/deploy
docker-compose up -d

# 检查服务状态
sleep 5
if docker ps | grep -q "ai-service"; then
    info "AI服务已成功启动!"
    
    # 获取服务器IP
    SERVER_IP=$(hostname -I | awk '{print $1}')
    echo ""
    echo "=================================================="
    echo "    iBrushPal 爱伢伴 AI 系统部署成功!"
    echo "=================================================="
    echo ""
    echo "API服务地址: http://$SERVER_IP:8000"
    echo "API文档地址: http://$SERVER_IP:8000/docs"
    echo ""
    echo "日志目录: $LOG_DIR"
    echo "项目目录: $PROJECT_DIR"
    echo ""
    echo "如需查看服务日志，请运行:"
    echo "docker logs -f ibrushpal_ai-service_1"
else
    error "AI服务启动失败，请检查日志:"
    docker-compose logs
fi

echo ""
info "部署完成!"