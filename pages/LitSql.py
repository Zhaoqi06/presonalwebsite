import sqlite3
#初始化notification.sql
def execute_sql_script(db_path, sql_script_path):
    """
    执行SQL脚本文件
    :param db_path: 数据库文件路径（如../data/notification.db）
    :param sql_script_path: SQL脚本文件路径（如./sql_scripts/notification.sql）
    """
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 读取并执行SQL脚本
        with open(sql_script_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            cursor.executescript(sql_content)

        # 提交事务并关闭连接
        conn.commit()
        print("notification.sql脚本执行成功！数据库初始化完成")
    except sqlite3.Error as e:
        print(f"执行脚本出错：{e}")
    finally:
        if conn:
            conn.close()


# 调用函数（请根据你的文件路径调整）
if __name__ == "__main__":
    execute_sql_script(
        db_path="../data/notification.db",  # 你的db文件路径
        sql_script_path="../sql_scripts/notification.sql"  # 你的sql文件路径
    )
