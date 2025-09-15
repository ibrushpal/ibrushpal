#!/bin/bash
# iBrushPal API服务修复脚本

echo "🔧 开始修复iBrushPal API服务..."

# 1. 检查服务状态
echo "📊 当前服务状态:"
sudo systemctl status ibrushpal-api --no-pager -l

# 2. 查看详细错误日志
echo "📋 查看错误日志:"
sudo journalctl -u ibrushpal-api --no-pager -n 20

# 3. 检查Python依赖
echo "🐍 检查Python依赖:"
cd /home/ubuntu/ibrushpal
/home/ubuntu/.venv/bin/python -c "
try:
    import fastapi, uvicorn, cv2, numpy
    print('✅ 主要依赖正常')
except ImportError as e:
    print(f'❌ 依赖缺失: {e}')
    print('请运行: pip install fastapi uvicorn opencv-python numpy')
"

# 4. 检查API文件语法
echo "📝 检查API文件语法:"
if /home/ubuntu/.venv/bin/python -m py_compile teeth_detection_api.py; then
    echo "✅ API文件语法正确"
else
    echo "❌ API文件存在语法错误"
    echo "请检查文件内容或重新上传"
fi

# 5. 尝试手动启动测试
echo "🚀 尝试手动启动API:"
timeout 10s /home/ubuntu/.venv/bin/python teeth_detection_api.py || echo "手动启动测试完成"

# 6. 重新加载系统服务
echo "🔄 重新加载系统服务配置:"
sudo systemctl daemon-reload

# 7. 重启服务
echo "🔄 重启服务:"
sudo systemctl restart ibrushpal-api
sleep 3

# 8. 再次检查状态
echo "📊 重启后服务状态:"
sudo systemctl status ibrushpal-api --no-pager -l

# 9. 检查端口监听
echo "🌐 检查端口监听:"
sudo netstat -tlnp | grep :8000 || echo "端口8000未监听"

echo "✨ 修复完成！如果仍有问题，请检查："
echo "1. Python依赖是否完整安装"
echo "2. API文件语法是否正确"
echo "3. 虚拟环境路径配置"
echo "4. 文件权限设置"