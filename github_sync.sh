#!/bin/bash

# iBrushPal GitHub同步脚本
echo "=== GitHub同步设置 ==="

# 1. 检查是否已初始化Git
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
    git config --global user.email "your-email@example.com"
    git config --global user.name "Your Name"
fi

# 2. 设置GitHub远程仓库
echo "设置GitHub远程仓库..."
repo_url="https://github.com/ibrushpal/ibrushpal.git"
git remote add origin $repo_url 2>/dev/null || git remote set-url origin $repo_url
echo "使用仓库: $repo_url"

# 3. 添加文件到Git
echo "添加文件到Git..."
git add .

# 4. 提交更改
echo "提交更改..."
git commit -m "服务器更新 $(date '+%Y-%m-%d %H:%M:%S')"

# 5. 推送到GitHub
echo "推送到GitHub..."
git branch -M main
git push -u origin main

echo "=== GitHub同步完成 ==="
echo "下次更新只需运行: git add . && git commit -m '更新消息' && git push"