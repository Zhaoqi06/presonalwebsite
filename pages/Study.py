import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import os
from docx import Document

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏",
                           ["首页", "任务查看", "提交入口", "高等数学", "线性代数", "英语四级", "英语六级", "雅思",
                            "TED", "专四", "专升本", "计算机", "Python", "C语言", "MATLAB", "STM32", "51单片机",
                            "MYSQL", "数学竞赛", "英语竞赛", "论文"])
if nav == "首页":
    # st.markdown("<style>.stApp{background:linear-gradient(123deg,#F1FAEE 0%,#A8DADC 100%);}</style>",unsafe_allow_html=True)
    st.title("欢迎来到学习板块！")
    st.write("在这里有你想知道并且我们有的资料，点击左边导航栏查看详情！")

    st.divider()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docx_file_path = os.path.join(script_dir, "..", "vedio", "北大数学.mp4")
    video_path = os.path.normpath(docx_file_path)
    if os.path.exists(video_path):
        st.video(video_path, format="video/mp4", start_time=0,autoplay=True)
    else:
        st.error(f"视频文件未找到：{os.path.abspath(video_path)}")

  
elif nav == "论文":
    st.title("论文")
    with st.expander("智能流水车间调度与优化的仿真模拟——基于Python的遥控器生产线建模与优化"):
        st.subheader("第一届全国大学生仿真建模应用挑战赛")
        # 使用 pdf_viewer 替代 st.pdf()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        docx_file_path = os.path.join(script_dir, "..", "document", "ACSFJM2512633.pdf")
        pdf_path = os.path.normpath(docx_file_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")

    with st.expander("基于大数据分析的三种重大慢性病的相关风险评估与防控策略研究"):
        st.subheader("2025 年第十五届APMCM 亚太地区大学生数学建模竞赛（中文赛项）")
        # 使用 pdf_viewer 替代 st.pdf()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        docx_file_path = os.path.join(script_dir, "..", "document",
                                      "基于大数据分析的三种重大慢性病的相关风险评估与防控策略研究.pdf")
        pdf_path = os.path.normpath(docx_file_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")

    with st.expander("基于大数据分析的三种重大慢性病的相关风险评估与防控策略研究"):
        st.subheader("2025 年第七届中青杯全国大学生数学解模竞赛")
        # 使用 pdf_viewer 替代 st.pdf()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        docx_file_path = os.path.join(script_dir, "..", "document",
                                      "B202501829.pdf")
        pdf_path = os.path.normpath(docx_file_path)
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")
