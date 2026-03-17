import streamlit as st
# 注意：确保 function.py 文件存在且 read_count_password() 函数返回正确格式的用户数据列表
import function as f

# ========== 1. 页面配置（必须放在最前面） ==========
st.set_page_config(
    page_title="登录",
    page_icon=":lock:",
    layout="centered"
)

# ========== 2. 初始化Session State（精简冗余状态） ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # 统一登录状态标识
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""

# ========== 3. 样式优化（适配新版Streamlit） ==========

# ========== 4. 加载用户数据 ==========
try:
    # 读取用户数据（格式：[{"username": "xxx", "password": "xxx"}, ...]）
    information = f.read_count_password()
    user_data = {info["username"]: info["password"] for info in information}
except Exception as e:
    st.error(f"加载用户数据失败：{str(e)}")
    user_data = {}  # 兜底空字典，避免程序崩溃

# ========== 5. 登录表单逻辑 ==========
st.title("系统登录")
with st.form("login_form", clear_on_submit=False):
    # 表单输入（绑定session_state，保留输入值）
    st.session_state.username = st.text_input(
        "用户名",
        placeholder="请输入您的姓名",
        value=st.session_state.username
    )
    st.session_state.password = st.text_input(
        "密码",
        type="password",
        placeholder="请输入您的密码",
        value=st.session_state.password
    )

    # 按钮布局
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        submit_login = st.form_submit_button("登录", type="primary", disabled=st.session_state.logged_in)
    with col_btn2:
        submit_register = st.form_submit_button("注册", type="secondary", disabled=st.session_state.logged_in)

# ========== 6. 登录按钮逻辑 ==========
if submit_login and not st.session_state.logged_in:
    # 1. 空值校验
    username = st.session_state.username.strip()
    password = st.session_state.password.strip()
    if not username or not password:
        st.error("⚠️ 用户名和密码不能为空！")
    # 2. 用户名存在性校验
    elif username not in user_data:
        st.error(f"❌ 用户名「{username}」不存在，请检查！")
        # 清空错误输入
        st.session_state.username = ""
        st.session_state.password = ""
    # 3. 密码校验
    elif user_data[username] != password:
        st.error("❌ 密码错误，请重新输入！")
        st.session_state.password = ""  # 仅清空密码，保留用户名
    # 4. 登录成功
    else:
        st.session_state.logged_in = True
        st.success(f"✅ 欢迎 {username}！登录成功，正在跳转...")
        # 页面跳转（增加延迟+兜底提示）
        st.balloons()  # 增加交互反馈
        try:
            # 确保主页面文件存在（路径需与实际项目一致）
            st.switch_page("streamlit_app.py")
        except Exception as e:
            st.info(f"跳转失败，请手动打开主页面！错误信息：{str(e)}")
            # 可选：添加主页面链接（需配合多页面配置）
            st.markdown("[点击进入主页面](http://localhost:8501/streamlit_app)", unsafe_allow_html=True)

# ========== 7. 注册按钮逻辑 ==========
if submit_register and not st.session_state.logged_in:
    try:
        st.switch_page("pages/register.py")
    except Exception as e:
        st.error(f"跳转注册页面失败：{str(e)}")

# ========== 8. 已登录状态提示 ==========
if st.session_state.logged_in:
    st.info(f"您已登录（{st.session_state.username}），无需重复登录！")
    if st.button("退出登录"):
        # 重置登录状态
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.password = ""
        st.rerun()  # 刷新页面