import streamlit as st
st.set_page_config(page_title="首页", layout="wide")
# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")
st.title(f"欢迎回来!{st.session_state['username']}")
# 添加退出登录功能
if st.button("退出登录"):
    st.session_state.clear()
    st.switch_page("pages/login.py")
elif st.button("国际交流协会"):
    st.switch_page("pages/association.py")

