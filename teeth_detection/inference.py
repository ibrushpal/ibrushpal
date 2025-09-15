import numpy as np
from typing import Dict, Any, List
from ultralytics import YOLO
import cv2
from .preprocessing import TeethImagePreprocessor
from .postprocessing import TeethDetectionPostprocessor

class TeethDetectionInference:
    """牙齿检测推理类"""
    
    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.preprocessor = TeethImagePreprocessor()
        self.postprocessor = TeethDetectionPostprocessor(confidence_threshold)
        
    def load_model(self):
        """加载YOLOv8模型"""
        try:
            self.model = YOLO(self.model_path)
            print(f"✅ YOLOv8模型加载成功: {self.model_path}")
            return True
        except Exception as e:
            print(f"❌ 模型加载失败: {str(e)}")
            return False
    
    def predict(self, image_data: bytes) -> Dict[str, Any]:
        """执行完整的牙齿检测推理"""
        if self.model is None:
            if not self.load_model():
                return {'error': '模型加载失败'}
        
        try:
            # 预处理
            processed_image, preprocess_info = self.preprocessor.preprocess(image_data)
            
            # 模型推理
            results = self.model(processed_image, conf=self.confidence_threshold, verbose=False)
            
            # 解析原始检测结果
            raw_detections = self._parse_yolo_results(results, preprocess_info)
            
            # 后处理
            final_result = self.postprocessor.postprocess(
                raw_detections, preprocess_info['original_shape']
            )
            
            # 添加预处理信息
            final_result['preprocess_info'] = preprocess_info
            
            return final_result
            
        except Exception as e:
            return {'error': f'推理失败: {str(e)}'}
    
    def _parse_yolo_results(self, results, preprocess_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """解析YOLO模型输出结果"""
        raw_detections = []
        
        if not results or len(results) == 0:
            return raw_detections
        
        # 获取第一个结果（单张图像）
        result = results[0]
        
        if result.boxes is None:
            return raw_detections
        
        # 获取检测框信息
        boxes = result.boxes.xyxy.cpu().numpy()  # 边界框坐标
        confidences = result.boxes.conf.cpu().numpy()  # 置信度
        class_ids = result.boxes.cls.cpu().numpy()  # 类别ID
        
        for i in range(len(boxes)):
            # 转换为整数坐标
            x1, y1, x2, y2 = boxes[i].astype(int)
            confidence = float(confidences[i])
            class_id = int(class_ids[i])
            
            # 获取类别名称
            class_name = self._get_class_name(class_id)
            
            raw_detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': confidence,
                'class_id': class_id,
                'class_name': class_name
            })
        
        return raw_detections
    
    def _get_class_name(self, class_id: int) -> str:
        """根据类别ID获取类别名称"""
        # YOLOv8牙齿检测模型的类别映射
        class_names = {
            0: 'tooth',      # 牙齿
            1: 'caries',     # 龋齿
            2: 'plaque',     # 牙菌斑
            3: 'gingivitis'  # 牙龈炎
        }
        return class_names.get(class_id, f'class_{class_id}')
    
    def visualize_detections(self, image_data: bytes, detections: List[Dict[str, Any]]) -> bytes:
        """可视化检测结果并返回图像字节数据"""
        # 加载原始图像
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        
        # 绘制检测框
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            confidence = det['confidence']
            class_name = det['class_name']
            
            # 绘制边界框
            color = self._get_class_color(class_name)
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # 绘制标签
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # 转换为字节数据
        success, encoded_image = cv2.imencode('.jpg', image)
        if not success:
            raise ValueError("无法编码可视化图像")
        
        return encoded_image.tobytes()
    
    def _get_class_color(self, class_name: str) -> tuple:
        """根据类别名称获取颜色"""
        colors = {
            'tooth': (0, 255, 0),      # 绿色 - 牙齿
            'caries': (0, 0, 255),     # 红色 - 龋齿
            'plaque': (255, 255, 0),   # 黄色 - 牙菌斑
            'gingivitis': (255, 0, 0)  # 蓝色 - 牙龈炎
        }
        return colors.get(class_name, (255, 255, 255))  # 默认白色
    
    def batch_predict(self, image_data_list: List[bytes]) -> List[Dict[str, Any]]:
        """批量预测多张图像"""
        results = []
        for image_data in image_data_list:
            results.append(self.predict(image_data))
        return results

# 测试推理流程
if __name__ == "__main__":
    # 初始化推理器
    detector = TeethDetectionInference(
        model_path="models/yolov8n-seg.pt",  # 使用较小的模型进行测试
        confidence_threshold=0.5
    )
    
    # 创建测试图像
    from preprocessing import create_sample_teeth_image
    test_image_data = create_sample_teeth_image()
    
    # 执行推理
    print("🧪 测试牙齿检测推理...")
    result = detector.predict(test_image_data)
    
    if 'error' in result:
        print(f"❌ 推理失败: {result['error']}")
    else:
        print("✅ 推理成功!")
        print(f"检测到牙齿数: {result['total_teeth_detected']}")
        print(f"覆盖率: {result['coverage_percentage']:.1f}%")
        print(f"牙齿分布: {result['tooth_distribution']}")
        
        # 可视化结果
        try:
            visualized_image = detector.visualize_detections(test_image_data, result['detections'])
            print("✅ 可视化图像生成成功")
            
            # 保存可视化结果（可选）
            with open('test_detection_result.jpg', 'wb') as f:
                f.write(visualized_image)
            print("📁 可视化结果已保存为 test_detection_result.jpg")
            
        except Exception as e:
            print(f"❌ 可视化失败: {str(e)}")