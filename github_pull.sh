#!/bin/bash

# iBrushPal GitHub拉取更新脚本
echo "=== 从GitHub拉取更新 ==="

# 1. 检查是否已初始化Git
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
    git config --global user.email "hzd@ibrushpal.com"
    git config --global user.name "ibrushpal"
fi

# 2. 设置GitHub远程仓库
echo "设置GitHub远程仓库..."
repo_url="https://github.com/ibrushpal/ibrushpal.git"
git remote add origin $repo_url 2>/dev/null || git remote set-url origin $repo_url
echo "使用仓库: $repo_url"

# 3. 拉取最新代码
echo "拉取最新代码..."
git pull origin main

# 4. 检查是否有冲突
if [ $? -eq 0 ]; then
    echo "✅ 拉取成功！"
    echo "更新内容:"
    git log -1 --oneline
else
    echo "❌ 拉取失败，可能有冲突"
    echo "请手动解决冲突后运行: git add . && git commit -m '解决冲突'"
fi

echo "=== 拉取更新完成 ==="