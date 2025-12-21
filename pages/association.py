import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import os
st.set_page_config(page_title="协会", layout="wide")

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏", ["首页","协会成员", "活动风采","照片", "奖状"])

if nav == "首页":
    st.title("国际交流协会")
    st.write(
        "四川信息职业技术学院国际交流协会，宛如一座璀璨的文化桥梁，搭建起学院与国际的沟通之路。协会成立于2014，自诞生起，就以跨越信息边界，共筑国际交流为宗旨，积极推动学院在国际舞台上绽放光彩。")
    st.divider()
    video_path = "vedio/一带一路英文_20251219_09504850.mp4"
    if os.path.exists(video_path):
        st.video(video_path, format="video/mp4", start_time=0,autoplay=True)
    else:
        st.error(f"视频文件未找到：{os.path.abspath(video_path)}")


elif nav == "协会成员":
    file_Path = "document/协会现有成员信息表.xlsx"
    file_data = pd.read_excel(file_Path, engine='openpyxl')
    try:
        # 成员数量
        length = len(file_data.iloc[:, 6])
        temp_length = 0
        for i in range(length):
            if file_data.iloc[i, 6] != 1:
                temp_length += 1
            else:
                break
        length = temp_length
        # 主键数据唯一性标识
        name = []
        id = []
        identity = []
        for i in range(length):
            name.append(file_data.iloc[i, 6])
            id.append(str(file_data.iloc[i, 5]))
            identity.append(file_data.iloc[i, 9])
        Mark = file_data.iloc[:, 6]
        def Name():
            return name
        def ID():
            return id
        def Identity():
            return identity
    except:
        print(e)
    # -------------------------------------------------------------------------------------
    st.title("国际交流协会成员信息表")
    st.write("#### 国际交流协会负责人信息")
    st.table(data={
        '姓名：': ['刘钊齐'],
        '学号：': ['24407077'],
        '联系方式：': [19130786589],
        '职务：': ['协会负责人'],
        '班级：': ['智控24-2'],
    })
    st.divider()
    st.write("#### 国际交流协会成员信息")
    df = pd.DataFrame(data={
        '姓名：': Name(),
        '学号：': ID(),
        '社团职务': Identity()
    })
    st.dataframe(df, use_container_width=True)
    st.divider()
    st.write("#### 内部成员信息核对")


elif nav == "活动风采":
    st.title("协会活动")
    st.write("新任主席上任以来所接手的所有活动")

    st.divider()
    st.markdown("#### <center>**2025年10月10日迎接2025级国际新生志愿活动**</center>", unsafe_allow_html=True)
    st.markdown(
        "&emsp;&emsp;2025年10月10日在31名四川信息职业技术学院雪峰校区开展迎新活动，在全体师生的共同努力下圆满结束,不仅为新生们营造了一个温馨、热情的入学氛围,也展现了学校的凝聚力和向心力。活动前期,我们进行了周密的筹备工作,包括场地布置、物资准备、人员分工等,确保每一个细节都能体现对新生的关怀。&emsp;&emsp;<br>&emsp;&emsp;活动中,志愿者们积极投入,耐心解答新生疑问,引导他们完成报到手续,并详细介绍校园环境和生活设施。迎新活动圆满落幕,我们见证了新成员们从陌生到熟悉的转变过程。活动中,我们注重互动与交流,通过才艺展示、互动问答等环节,让新成员们充分展示自我,增进彼此的了解。同时,我们也为新成员们准备了丰富的迎新礼包和贴心的生活指南,帮助他们更快地适应新环境。此次迎新活动不仅让新成员们感受到了学校的温暖与关怀,也激发了他们对未来学习生活的热情与憧憬。例如,部分环节衔接不够流畅,部分志愿者对新生报到流程不够熟悉,导致出现了一些小混乱。未来,我们将总结经验教训,进一步优化迎新流程,提高活动效率和质量。",
        unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(
            "image/迎新.jpeg",
            caption='迎新活动照片')
    col_left, col_right = st.columns([7, 3])
    with col_right:
        st.write("国际交流协会")
        st.write("2025年10月10日")

    st.divider()
    st.markdown("#### <center>**2025年11月1日国际交流协会“认识你很高兴”破冰活动总结**</center>", unsafe_allow_html=True)
    st.markdown("&emsp;&emsp;2025年11月1日14：00～15：30在雪峰校区电气楼2312国际交流协会联合自动化协会成功举办“认识你很高兴”破冰活动，协会"
                "与自动化协会内部中国籍成员与在校国际学生共同参与，协会成员共59人，其中本协会39人，自动化协会20人。本协会活动促进新老成员交流、拓宽"
                "交际圈，推动中外学生友好互动。&emsp;&emsp;<br>&emsp;&emsp;活动前期，工作人员提前完成场地布置、奖品采购、指令盲盒准备等工作"
                "，14:10-14:20参与成员有序签到。14:20-14:50开展“红蓝指令盲盒”活动，成员分为红蓝阵营（中国籍成员为红方、国际学生为蓝方），"
                "通过抽取箱子中的互动指令完成交流任务，完成者获得小挂件、圆珠笔等奖励；在才艺表演环节，表现突出的同学获得毛绒玩偶奖励；开展“击鼓传花"
                "”活动，接到“炸弹玩偶”的成员上台表演或接受挑战。活动结束，工作人员组织清理场地卫生，确保场地恢复整洁。&emsp;&emsp;<br>&emsp;&emsp;活动全程秩序井然，安全保障到"
                "位，活动有效促进了协会成员间的相互认识，为中外学生文化交流搭建了良好平台，丰富了大家的校园生活。",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(
            "image/破冰.jpg",
            caption='破冰活动照片')
    col_left, col_right = st.columns([7, 3])
    with col_right:
        st.write("国际交流协会")
        st.write("2025年11月1日")

    st.divider()
    st.markdown("#### <center>**2025年12月4日国际交流协会“剪韵传世界·非遗架心桥”活动总结**</center>",
                unsafe_allow_html=True)
    st.markdown("&emsp;&emsp;2025年12月4日14:00-15:30，国际交流协会在雪峰校区图书馆成功举办“剪韵传世界·非遗架心桥”非遗剪纸交流活"
                "动，协会内部成员33人全程参与。活动以非遗剪纸文化为核心，分为三大板块有序开展：14:00-14:10完成前期工作安排，确保活动顺利启动"
                "；14:10-14:20，指导老师详细讲解剪纸历史文化知识，让成员深入了解非遗魅力；14:20-14:40，老师示范剪纸基础技法，耐心指导成员掌握"
                "核心技巧；14:40-15:20为实践创作环节，成员们动手制作剪纸及相关文创作品，尽情展现创意与动手能力；15:20-15:30活动总结收尾，成员们"
                "展示作品、交流心得，随后共同完成场地卫生清洁。&emsp;&emsp;<br>&emsp;&emsp;活动全程严格遵守纪律要求，无中途私自离席情况，安全"
                "保障组按分工落实治安、消防、交通秩序维护及突发事件处置准备，确保活动安全有序。通过本次活动，中外学生不仅学习了剪纸技艺、传承了非遗文化"
                "，更搭建了友好交流的桥梁，增强了协会凝聚力与文化认同感，有效提升了成员的文化沟通与交际能力。",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(
            "image/剪纸.jpeg",
            caption='非遗剪纸交流活动照片')
    col_left, col_right = st.columns([7, 3])
    with col_right:
        st.write("国际交流协会")
        st.write("2025年12月4日")


elif nav == "照片":
    st.title("照片")
elif nav == "奖状":
    st.title("奖状")


