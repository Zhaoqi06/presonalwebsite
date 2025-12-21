import streamlit as st
st.set_page_config(page_title="首页", layout="wide")
# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")
st.title(f"欢迎回来!{st.session_state['username']}")
st.write("单丝不成线、独木不成林！共建开放包容之路，共赢共同发展之果！")
#----------------------------------------------------------------------------
st.divider()
col1,col2,col3,col4,col5,col6 = st.columns([1.5,1.7,1.2,1.2,1,1.2])
# 添加退出登录功能
with col1:
    if st.button("国际交流协会"):
        st.switch_page("pages/association.py")
with col2:
    if st.button("创新创业俱乐部"):
        st.switch_page("pages/association.py")
with col3:
    if st.button("实用工具"):
        st.switch_page("pages/association.py")
with col4:
    if st.button("学习资料"):
        st.switch_page("pages/Study.py")
with col5:
    if st.button("个人"):
        st.switch_page("pages/association.py")
with col6:
    if st.button("退出登录"):
        st.session_state.clear()
        st.switch_page("pages/login.py")
