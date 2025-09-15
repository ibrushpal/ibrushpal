# iBrushPal API 部署指南

## 服务器状态面板修复部署说明

### 问题描述
状态面板路由 `/status-dashboard` 返回404错误，需要更新服务器上的API文件。

### 修复内容
已修复 `teeth_detection_api.py` 文件中的状态面板路由，确保：
1. 状态面板路由 `/status-dashboard` 正确返回HTML内容
2. 添加了根路径 `/` 的欢迎页面
3. 所有HTML内容已内嵌在API文件中

### 手动更新步骤

#### 1. 连接到服务器
```bash
ssh ubuntu@42.194.142.158
```

#### 2. 备份当前文件
```bash
cd /home/ubuntu/ibrushpal
cp teeth_detection_api.py teeth_detection_api.py.backup
```

#### 3. 上传修复后的文件（从本地）
```bash
# 在本地终端执行
scp teeth_detection_api.py ubuntu@42.194.142.158:/home/ubuntu/ibrushpal/
```

#### 4. 重启API服务
```bash
sudo systemctl restart ibrushpal-api
```

#### 5. 验证服务状态
```bash
sudo systemctl status ibrushpal-api
```

#### 6. 测试状态面板
访问以下URL验证修复：
- http://42.194.142.158:8000/status-dashboard
- http://42.194.142.158:8000/

### 验证修复

#### 预期结果
1. ✅ 状态面板页面正常显示（不再是404错误）
2. ✅ 页面包含服务状态监控信息
3. ✅ 根路径显示欢迎页面
4. ✅ 所有API端点正常工作

#### 测试端点
- `/` - 欢迎页面
- `/status-dashboard` - 状态面板
- `/health` - 健康检查
- `/model-info` - 模型信息
- `/docs` - API文档

### 故障排除

#### 如果服务启动失败
```bash
# 查看详细错误日志
journalctl -u ibrushpal-api -f

# 检查Python依赖
cd /home/ubuntu/ibrushpal
python -c "import fastapi, uvicorn, cv2; print('依赖正常')"
```

#### 如果文件权限问题
```bash
sudo chown ubuntu:ubuntu /home/ubuntu/ibrushpal/teeth_detection_api.py
sudo chmod 644 /home/ubuntu/ibrushpal/teeth_detection_api.py
```

### 文件变更摘要

#### 修复内容
1. **添加根路径路由** (`@app.get("/")`)
   - 返回欢迎页面HTML
   - 提供主要功能链接

2. **修复状态面板路由** (`@app.get("/status-dashboard")`)
   - 内嵌完整的HTML内容
   - 添加JavaScript动态数据获取
   - 修复HTML语法错误

3. **增强功能**
   - 实时状态监控
   - 自动数据刷新（30秒间隔）
   - 友好的用户界面

#### 技术细节
- 使用FastAPI的HTMLResponse类
- 内联CSS和JavaScript
- 响应式设计
- 支持移动端访问

### 版本信息
- **当前版本**: 2.0.0
- **修复版本**: 2.0.1
- **更新日期**: 2025/9/15

### 联系方式
如有问题，请联系技术支持团队。