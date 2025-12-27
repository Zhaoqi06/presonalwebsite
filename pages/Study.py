import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import os
# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏", ["首页","任务查看","提交入口", "高等数学","线性代数","英语四级", "英语六级","雅思","TED","专四","专升本", "计算机","Python","C语言","MATLAB","STM32","51单片机","MYSQL","数学竞赛","英语竞赛","论文"])
if nav == "首页":
    #st.    #st.markdown("<style>.stApp{background:linear-gradient(123deg,#F1FAEE 0%,#A8DADC 100%);}</style>",unsafe_allow_ht
    st.title("欢迎来到学习板块！")
    st.write("在这里有你想知道并且我们有的资料，点击左边导航栏查看详情！")

    st.divider()
    card_file_path = "document\card_file.txt"
    with open(card_file_path, 'r', encoding="utf-8") as f:
        data = f.readlines()
        new_title = []
        new_text = []
        new_time = []

        for line in data:
            if line[:2] == "标题":
                new_title.append(line[3:].strip())
            if line[:2] == "文本":
                new_text.append(line[3:].strip())
            if line[:2] == "时间":
                new_time.append(line[3:].strip())

    card = st.container(border=True)
    # 获取三个列表中最短的长度，避免索引越界
    min_length = min(len(new_title), len(new_text), len(new_time))
    for i in range(min_length):  # 使用 min_length 而不是 len(new_title)
        card_name = "card" + str(i + 1)
        card = st.container(border=True)
        with card:
            st.subheader(new_title[i])
            st.write(new_text[i])
            st.write(f"时间：{new_time[i]}")
            f.close()




elif nav == "论文":
    st.title("论文")
    with st.expander("智能流水车间调度与优化的仿真模拟——基于Python的遥控器生产线建模与优化"):
        st.subheader("第一届全国大学生仿真建模应用挑战赛")
        # 使用 pdf_viewer 替代 st.pdf()
        pdf_path = "document\ACSFJM2512633.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")
