import streamlit as st
import function as f
# ==================== Streamlit页面逻辑 ====================
# 页面基础配置
st.set_page_config(page_title="首页", layout="wide")

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 初始化通知表（确保表存在）
f.init_notification_table()

# 页面内容
st.title(f"欢迎回来! {st.session_state['username']}")
st.write("单丝不成线、独木不成林！共建开放包容之路，共赢共同发展之果！")

# 分割线
st.divider()

# 功能按钮列
col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.7, 1.2, 1.2, 1, 1.2])
with col1:
    if st.button("国际交流协会"):
        st.switch_page("pages/association.py")
with col2:
    if st.button("协会实时活动排名"):
        st.switch_page("pages/Rank.py")
with col3:
    if st.button("实用工具"):
        st.switch_page("pages/tool.py")
with col4:
    if st.button("学习资料"):
        st.switch_page("pages/Study.py")
with col5:
    if st.button("个人"):
        st.switch_page("pages/self_person.py")
with col6:
    if st.button("退出登录"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# 读取并显示通知
st.divider()
st.subheader("最新通知")
notifications = f.read_notifications()

# 处理通知显示逻辑（修复缩进错误）
if not notifications:
    st.info("暂无通知")
else:
    # 遍历通知，显示卡片
    for notice in notifications:
        with st.container(border=True):
            st.subheader(notice["title"])
            st.write(notice["text"])
            st.caption(f"发布时间：{notice['time']}")  # 用caption显示时间，更美观