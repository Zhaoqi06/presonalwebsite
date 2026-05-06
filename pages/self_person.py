import streamlit as st
import function as f
# ==================== 全局前置校验 ====================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

if "change_password" not in st.session_state:
    st.session_state["change_password"] = ""

if "change_username" not in st.session_state:
    st.session_state["change_username"] = ""
st.title("个人中心")
st.divider()
f.init_count_password_table()
nav = st.sidebar.selectbox("导航栏", ["首页","荣誉"])
ADMIN_USER = "刘钊齐"

if nav == "首页":
    st.write("修改账户名以及密码")
    st.session_state["change_username"] = st.text_input("请输入用户名：")
    st.session_state["change_password"] = st.text_input("请输入密码：", type="password")
    if st.button("修改"):
        if st.session_state["change_username"] == st.session_state["username"]:
            f.Updata_count_password(st.session_state["change_username"], st.session_state["change_password"])
            st.success("修改成功！")
        else:
            st.error("请输入自己用户名！")
            st.session_state["change_username"] = ""
            st.session_state["change_password"] = ""

if nav == "荣誉":
    if ADMIN_USER == st.session_state["username"]:
        st.header("获奖情况")
        certificates = [
        {
            "image":"./image/1.jpg",
            "title1":"第五届四川省中华职业教育创新创业大赛",
            "title2":"省级 三等奖",
        },
        {
            "image":"./image/2.jpg",
            "title1":"中国国际大学生创新大赛（2025）",
            "title2":"校级 一等奖",
        },
        {
            "image":"./image/3.jpg",
            "title1":"第五届四川省中华职业教育创新创业大赛",
            "title2":"校级 二等奖",
        },
        {
            "image":"./image/4.jpg",
            "title1":"2025全国大学生仿真建模应用挑战赛",
            "title2":"国家级 三等奖",
        },
        {
            "image":"./image/5.jpg",
            "title1":"2024年四川信息职业技术学院人工智能优秀案例评选",
            "title2":"校级 三等奖",
        },
        {
            "image":"./image/6.jpg",
            "title1":"中国国际大学生创新大赛（2025）",
            "title2":"省级 金奖",
        },
        {
            "image":"./image/7.jpg",
            "title1":"第五届四川省中华职业教育创新创业大赛",
            "title2":"校级 一等奖",
        },
        {
            "image":"./image/8.jpg",
            "title1":"第五届四川省中华职业教育创新创业大赛",
            "title2":"校级 二等奖",
        },
        {
            "image":"./image/9.jpg",
            "title1":"2025年APMCM亚太地区大学生数学建模竞赛",
            "title2":"国家级 三等奖",
        },
        {
            "image":"./image/10.jpg",
            "title1":"第三届四川信息职业技术学院数学建模竞赛",
            "title2":"校级 一等奖",
        },
        {
            "image":"./image/11.jpg",
            "title1":"中国国际大学生创新大赛（2025）",
            "title2":"省级 银奖",
        },
        {
            "image":"./image/12.jpg",
            "title1":"中国国际大学生创新大赛（2025）",
            "title2":"校级 一等奖",
        },
        {
            "image":"./image/13.jpg",
            "title1":"第三届全国大学生职业规划大赛",
            "title2":"校级 二等奖",
        },
        {
            "image":"./image/14.jpg",
            "title1":"广元市新媒体联盟通讯员聘书",
            "title2":"广元团市委新媒体中心实习",
        },
        {
            "image":"./image/15.jpg",
            "title1":"2025第十五届MathorCup数学应用挑战赛",
            "title2":"国家级 成功参赛奖",
        },
        {
            "image":"./image/16.jpg",
            "title1": "中国国际大学生创新大赛（2025）",
            "title2": "省级 铜奖",

        },
        {
            "image":"./image/2024-2025国家励志奖学金.png",
            "title1": "2024-2025年度国家励志奖学金",
            "title2": "国家级",

        },
        {
            "image":"./image/25仿真认定表.jpg",
            "title1": "全国大学生仿真建模应用挑战赛",
            "title2": "竞赛训练审批表",

        },
        {
            "image":"./image/2024传统文化证书.jpg",
            "title1": "第二届全国大学生传统文化水平竞赛",
            "title2": "荣誉证书",

        },
        {
            "image":"./image/2024金融荣誉证书.jpg",
            "title1":"2024年全国大学生金融素养知识竞赛",
            "title2":"晋级证书",
        },
        {
            "image":"./image/全国大学生创新创业联盟协会2025三等奖.JPG",
            "title1":"全国大学生创新创业联盟协会（2025）暨“人工智能+”产学研融合发展论坛“AI+”优秀项目评比",
            "title2":"国家级 三等奖",
        },
        {
            "image":"./image/博爱四川.jpg",
            "title1":"第二届“博爱四川”红十字运动知识大赛",
            "title2":"初赛 100分",
        },
        {
            "image":"./image/第七届中青杯数学建模 本科二等.png",
            "title1":"2025年第七届中青杯全国大学生数学建模竞赛",
            "title2":"国家级 三等奖",
        },
        {
            "image":"./image/计算机一级MS Office.jpg",
            "title1":"计算机一级MS Office",
            "title2":"成绩 合格",
        },
        {
            "image":"./image/计算机一级WPS Office.jpg",
            "title1":"计算机一级WPS Office",
            "title2":"成绩 良好",
        },
        {
            "image":"./image/实习.jpg",
            "title1":"广元市新媒体联盟通讯员实习证明",
            "title2":"广元团市委新媒体中心实习",
        },
        {
            "image":"./image/中国仿真学会证书.jpg",
            "title1":"中国仿真学会",
            "title2":"中国仿真学会学生会员电子证",
        },
        {
            "image":"./image/2025数维杯秋季赛.jpg",
            "title1":"ShuWei Cup IMCMCertificate of Achievement",
            "title2":"Successful Participant",
        },
        {
            "image":"./image/第三届四川省大学生职业规划大赛.png",
            "title1":"第三届全国大学生职业规划大赛",
            "title2":"省级金奖",
        },
        ]

        st.markdown(
            """
            <style>
            img {
                object-fit: contain !important;
                max-height: 500px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        for i,cert in enumerate(certificates):
            st.image(cert["image"],use_container_width=False )
            st.markdown(f"**奖项：** {cert['title1']}")
            st.markdown(f"**等级：** {cert['title2']}")

            try:
                with open(cert["image"],"rb") as f:
                    st.download_button(
                        label = "下载",
                        data = f,
                        file_name = cert["title1"],
                        mime = "image/jpeg",
                        key = f"download_{i}"
                    )
            except:
                st.error(f"找不到图片：{cert['image']}")
            st.divider()
