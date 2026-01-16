import sqlite3


def get_db_connection():
    """提取公共连接函数"""
    try:
        conn = sqlite3.connect("../data/notification.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"数据库连接失败：{e}")
        return None


def init_table():
    """初始化表（先删除旧表，再创建新表，含title字段）"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        # 第一步：删除旧表（测试阶段可执行，有数据则慎用）
        cursor.execute("DROP TABLE IF EXISTS notifications")
        # 第二步：重新创建包含title字段的表
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
                           NULL, -- 新增title字段
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
        print("表初始化成功（已创建含title字段的notifications表）")
    except sqlite3.Error as e:
        print(f"初始化表出错：{e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def write_sql(title, text, time):
    """写入数据"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()
        # 插入数据（表已初始化，直接插入）
        cursor.execute(
            "INSERT INTO notifications (title, text, time) VALUES (?, ?, ?)",
            (title, text, time)
        )
        conn.commit()
        print(f"数据插入成功！共插入 {cursor.rowcount} 条数据")
    except sqlite3.Error as e:
        print(f"插入数据出错：{e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def read_sql():
    """读取数据"""
    conn = None
    try:
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()
        # 读取数据（表已初始化，直接读取）
        cursor.execute("SELECT * FROM notifications")
        rows = cursor.fetchall()
        for row in rows:
            print(f"id: {row[0]}, title: {row[1]}, text: {row[2]}, time: {row[3]}")
    except Exception as e:
        print(f"读取数据出错：{e}")
    finally:
        if conn:
            conn.close()
# 先初始化表（删除旧表+创建新表），再写入数据
init_table()
write_sql('通知', '你好', '2023-05-05')
read_sql()