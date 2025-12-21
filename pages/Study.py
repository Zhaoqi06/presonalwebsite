import streamlit as st

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏", ["首页","任务查看","提交入口", "高等数学","线性代数","英语四级", "英语六级","雅思","TED","专四","专升本", "计算机","Python","C语言","MATLAB","STM32","51单片机","MYSQL","数学竞赛","英语竞赛","论文"])
if nav == "首页":
    st.markdown("<style>.stApp{background:linear-gradient(123deg,#F1FAEE 0%,#A8DADC 100%);}</style>",unsafe_allow_html=True)
    st.title("欢迎来到学习板块！")
    st.write("在这里有你想知道并且我们有的资料，点击左边导航栏查看详情！")
    st.divider()
    card1 = st.container(border = True)
    with card1:
        st.subheader("行课通知")
        st.write("由于授课结构调整，本次会有短期行课安排，行课时间为2025/12/22日开始的每周六下午，具体时间听从安排。")
        st.write("行课内容为 数学必修一 必修二 必修三 必修四 必修五 选修4-5.各位同学提前准备！")

elif nav == "论文":
    st.title("论文")
    with st.expander("智能流水车间调度与优化的仿真模拟——基于Python的遥控器生产线建模与优化"):
        st.subheader("第一届全国大学生仿真建模应用挑战赛")
        # 使用 pdf_viewer 替代 st.pdf()
        pdf_path = "document/ACSFJM2512633.pdf"
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_viewer(f.read(), width=700, height=600)
        else:
            st.error(f"PDF文件未找到：{pdf_path}")

