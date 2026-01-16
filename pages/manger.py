import streamlit as st
import os
# 关键修改1：显式导入datetime和date，避免层级引用异常
from datetime import datetime
import sqlite3

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

# ==================== 数据库核心函数 ====================
def init_data_folder():
    """自动创建data文件夹，避免路径不存在"""
    data_dir = "../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        st.success("自动创建data文件夹成功")

def get_db_connection():
    """提取公共连接函数，增加路径初始化"""
    init_data_folder()
    try:
        db_path = os.path.join("../data", "notification.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"数据库连接失败：{e}")
        return None

def init_notification_table():
    """初始化通知表，确保表结构完整"""
    conn = get_db_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS notifications
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           text TEXT NOT NULL,
                           time TEXT NOT NULL
                       )
                       """)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"初始化通知表出错：{e}")
    finally:
        conn.close()

# 关键修改2：移除多余的isinstance类型检测，直接格式化时间
def write_sql(title, text, notice_time):
    """写入数据，优化错误提示和时间格式"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()
        # 直接格式化（st.date_input返回的一定是date对象，无需检测）
        time_str = notice_time.strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO notifications (title, text, time) VALUES (?, ?, ?)",
            (title, text, time_str)
        )
        conn.commit()
        st.success(f"数据插入成功！共插入 {cursor.rowcount} 条数据")
    except sqlite3.Error as e:
        st.error(f"插入数据出错：{e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_sql(title=None, text=None, time=None, id=None):
    """优化删除逻辑，增加类型校验和页面提示"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()
        if id:
            try:
                id_int = int(id)
            except ValueError:
                st.error("ID必须是数字！")
                return
            sql = "DELETE FROM notifications WHERE id = ?"
            params = (id_int,)
        elif title and text and time:
            sql = "DELETE FROM notifications WHERE title=? AND text=? AND time=?"
            params = (title, text, time)
        elif title:
            sql = "DELETE FROM notifications WHERE title=?"
            params = (title,)
        else:
            st.error("删除条件不能为空！请至少传入id或title（或组合条件）")
            return

        cursor.execute(sql, params)
        conn.commit()

        if cursor.rowcount > 0:
            st.success(f"数据删除成功！共删除 {cursor.rowcount} 条数据")
        else:
            st.warning("未找到匹配的数据，删除操作无效果")
    except sqlite3.Error as e:
        st.error(f"删除数据出错：{e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def read_notifications():
    """读取所有通知，用于管理页面显示"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, text, time FROM notifications ORDER BY id DESC")
        rows = cursor.fetchall()
        notifications = [{"id": row["id"], "title": row["title"], "text": row["text"], "time": row["time"]} for row in
                         rows]
        return notifications
    except sqlite3.Error as e:
        st.error(f"读取通知出错：{e}")
        return []
    finally:
        conn.close()

# ==================== 页面逻辑 ====================
init_notification_table()

ADMIN_USER = "刘钊齐"
if ADMIN_USER == st.session_state["username"]:
    st.title("欢迎进入管理页面")
    st.divider()
    nav = st.sidebar.selectbox("导航栏", ["首页", "数学教学"])

    if nav == "首页":
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
                write_sql(title_input, text_input, time_input)

        st.divider()

        # 删除通知模块
        st.header("删除通知")
        st.subheader("现有通知列表")
        notifications = read_notifications()
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
                delete_sql(id=id_input)

else:
    st.error("非管理员人员不能进入该页面")