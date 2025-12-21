import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")
# 隐藏默认导航/水印
st.markdown("""
            <style>
            .css-14xtw13,.css-1v3fvcr{display:none !important;}
            </style>
              """, unsafe_allow_html=True)

if "刘钊齐" == st.session_state["username"]:
    st.write("欢迎进入管理页面")
    st.divider()
    st.markdown("#### 分布活动")
else:
    st.error("非管理员人员不能进入该页面")

