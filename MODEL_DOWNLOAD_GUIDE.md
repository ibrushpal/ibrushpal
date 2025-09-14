# YOLOv8 模型下载指南

## 问题描述
YOLOv8模型从GitHub下载很慢，影响程序启动速度。

## 解决方案

### 方法一：使用下载脚本（推荐）
```bash
# 运行下载脚本
python download_yolov8.py
```

### 方法二：手动下载
1. 访问下载地址：
   - 国内镜像1: https://mirror.ghproxy.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt
   - 国内镜像2: https://pd.zwc365.com/https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt
   - 官方源: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-seg.pt

2. 下载后保存到：
   ```
   models/weights/yolov8n-seg.pt
   ```

### 方法三：预下载模型
程序首次运行时，脚本会自动下载模型到正确位置。

## 文件位置
- 模型文件: `models/weights/yolov8n-seg.pt`
- 下载脚本: `download_yolov8.py`
- 配置文件: `config.py`

## 验证下载
```bash
# 检查模型文件
ls -la models/weights/

# 检查文件大小（应该约14MB）
du -h models/weights/yolov8n-seg.pt
```

## 注意事项
1. 确保有足够的磁盘空间（至少50MB）
2. 确保网络连接正常
3. 如果下载中断，删除不完整的文件重新下载

## 故障排除
如果下载失败：
1. 检查网络连接
2. 尝试不同的镜像源
3. 手动下载并放置到指定目录