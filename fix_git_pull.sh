#!/bin/bash

# Git拉取失败修复脚本
echo "=== 修复Git拉取失败 ==="

# 1. 检查错误类型
echo "诊断Git连接问题..."

# 2. 尝试禁用HTTP2（解决curl 16错误）
echo "尝试禁用HTTP2协议..."
git config --global http.version HTTP/1.1

# 3. 增加Git缓冲区大小
echo "增加Git缓冲区大小..."
git config --global http.postBuffer 1048576000

# 4. 设置低速度限制
echo "设置低速度限制..."
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999

# 5. 尝试使用SSH方式（备用）
echo "配置备用拉取方式..."
original_url=$(git remote get-url origin 2>/dev/null || echo "")
if [[ "$original_url" == https://* ]]; then
    # 转换为SSH格式
    ssh_url=$(echo "$original_url" | sed 's|https://|git@|' | sed 's|/|:|')
    echo "添加SSH远程: $ssh_url"
    git remote add ssh-origin $ssh_url 2>/dev/null
fi

# 6. 尝试不同的拉取方法
echo "尝试方法1: 使用浅层克隆..."
git fetch --depth 1

if [ $? -ne 0 ]; then
    echo "尝试方法2: 使用HTTP/1.1直接拉取..."
    GIT_CURL_VERBOSE=1 GIT_TRACE=1 git pull origin main --no-rebase
fi

# 7. 如果仍然失败，提供手动解决方案
if [ $? -ne 0 ]; then
    echo "❌ 自动修复失败，请尝试手动方案:"
    echo "1. 手动下载ZIP: https://github.com/ibrushpal/ibrushpal/archive/refs/heads/main.zip"
    echo "2. 解压后覆盖当前文件"
    echo "3. 或者运行: git clone --depth 1 https://github.com/ibrushpal/ibrushpal.git temp_dir && cp -r temp_dir/* . && rm -rf temp_dir"
else
    echo "✅ 拉取成功！"
fi

echo "=== 修复完成 ==="