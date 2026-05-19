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
    nav = st.sidebar.selectbox("导航栏",
                               ["分布通知", "查看用户及密码", "增删成员", "查看邀请码", "麻将成员管理", "协会活动排名"])

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
        col1, col2, col3 = st.columns([1, 1, 8])
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
                nation_col = None

                for col in df.columns:
                    c = str(col).replace(" ", "")
                    if "学号" in c: id_col = col
                    if "姓名" in c: name_col = col
                    if "班级" in c: class_col = col
                    if "国籍" in c: nation_col = col

                # 找不到就按位置取（适配你的固定格式）
                if len(df.columns) >= 4:
                    if id_col is None: id_col = df.columns[1]
                    if name_col is None: name_col = df.columns[2]
                    if class_col is None: class_col = df.columns[3]
                    # G列是索引6，如果存在则作为国籍列
                    if nation_col is None and len(df.columns) > 6:
                        nation_col = df.columns[6]

                if not all([id_col, name_col, class_col]):
                    st.error("❌ 未找到 学号/姓名/班级 列，请检查表格")
                else:
                    # 读取并清理数据
                    columns_to_read = [id_col, name_col, class_col]
                    if nation_col:
                        columns_to_read.append(nation_col)

                    df_clean = df[columns_to_read].dropna(subset=[name_col])
                    existing_dict = {item["name"]: item for item in score_data}
                    new_score_data = []

                    for _, row in df_clean.iterrows():
                        sid = str(row[id_col]).strip()
                        name = str(row[name_col]).strip()
                        cls = str(row[class_col]).strip()

                        # 自动识别国籍 - 修复版
                        nation = ""
                        if nation_col and nation_col in df_clean.columns:
                            nation_val_raw = row[nation_col]
                            if pd.notna(nation_val_raw):
                                nation_val = str(nation_val_raw).strip()
                                # 更精确的国籍判断逻辑
                                if "中国" in nation_val:
                                    nation = "中国籍"
                                elif nation_val == "":
                                    nation = "中国籍"  # 空值默认为中国籍
                                else:
                                    # 其他所有非空且不含"中国"的情况都视为国际学生
                                    nation = "国际学生"
                            else:
                                nation = "中国籍"  # NaN值默认为中国籍
                        else:
                            nation = "中国籍"  # 没有国籍列时默认为中国籍

                        if not name: continue

                        # 保留原有积分
                        score = existing_dict.get(name, {}).get("score", 0)
                        new_score_data.append({
                            "name": name,
                            "id": sid,
                            "class": cls,
                            "score": score,
                            "nation": nation
                        })

                    # 去重
                    unique_data = {item["name"]: item for item in new_score_data}.values()
                    score_data = list(unique_data)

                    # 保存
                    with open(JSON_FILE, "w", encoding="utf-8") as jf:
                        json.dump(score_data, jf, ensure_ascii=False, indent=2)

                    st.success(f"✅ 上传成功！共 {len(score_data)} 人")

                    # 显示国籍统计信息（用于调试）
                    chinese_count = sum(1 for item in score_data if item.get('nation') == '中国籍')
                    foreign_count = sum(1 for item in score_data if item.get('nation') == '国际学生')
                    st.info(f"📊 国籍统计：中国籍 {chinese_count} 人 | 国际学生 {foreign_count} 人")

                    # 如果有国际学生，显示前几个示例
                    foreign_examples = [item for item in score_data if item.get('nation') == '国际学生'][:5]
                    if foreign_examples:
                        st.write("**国际学生示例：**")
                        for item in foreign_examples:
                            st.write(f"- {item['name']} (国籍: {item.get('nation', '未知')})")

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

        # ====================== 【新增】活动赋分系统 ======================
        st.subheader("📐 活动赋分系统（中国籍vs国际学生）")

        # 使用expander折叠赋分功能
        with st.expander("🔧 展开赋分功能", expanded=False):
            st.info("💡 根据中国选手和国际学生的表现进行积分调整，系统将自动计算换算系数")

            if not score_data:
                st.warning("⚠️ 请先上传报名表后再使用赋分功能")
            else:
                # 初始化session_state用于赋分
                if 'scored_result' not in st.session_state:
                    st.session_state.scored_result = None

                # 转换为DataFrame
                df_scores = pd.DataFrame(score_data)

                # 检查必要的列
                required_columns = ['name', 'id', 'class', 'score']
                missing_columns = [col for col in required_columns if col not in df_scores.columns]
                if missing_columns:
                    st.error(f"❌ 数据缺少必要字段：{', '.join(missing_columns)}")
                else:
                    # 确保有国籍列，如果没有则添加默认值
                    if 'nation' not in df_scores.columns:
                        df_scores['nation'] = '中国籍'  # 默认为中国籍

                    st.write("#### 步骤1：查看当前选手信息及国籍")
                    st.info("💡 国籍已从报名表中自动识别，如需修改可在下方表格中调整")

                    # 使用data_editor让用户可以查看和修改国籍
                    edited_df = st.data_editor(
                        df_scores[['name', 'id', 'class', 'score', 'nation']],
                        column_config={
                            "name": st.column_config.TextColumn("姓名", disabled=True),
                            "id": st.column_config.TextColumn("学号", disabled=True),
                            "class": st.column_config.TextColumn("班级", disabled=True),
                            "score": st.column_config.NumberColumn("基础得分", disabled=True),
                            "nation": st.column_config.SelectboxColumn(
                                "国籍",
                                options=["中国籍", "国际学生"],
                                required=True,
                                width="medium"
                            )
                        },
                        hide_index=True,
                        use_container_width=True,
                        key="nation_editor_manager"
                    )

                    st.divider()

                    # 统计信息
                    chinese_mask = edited_df['nation'] == '中国籍'
                    foreign_mask = edited_df['nation'] == '国际学生'

                    chinese_count = chinese_mask.sum()
                    foreign_count = foreign_mask.sum()

                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    with col_stat1:
                        st.metric("中国籍选手", f"{chinese_count} 人")
                    with col_stat2:
                        st.metric("国际学生", f"{foreign_count} 人")
                    with col_stat3:
                        st.metric("总人数", f"{len(edited_df)} 人")

                    # 验证是否有足够的数据
                    if chinese_count == 0:
                        st.warning("⚠️ 请至少标注一名中国籍选手以计算换算系数")
                    elif foreign_count == 0:
                        st.warning("⚠️ 没有国际学生选手，无需进行赋分调整")
                    else:
                        # 计算平均分
                        chinese_avg = edited_df.loc[chinese_mask, 'score'].mean()
                        foreign_avg = edited_df.loc[foreign_mask, 'score'].mean()

                        st.write("#### 步骤2：基础得分统计")
                        col_avg1, col_avg2 = st.columns(2)
                        with col_avg1:
                            st.metric(
                                "中国选手平均得分",
                                f"{chinese_avg:.1f} 分",
                                help=f"计算方式：中国选手总得分 / 中国选手人数"
                            )
                        with col_avg2:
                            st.metric(
                                "国际学生平均得分",
                                f"{foreign_avg:.1f} 分",
                                help=f"计算方式：国际学生总得分 / 国际学生人数"
                            )

                        st.divider()

                        # 计算赋分百分比（换算系数）
                        if chinese_avg != 0:
                            raw_percentage = (foreign_avg / chinese_avg) * 100
                        else:
                            raw_percentage = 100.0

                        st.write("#### 步骤3：换算系数设置")
                        st.info(
                            f"📐 原始换算系数 = 外籍选手平均分 ÷ 中国选手平均分 × 100% = {foreign_avg:.1f} ÷ {chinese_avg:.1f} × 100% = **{raw_percentage:.1f}%**")

                        # 设置上下限
                        col_limit1, col_limit2 = st.columns(2)
                        with col_limit1:
                            min_percentage = st.number_input(
                                "换算系数下限 (%)",
                                min_value=0.0,
                                max_value=100.0,
                                value=80.0,
                                step=1.0,
                                help="主席团商讨确认的最低换算系数"
                            )
                        with col_limit2:
                            max_percentage = st.number_input(
                                "换算系数上限 (%)",
                                min_value=100.0,
                                max_value=200.0,
                                value=120.0,
                                step=1.0,
                                help="主席团商讨确认的最高换算系数"
                            )

                        # 限制范围校验
                        if min_percentage > max_percentage:
                            st.error("❌ 下限不能大于上限")
                        else:
                            # 应用上下限约束
                            final_percentage = max(min_percentage, min(max_percentage, raw_percentage))

                            st.divider()

                            st.write("#### 步骤4：赋分确认")
                            col_confirm1, col_confirm2 = st.columns(2)
                            with col_confirm1:
                                st.metric("原始计算值", f"{raw_percentage:.1f}%")
                            with col_confirm2:
                                st.metric("最终采用值", f"{final_percentage:.1f}%",
                                          delta=f"{final_percentage - raw_percentage:.1f}%" if abs(
                                              final_percentage - raw_percentage) > 0.01 else "无调整")

                            if abs(final_percentage - raw_percentage) > 0.01:
                                st.info(
                                    f"📋 说明：由于原始值 {raw_percentage:.1f}% {'超过' if final_percentage == max_percentage else '低于'} 设定范围，已调整为边界值 {final_percentage:.1f}%")
                            else:
                                st.success(f"✅ 原始值 {raw_percentage:.1f}% 在合理范围内，直接采用")

                            st.divider()

                            # 执行赋分按钮
                            if st.button("🔢 计算并预览赋分结果", type="primary", use_container_width=True,
                                         key="btn_scoring"):
                                # 计算每个选手的最终得分
                                result_data = []

                                for _, row in edited_df.iterrows():
                                    base_score = row['score']
                                    nation = row['nation']

                                    if nation == '国际学生':
                                        # 外籍选手最终赋分 = 外籍选手原始得分 × 换算系数（保留整数，四舍五入）
                                        final_score = round(base_score * (final_percentage / 100))
                                    else:
                                        # 中国选手得分不变
                                        final_score = base_score

                                    result_data.append({
                                        '姓名': row['name'],
                                        '学号': row['id'],
                                        '班级': row['class'],
                                        '国籍': nation,
                                        '原始得分': int(base_score),
                                        '换算系数': f"{final_percentage:.1f}%" if nation == '国际学生' else '-',
                                        '最终得分': int(final_score)
                                    })

                                result_df = pd.DataFrame(result_data)
                                st.session_state.scored_result = result_df

                            # 显示赋分结果
                            if st.session_state.scored_result is not None:
                                st.divider()
                                st.success("✅ 赋分计算完成！请查看下方总分表后确认")

                                # 显示两个表格对比
                                st.write("#### 📊 赋分前后对比（总分表）")

                                # 表格1：原始得分表
                                st.write("**表1：原始得分情况**")
                                original_df = st.session_state.scored_result[
                                    ['姓名', '学号', '班级', '国籍', '原始得分']].copy()
                                st.dataframe(
                                    original_df,
                                    use_container_width=True,
                                    hide_index=True,
                                    column_config={
                                        "原始得分": st.column_config.NumberColumn(format="%d")
                                    }
                                )

                                st.divider()

                                # 表格2：赋分后得分表
                                st.write("**表2：赋分后最终得分**")
                                final_df = st.session_state.scored_result[
                                    ['姓名', '学号', '班级', '国籍', '原始得分', '换算系数', '最终得分']].copy()
                                st.dataframe(
                                    final_df,
                                    use_container_width=True,
                                    hide_index=True,
                                    column_config={
                                        "原始得分": st.column_config.NumberColumn(format="%d"),
                                        "最终得分": st.column_config.NumberColumn(format="%d")
                                    }
                                )

                                st.divider()

                                # 对比分析
                                st.write("#### 📈 得分变化分析")

                                # 国际学生得分变化
                                foreign_result = st.session_state.scored_result[
                                    st.session_state.scored_result['国籍'] == '国际学生']
                                if len(foreign_result) > 0:
                                    avg_before = foreign_result['原始得分'].mean()
                                    avg_after = foreign_result['最终得分'].mean()

                                    col_change1, col_change2, col_change3 = st.columns(3)
                                    with col_change1:
                                        st.metric("国际学生调整前平均", f"{avg_before:.1f} 分")
                                    with col_change2:
                                        st.metric("国际学生调整后平均", f"{avg_after:.1f} 分",
                                                  delta=f"{avg_after - avg_before:.1f} 分")
                                    with col_change3:
                                        change_rate = ((
                                                                   avg_after - avg_before) / avg_before * 100) if avg_before != 0 else 0
                                        st.metric("变化幅度", f"{change_rate:+.1f}%")

                                    st.divider()

                                    # 显示国际学生详细变化
                                    st.write("**国际学生得分变化详情：**")
                                    foreign_detail = foreign_result[['姓名', '原始得分', '换算系数', '最终得分']].copy()
                                    foreign_detail['得分变化'] = foreign_detail['最终得分'] - foreign_detail['原始得分']
                                    foreign_detail.columns = ['姓名', '原始得分', '换算系数', '最终得分', '得分变化']
                                    st.dataframe(
                                        foreign_detail,
                                        use_container_width=True,
                                        hide_index=True,
                                        column_config={
                                            "原始得分": st.column_config.NumberColumn(format="%d"),
                                            "最终得分": st.column_config.NumberColumn(format="%d"),
                                            "得分变化": st.column_config.NumberColumn(format="%+d")
                                        }
                                    )

                                st.divider()

                                # 导出结果
                                st.write("#### 💾 导出赋分结果")
                                col_export1, col_export2 = st.columns(2)

                                with col_export1:
                                    # 导出CSV
                                    csv_data = st.session_state.scored_result.to_csv(index=False, encoding='utf-8-sig')
                                    st.download_button(
                                        label="📥 下载 CSV 格式",
                                        data=csv_data,
                                        file_name=f"活动赋分结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                        mime="text/csv",
                                        use_container_width=True,
                                        key="download_csv_scoring"
                                    )

                                with col_export2:
                                    # 导出Excel
                                    from io import BytesIO

                                    output = BytesIO()
                                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                        # 写入原始得分表
                                        original_df.to_excel(writer, index=False, sheet_name='原始得分')
                                        # 写入最终得分表
                                        final_df.to_excel(writer, index=False, sheet_name='最终得分')
                                    excel_data = output.getvalue()

                                    st.download_button(
                                        label="📥 下载 Excel 格式（含两个表格）",
                                        data=excel_data,
                                        file_name=f"活动赋分对比_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        use_container_width=True,
                                        key="download_excel_scoring"
                                    )

                                # 更新JSON文件选项 - 放在最后，需要用户确认
                                st.divider()
                                st.write("#### 🔄 确认并保存赋分结果")
                                st.warning("⚠️ 点击确认按钮后，会将赋分后的最终得分保存到数据库，影响实时排名！")
                                st.info("💡 请仔细核对上方总分表，确认无误后再点击确认按钮")

                                if st.button("✅ 确认赋分并保存到数据库", type="primary", use_container_width=True,
                                             key="btn_save_scoring"):
                                    try:
                                        # 构建更新后的数据
                                        updated_data = []
                                        for _, row in st.session_state.scored_result.iterrows():
                                            updated_data.append({
                                                'name': row['姓名'],
                                                'id': row['学号'],
                                                'class': row['班级'],
                                                'score': int(row['最终得分']),
                                                'nation': row['国籍']
                                            })

                                        # 写入JSON文件
                                        with open(JSON_FILE, "w", encoding="utf-8") as jf:
                                            json.dump(updated_data, jf, ensure_ascii=False, indent=2)

                                        st.success("✅ 积分数据已更新！实时排名将自动同步最新分数")

                                        # 清除缓存的结果，避免重复保存
                                        st.session_state.scored_result = None

                                        time.sleep(1)
                                        st.rerun()

                                    except Exception as e:
                                        st.error(f"❌ 保存失败：{str(e)}")

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
                        st.success(
                            f"找到：{match_item['name']} | {match_item['class']} | 当前积分：{match_item['score']}")
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
