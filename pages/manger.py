import streamlit as st
from datetime import datetime
import function as f
import pandas as pd

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
    nav = st.sidebar.selectbox("导航栏", ["分布通知", "查看用户及密码","增删成员","查看邀请码"])

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
        with col2:
            if st.button("删除"):
                f.delete_count_password(username)
                st.success("删除成功！")
    if nav == "查看邀请码":
        st.header("查看邀请码")
        st.success(f.get_daily_invite_num())

else:
    st.error("非管理员人员不能进入该页面")