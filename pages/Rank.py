import streamlit as st
import json
import os
import pandas as pd
import time

st.title("🏆 协会活动实时积分排行榜")
st.markdown("## 实时更新 · 自动刷新")
st.divider()

JSON_FILE = "./document/members_score.json"

# 加载数据
try:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
except:
    data = []

if not data:
    st.info("暂无积分数据，管理员请先上传报名表")
    st.stop()

# 上次排名（用于判断上升/下降）
if "last_rank" not in st.session_state:
    st.session_state.last_rank = []

last_names = {item["name"]: idx + 1 for idx, item in enumerate(st.session_state.last_rank)}

# 本次排序
df = pd.DataFrame(data)
df = df.sort_values("score", ascending=False).reset_index(drop=True)
df["排名"] = df.index + 1
current_list = df.to_dict("records")

# 保存本次排名
st.session_state.last_rank = current_list

# 展示样式
for idx, row in df.iterrows():
    rank = int(row["排名"])
    name = row["name"]
    sid = row["id"]
    cls = row["class"]
    score = int(row["score"])

    # 名次变化
    change = ""
    icon = ""
    color = "#ffffff"

    if name in last_names:
        prev = last_names[name]
        if rank < prev:
            change = f"↑ 上升 {prev - rank} 名"
            icon = "📈"
            color = "#2ECC71"
        elif rank > prev:
            change = f"↓ 下降 {rank - prev} 名"
            icon = "📉"
            color = "#E74C3C"
        else:
            change = "→ 持平"
            icon = "➖"
            color = "#95A5A6"

    # 前三名样式
    if rank == 1:
        bg = "linear-gradient(90deg, #FFD700, #FFC107)"
        top = "🥇 冠军"
    elif rank == 2:
        bg = "linear-gradient(90deg, #C0C0C0, #E0E0E0)"
        top = "🥈 亚军"
    elif rank == 3:
        bg = "linear-gradient(90deg, #CD7F32, #D4A76A)"
        top = "🥉 季军"
    else:
        bg = "#1E1E2E"
        top = f"第 {rank} 名"

    # 卡片 HTML
    card = f"""
        <div style="
            background: {bg};
            padding: 15px 20px;
            border-radius: 12px;
            margin: 8px 0;
            color: white;
            font-size: 16px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <div style="font-size:20px;">{top} | {name}</div>
                <div style="font-size:14px; opacity:0.9;">学号：{sid}　班级：{cls}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:22px;">{score} 分</div>
                <div style="color:{color}; font-size:14px;">{icon} {change}</div>
            </div>
        </div>
        """
    st.markdown(card, unsafe_allow_html=True)

# 自动刷新（每 5 秒刷新一次）
time.sleep(5)
st.rerun()
