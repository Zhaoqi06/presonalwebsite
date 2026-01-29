import streamlit as st
import function as f

if "invite_number" not in st.session_state:
    st.session_state["invite_number_register"] = ""  # 用session_state保存邀请码


# 隐藏默认导航/水印
st.markdown("""
    <style>
    .css-14xtw13,.css-1v3fvcr{display:none !important;}
    /* 优化表单样式 */
    .stForm {border: none !important; padding: 2rem; background-color: #f8f9fa; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

f.init_count_password_table()
information = f.read_count_password()
user_data = {}
for info in information:
    user_data[info["username"]] = info["password"]

st.title("注册系统")
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("用户名", placeholder="请输入您的姓名",key="username_input")
    password = st.text_input("密码", type="password", placeholder="请输入您的密码", key="password_input")
    invite_number = st.text_input("邀请码", type="password", placeholder="请输入您的邀请码", key="invite_input")
    submit_register = st.form_submit_button("注册", type="primary")

if submit_register:
    # 实时更新session_state（输入框内容变化时同步）
    st.session_state["invite_number_register"] = invite_number

    if username not in user_data:
        if not username.strip() or not password.strip():
            st.error("用户名和密码不能为空！")
        elif not invite_number.strip():
            st.error("邀请码不能为空！")
        elif invite_number.strip() == str(f.get_daily_invite_num()):
            f.write_count_password(username, password)
            st.success("注册成功！")
            # 3. 重置状态（清空输入框+重置邀请码状态）
            st.session_state["invite_number_register"] = ""
            st.switch_page("pages/login.py")

        else:
            st.error("邀请码错误！")
    else:
        st.error("用户名已存在！")