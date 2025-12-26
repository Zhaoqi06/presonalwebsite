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
    st.title("欢迎进入管理页面")
    st.divider()
    nav = st.sidebar.selectbox("导航栏",["首页", "数学教学"])
    if nav == "首页":
        st.header("分布通知")
        with st.form("input_form"):
            title_input = st.text_input("标题")
            text_input = st.text_area("文本")
            time_input = st.date_input("时间")
            submit_btn = st.form_submit_button("提交")
        if submit_btn:
            if not title_input or not text_input or not time_input:
                st.error("请填写完整的信息")
            else:
                card_file_path = "document\card_file.txt"
                with open(card_file_path,'a',encoding = "utf-8") as f:
                    f.write("标题:"+title_input+"\n")
                    f.write("文本:"+text_input+"\n")
                    f.write(f"时间:{time_input}\n")
                    f.write("\n")


else:
    st.error("非管理员人员不能进入该页面")



    #with card1:
        #st.subheader("行课通知")
        #st.write("由于授课结构调整，本次会有短期行课安排，行课时间为2025/12/22日开始的每周六下午，具体时间听从安排。")
        #st.write("行课内容为 数学必修一 必修二 必修三 必修四 必修五 选修4-5.各位同学提前准备！")
