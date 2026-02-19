import streamlit as st
from datetime import datetime
import function as f
import pandas as pd
import time
# ==================== 全局前置校验 ====================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 隐藏默认导航/水印
st.markdown("""
    <style>
    .css-14xtw13,.css-1v3fvcr{display:none !important;}
    </style>
""", unsafe_allow_html=True)


# ==================== 页面逻辑 ====================
f.init_notification_table()

ADMIN_USER = "刘钊齐"
if ADMIN_USER == st.session_state["username"]:
    st.title("欢迎进入管理页面")
    st.divider()
    nav = st.sidebar.selectbox("导航栏", ["分布通知", "查看用户及密码","增删成员","查看邀请码","麻将成员管理"])

    if nav == "分布通知":
        # 发布通知模块
        st.header("发布通知")
        with st.form("input_form", clear_on_submit=True):
            title_input = st.text_input("标题")
            text_input = st.text_area("文本")
            time_input = st.date_input("时间", value=datetime.now().date())
            submit_publish = st.form_submit_button("发布通知")

        if submit_publish:
            if not title_input or not text_input or not time_input:
                st.error("请填写完整的信息！")
            else:
                f.write_notification(title_input, text_input, time_input)
                st.success("发布成功")
                time.sleep(1)
                st.rerun()

        st.divider()

        # 删除通知模块
        st.header("删除通知")
        st.subheader("现有通知列表")
        notifications = f.read_notifications()
        if notifications:
            for notice in notifications:
                st.write(f"ID：{notice['id']} | 标题：{notice['title']} | 时间：{notice['time']}")
        else:
            st.info("暂无通知数据")

        with st.form("delete_form"):
            id_input = st.text_input("输入要删除的通知ID（数字）")
            submit_delete = st.form_submit_button("删除通知")

        if submit_delete:
            if not id_input:
                st.error("请输入要删除的通知ID！")
            else:
                f.delete_notification(id=id_input)
                st.success("删除成功")
                time.sleep(1)
                st.rerun()
    if nav == "查看用户及密码":
        st.header("网站所有用户及密码")
        user = []
        password = []
        f.init_count_password_table()
        information = f.read_count_password()
        for info in information:
            user.append(info["username"])
            password.append(info["password"])

        df = pd.DataFrame(data={
            '用户名：': user,
            '密码：': password,
        })
        st.dataframe(df, use_container_width=True)
        st.divider()
        st.title("更改密码")
        username = st.text_input("请输入用户名：")
        password = st.text_input("请输入密码：", type="password")
        if st.button("修改"):
            if username in user:
                f.Updata_count_password(username, password)
                st.success("修改成功！")
                time.sleep(1)
                st.rerun()

            else:
                st.error("用户名不存在！")

    if nav == "增删成员":
        st.header("增删成员")
        f.init_count_password_table()
        information = f.read_count_password()
        invite_number = f.get_daily_invite_num()

        for info in information:
            username = info["username"]
            password = info["password"]
            user_data = {"valid_map": {username: password}}
        username = st.text_input("请输入用户名：")
        password = st.text_input("请输入密码：", type="password")
        col1, col2 ,col3= st.columns([1, 1,8])
        with col1:
            if st.button("添加"):
                if username in user_data["valid_map"]:
                    st.error("用户名已存在！")
                else:
                    f.write_count_password(username, password)
                    st.success("添加成功！")
                    time.sleep(1)
                    st.rerun()
        with col2:
            if st.button("删除"):
                f.delete_count_password(username)
                st.rerun()
                st.success("删除成功！")
    if nav == "查看邀请码":
        st.header("查看邀请码")
        st.success(f.get_daily_invite_num())

    if nav == "麻将成员管理":
        st.header("在这里管理麻将成员信息")
        st.write("注意该页面最好在GITHUB上运行，每天数据会自动清除，本地不会！！！")
        st.divider()

        f.get_db_connection_count_password()
        f.init_count_majiang()
        f.init_count_password_table()

        st.write("添加成员，一次只能添加四个")
        information = f.read_majiang()
        temp = f.read_count_password()
        user = []
        score = []
        username_majiang = []
        for info in temp:
            if "username" in info:
                username_majiang.append(info["username"])

        for info in information:
            user.append(info["username"])
            score.append(info.get("score", info.get("socre", 0)))

            # 展示成员列表
        if user:
            df = pd.DataFrame(data={
                '用户名：': user,
                '得分：': score,
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.success("当前无麻将搭子")
        st.write("添加搭子")
        col1, col2 = st.columns([1, 1])
        with col1:
            name = st.text_input("姓名（添加）", placeholder="请输入姓名", key="add_name")
        with col2:
            score_add = st.number_input("默认得分为 0 ", value=0, key="add_score")  # 变量名区分，避免覆盖

        if st.button("添加", type="primary", key="btn_add"):
            if len(user) >= 4:
                st.error("最多只能添加4个麻将搭子！")
            elif name not in username_majiang:
                st.error("该用户未注册账户！")
            elif name in user:
                st.error("名字重复！")
            else:
                f.write_majiang(name, score_add)
                st.success("写入成功")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()

        st.divider()

        st.write("删除搭子")
        name_del = st.text_input("姓名（删除）", placeholder="请输入姓名", key="del_name")
        if st.button("删除", type="primary", key="btn_del"):
            if name_del in user:
                f.delete_majiang(name_del)
                st.success("删除成功")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()
            else:
                st.error("该用户不是你的搭子！")

        st.divider()

        # 清除得分数据区域
        st.write("清除得分数据")
        if st.button("清除得分数据", type="primary", key="btn_clear"):
            for username in user:
                f.Updata_majiang(username, 0)
            st.success("清除成功！")
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()
else:
    st.error("非管理员人员不能进入该页面")