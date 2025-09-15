import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io
from typing import Tuple, List, Dict, Any

class TeethImagePreprocessor:
    """牙齿图像预处理类"""
    
    def __init__(self):
        self.target_size = (640, 640)
        
    def load_image(self, image_data: bytes) -> np.ndarray:
        """从字节数据加载图像"""
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("无法解码图像数据")
        return image
    
    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """调整图像尺寸并保持宽高比"""
        h, w = image.shape[:2]
        
        # 计算缩放比例
        scale = min(self.target_size[0] / w, self.target_size[1] / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        # 调整尺寸
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        # 填充到目标尺寸
        pad_w = self.target_size[0] - new_w
        pad_h = self.target_size[1] - new_h
        pad_top = pad_h // 2
        pad_bottom = pad_h - pad_top
        pad_left = pad_w // 2
        pad_right = pad_w - pad_left
        
        padded = cv2.copyMakeBorder(
            resized, 
            pad_top, pad_bottom, 
            pad_left, pad_right, 
            cv2.BORDER_CONSTANT, 
            value=(114, 114, 114)
        )
        
        return padded, (scale, (pad_left, pad_top))
    
    def enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """增强图像对比度"""
        # 转换为PIL图像进行增强
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # 对比度增强
        enhancer = ImageEnhance.Contrast(pil_image)
        enhanced = enhancer.enhance(1.2)
        
        # 锐度增强
        enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = enhancer.enhance(1.1)
        
        # 转换回OpenCV格式
        return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)
    
    def normalize_image(self, image: np.ndarray) -> np.ndarray:
        """图像归一化"""
        # 转换为float32并归一化到0-1
        normalized = image.astype(np.float32) / 255.0
        
        # 转换为RGB格式（YOLOv8需要）
        normalized = cv2.cvtColor(normalized, cv2.COLOR_BGR2RGB)
        
        # 转换为CHW格式
        normalized = normalized.transpose(2, 0, 1)
        
        return normalized
    
    def preprocess(self, image_data: bytes) -> Tuple[np.ndarray, Dict[str, Any]]:
        """完整的预处理流水线"""
        # 加载图像
        image = self.load_image(image_data)
        original_shape = image.shape
        
        # 增强对比度
        enhanced = self.enhance_contrast(image)
        
        # 调整尺寸
        resized, padding_info = self.resize_image(enhanced)
        
        # 归一化
        normalized = self.normalize_image(resized)
        
        # 准备预处理信息
        preprocess_info = {
            'original_shape': original_shape,
            'scale': padding_info[0],
            'padding': padding_info[1],
            'target_size': self.target_size
        }
        
        return normalized, preprocess_info
    
    def postprocess_detections(self, detections: List[Dict[str, Any]], preprocess_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """后处理检测结果，转换回原始坐标"""
        scale = preprocess_info['scale']
        pad_left, pad_top = preprocess_info['padding']
        orig_h, orig_w = preprocess_info['original_shape'][:2]
        
        processed_detections = []
        
        for detection in detections:
            # 获取边界框坐标
            x1, y1, x2, y2 = detection['bbox']
            
            # 去除填充并缩放回原始尺寸
            x1 = (x1 - pad_left) / scale
            y1 = (y1 - pad_top) / scale
            x2 = (x2 - pad_left) / scale
            y2 = (y2 - pad_top) / scale
            
            # 确保坐标在图像范围内
            x1 = max(0, min(x1, orig_w))
            y1 = max(0, min(y1, orig_h))
            x2 = max(0, min(x2, orig_w))
            y2 = max(0, min(y2, orig_h))
            
            processed_detection = {
                'bbox': [x1, y1, x2, y2],
                'confidence': detection['confidence'],
                'class_id': detection['class_id'],
                'class_name': detection['class_name']
            }
            
            processed_detections.append(processed_detection)
        
        return processed_detections

def create_sample_teeth_image() -> bytes:
    """创建示例牙齿测试图像"""
    # 创建一个简单的测试图像
    image = np.ones((300, 300, 3), dtype=np.uint8) * 255
    
    # 添加一些模拟牙齿的形状
    for i in range(5):
        center_x = 60 + i * 45
        cv2.ellipse(image, (center_x, 150), (20, 30), 0, 0, 360, (200, 200, 200), -1)
        cv2.ellipse(image, (center_x, 150), (20, 30), 0, 0, 360, (100, 100, 100), 2)
    
    # 转换为字节数据
    success, encoded_image = cv2.imencode('.jpg', image)
    if not success:
        raise ValueError("无法编码测试图像")
    
    return encoded_image.tobytes()

# 测试预处理流程
if __name__ == "__main__":
    preprocessor = TeethImagePreprocessor()
    
    # 创建测试图像
    test_image_data = create_sample_teeth_image()
    
    # 测试预处理
    try:
        processed, info = preprocessor.preprocess(test_image_data)
        print(f"✅ 预处理成功")
        print(f"原始形状: {info['original_shape']}")
        print(f"处理后形状: {processed.shape}")
        print(f"缩放比例: {info['scale']}")
        print(f"填充信息: {info['padding']}")
        
    except Exception as e:
        print(f"❌ 预处理失败: {str(e)}")