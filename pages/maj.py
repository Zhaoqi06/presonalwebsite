import os
import streamlit as st
import time
import json
import pandas as pd
import function as f

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# =============记忆中枢====================
RECORD_FILE = "./document/mahjiong_scores.json"

if not os.path.exists(RECORD_FILE):
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


def load_records():
    with open(RECORD_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_records(new_name):
    records = load_records()
    records.append(new_name)
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


f.get_db_connection_count_password()
f.init_count_majiang()
information = f.read_majiang()
user = []
socre = []
for info in information:
    user.append(info["username"])
    socre.append(info["socre"])
st.header("麻将计分系统")
if st.session_state['username'] not in user:
    st.error("不好意思，你不是麻将搭子，请联系管理员将你设为搭子！")
    st.stop()
st.write("当前成员及其得分情况！")
if user:
    df = pd.DataFrame(data={
        '用户名：': user,
        '得分：': socre,
    })
    st.dataframe(df, use_container_width=True)
    new_name = user.remove(st.session_state['username'])
    col1, col2 = st.columns(2)
    with col1:
        name = st.selectbox("请选择人名！", options=user)
    with col2:
        score_grain = st.number_input("得分 ", value=0)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("提交", type="primary"):
            if name:
                new_record = {
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "from": st.session_state['username'],
                    "to": name,
                    "score": score_grain,
                }
                save_records(new_record)
                f.get_db_connection_count_password()
                f.init_count_majiang()
                information = f.read_majiang()
                user = []
                socre = []
                for info in information:
                    user.append(info["username"])
                    socre.append(info["socre"])
                temp = user.index(name)
                temp_self = user.index(st.session_state['username'])
                temp_num = socre[temp]
                temp_self_num = socre[temp_self]
                score_grain = score_grain + temp_num
                score_reduce = temp_self_num - score_grain
                f.Updata_majiang(name, score_grain)
                f.Updata_majiang(st.session_state['username'], score_reduce)
                st.success("提交成功")
                st.rerun()
            else:
                st.error("请正确填写")
    with col2:
        if st.button("刷新", type="primary"):
            st.rerun()

    st.header("积分记录")
    records = load_records()
    if records:
        for idx, r in enumerate(reversed(records), 1):
            st.markdown(f"""**{r['time']}**  **{r['from']}-->{r['to']} :{r['score']}**""")
    else:
        st.info("暂无积分记录")
