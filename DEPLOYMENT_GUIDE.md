# iBrushPal API 部署指南

## 快速启动
```bash
# 给启动脚本添加执行权限
chmod +x run_api.sh

# 直接运行（前台运行）
./run_api.sh

# 后台运行
nohup ./run_api.sh > api.log 2>&1 &

# 查看日志
tail -f api.log
```

## 系统服务部署
```bash
# 复制服务配置文件
sudo cp ibrushpal-api.service /etc/systemd/system/

# 重新加载系统服务
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ibrushpal-api

# 设置开机自启
sudo systemctl enable ibrushpal-api

# 查看服务状态
sudo systemctl status ibrushpal-api

# 查看日志
sudo journalctl -u ibrushpal-api -f
```

## 常用命令
```bash
# 重启服务
sudo systemctl restart ibrushpal-api

# 停止服务
sudo systemctl stop ibrushpal-api

# 查看服务日志
sudo journalctl -u ibrushpal-api -n 100
```

## 端口检查
```bash
# 检查API是否运行
netstat -tlnp | grep :8000

# 测试API健康状态
curl http://localhost:8000/health
```

服务启动后，API将在 http://42.194.142.158:8000 持续运行。