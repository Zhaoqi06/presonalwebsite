import streamlit as st
import function as f
# 设置页面配置（必须放在最前面）
st.set_page_config(page_title="登录", page_icon=":lock:", layout="centered")

# 初始化session状态
if "is_login" not in st.session_state:
    st.session_state["is_login"] = False
if "logged_in" not in st.session_state:  # 统一登录状态标识
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""
# 隐藏默认导航/水印
st.markdown("""
    <style>
    .css-14xtw13,.css-1v3fvcr{display:none !important;}
    /* 优化表单样式 */
    .stForm {border: none !important; padding: 2rem; background-color: #f8f9fa; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

information = f.read_count_password()
user_data = {}
for info in information:
    user_data[info["username"]] = info["password"]

# 登录表单
st.title("登录系统")
with st.form("login_form", clear_on_submit=False):
    st.session_state["username"] = st.text_input("用户名", placeholder="请输入您的姓名", value="")
    st.session_state["password"] = st.text_input("密码", type="password", placeholder="请输入您的密码", value="")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        submit_login = st.form_submit_button("登录", type="primary")
    with col_btn2:
        submit_register = st.form_submit_button("注册", type="primary")

if submit_login:
    if not st.session_state["username"].strip() or not st.session_state["password"].strip():
        st.error("用户名和密码不能为空！")
    else:
        # 验证用户名和密码
        if st.session_state["username"] in user_data:
            if user_data[st.session_state["username"]] == st.session_state["password"]:
                # 更新登录状态
                st.session_state["logged_in"] = True
                st.session_state["is_login"] = True
                st.success(f"欢迎 {st.session_state["username"]}！登录成功，即将跳转...")

                try:
                    st.switch_page("streamlit_app.py")
                except Exception as e:
                    st.warning(f"跳转失败，请手动访问主页面：{str(e)}")
            else:
                st.error("密码错误，请检查您的ID号！")
                st.session_state["username"] = ""
        else:
            st.error("用户名不存在，请检查您的姓名！")
            st.session_state["username"] = ""

if submit_register:
    st.switch_page("pages/register.py")