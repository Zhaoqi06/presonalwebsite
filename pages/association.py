import streamlit as st
from datetime import datetime
import pandas as pd
import os
import numpy as np
import json
st.set_page_config(page_title="协会", layout="wide")

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏", ["首页","协会成员", "实时积分排名","活动风采","活动选人"])

if nav == "首页":
    st.title("国际交流协会")
    st.write(
        "四川信息职业技术学院国际交流协会，宛如一座璀璨的文化桥梁，搭建起学院与国际的沟通之路。协会成立于2014，自诞生起，就以跨越信息边界，共筑国际交流为宗旨，积极推动学院在国际舞台上绽放光彩。")
    st.divider()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docx_file_path = os.path.join(script_dir, "..", "vedio", "一带一路英文.mp4")
    video_path = os.path.normpath(docx_file_path)
    if os.path.exists(video_path):
        st.video(video_path, format="video/mp4", start_time=0,autoplay=True)
    else:
        st.error(f"视频文件未找到：{os.path.abspath(video_path)}")


elif nav == "协会成员":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docx_file_path = os.path.join(script_dir, "..", "document", "协会现有成员信息表.xlsx")
    file_Path = os.path.normpath(docx_file_path)
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
        menmber = []
        for i in range(length):
            if file_data.iloc[i, 9] == "非国际交流协会成员":
                continue
            else:
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
    except Exception as e:
        print(e)
    # -------------------------------------------------------------------------------------
    st.title("国际交流协会成员信息表")
    st.write("#### 国际交流协会负责人信息")
    st.table(data={
        '姓名：': ['刘钊齐'],
        '学号：': ['24407077'],
        '联系方式：': [19130786589],
        '职务：': ['协会负责人'],
        '班级：': ['智控24-2'],
    })
    st.divider()
    st.write("#### 国际交流协会成员信息")
    df = pd.DataFrame(data={
        '姓名：': Name(),
        '学号：': ID(),
        '社团职务': Identity()
    })
    st.dataframe(df, use_container_width=True)
    st.divider()
    st.write("#### 内部成员信息核对")

