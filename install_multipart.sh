#!/bin/bash
# 安装缺失的python-multipart依赖

echo "🔧 安装缺失的python-multipart依赖..."

# 1. 安装python-multipart
echo "📦 安装python-multipart..."
/home/ubuntu/.venv/bin/pip install python-multipart

# 2. 验证安装
echo "✅ 验证安装..."
/home/ubuntu/.venv/bin/python -c "import python_multipart; print('python-multipart安装成功')"

# 3. 重启服务
echo "🔄 重启API服务..."
sudo systemctl restart ibrushpal-api

# 4. 检查服务状态
echo "📊 检查服务状态..."
sleep 3
sudo systemctl status ibrushpal-api --no-pager -l

# 5. 检查端口监听
echo "🌐 检查端口监听..."
sudo netstat -tlnp | grep :8000 || echo "等待服务启动..."

echo "✨ 依赖安装完成！如果服务仍然无法启动，请检查其他依赖："
echo "/home/ubuntu/.venv/bin/pip install fastapi uvicorn opencv-python numpy ultralytics python-multipart"