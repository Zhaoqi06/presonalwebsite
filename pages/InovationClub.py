import streamlit as st
# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")
st.title("创新创业俱乐部")
st.divider()
st.error("由于权限调整，该页面暂不开放")
st.stop()