import streamlit as st
import function as f
# ==================== 全局前置校验 ====================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

st.title("个人中心")
st.divider()

nav = st.sidebar.selectbox("导航栏", ["首页","修改密码和账户名"])
if nav == "首页":
    pass

elif nav == "修改密码和账户名":
    st.write("这是修改密码和账户名")
    username = st.text_input("请输入用户名：")
    password = st.text_input("请输入密码：", type="password")
    if st.button("修改"):
        if username == st.session_state["username"]:
            f.Updata_count_password(username, password)
            st.success("修改成功！")
        else:
            st.error("请输入自己用户名！")
else:
    st.write("请选择导航栏")