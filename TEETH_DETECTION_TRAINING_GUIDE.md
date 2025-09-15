# 牙齿检测模型训练指南

## 问题分析
测试结果显示通用YOLOv8模型无法检测牙齿，原因：
1. 牙齿检测需要专门的训练数据
2. 牙齿形状、颜色、纹理特征特殊
3. 口腔环境复杂（光照、角度、遮挡）

## 解决方案

### 方案一：使用预训练牙齿检测模型
```python
# 使用专门针对牙齿检测训练的模型
# 推荐模型：DentalYOLO、ToothNet、OralAI

# 安装专门库
# pip install dentalai oralcv

from dentalai import ToothDetector

detector = ToothDetector()
results = detector.detect(image_path)
```

### 方案二：自定义训练牙齿检测模型

#### 1. 数据准备
```python
# 收集牙齿图像数据集
# 来源：公开数据集 + 合作诊所脱敏数据

数据集要求：
- 至少5000张标注图像
- 包含各种角度、光照条件
- 标注牙齿边界框和类别（门牙、犬齿、臼齿）
```

#### 2. 数据标注格式
```yaml
# YOLO格式标注
# class_id center_x center_y width height

# 牙齿类别映射：
# 0 - incisor (门牙)
# 1 - canine (犬齿)  
# 2 - premolar (前臼齿)
# 3 - molar (臼齿)
```

#### 3. 训练配置
```python
# train.py
import torch
from ultralytics import YOLO

# 加载预训练模型
model = YOLO('yolov8s.pt')  # 使用小模型作为基础

# 训练配置
results = model.train(
    data='teeth_dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='teeth_detection_v1'
)
```

#### 4. 数据集配置文件
```yaml
# teeth_dataset.yaml
path: /datasets/teeth
train: images/train
val: images/val
test: images/test

names:
  0: incisor
  1: canine
  2: premolar
  3: molar
```

### 方案三：使用牙齿分割模型
```python
# 分割模型能提供更精确的牙齿轮廓
from ultralytics import YOLO

# 使用分割模型
model = YOLO('yolov8s-seg.pt')
results = model(image_path)

# 获取分割掩码
masks = results[0].masks
```

## 实施步骤

### 阶段一：快速验证（1-2天）
1. 尝试现有牙齿检测模型
2. 测试在模拟数据上的效果
3. 评估准确率和速度

### 阶段二：数据收集（1-2周）
1. 收集公开牙齿数据集
2. 与诊所合作获取脱敏数据
3. 数据清洗和标注

### 阶段三：模型训练（3-7天）
1. 准备训练环境（GPU服务器）
2. 配置训练参数
3. 开始模型训练
4. 验证模型性能

### 阶段四：部署集成（2-3天）
1. 模型量化优化
2. API接口开发
3. 性能测试

## 推荐数据集

### 公开数据集
1. **UFBA-UESC Dental Images Dataset**
   - 包含1200张牙齿图像
   - 标注了牙齿和病变区域

2. **TeethSeg Dataset**
   - 专注于牙齿分割
   - 包含多种牙齿状态

3. **DentalFlickr Dataset**
   - 从Flickr收集的牙齿图像
   - 需要清洗和标注

### 数据增强策略
```python
# 增强方法
augmentations = [
    'horizontal_flip',
    'vertical_flip', 
    'random_brightness',
    'random_contrast',
    'random_rotation',
    'random_zoom'
]
```

## 性能目标

### MVP阶段目标
- 牙齿检测准确率: ≥80%
- 推理时间: ≤500ms
- 支持同时检测: 4-8颗牙齿

### 生产环境目标  
- 牙齿检测准确率: ≥95%
- 推理时间: ≤200ms
- 支持全口牙齿检测

## 下一步行动

1. **立即行动**: 尝试现有的牙齿检测开源模型
2. **短期计划**: 开始数据收集和标注工作
3. **长期规划**: 建立完整的牙齿AI检测流水线

## 紧急解决方案

在专门模型训练完成前，可以使用以下临时方案：

```python
def simple_teeth_detection(image):
    """基于颜色和形状的简单牙齿检测"""
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 牙齿颜色范围（白色到浅黄色）
    lower_teeth = np.array([0, 0, 200])
    upper_teeth = np.array([30, 50, 255])
    
    # 创建掩码
    mask = cv2.inRange(hsv, lower_teeth, upper_teeth)
    
    # 形态学操作
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours
```

## 联系专家

建议联系：
1. 牙科AI研究团队
2. 医学影像处理专家
3. 口腔医学研究所

通过专业合作可以加速模型开发进程。