#!/usr/bin/env python3
"""
修复PyTorch 2.6权重加载问题
解决: Weights only load failed 错误
"""

import torch
import os
import sys
from pathlib import Path

def fix_pytorch_weights_loading():
    """修复PyTorch 2.6权重加载问题"""
    
    print("🔧 修复PyTorch 2.6权重加载问题")
    print("=" * 50)
    
    # 检查PyTorch版本
    print(f"PyTorch版本: {torch.__version__}")
    
    # 添加安全全局变量（解决所有必要的ultralytics模块加载问题）
    try:
        # 尝试导入所有必要的ultralytics模块
        import ultralytics.nn.tasks as tasks
        import ultralytics.nn.modules as modules
        import torch.nn.modules.container as container
        
        # 添加所有必要的安全全局变量
        torch.serialization.add_safe_globals([
            tasks.SegmentationModel,
            modules.Conv,  # 添加Conv模块
            container.Sequential
        ])
        print("✅ 已添加所有必要的安全全局变量 (SegmentationModel, Conv, Sequential)")
        
    except ImportError as e:
        print(f"⚠️  无法导入必要模块: {e}")
        return False
    except Exception as e:
        print(f"⚠️  添加安全全局变量失败: {e}")
        return False
    
    return True

def test_model_loading(model_path: str = "models/yolov8n-seg.pt"):
    """测试模型加载"""
    
    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在: {model_path}")
        return False
    
    print(f"\n🧪 测试模型加载: {model_path}")
    
    try:
        # 方法1: 使用 weights_only=False (需要信任源)
        print("方法1: 使用 weights_only=False")
        model = torch.load(model_path, weights_only=False)
        print("✅ 方法1成功: weights_only=False")
        return True
        
    except Exception as e:
        print(f"❌ 方法1失败: {e}")
    
    try:
        # 方法2: 使用安全上下文管理器
        print("\n方法2: 使用安全上下文管理器")
        import ultralytics.nn.tasks as tasks
        
        with torch.serialization.safe_globals([tasks.SegmentationModel]):
            model = torch.load(model_path, weights_only=True)
            print("✅ 方法2成功: 使用安全上下文管理器")
            return True
            
    except Exception as e:
        print(f"❌ 方法2失败: {e}")
    
    try:
        # 方法3: 直接使用YOLO类加载
        print("\n方法3: 使用YOLO类直接加载")
        from ultralytics import YOLO
        
        model = YOLO(model_path)
        print("✅ 方法3成功: 使用YOLO类直接加载")
        return True
        
    except Exception as e:
        print(f"❌ 方法3失败: {e}")
    
    return False

def update_teeth_detection_api():
    """更新牙齿检测API以修复加载问题"""
    
    api_file = "teeth_detection_api.py"
    if not os.path.exists(api_file):
        print(f"❌ API文件不存在: {api_file}")
        return False
    
    print(f"\n📝 更新API文件: {api_file}")
    
    # 读取文件内容
    with open(api_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找模型加载部分
    if '_init_dl_model' in content:
        print("✅ 找到模型初始化方法")
        
        # 添加安全加载代码
        new_init_code = '''
    def _init_dl_model(self):
        """初始化深度学习模型"""
        try:
            model_path = "models/yolov8n-seg.pt"
            if os.path.exists(model_path):
                # 修复PyTorch 2.6权重加载问题
                import torch
                import ultralytics.nn.tasks as tasks
                
                # 添加安全全局变量
                import ultralytics.nn.modules as modules
                import torch.nn.modules.container as container
                torch.serialization.add_safe_globals([
                    tasks.SegmentationModel,
                    modules.Conv,  # 添加Conv模块
                    container.Sequential
                ])
                
                # 使用安全上下文加载模型
                with torch.serialization.safe_globals([
                    tasks.SegmentationModel,
                    modules.Conv,  # 添加Conv模块
                    container.Sequential
                ]):
                    self.dl_model = torch.load(model_path, weights_only=True)
                
                print("✅ 深度学习模型加载成功 (安全模式)")
            else:
                print("⚠️  深度学习模型文件不存在，将使用传统方法")
                self.dl_available = False
        except Exception as e:
            print(f"❌ 深度学习模型加载失败: {e}")
            # 回退到传统方法
            self.dl_available = False
'''
        
        # 替换原有的_init_dl_model方法
        old_init_pattern = r'    def _init_dl_model\(self\):.*?        except Exception as e:.*?            self\.dl_available = False'
        
        import re
        updated_content = re.sub(old_init_pattern, new_init_code, content, flags=re.DOTALL)
        
        # 保存更新后的文件
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ API文件更新完成")
        return True
    
    else:
        print("❌ 未找到模型初始化方法")
        return False

def main():
    """主函数"""
    print("🦷 PyTorch 2.6权重加载修复工具")
    print("=" * 50)
    
    # 修复安全全局变量
    if not fix_pytorch_weights_loading():
        print("❌ 安全全局变量修复失败")
        return False
    
    # 测试模型加载
    if not test_model_loading():
        print("❌ 所有模型加载方法都失败")
        return False
    
    # 更新API文件
    if update_teeth_detection_api():
        print("\n🎉 修复完成！请重启API服务")
        print("重启命令: sudo systemctl restart ibrushpal-api")
    else:
        print("\n❌ 修复失败")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)