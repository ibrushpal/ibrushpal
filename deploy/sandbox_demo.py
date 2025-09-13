import streamlit as st
import numpy as np
import cv2
import os
import json
from PIL import Image
import time
import random
import matplotlib.pyplot as plt
import tempfile

# 设置页面配置
st.set_page_config(
    page_title="iBrushPal 爱伢伴 - 沙盒演示",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0078d4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #444;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #e6ffe6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff8e6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# 显示标题
st.markdown("<h1 class='main-header'>iBrushPal 爱伢伴 - AI口腔健康助手</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center'>沙盒演示环境 - 技术验证版本</p>", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.image("https://placehold.co/600x400/0078d4/ffffff?text=iBrushPal+爱伢伴", width=200)
    st.markdown("### 系统功能")
    st.markdown("- 🦷 牙齿区域检测")
    st.markdown("- 🧼 口腔清洁度评分")
    st.markdown("- 📊 刷牙覆盖率分析")
    st.markdown("- 📋 个性化刷牙方案")
    
    st.markdown("---")
    st.markdown("### 关于沙盒环境")
    st.markdown("这是一个技术验证环境，用于演示iBrushPal系统的核心功能。实际系统将部署在云服务器上，并通过小程序前端提供服务。")

# 创建标签页
tab1, tab2, tab3 = st.tabs(["数据采集", "AI分析", "个性化方案"])

# 标签页1：数据采集
with tab1:
    st.markdown("<h2 class='sub-header'>步骤1：数据采集</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 问卷信息")
        
        with st.form("questionnaire_form"):
            st.markdown("#### 基本信息")
            age = st.slider("年龄", 3, 80, 30)
            gender = st.radio("性别", ["男", "女"])
            
            st.markdown("#### 刷牙习惯")
            brushing_frequency = st.selectbox("每天刷牙次数", [1, 2, 3, "3次以上"])
            brushing_duration = st.selectbox("平均每次刷牙时长", ["少于1分钟", "1-2分钟", "2-3分钟", "3分钟以上"])
            
            st.markdown("#### 口腔健康状况")
            dental_issues = st.multiselect(
                "是否有以下口腔问题（可多选）",
                ["牙龈出血", "牙齿敏感", "口臭", "蛀牙史", "无"]
            )
            
            floss_use = st.checkbox("是否使用牙线")
            mouthwash_use = st.checkbox("是否使用漱口水")
            
            submit_questionnaire = st.form_submit_button("提交问卷")
    
    with col2:
        st.markdown("### 口腔照片/视频")
        
        upload_type = st.radio("上传类型", ["照片", "视频"])
        
        if upload_type == "照片":
            st.markdown("请上传3张口腔照片（正面、左侧、右侧）")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                front_photo = st.file_uploader("正面照", type=["jpg", "jpeg", "png"])
                if front_photo:
                    st.image(front_photo, caption="正面照", width=150)
            
            with col_b:
                left_photo = st.file_uploader("左侧照", type=["jpg", "jpeg", "png"])
                if left_photo:
                    st.image(left_photo, caption="左侧照", width=150)
            
            with col_c:
                right_photo = st.file_uploader("右侧照", type=["jpg", "jpeg", "png"])
                if right_photo:
                    st.image(right_photo, caption="右侧照", width=150)
            
            # 示例图片
            if not (front_photo or left_photo or right_photo):
                st.markdown("<p style='text-align: center'>示例图片：</p>", unsafe_allow_html=True)
                col_d, col_e, col_f = st.columns(3)
                with col_d:
                    st.image("https://placehold.co/300x200/dddddd/666666?text=正面照示例", width=150)
                with col_e:
                    st.image("https://placehold.co/300x200/dddddd/666666?text=左侧照示例", width=150)
                with col_f:
                    st.image("https://placehold.co/300x200/dddddd/666666?text=右侧照示例", width=150)
        else:
            st.markdown("请上传刷牙视频（不超过30秒）")
            video_file = st.file_uploader("刷牙视频", type=["mp4", "mov", "avi"])
            
            if video_file:
                # 创建临时文件
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(video_file.read())
                
                # 显示视频
                st.video(tfile.name)
                
                # 清理临时文件
                os.unlink(tfile.name)
            else:
                st.markdown("<p style='text-align: center'>示例视频：</p>", unsafe_allow_html=True)
                st.image("https://placehold.co/600x400/dddddd/666666?text=视频示例", width=300)
    
    # 提交按钮
    if st.button("提交数据进行分析", key="submit_data"):
        if submit_questionnaire or (front_photo and left_photo and right_photo) or video_file:
            st.session_state.data_submitted = True
            st.success("数据提交成功！请前往「AI分析」标签页查看分析结果。")
        else:
            st.warning("请至少完成问卷或上传照片/视频。")

# 标签页2：AI分析
with tab2:
    st.markdown("<h2 class='sub-header'>步骤2：AI分析</h2>", unsafe_allow_html=True)
    
    if not st.session_state.get("data_submitted", False):
        st.warning("请先在「数据采集」标签页提交数据。")
    else:
        # 模拟分析过程
        if st.button("开始AI分析", key="start_analysis"):
            with st.spinner("正在进行AI分析..."):
                # 模拟进度条
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.05)
                    progress_bar.progress(i + 1)
                
                # 设置分析完成状态
                st.session_state.analysis_completed = True
                st.success("分析完成！")
        
        # 显示分析结果
        if st.session_state.get("analysis_completed", False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 牙齿区域检测")
                
                # 模拟牙齿检测结果图
                fig, ax = plt.subplots(figsize=(8, 6))
                
                # 创建一个示例图像
                img = np.ones((400, 600, 3), dtype=np.uint8) * 240
                
                # 绘制牙齿轮廓
                teeth_positions = [
                    (150, 200, 50, 30),  # x, y, width, height
                    (210, 200, 50, 30),
                    (270, 200, 50, 30),
                    (330, 200, 50, 30),
                    (390, 200, 50, 30),
                    (150, 250, 50, 30),
                    (210, 250, 50, 30),
                    (270, 250, 50, 30),
                    (330, 250, 50, 30),
                    (390, 250, 50, 30)
                ]
                
                for i, (x, y, w, h) in enumerate(teeth_positions):
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, f"T{i+1}", (x+5, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                ax.axis('off')
                st.pyplot(fig)
                
                st.markdown("**检测结果：**")
                st.markdown("- 检测到牙齿数量：28")
                st.markdown("- 检测置信度：92%")
            
            with col2:
                st.markdown("### 清洁度评分")
                
                # 模拟清洁度评分
                cleanliness_score = random.randint(65, 85)
                
                # 创建仪表盘
                fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(polar=True))
                
                # 设置仪表盘参数
                theta = np.linspace(0, np.pi, 100)
                r = np.ones_like(theta)
                
                # 绘制仪表盘背景
                ax.fill_between(theta, 0, r, color='lightgray', alpha=0.5)
                
                # 绘制得分区域
                score_theta = np.linspace(0, np.pi * cleanliness_score / 100, 100)
                ax.fill_between(score_theta, 0, r[:len(score_theta)], color='skyblue', alpha=0.8)
                
                # 设置刻度
                ax.set_xticks(np.linspace(0, np.pi, 5))
                ax.set_xticklabels(['0', '25', '50', '75', '100'])
                ax.set_yticks([])
                
                # 添加得分文本
                ax.text(np.pi/2, 0.5, f"{cleanliness_score}", 
                        ha='center', va='center', fontsize=24, fontweight='bold')
                ax.text(np.pi/2, 0.3, "清洁度评分", ha='center', va='center', fontsize=12)
                
                st.pyplot(fig)
                
                # 区域详细评分
                st.markdown("**区域详细评分：**")
                
                area_scores = {
                    "前牙区": random.randint(70, 90),
                    "左侧磨牙区": random.randint(60, 80),
                    "右侧磨牙区": random.randint(60, 80),
                    "上颌": random.randint(65, 85),
                    "下颌": random.randint(65, 85)
                }
                
                for area, score in area_scores.items():
                    st.markdown(f"- {area}：{score}分")
                
                # 风险标记
                st.markdown("**风险区域：**")
                if min(area_scores.values()) < 70:
                    risk_area = min(area_scores.items(), key=lambda x: x[1])[0]
                    st.markdown(f"⚠️ {risk_area}（{min(area_scores.values())}分）需要额外关注")
                else:
                    st.markdown("✅ 未发现明显风险区域")
            
            # 刷牙覆盖率分析（如果上传了视频）
            if st.session_state.get("video_uploaded", False):
                st.markdown("### 刷牙覆盖率分析")
                
                # 模拟覆盖率数据
                coverage_data = {
                    "上前牙": random.randint(70, 95),
                    "上左侧": random.randint(60, 90),
                    "上右侧": random.randint(60, 90),
                    "下前牙": random.randint(70, 95),
                    "下左侧": random.randint(60, 90),
                    "下右侧": random.randint(60, 90)
                }
                
                # 创建条形图
                fig, ax = plt.subplots(figsize=(8, 4))
                areas = list(coverage_data.keys())
                scores = list(coverage_data.values())
                
                # 设置条形颜色
                colors = ['green' if s >= 80 else 'orange' if s >= 70 else 'red' for s in scores]
                
                ax.bar(areas, scores, color=colors)
                ax.set_ylim(0, 100)
                ax.set_ylabel('覆盖率 (%)')
                ax.set_title('刷牙覆盖率分析')
                
                # 添加数值标签
                for i, v in enumerate(scores):
                    ax.text(i, v + 3, str(v), ha='center')
                
                st.pyplot(fig)
                
                # 平均覆盖率
                avg_coverage = sum(coverage_data.values()) / len(coverage_data)
                st.markdown(f"**平均覆盖率：** {avg_coverage:.1f}%")
                
                # 覆盖率评价
                if avg_coverage >= 85:
                    st.markdown("**评价：** 优秀 ✅")
                elif avg_coverage >= 75:
                    st.markdown("**评价：** 良好 👍")
                elif avg_coverage >= 65:
                    st.markdown("**评价：** 一般 ⚠️")
                else:
                    st.markdown("**评价：** 需要改进 ❗")

# 标签页3：个性化方案
with tab3:
    st.markdown("<h2 class='sub-header'>步骤3：个性化刷牙方案</h2>", unsafe_allow_html=True)
    
    if not st.session_state.get("analysis_completed", False):
        st.warning("请先完成「AI分析」。")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 个性化建议")
            
            # 模拟个性化建议
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.markdown("#### 核心建议")
            st.markdown("- **刷牙时长：** 建议每次刷牙时间不少于2分钟")
            st.markdown("- **刷牙频率：** 每天至少2次，早晚各一次")
            st.markdown("- **重点区域：** 左下磨牙区需要额外关注，建议使用巴氏刷牙法")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='success-box'>", unsafe_allow_html=True)
            st.markdown("#### 推荐使用")
            st.markdown("- **牙刷类型：** 软毛牙刷")
            st.markdown("- **牙膏选择：** 含氟牙膏")
            st.markdown("- **辅助工具：** 牙线、牙间刷")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
            st.markdown("#### 注意事项")
            st.markdown("- 避免使用硬毛牙刷，可能损伤牙龈")
            st.markdown("- 刷牙力度适中，避免过度用力")
            st.markdown("- 定期更换牙刷，建议2-3个月更换一次")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 刷牙动画指导")
            
            # 模拟动画（使用图片代替）
            st.image("https://placehold.co/400x300/dddddd/666666?text=刷牙动画示例", width=250)
            
            # 添加动画控制按钮（模拟）
            st.button("播放动画", key="play_animation")
            st.button("暂停动画", key="pause_animation")
            
            # 添加动画说明
            st.markdown("**动画说明：**")
            st.markdown("此动画展示了巴氏刷牙法的正确姿势和动作，特别强调了左下磨牙区的刷牙技巧。")
    
    # 添加下载报告按钮
    if st.session_state.get("analysis_completed", False):
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 保存分析报告")
            st.markdown("您可以下载完整的分析报告，包含所有评分数据和个性化建议。")
        
        with col2:
            if st.button("下载PDF报告", key="download_report"):
                # 模拟下载过程
                with st.spinner("正在生成报告..."):
                    time.sleep(2)
                    st.success("报告已生成！")
                    
                    # 创建下载链接（模拟）
                    st.markdown("[点击此处下载报告](https://example.com/report.pdf)")

# 页脚
st.markdown("---")
st.markdown("<p class='footer'>© 2025 iBrushPal 爱伢伴 | 技术支持：CodeBuddy</p>", unsafe_allow_html=True)