import os
import streamlit as st
import time
import json
import pandas as pd
import function as f
from filelock import FileLock

# 登录校验
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 配置文件路径和锁文件
RECORD_FILE = "./document/mahjiong_scores.json"
LOCK_FILE = "./document/mahjiong.lock"

# 确保document文件夹存在
os.makedirs("./document", exist_ok=True)

# 初始化空的积分记录文件（如果不存在）
if not os.path.exists(RECORD_FILE):
    with open(RECORD_FILE, "w", encoding="utf-8") as f_file:
        json.dump([], f_file, ensure_ascii=False, indent=2)


# 加载记录（读操作单独加锁）
def load_records():
    with FileLock(LOCK_FILE):
        with open(RECORD_FILE, "r", encoding="utf-8") as f_file:
            return json.load(f_file)


# 保存记录（同一锁内完成读+写，避免死锁）
def save_records(new_record):
    with FileLock(LOCK_FILE):
        try:
            with open(RECORD_FILE, "r", encoding="utf-8") as f_file:
                records = json.load(f_file)
        except:
            records = []

        records.append(new_record)
        with open(RECORD_FILE, "w", encoding="utf-8") as f_file:
            json.dump(records, f_file, ensure_ascii=False, indent=2)


# 加载麻将搭子数据
def refresh_majiang_data():
    """封装数据加载逻辑，方便复用"""
    f.get_db_connection_count_password()
    f.init_count_majiang()
    return f.read_majiang()


information = refresh_majiang_data()

# 提取用户和得分
user_list = []
score_list = []
for info in information:
    user_list.append(info["username"])
    score_list.append(info["socre"])

# 页面标题和权限校验
st.header("麻将计分系统")
current_user = st.session_state['username']
if current_user not in user_list:
    st.error("不好意思，你不是麻将搭子，请联系管理员将你设为搭子！")
    st.stop()

# 显示当前成员得分
st.write("当前成员及其得分情况！")
if user_list:
    df = pd.DataFrame(data={
        '用户名：': user_list,
        '得分：': score_list,
    })
    st.dataframe(df, use_container_width=True)

    # 排除当前用户，生成对手列表
    other_users = [u for u in user_list if u != current_user]

    # 选择对手和输入分数
    col1, col2 = st.columns(2)
    with col1:
        target_user = st.selectbox("请选择人名！", options=other_users)
    with col2:
        score_change = st.number_input("得分 ", value=0)

    # 提交和刷新按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("提交", type="primary"):
            time.sleep(0.5)
            if target_user and score_change != 0:  # 分数不能为0，避免无效提交
                # 1. 构造新记录
                new_record = {
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "from": current_user,
                    "to": target_user,
                    "score": score_change,
                }
                save_records(new_record)

                # 2. 核心修复：直接从数据库取最新得分，不依赖session_state
                # 重新加载最新数据
                latest_info = refresh_majiang_data()

                # 找到当前用户和目标用户的最新得分
                current_user_score = 0
                target_user_score = 0
                for info in latest_info:
                    if info["username"] == current_user:
                        current_user_score = info["socre"]
                    if info["username"] == target_user:
                        target_user_score = info["socre"]

                # 3. 计算新得分（当前用户减分，目标用户加分）
                new_current_score = current_user_score - score_change
                new_target_score = target_user_score + score_change

                # 4. 更新数据库（直接用计算后的新值，无中转）
                f.Updata_majiang(current_user, new_current_score)
                f.Updata_majiang(target_user, new_target_score)

                st.success(f"提交成功！{current_user} 扣 {score_change} 分，{target_user} 加 {score_change} 分")
                st.rerun()
            else:
                st.error("请选择对手，并输入非0的得分！")
    with col2:
        if st.button("刷新", type="primary"):
            st.rerun()

    # 显示积分记录
    st.header("积分记录")
    records = load_records()
    if records:
        for idx, r in enumerate(reversed(records), 1):
            st.markdown(f"""**{r['time']}**  **{r['from']}-->{r['to']} :{r['score']}**""")
    else:
        st.info("暂无积分记录")