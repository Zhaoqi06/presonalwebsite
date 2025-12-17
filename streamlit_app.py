import streamlit as st
if "is_login" not in st.session_state:
    st.session_state.is_login = False
st.set_page_config(page_title="首页",layout="wide")
#拦截未登录用户
if "is_login" not in st.session_state or not st.session_state["is_login"]:
    st.error("请先登录！！！")
    # 尝试使用英文路径或相对路径
    # 尝试使用完整的相对路径
    st.markdown('<meta http-equiv="refresh" content="1;URL=/login" />', unsafe_allow_html=True)
else:
   st.title(f"欢迎回来，{st.session_state['username']}")
