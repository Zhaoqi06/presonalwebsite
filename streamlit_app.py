import streamlit as st
import os
import sqlite3


# ==================== 数据库核心函数 ====================
def get_db_connection():
    """提取公共连接函数，确保data文件夹存在"""
    # 先创建data文件夹（避免路径不存在）
    data_dir = "../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    try:
        # 拼接绝对路径，避免相对路径歧义
        db_path = os.path.join(data_dir, "notification.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # 支持按字段名取值
        return conn
    except sqlite3.Error as e:
        st.error(f"数据库连接失败：{e}")  # Streamlit页面显示错误，而非print
        return None


def init_notification_table():
    """初始化通知表（确保表存在且字段完整）"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # 创建表（含id/title/text/time字段）
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS notifications
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           title
                           TEXT
                           NOT
                           NULL,
                           text
                           TEXT
                           NOT
                           NULL,
                           time
                           TEXT
                           NOT
                           NULL
                       )
                       """)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"初始化通知表出错：{e}")
    finally:
        conn.close()


def read_notifications():
    """读取通知数据，返回结构化列表（避免全局变量）"""
    notifications = []  # 用列表存储字典，更易读
    conn = get_db_connection()
    if not conn:
        return notifications

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, text, time FROM notifications ORDER BY id DESC")  # 按ID倒序（最新的在前）
        rows = cursor.fetchall()

        # 按字段名取值，而非索引，更健壮
        for row in rows:
            notifications.append({
                "id": row["id"],
                "title": row["title"],
                "text": row["text"],
                "time": row["time"]
            })
    except sqlite3.Error as e:
        st.error(f"读取通知数据出错：{e}")
    finally:
        conn.close()

    return notifications


# ==================== Streamlit页面逻辑 ====================
# 页面基础配置
st.set_page_config(page_title="首页", layout="wide")

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# 初始化通知表（确保表存在）
init_notification_table()

# 页面内容
st.title(f"欢迎回来! {st.session_state['username']}")
st.write("单丝不成线、独木不成林！共建开放包容之路，共赢共同发展之果！")

# 分割线
st.divider()

# 功能按钮列
col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.7, 1.2, 1.2, 1, 1.2])
with col1:
    if st.button("国际交流协会"):
        st.switch_page("pages/association.py")
with col2:
    if st.button("创新创业俱乐部"):
        st.switch_page("pages/association.py")
with col3:
    if st.button("实用工具"):
        st.switch_page("pages/tool.py")
with col4:
    if st.button("学习资料"):
        st.switch_page("pages/Study.py")
with col5:
    if st.button("个人"):
        st.switch_page("pages/association.py")
with col6:
    if st.button("退出登录"):
        st.session_state.clear()
        st.switch_page("pages/login.py")

# 读取并显示通知
st.divider()
st.subheader("最新通知")
notifications = read_notifications()

# 处理通知显示逻辑（修复缩进错误）
if not notifications:
    st.info("暂无通知")
else:
    # 遍历通知，显示卡片
    for notice in notifications:
        with st.container(border=True):
            st.subheader(notice["title"])
            st.write(notice["text"])
            st.caption(f"发布时间：{notice['time']}")  # 用caption显示时间，更美观