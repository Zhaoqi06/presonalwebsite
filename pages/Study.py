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

    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docx_file_path = os.path.join(script_dir, "..", "document", "notifications.docx")
    docx_file_path = os.path.normpath(docx_file_path)

    # 从 docx 文件读取通知内容
    titles = []
    texts = []
    times = []

    try:
        if os.path.exists(docx_file_path):
            doc = Document(docx_file_path)

            # 遍历文档中的所有段落
            i = 0
            while i < len(doc.paragraphs):
                para = doc.paragraphs[i]

                # 查找标题段落
                if para.text.startswith("标题:"):
                    title = para.text[3:].strip()  # 去掉"标题:"前缀
                    titles.append(title)

                    # 查找下一个文本段落
                    if i + 1 < len(doc.paragraphs):
                        content_para = doc.paragraphs[i + 1]
                        if content_para.text.startswith("文本:"):
                            text = content_para.text[3:].strip()
                            texts.append(text)
                        else:
                            texts.append("")  # 如果没有找到文本段落，添加空字符串
                    else:
                        texts.append("")

                    # 查找下一个时间段落
                    if i + 2 < len(doc.paragraphs):
                        time_para = doc.paragraphs[i + 2]
                        if time_para.text.startswith("时间:"):
                            time = time_para.text[3:].strip()
                            times.append(time)
                        else:
                            times.append("")  # 如果没有找到时间段落，添加空字符串
                    else:
                        times.append("")

                    # 跳过当前通知块（标题、内容、时间、分隔线共4段）
                    i += 4
                    continue
                else:
                    i += 1
        else:
            st.info("暂无通知")
    except Exception as e:
        st.error(f"读取通知文件失败：{str(e)}")

    # 显示通知卡片
    # 获取三个列表中最短的长度，避免索引越界
    min_length = min(len(titles), len(texts), len(times))
    for i in range(min_length):
        card_name = "card" + str(i + 1)
        card = st.container(border=True)
        with card:
            st.subheader(titles[i])
            st.write(texts[i])
            st.write(f"时间：{times[i]}")

elif nav == "论文":
    st.title("论文")
    with st.expander("智能流水车间调度与优化的仿真模拟——基于Python的遥控器生产线建模与优化"):
        st.subheader("第一届全国大学生仿真建模应用挑战赛")
        # 使用 pdf_viewer 替代 st.pdf()
        pdf_path = r"D:\pycharm\Application\personalwebsite\document\ACSFJM2512633.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")
