import os
import sqlite3
import streamlit as st
from datetime import datetime
import random

#=======================邀请码==============
import random
from datetime import datetime
import sqlite3

#===================邀请码=====================
def init_invite_table():
    """初始化邀请码表"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS invite_number
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           date
                           TEXT
                           NOT
                           NULL
                           UNIQUE,
                           invite_num
                           INTEGER
                           NOT
                           NULL,
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )
                       ''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"初始化用户信息表出错：{e}")
    finally:
        conn.close()


def get_daily_invite_num():
    """获取当日邀请码，基于数据库存储"""
    # 初始化表
    init_invite_table()
    # 获取今日日期
    today = datetime.now().date().strftime("%Y-%m-%d")

    # 查询数据库
    conn = sqlite3.connect('count_password.db')
    cursor = conn.cursor()

    cursor.execute("SELECT invite_num FROM invite_number WHERE date = ?", (today,))
    result = cursor.fetchone()

    if result:
        # 今日邀请码已存在
        invite_num = result[0]
        conn.close()
        return invite_num
    else:
        # 生成新的邀请码
        new_invite_num = random.randint(10000000, 99999999)

        # 插入数据库
        cursor.execute("INSERT INTO invite_number (date, invite_num) VALUES (?, ?)", (today, new_invite_num))
        conn.commit()
        conn.close()

        return new_invite_num

def read_invite_number():
    conn = get_db_connection_count_password()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM invite_number")
        rows = cursor.fetchall()
        information = [{"id": row["id"], "date": row["date"], "invite_num": row["invite_num"]} for row in rows]
        return information
    except sqlite3.Error as e:
        st.error(f"读取邀请码出错：{e}")
#=================管理账号密码数据库===================

def get_db_connection_count_password():
    """提取公共连接函数，增加路径初始化"""
    try:
        db_path = os.path.join("data", "count_password.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"数据库连接失败：{e}")
        return None

def read_count_password():
    """读取用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM information")
        rows = cursor.fetchall()
        information = [{"id": row["id"], "username": row["username"], "password": row["password"]} for row in rows]
        return information
    except sqlite3.Error as e:
        st.error(f"读取用户信息出错：{e}")

def write_count_password(username, password):
    """写入用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO information (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"写入用户信息出错：{e}")

def Updata_count_password(username, password):
    """更新用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE information SET password=? WHERE username=?", (password, username))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"更新用户信息出错：{e}")
    finally:
        conn.close()

def init_count_password_table():
    """初始化用户信息表，确保表结构完整"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS information
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL
                       )
                       """)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"初始化用户信息表出错：{e}")
    finally:
        conn.close()
def delete_count_password(username):
    """删除用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM information WHERE username=?", (username,))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"删除用户信息出错：{e}")
    finally:
        conn.close()

#================管理信息函数============================

def get_db_connection_notification():
    """提取公共连接函数，增加路径初始化"""
    try:
        db_path = os.path.join("./data", "notification.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"数据库连接失败：{e}")
        return None

def init_notification_table():
    """初始化通知表，确保表结构完整"""
    conn = get_db_connection_notification()
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
def write_notification(title, text, notice_time):
    """写入数据，优化错误提示和时间格式"""
    conn = None
    try:
        conn = get_db_connection_notification()
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

def delete_notification(title=None, text=None, time=None, id=None):
    """优化删除逻辑，增加类型校验和页面提示"""
    conn = None
    try:
        conn = get_db_connection_notification()
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
    conn = get_db_connection_notification()
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