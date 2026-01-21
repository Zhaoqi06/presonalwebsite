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
user_data = {"valid_map": {}}
for info in information:
    username = info["username"]
    password = info["password"]
    user_data = {"valid_map": {username: password}}

# 登录表单
st.title("登录系统")
with st.form("login_form", clear_on_submit=False):
    username = st.text_input("用户名", placeholder="请输入您的姓名", value="")
    password = st.text_input("密码", type="password", placeholder="请输入您的ID号", value="")
    submit_btn = st.form_submit_button("登录", type="primary")

# 登录验证逻辑
if submit_btn:
    # 空值检查
    if not username.strip() or not password.strip():
        st.error("用户名和密码不能为空！")
    else:
        # 验证用户名和密码
        if username in user_data["valid_map"]:
            if user_data["valid_map"][username] == password:
                # 更新登录状态
                st.session_state["logged_in"] = True
                st.session_state["is_login"] = True  # 保持兼容
                st.session_state["username"] = username
                st.success(f"欢迎 {username}！登录成功，即将跳转...")
                
                # 跳转到主页面（确保streamlit_app.py在pages目录下或同级目录）
                # 注意：st.switch_page需要Streamlit 1.18.0+版本，且目标文件路径要正确
                try:
                    st.switch_page("streamlit_app.py")
                except Exception as e:
                    st.warning(f"跳转失败，请手动访问主页面：{str(e)}")
            else:
                st.error("密码错误，请检查您的ID号！")
        else:
            st.error("用户名不存在，请检查您的姓名！")

# 显示调试信息（开发阶段使用，上线时注释）
# st.subheader("调试信息")
# st.write("已加载的用户：", user_data["valid_map"])
# st.write("Session状态：", st.session_state)
