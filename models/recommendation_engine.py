from typing import Dict, List
import xgboost as xgb
import numpy as np
import json

class RecommendationEngine:
    """混合推荐引擎（规则+机器学习）"""
    
    def __init__(self):
        self.rule_base = self._load_rules()
        self.ml_model = self._load_model()
        
    def _load_rules(self) -> Dict:
        """加载临床规则"""
        return {
            "caries_history": {
                "must": ["floss"],
                "suggest": ["fluoride_toothpaste"]
            },
            "gingivitis": {
                "must": ["soft_bristle"],
                "suggest": ["mouthwash"]
            }
        }
    
    def _load_model(self) -> xgb.Booster:
        """加载XGBoost模型（示例）"""
        # TODO: 替换为实际训练好的模型
        return xgb.Booster()
    
    def generate_recommendation(self, inputs: Dict) -> Dict:
        """生成个性化刷牙方案"""
        # 1. 应用临床规则
        rule_results = self._apply_rules(inputs)
        
        # 2. 机器学习预测
        ml_results = self._ml_predict(inputs)
        
        # 3. 混合决策
        return {
            "must": list(set(rule_results["must"] + ml_results["must"])),
            "suggest": list(set(rule_results["suggest"] + ml_results["suggest"])),
            "avoid": ml_results["avoid"]
        }
    
    def _apply_rules(self, inputs: Dict) -> Dict:
        """应用临床规则逻辑"""
        recommendations = {"must": [], "suggest": []}
        
        # 检查龋齿历史
        if inputs.get("caries_history"):
            recommendations["must"].extend(self.rule_base["caries_history"]["must"])
            recommendations["suggest"].extend(self.rule_base["caries_history"]["suggest"])
            
        # 检查牙龈炎
        if inputs.get("gingivitis"):
            recommendations["must"].extend(self.rule_base["gingivitis"]["must"])
            recommendations["suggest"].extend(self.rule_base["gingivitis"]["suggest"])
            
        return recommendations
    
    def _ml_predict(self, inputs: Dict) -> Dict:
        """机器学习预测逻辑"""
        # 示例特征工程
        features = np.array([
            inputs.get("cleanliness_score", 50) / 100,
            inputs.get("coverage_score", 50) / 100,
            1 if inputs.get("caries_history") else 0,
            1 if inputs.get("gingivitis") else 0
        ]).reshape(1, -1)
        
        # 示例预测（实际应使用训练好的模型）
        dmatrix = xgb.DMatrix(features)
        pred = self.ml_model.predict(dmatrix)
        
        # 示例结果映射
        return {
            "must": ["fluoride_toothpaste"] if pred[0] > 0.7 else [],
            "suggest": ["mouthwash"],
            "avoid": ["hard_bristle"] if inputs.get("gingivitis") else []
        }