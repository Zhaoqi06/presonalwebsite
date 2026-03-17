import streamlit as st
from datetime import datetime
import function as f
import pandas as pd
import time
import os
import json
# ==================== 全局前置校验 ====================
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 隐藏默认导航/水印
st.markdown("""
    <style>
    .css-14xtw13,.css-1v3fvcr{display:none !important;}
    </style>
""", unsafe_allow_html=True)


# ==================== 页面逻辑 ====================
f.init_notification_table()

ADMIN_USER = "刘钊齐"
if ADMIN_USER == st.session_state["username"]:
    st.title("欢迎进入管理页面")
    st.divider()
    nav = st.sidebar.selectbox("导航栏", ["分布通知", "查看用户及密码","增删成员","查看邀请码","麻将成员管理","协会活动排名"])

    if nav == "分布通知":
        # 发布通知模块
        st.header("发布通知")
        with st.form("input_form", clear_on_submit=True):
            title_input = st.text_input("标题")
            text_input = st.text_area("文本")
            time_input = st.date_input("时间", value=datetime.now().date())
            submit_publish = st.form_submit_button("发布通知")

        if submit_publish:
            if not title_input or not text_input or not time_input:
                st.error("请填写完整的信息！")
            else:
                f.write_notification(title_input, text_input, time_input)
                st.success("发布成功")
                time.sleep(1)
                st.rerun()

        st.divider()

        # 删除通知模块
        st.header("删除通知")
        st.subheader("现有通知列表")
        notifications = f.read_notifications()
        if notifications:
            for notice in notifications:
                st.write(f"ID：{notice['id']} | 标题：{notice['title']} | 时间：{notice['time']}")
        else:
            st.info("暂无通知数据")

        with st.form("delete_form"):
            id_input = st.text_input("输入要删除的通知ID（数字）")
            submit_delete = st.form_submit_button("删除通知")

        if submit_delete:
            if not id_input:
                st.error("请输入要删除的通知ID！")
            else:
                f.delete_notification(id=id_input)
                st.success("删除成功")
                time.sleep(1)
                st.rerun()
    if nav == "查看用户及密码":
        st.header("网站所有用户及密码")
        user = []
        password = []
        f.init_count_password_table()
        information = f.read_count_password()
        for info in information:
            user.append(info["username"])
            password.append(info["password"])

        df = pd.DataFrame(data={
            '用户名：': user,
            '密码：': password,
        })
        st.dataframe(df, use_container_width=True)
        st.divider()
        st.title("更改密码")
        username = st.text_input("请输入用户名：")
        password = st.text_input("请输入密码：", type="password")
        if st.button("修改"):
            if username in user:
                f.Updata_count_password(username, password)
                st.success("修改成功！")
                time.sleep(1)
                st.rerun()

            else:
                st.error("用户名不存在！")

    if nav == "增删成员":
        st.header("增删成员")
        f.init_count_password_table()
        information = f.read_count_password()
        invite_number = f.get_daily_invite_num()

        for info in information:
            username = info["username"]
            password = info["password"]
            user_data = {"valid_map": {username: password}}
        username = st.text_input("请输入用户名：")
        password = st.text_input("请输入密码：", type="password")
        col1, col2 ,col3= st.columns([1, 1,8])
        with col1:
            if st.button("添加"):
                if username in user_data["valid_map"]:
                    st.error("用户名已存在！")
                else:
                    f.write_count_password(username, password)
                    st.success("添加成功！")
                    time.sleep(1)
                    st.rerun()
        with col2:
            if st.button("删除"):
                f.delete_count_password(username)
                st.rerun()
                st.success("删除成功！")
    if nav == "查看邀请码":
        st.header("查看邀请码")
        st.success(f.get_daily_invite_num())

    if nav == "麻将成员管理":
        st.header("在这里管理麻将成员信息")
        st.write("注意该页面最好在GITHUB上运行，每天数据会自动清除，本地不会！！！")
        st.divider()

        f.get_db_connection_count_password()
        f.init_count_majiang()
        f.init_count_password_table()

        st.write("添加成员，一次只能添加四个")
        information = f.read_majiang()
        temp = f.read_count_password()
        user = []
        score = []
        username_majiang = []
        for info in temp:
            if "username" in info:
                username_majiang.append(info["username"])

        for info in information:
            user.append(info["username"])
            score.append(info.get("score", info.get("socre", 0)))

            # 展示成员列表
        if user:
            df = pd.DataFrame(data={
                '用户名：': user,
                '得分：': score,
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.success("当前无麻将搭子")
        st.write("添加搭子")
        col1, col2 = st.columns([1, 1])
        with col1:
            name = st.text_input("姓名（添加）", placeholder="请输入姓名", key="add_name")
        with col2:
            score_add = st.number_input("默认得分为 0 ", value=0, key="add_score")  # 变量名区分，避免覆盖

        if st.button("添加", type="primary", key="btn_add"):
            if len(user) >= 4:
                st.error("最多只能添加4个麻将搭子！")
            elif name not in username_majiang:
                st.error("该用户未注册账户！")
            elif name in user:
                st.error("名字重复！")
            else:
                f.write_majiang(name, score_add)
                st.success("写入成功")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()

        st.divider()

        st.write("删除搭子")
        name_del = st.text_input("姓名（删除）", placeholder="请输入姓名", key="del_name")
        if st.button("删除", type="primary", key="btn_del"):
            if name_del in user:
                f.delete_majiang(name_del)
                st.success("删除成功")
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()
            else:
                st.error("该用户不是你的搭子！")

        st.divider()

        # 清除得分数据区域
        st.write("清除得分数据")
        if st.button("清除得分数据", type="primary", key="btn_clear"):
            for username in user:
                f.Updata_majiang(username, 0)
            st.success("清除成功！")
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()
    if nav == "协会活动排名":
        st.header("协会活动排名")
        st.divider()

        import os
        import json
        import time
        import pandas as pd

        # 配置文件路径
        JSON_FILE = "./document/members_score.json"
        os.makedirs("./document", exist_ok=True)

        # 初始化 JSON 文件
        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, "w", encoding="utf-8") as jf:
                json.dump([], jf, ensure_ascii=False, indent=2)

        # 加载积分数据
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as jf:
                score_data = json.load(jf)
        except:
            score_data = []

        # ====================== 上传报名表 ======================
        st.subheader("📤 上传活动报名表")
        uploaded_file = st.file_uploader("请上传活动报名表（支持 .xlsx / .csv）", type=['xlsx', 'xls', 'csv'])

        if uploaded_file is not None:
            try:
                file_name = uploaded_file.name
                if file_name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, skiprows=2)
                else:
                    df = pd.read_excel(uploaded_file, engine='openpyxl', skiprows=2)

                # 自动匹配列（你的表格：序号、学号、姓名、班级...）
                id_col = None
                name_col = None
                class_col = None

                for col in df.columns:
                    c = str(col).replace(" ", "")
                    if "学号" in c: id_col = col
                    if "姓名" in c: name_col = col
                    if "班级" in c: class_col = col

                # 找不到就按位置取（适配你的固定格式）
                if len(df.columns) >= 4:
                    if id_col is None: id_col = df.columns[1]
                    if name_col is None: name_col = df.columns[2]
                    if class_col is None: class_col = df.columns[3]

                if not all([id_col, name_col, class_col]):
                    st.error("❌ 未找到 学号/姓名/班级 列，请检查表格")
                else:
                    # 读取并清理数据
                    df_clean = df[[id_col, name_col, class_col]].dropna()
                    existing_dict = {item["name"]: item for item in score_data}
                    new_score_data = []

                    for _, row in df_clean.iterrows():
                        sid = str(row[id_col]).strip()
                        name = str(row[name_col]).strip()
                        cls = str(row[class_col]).strip()

                        if not name: continue

                        # 保留原有积分
                        score = existing_dict.get(name, {}).get("score", 0)
                        new_score_data.append({
                            "name": name,
                            "id": sid,
                            "class": cls,
                            "score": score
                        })

                    # 去重
                    unique_data = {item["name"]: item for item in new_score_data}.values()
                    score_data = list(unique_data)

                    # 保存
                    with open(JSON_FILE, "w", encoding="utf-8") as jf:
                        json.dump(score_data, jf, ensure_ascii=False, indent=2)

                    st.success(f"✅ 上传成功！共 {len(score_data)} 人")

            except Exception as e:
                st.error(f"❌ 读取失败：{str(e)}")

        st.divider()

        # ====================== 清除所有数据按钮 ======================
        if score_data:
            with st.expander("⚠️ 危险操作：清空所有成员数据"):
                st.warning("此操作会清空【所有成员、学号、班级、积分】，无法恢复！")
                col1, col2 = st.columns(2)
                with col1:
                    confirm = st.checkbox("我确认要清空所有数据")
                with col2:
                    clear_btn = st.button("🗑️ 一键清除所有", type="secondary")

                if clear_btn and confirm:
                    # 彻底清空 JSON 文件
                    score_data = []
                    with open(JSON_FILE, "w", encoding="utf-8") as jf:
                        json.dump([], jf, ensure_ascii=False, indent=2)
                    st.success("✅ 所有数据已清空！可以重新上传表格啦")
                    time.sleep(1)
                    st.rerun()

        st.divider()

        # ====================== 积分排名 ======================
        st.subheader("📊 成员积分排名")
        if score_data:
            df_show = pd.DataFrame(score_data)
            df_show = df_show[["name", "id", "class", "score"]]
            df_show.columns = ["姓名", "学号", "班级", "积分"]
            df_show = df_show.sort_values("积分", ascending=False).reset_index(drop=True)
            st.dataframe(df_show, use_container_width=True, height=400)
        else:
            st.info("ℹ️ 暂无数据，请先上传报名表")

        st.divider()

        # ====================== 计分系统（两种加分方式） ======================
        st.subheader("✏️ 积分管理（累加模式）")
        add_type = st.radio("选择加分方式", ["按姓名", "按学号"], horizontal=True)

        if not score_data:
            st.warning("请先上传报名表")
        else:
            if add_type == "按姓名":
                # 按姓名
                name_options = [f"{item['name']} | {item['class']}" for item in score_data]
                selected_option = st.selectbox("选择成员", name_options)
                selected_name = selected_option.split("|")[0].strip()

                # 找到当前成员
                selected_item = None
                for item in score_data:
                    if item["name"] == selected_name:
                        selected_item = item
                        break

                if selected_item:
                    st.info(f"当前积分：{selected_item['score']} 分")
                    add_score = st.number_input("输入要增加的分数", step=1, value=0)
                    submit = st.button("✅ 确认加分", type="primary")

                    if submit and add_score != 0:
                        selected_item["score"] += int(add_score)
                        with open(JSON_FILE, "w", encoding="utf-8") as jf:
                            json.dump(score_data, jf, ensure_ascii=False, indent=2)
                        st.success(f"✅ 成功给 {selected_name} 加 {add_score} 分！最新积分：{selected_item['score']}")
                        time.sleep(0.7)
                        st.rerun()

            else:
                # 按学号加分
                input_id = st.text_input("输入学号", placeholder="请输入学号")
                match_item = None
                for item in score_data:
                    if item["id"] == input_id:
                        match_item = item
                        break

                if input_id:
                    if match_item:
                        st.success(f"找到：{match_item['name']} | {match_item['class']} | 当前积分：{match_item['score']}")
                        add_score = st.number_input("输入要增加的分数", step=1, value=0, key="add_by_id")
                        submit = st.button("✅ 确认加分", type="primary")

                        if submit and add_score != 0:
                            match_item["score"] += int(add_score)
                            with open(JSON_FILE, "w", encoding="utf-8") as jf:
                                json.dump(score_data, jf, ensure_ascii=False, indent=2)
                            st.success(f"✅ 加分成功！最新积分：{match_item['score']}")
                            time.sleep(0.7)
                            st.rerun()
                    else:
                        st.error("未找到该学号")
else:
    st.error("非管理员人员不能进入该页面")