# ====================== 【实时排名展示页】成员观看专用 ======================
elif nav == "实时积分排名":
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

    last_names = {item["name"]: idx+1 for idx, item in enumerate(st.session_state.last_rank)}

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
                change = f"↑ 上升 {prev-rank} 名"
                icon = "📈"
                color = "#2ECC71"
            elif rank > prev:
                change = f"↓ 下降 {rank-prev} 名"
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
elif nav == "活动风采":
    st.title("协会活动")
    st.write("新任主席上任以来所接手的所有活动")

    st.divider()
    st.markdown("#### <center>**2025年10月10日迎接2025级国际新生志愿活动**</center>", unsafe_allow_html=True)
    st.markdown(
        "&emsp;&emsp;2025年10月10日在31名四川信息职业技术学院雪峰校区开展迎新活动，在全体师生的共同努力下圆满结束,不仅为新生们营造了一个温馨、热情的入学氛围,也展现了学校的凝聚力和向心力。活动前期,我们进行了周密的筹备工作,包括场地布置、物资准备、人员分工等,确保每一个细节都能体现对新生的关怀。&emsp;&emsp;<br>&emsp;&emsp;活动中,志愿者们积极投入,耐心解答新生疑问,引导他们完成报到手续,并详细介绍校园环境和生活设施。迎新活动圆满落幕,我们见证了新成员们从陌生到熟悉的转变过程。活动中,我们注重互动与交流,通过才艺展示、互动问答等环节,让新成员们充分展示自我,增进彼此的了解。同时,我们也为新成员们准备了丰富的迎新礼包和贴心的生活指南,帮助他们更快地适应新环境。此次迎新活动不仅让新成员们感受到了学校的温暖与关怀,也激发了他们对未来学习生活的热情与憧憬。例如,部分环节衔接不够流畅,部分志愿者对新生报到流程不够熟悉,导致出现了一些小混乱。未来,我们将总结经验教训,进一步优化迎新流程,提高活动效率和质量。",
        unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_file_path_1 = os.path.join(script_dir, "..", "image", "迎新.jpeg")
    image_file_path_2 = os.path.join(script_dir, "..", "image", "破冰.jpg")
    image_file_path_3 = os.path.join(script_dir, "..", "image", "剪纸.jpeg")

    image_file_path_1 = os.path.normpath(image_file_path_1)
    image_file_path_2 = os.path.normpath(image_file_path_2)
    image_file_path_3 = os.path.normpath(image_file_path_3)
    with col2:
        st.image(
            image_file_path_1,
            caption='迎新活动照片')
    col_left, col_right = st.columns([7, 3])
    with col_right:
        st.write("国际交流协会")
        st.write("2025年10月10日")

    st.divider()
    st.markdown("#### <center>**2025年11月1日国际交流协会“认识你很高兴”破冰活动总结**</center>", unsafe_allow_html=True)
    st.markdown("&emsp;&emsp;2025年11月1日14：00～15：30在雪峰校区电气楼2312国际交流协会联合自动化协会成功举办“认识你很高兴”破冰活动，协会"
                "与自动化协会内部中国籍成员与在校国际学生共同参与，协会成员共59人，其中本协会39人，自动化协会20人。本协会活动促进新老成员交流、拓宽"
                "交际圈，推动中外学生友好互动。&emsp;&emsp;<br>&emsp;&emsp;活动前期，工作人员提前完成场地布置、奖品采购、指令盲盒准备等工作"
                "，14:10-14:20参与成员有序签到。14:20-14:50开展“红蓝指令盲盒”活动，成员分为红蓝阵营（中国籍成员为红方、国际学生为蓝方），"
                "通过抽取箱子中的互动指令完成交流任务，完成者获得小挂件、圆珠笔等奖励；在才艺表演环节，表现突出的同学获得毛绒玩偶奖励；开展“击鼓传花"
                "”活动，接到“炸弹玩偶”的成员上台表演或接受挑战。活动结束，工作人员组织清理场地卫生，确保场地恢复整洁。&emsp;&emsp;<br>&emsp;&emsp;活动全程秩序井然，安全保障到"
                "位，活动有效促进了协会成员间的相互认识，为中外学生文化交流搭建了良好平台，丰富了大家的校园生活。",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(
            image_file_path_2,
            caption='破冰活动照片')
    col_left, col_right = st.columns([7, 3])
    with col_right:
        st.write("国际交流协会")
        st.write("2025年11月1日")

    st.divider()
    st.markdown("#### <center>**2025年12月4日国际交流协会“剪韵传世界·非遗架心桥”活动总结**</center>",
                unsafe_allow_html=True)
    st.markdown("&emsp;&emsp;2025年12月4日14:00-15:30，国际交流协会在雪峰校区图书馆成功举办“剪韵传世界·非遗架心桥”非遗剪纸交流活"
                "动，协会内部成员33人全程参与。活动以非遗剪纸文化为核心，分为三大板块有序开展：14:00-14:10完成前期工作安排，确保活动顺利启动"
                "；14:10-14:20，指导老师详细讲解剪纸历史文化知识，让成员深入了解非遗魅力；14:20-14:40，老师示范剪纸基础技法，耐心指导成员掌握"
                "核心技巧；14:40-15:20为实践创作环节，成员们动手制作剪纸及相关文创作品，尽情展现创意与动手能力；15:20-15:30活动总结收尾，成员们"
                "展示作品、交流心得，随后共同完成场地卫生清洁。&emsp;&emsp;<br>&emsp;&emsp;活动全程严格遵守纪律要求，无中途私自离席情况，安全"
                "保障组按分工落实治安、消防、交通秩序维护及突发事件处置准备，确保活动安全有序。通过本次活动，中外学生不仅学习了剪纸技艺、传承了非遗文化"
                "，更搭建了友好交流的桥梁，增强了协会凝聚力与文化认同感，有效提升了成员的文化沟通与交际能力。",
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.image(
            image_file_path_3,
            caption='非遗剪纸交流活动照片')
    col_left, col_right = st.columns([7, 3])
    with col_right:
        st.write("国际交流协会")
        st.write("2025年12月4日")

elif nav == "活动选人":
    st.title("活动选人")

    # 初始化session_state用于保存选择结果
    if 'selected_result' not in st.session_state:
        st.session_state.selected_result = None
    if 'chinese_list' not in st.session_state:
        st.session_state.chinese_list = []
    if 'foreign_list' not in st.session_state:
        st.session_state.foreign_list = []

    uploaded_file = st.file_uploader("请上传活动报名表", type=['xlsx'])

    if uploaded_file is not None:
        try:
            # 显示原始Excel数据
            df = pd.read_excel(uploaded_file, engine='openpyxl')

            st.divider()
            st.write("### 本次参加活动人员名单")
            st.dataframe(df, use_container_width=True)
            st.divider()

            # 获取报名人员信息（假设姓名在第3列C列，国籍在第7列G列，索引从0开始）
            name_list = []
            nation_list = []

            # 从第3行开始读取数据（索引2，跳过表头）
            for i in range(2, len(df)):
                name_val = df.iloc[i, 2]  # C列：姓名
                nation_val = df.iloc[i, 6] if len(df.columns) > 6 else ""  # G列：国籍

                # 检查是否为空值
                if pd.notna(name_val) and str(name_val).strip():
                    name_list.append(str(name_val).strip())
                    nation_list.append(str(nation_val).strip() if pd.notna(nation_val) else "")

            # 按国籍分类
            chinese_names = []
            foreign_names = []

            for name, nation in zip(name_list, nation_list):
                # 判断是否为中国籍（包含"中国"或为空时默认为中国籍）
                if "中国" in nation or nation == "":
                    chinese_names.append(name)
                else:
                    foreign_names.append(name)

            # 保存到session_state
            st.session_state.chinese_list = chinese_names
            st.session_state.foreign_list = foreign_names

            st.write("### 随机选人设置")
            st.info(
                f"📊 统计信息：总人数 {len(name_list)} 人 | 中国籍 {len(chinese_names)} 人 | 国际学生 {len(foreign_names)} 人")

            # 验证是否有有效数据
            if len(name_list) == 0:
                st.warning("⚠️ 没有找到有效的报名人员数据")
            else:
                # 选择模式
                col_mode = st.columns(1)
                with col_mode[0]:
                    select_mode = st.radio(
                        "选择模式",
                        ["混合选择", "仅中国籍", "仅国际学生", "分别选择"],
                        horizontal=True
                    )

                st.divider()

                # 根据模式显示不同的输入框
                selected_chinese = []
                selected_foreign = []

                if select_mode == "混合选择":
                    col1, col2 = st.columns(2)
                    with col1:
                        total_select = st.number_input(
                            "总抽选人数",
                            min_value=0,
                            max_value=len(name_list),
                            value=min(5, len(name_list)),
                            step=1,
                            help="从所有报名人员中随机抽取"
                        )

                    with col2:
                        st.write("")
                        st.write("")
                        select_button = st.button("🎲 开始随机选择", type="primary", use_container_width=True)

                    if select_button:
                        if total_select > 0:
                            all_names = chinese_names + foreign_names
                            selected_names = np.random.choice(all_names, size=total_select, replace=False)
                            st.session_state.selected_result = pd.DataFrame({
                                '选中人员': selected_names,
                                '类型': ['中国籍' if n in chinese_names else '国际学生' for n in selected_names]
                            })
                        else:
                            st.warning("请选择要抽取的人数")

                elif select_mode == "仅中国籍":
                    col1, col2 = st.columns(2)
                    with col1:
                        chinese_select = st.number_input(
                            "中国籍抽选人数",
                            min_value=0,
                            max_value=len(chinese_names),
                            value=min(5, len(chinese_names)),
                            step=1,
                            help=f"共有 {len(chinese_names)} 名中国籍成员"
                        )

                    with col2:
                        st.write("")
                        st.write("")
                        select_button = st.button("🎲 开始随机选择", type="primary", use_container_width=True)

                    if select_button:
                        if chinese_select > 0:
                            selected_chinese = np.random.choice(chinese_names, size=chinese_select, replace=False)
                            st.session_state.selected_result = pd.DataFrame({
                                '选中人员': selected_chinese,
                                '类型': ['中国籍'] * len(selected_chinese)
                            })
                        else:
                            st.warning("请选择要抽取的人数")

                elif select_mode == "仅国际学生":
                    col1, col2 = st.columns(2)
                    with col1:
                        foreign_select = st.number_input(
                            "国际学生抽选人数",
                            min_value=0,
                            max_value=len(foreign_names),
                            value=min(5, len(foreign_names)),
                            step=1,
                            help=f"共有 {len(foreign_names)} 名国际学生"
                        )

                    with col2:
                        st.write("")
                        st.write("")
                        select_button = st.button("🎲 开始随机选择", type="primary", use_container_width=True)

                    if select_button:
                        if foreign_select > 0:
                            selected_foreign = np.random.choice(foreign_names, size=foreign_select, replace=False)
                            st.session_state.selected_result = pd.DataFrame({
                                '选中人员': selected_foreign,
                                '类型': ['国际学生'] * len(selected_foreign)
                            })
                        else:
                            st.warning("请选择要抽取的人数")

                elif select_mode == "分别选择":
                    st.write("#### 分别设置各类型人数")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        chinese_select = st.number_input(
                            "中国籍人数",
                            min_value=0,
                            max_value=len(chinese_names),
                            value=min(3, len(chinese_names)),
                            step=1,
                            help=f"共有 {len(chinese_names)} 名中国籍成员"
                        )

                    with col2:
                        foreign_select = st.number_input(
                            "国际学生人数",
                            min_value=0,
                            max_value=len(foreign_names),
                            value=min(2, len(foreign_names)),
                            step=1,
                            help=f"共有 {len(foreign_names)} 名国际学生"
                        )

                    with col3:
                        st.write("")
                        st.write("")
                        select_button = st.button("🎲 开始随机选择", type="primary", use_container_width=True)

                    if select_button:
                        if chinese_select > 0 or foreign_select > 0:
                            result_data = {'选中人员': [], '类型': []}

                            # 选择中国籍
                            if chinese_select > 0 and len(chinese_names) > 0:
                                selected_chinese = np.random.choice(chinese_names, size=chinese_select, replace=False)
                                result_data['选中人员'].extend(selected_chinese)
                                result_data['类型'].extend(['中国籍'] * len(selected_chinese))

                            # 选择国际学生
                            if foreign_select > 0 and len(foreign_names) > 0:
                                selected_foreign = np.random.choice(foreign_names, size=foreign_select, replace=False)
                                result_data['选中人员'].extend(selected_foreign)
                                result_data['类型'].extend(['国际学生'] * len(selected_foreign))

                            st.session_state.selected_result = pd.DataFrame(result_data)
                        else:
                            st.warning("请至少选择一个类型的人数")

                # 显示选择结果
                if st.session_state.selected_result is not None:
                    st.divider()
                    st.success(f"✅ 已成功选择 {len(st.session_state.selected_result)} 人")

                    # 按类型分组显示
                    st.write("### 🎯 选择结果")

                    # 显示统计表
                    type_count = st.session_state.selected_result['类型'].value_counts()
                    stats_cols = st.columns(len(type_count))
                    for idx, (type_name, count) in enumerate(type_count.items()):
                        with stats_cols[idx]:
                            st.metric(type_name, f"{count} 人")

                    st.divider()

                    # 显示详细列表
                    st.dataframe(
                        st.session_state.selected_result.reset_index(drop=True),
                        use_container_width=True,
                        hide_index=True
                    )

                    # 提供下载按钮
                    csv_data = st.session_state.selected_result.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 下载选择结果 (CSV)",
                        data=csv_data,
                        file_name=f"选中人员_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

        except ValueError as ve:
            if "Cannot take a larger sample than population" in str(ve):
                st.error("❌ 选择人数不能超过可用人员数量")
            else:
                st.error(f"❌ 数值错误：{str(ve)}")
        except Exception as e:
            st.error(f"❌ 处理失败：{str(e)}")
            st.exception(e)  # 开发时显示详细错误信息
