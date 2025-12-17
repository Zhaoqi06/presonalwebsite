# 导入
import streamlit as st

if "is_login" not in st.session_state:
    st.session_state.is_login = False
st.set_page_config(page_title="登录",page_icon=":lock:",layout="centered")
#隐藏默认导航/水印
st.markdown("""
            <style>
            .css-14xtw13,.css-1v3fvcr{display:none !important;}
            </style>
              """, unsafe_allow_html=True)
#登录表单
st.title("登录")
with st.form("login"):
    username = st.text_input("用户名",placeholder="请输入用户名")
    password = st.text_input("密码",type="password",placeholder="请输入密码")
    submit = st.form_submit_button("登录",type = "primary")

#校验+保存（核心：session_state)
valid_users = {"刘钊齐":"24407077","user1":"user123"}
if submit:
    if username in valid_users and valid_users[username] == password:
        st.success("登录成功")
        st.session_state["is_login"]=True
        st.session_state["username"] = username
        st.success("登录成功，跳转中.....")
        st.markdown('<meta http-equiv="refresh" content="1;URL=/" />', unsafe_allow_html=True)
        st.error("用户名或密码错误")
