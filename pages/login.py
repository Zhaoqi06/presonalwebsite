import streamlit as st
file_Path = "document/协会现有成员信息表.xlsx"
file_data = pd.read_excel(file_Path, engine='openpyxl')
try:
    # 成员数量
    length = len(file_data.iloc[:, 6])
    temp_length = 0
     for i in range(length):
        if file_data.iloc[i, 6] != 1:
            temp_length += 1
        else:
            break
    length = temp_length
    # 主键数据唯一性标识
    name = []
    id = []
    identity = []
    for i in range(length):
        name.append(file_data.iloc[i, 6])
        id.append(str(file_data.iloc[i, 5]))
        identity.append(file_data.iloc[i, 9])
    Mark = file_data.iloc[:, 6]
    def Name():
        return name
    def ID():
        return id
    def Identity():
        return identity
except:
    print(e)


st.set_page_config(page_title="登录", page_icon=":lock:", layout="centered")
# 初始化session状态
if "is_login" not in st.session_state:
    st.session_state["is_login"] = False

# 隐藏默认导航/水印
st.markdown("""
            <style>
            .css-14xtw13,.css-1v3fvcr{display:none !important;}
            </style>
              """, unsafe_allow_html=True)

# 登录表单
st.title("登录")
with st.form("login"):
    username = st.text_input("用户名", placeholder="请输入用户名")
    password = st.text_input("密码", type="password", placeholder="请输入密码")
    submit = st.form_submit_button("登录", type="primary")

# 校验+保存（核心：session_state)
valid_users = dict(zip(Name(), ID())) 
if submit:
    if username in valid_users and valid_users[username] == password:
        # 设置登录状态
        st.session_state.logged_in = True
        st.session_state["username"] = username
        st.success("登录成功，跳转中...")
        st.switch_page("streamlit_app.py")
    else:
        st.error("用户名或密码错误")





