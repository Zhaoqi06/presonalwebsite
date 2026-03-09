import os
import streamlit as st
import time
import json
import pandas as pd
import function as f
from filelock import FileLock
import random
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

nav = st.sidebar.selectbox("导航栏",["麻将计分","卡牌战争"])
if nav == "麻将计分":

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
                if score_change < 0:
                    st.error("输入的分数有误，请重新输入！")
                else:
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



# 模拟你的 f 模块（用户信息相关）
# 实际使用时替换为你自己的文件操作逻辑
class FakeFileModule:
    def init_count_password_table(self):
        """初始化用户信息表（模拟）"""
        pass

    def read_count_password(self):
        """读取用户信息，返回包含 username 的列表"""
        # 模拟一些测试用户
        return [
            {"username": "玩家1"},
            {"username": "玩家2"},
            {"username": "测试用户"}
        ]
'''
f = FakeFileModule()
# 主游戏逻辑
def card_war_game():
    st.header("卡牌战争")
    st.write("""
    规则：每人手中共有52/n（n = 参加人数）张卡牌，其中包括 2，3，4，5，6，7，8，9，10，J = 10，Q = 12，K = 13，A = 14，
    每回合每位选手出一张牌，牌大者将桌上卡牌收为己有，如果相同则再出三张牌，出完后再出一张卡牌比大小，
    规则与前面相同，牌为0的视为淘汰！
    """)
    st.divider()

    if "plays" not in st.session_state:
        st.session_state["plays"] = []  # 存储游戏参与者

    if "game_symbol" not in st.session_state:
        st.session_state["game_symbol"] = 0  # 0=未开始，1=已开始

    if "deck" not in st.session_state:
        st.session_state["deck"] = []  # 总牌库

    if "p1_cards" not in st.session_state:
        st.session_state["p1_cards"] = []  # 玩家1的牌

    if "p2_cards" not in st.session_state:
        st.session_state["p2_cards"] = []  # 对手的牌

    if "table_cards" not in st.session_state:
        st.session_state["table_cards"] = []  # 桌上的牌

    # 读取所有用户
    user = []
    f.init_count_password_table()
    information = f.read_count_password()
    for info in information:
        user.append(info["username"])

    # 选择对手
    if st.session_state["username"] not in st.session_state["plays"]:
        with st.form("choose", clear_on_submit=True):
            compete = st.text_input("请选择对手，输入对手名字！", placeholder="例如：玩家2")
            submit_login = st.form_submit_button("提交", type="primary")

            if submit_login:
                if compete not in user:
                    st.error("你输入的名字有误，请重新输入！")
                elif compete == st.session_state["username"]:
                    st.error("不能选择自己作为对手！")
                else:
                    # 记录游戏参与者
                    st.session_state["plays"] = [st.session_state["username"], compete]
                    st.success(f"已选择对手：{compete}，可以开始游戏了！")

    # 游戏主体（已选择对手后）
    if len(st.session_state["plays"]) == 2:
        player1 = st.session_state["plays"][0]
        player2 = st.session_state["plays"][1]

        # 牌面数值映射（用于比较大小）
        card_value = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "10": 10, "J": 10, "Q": 12, "K": 13, "A": 14
        }

        # 洗牌和分牌按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("洗牌并分牌", type="primary"):
                if st.session_state["game_symbol"] == 1:
                    st.error("游戏已开始，不能重新洗牌！")
                else:
                    # 生成完整的52张牌（4种花色×13个点数）
                    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
                    deck = values * 4  # 每种牌4张，共52张
                    random.shuffle(deck)  # 洗牌

                    # 分牌：每人26张
                    st.session_state["deck"] = deck
                    st.session_state["p1_cards"] = deck[:26]
                    st.session_state["p2_cards"] = deck[26:]
                    st.session_state["game_symbol"] = 1  # 标记游戏开始
                    st.success("洗牌分牌完成！游戏开始！")

        with col2:
            if st.button("重置游戏"):
                # 重置所有游戏状态
                st.session_state["plays"] = []
                st.session_state["game_symbol"] = 0
                st.session_state["deck"] = []
                st.session_state["p1_cards"] = []
                st.session_state["p2_cards"] = []
                st.session_state["table_cards"] = []
                st.rerun()

        # 显示玩家手牌（游戏开始后）
        if st.session_state["game_symbol"] == 1:
            col_p1, col_p2 = st.columns(2)

            # 显示玩家1的牌
            with col_p1:
                st.subheader(f"{player1}的牌（剩余{len(st.session_state['p1_cards'])}张）")
                # 限制显示数量（避免列过多）
                display_p1 = st.session_state["p1_cards"][:10] if len(st.session_state["p1_cards"]) > 10 else \
                st.session_state["p1_cards"]
                cols = st.columns(len(display_p1))
                for idx, card in enumerate(display_p1):
                    with cols[idx]:
                        st.markdown(f"""
                        <div style='
                            border:2px solid #333;
                            padding:10px 14px;
                            border-radius:8px;
                            text-align:center;
                            background:white;
                            color:black;
                            font-size:16px;
                            font-weight:bold;
                        '>
                        {card}
                        </div>
                        """, unsafe_allow_html=True)
                if len(st.session_state["p1_cards"]) > 10:
                    st.write(f"... 还有 {len(st.session_state['p1_cards']) - 10} 张牌")

            # 显示玩家2的牌
            with col_p2:
                st.subheader(f"{player2}的牌（剩余{len(st.session_state['p2_cards'])}张）")
                # 对手的牌隐藏具体内容，只显示数量和背面
                display_p2 = st.session_state["p2_cards"][:10] if len(st.session_state["p2_cards"]) > 10 else \
                st.session_state["p2_cards"]
                cols = st.columns(len(display_p2))
                for idx, _ in enumerate(display_p2):
                    with cols[idx]:
                        st.markdown(f"""
                        <div style='
                            border:2px solid #333;
                            padding:10px 14px;
                            border-radius:8px;
                            text-align:center;
                            background:#e74c3c;
                            color:white;
                            font-size:16px;
                            font-weight:bold;
                        '>
                            🂠
                        </div>
                        """, unsafe_allow_html=True)
                if len(st.session_state["p2_cards"]) > 10:
                    st.write(f"... 还有 {len(st.session_state['p2_cards']) - 10} 张牌")

            st.divider()

            # 出牌逻辑
            if st.button("出一张牌",
                         disabled=len(st.session_state["p1_cards"]) == 0 or len(st.session_state["p2_cards"]) == 0):
                # 双方各出一张牌
                p1_card = st.session_state["p1_cards"].pop(0)
                p2_card = st.session_state["p2_cards"].pop(0)

                # 记录桌上的牌
                st.session_state["table_cards"].extend([p1_card, p2_card])

                # 显示本轮出牌
                st.subheader("本轮出牌")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"{player1} 出：")
                    st.markdown(f"""
                    <div style='
                        border:2px solid #333;
                        padding:15px 20px;
                        border-radius:8px;
                        text-align:center;
                        background:white;
                        color:black;
                        font-size:20px;
                        font-weight:bold;
                    '>
                    {p1_card}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.write(f"{player2} 出：")
                    st.markdown(f"""
                    <div style='
                        border:2px solid #333;
                        padding:15px 20px;
                        border-radius:8px;
                        text-align:center;
                        background:white;
                        color:black;
                        font-size:20px;
                        font-weight:bold;
                    '>
                    {p2_card}
                    </div>
                    """, unsafe_allow_html=True)

                # 比较牌的大小
                p1_val = card_value[p1_card]
                p2_val = card_value[p2_card]

                if p1_val > p2_val:
                    # 玩家1赢，收走桌上所有牌
                    st.session_state["p1_cards"].extend(st.session_state["table_cards"])
                    st.success(f"{player1} 赢了本轮！收走桌上所有牌")
                    st.session_state["table_cards"] = []
                elif p2_val > p1_val:
                    # 玩家2赢，收走桌上所有牌
                    st.session_state["p2_cards"].extend(st.session_state["table_cards"])
                    st.success(f"{player2} 赢了本轮！收走桌上所有牌")
                    st.session_state["table_cards"] = []
                else:
                    # 牌面相同，进入战争模式
                    st.warning("牌面相同！进入战争模式，双方各出3张牌打底，再比大小！")
                    # 检查是否有足够的牌
                    if len(st.session_state["p1_cards"]) >= 3 and len(st.session_state["p2_cards"]) >= 3:
                        # 各出3张打底牌
                        war_p1 = st.session_state["p1_cards"][:3]
                        war_p2 = st.session_state["p2_cards"][:3]
                        # 移除打底牌并加入桌面
                        st.session_state["p1_cards"] = st.session_state["p1_cards"][3:]
                        st.session_state["p2_cards"] = st.session_state["p2_cards"][3:]
                        st.session_state["table_cards"].extend(war_p1 + war_p2)

                        # 显示打底牌
                        st.write(f"{player1} 打底牌：{', '.join(war_p1)}")
                        st.write(f"{player2} 打底牌：{', '.join(['🂠'] * 3)}")  # 隐藏对手打底牌
                    else:
                        st.error("某方牌数不足，无法进行战争模式！")

            # 淘汰判断
            if len(st.session_state["p1_cards"]) == 0:
                st.error(f"{player1} 牌已用完，被淘汰！{player2} 获胜！")
                st.session_state["game_symbol"] = 0
            elif len(st.session_state["p2_cards"]) == 0:
                st.error(f"{player2} 牌已用完，被淘汰！{player1} 获胜！")
                st.session_state["game_symbol"] = 0

if nav == "卡牌战争":
    card_war_game()
    if st.button("重置"):
        st.session_state["plays"] = []  # 存储游戏参与者
        st.session_state["game_symbol"] = 0  # 0=未开始，1=已开始
        st.session_state["deck"] = []  # 总牌库
        st.session_state["p1_cards"] = []  # 玩家1的牌
        st.session_state["p2_cards"] = []  # 对手的牌
        st.session_state["table_cards"] = []  # 桌上的牌
'''