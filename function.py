import os
import sqlite3
import streamlit as st
from datetime import datetime
import random
import ffmpeg
import tempfile
from pathlib import Path
import subprocess
import zipfile
import shutil
import requests
import time
from urllib.parse import urlencode
from bs4 import BeautifulSoup
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


#===============================视频转GIF与视频调速===========================================
def mp4_to_gif_high_quality(input_file, output_file, start_time=0, duration=None, fps=15, scale_width=480):

    try:
        # 创建调色板
        palette_stream = ffmpeg.input(input_file, ss=start_time)
        if duration:
            # 使用正确的ffmpeg-python语法截取时间段
            palette_stream = ffmpeg.trim(palette_stream, duration=duration)
        else:
            palette_stream = ffmpeg.setpts(palette_stream, 'PTS-STARTPTS')

        palette_stream = palette_stream.filter('fps', fps=fps)
        palette_stream = palette_stream.filter('scale', scale_width, -1)
        palette_stream = palette_stream.filter('palettegen')

        # 生成调色板文件
        palette_file = "palette.png"
        ffmpeg.output(palette_stream, palette_file).run(overwrite_output=True)

        # 使用调色板生成高质量GIF
        video_stream = ffmpeg.input(input_file, ss=start_time)
        if duration:
            # 使用正确的ffmpeg-python语法截取时间段
            video_stream = ffmpeg.trim(video_stream, duration=duration)
        else:
            video_stream = ffmpeg.setpts(video_stream, 'PTS-STARTPTS')

        video_stream = video_stream.filter('fps', fps=fps)
        video_stream = video_stream.filter('scale', scale_width, -1)

        palette_input = ffmpeg.input(palette_file)
        output_stream = ffmpeg.filter([video_stream, palette_input], 'paletteuse')

        ffmpeg.output(output_stream, output_file).run(overwrite_output=True)

        # 清理临时调色板文件
        if os.path.exists(palette_file):
            os.remove(palette_file)

        return True
    except Exception as e:
        st.error(f"转换失败: {e}")
        return False


def adjust_video_speed_improved(input_file, output_file, speed_factor=1.0):
    """
    改进版视频速度调整函数，解决音视频同步问题
    """
    try:
        # 首先尝试使用 ffprobe 命令行工具诊断文件
        print(f"正在诊断文件: {input_file}")
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1', input_file]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"ffprobe 诊断失败: {result.stderr}")
            return False

        print("文件诊断通过，正在处理...")

        # 获取视频基本信息
        probe = ffmpeg.probe(input_file)
        video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']

        if not video_streams:
            print("❌ 未找到视频流")
            return False

        video_info = video_streams[0]
        print(f"检测到视频流: {video_info['codec_name']} {video_info['width']}x{video_info['height']}")

        input_stream = ffmpeg.input(input_file)

        if speed_factor == 1.0:
            # 速度不变，直接复制流
            output_stream = ffmpeg.output(
                input_stream,
                output_file,
                vcodec='copy',
                acodec='copy'
            )
        else:
            # 处理视频流
            video_stream = input_stream.video.filter('setpts', f'{1 / speed_factor}*PTS')

            # 检查是否有音频流
            audio_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'audio']

            if audio_streams and input_stream.audio is not None:
                # 音频速度调整，支持大于2倍的速度
                audio_stream = input_stream.audio
                remaining_speed = speed_factor

                # atempo滤镜限制在0.5-2.0之间，需要分段处理
                while remaining_speed > 2.0:
                    audio_stream = audio_stream.filter('atempo', 2.0)
                    remaining_speed /= 2.0

                if remaining_speed >= 0.5:
                    audio_stream = audio_stream.filter('atempo', remaining_speed)

                output_stream = ffmpeg.output(video_stream, audio_stream, output_file)
            else:
                # 无音频或音频流不可用
                output_stream = ffmpeg.output(video_stream, output_file)

        # 执行转换
        ffmpeg.run(output_stream, overwrite_output=True, quiet=True)
        print(f"✅ 视频速度调整完成: {output_file}")
        return True

    except ffmpeg.Error as e:
        print(f"❌ FFmpeg 错误:")
        if e.stderr:
            print(f"stderr: {e.stderr.decode()}")
        return False
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        return False

#=============M4A转MP3=====================
def ffmpeg_m4a_to_mp3_best(input_file, output_file):
    """使用 FFmpeg 原生 MP3 编码器进行最高质量转换"""
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vn',
        '-acodec', 'mp3',  # 使用原生 MP3 编码器（兼容所有 FFmpeg）
        '-b:a', '320k',  # 比特率 320k
        '-q:a', '0',  # 质量等级 0（0=最好，9=最差）
        '-y',
        output_file
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)
        return True
    except subprocess.CalledProcessError as e:
        st.error(f"FFmpeg 错误: {e.stderr}")
        return False
    except FileNotFoundError:
        st.error("未找到 FFmpeg，请确保已安装并添加到系统 PATH。")
        return False


def batch_convert_m4a_to_mp3(source_dir, target_dir, progress_callback=None):
    """批量转换文件夹内所有 .m4a 文件"""
    if not os.path.exists(source_dir):
        st.error(f"源文件夹不存在：{source_dir}")
        return 0, 0
    os.makedirs(target_dir, exist_ok=True)
    m4a_files = [f for f in os.listdir(source_dir) if f.lower().endswith('.m4a')]
    total = len(m4a_files)
    if total == 0:
        st.warning("源文件夹中没有找到 .m4a 文件")
        return 0, 0
    success, fail = 0, 0
    for idx, filename in enumerate(m4a_files):
        input_path = os.path.join(source_dir, filename)
        output_path = os.path.join(target_dir, f"{Path(filename).stem}.mp3")
        if progress_callback:
            progress_callback(idx, total, filename)
        if ffmpeg_m4a_to_mp3_best(input_path, output_path):
            success += 1
        else:
            fail += 1
    return success, fail

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except:
        return False

#==================批量找图====================
def bing_image_downloader(keyword, save_dir, max_count):
    """
    批量下载必应图片搜索结果
    :param keyword: 搜索关键词（如"风景"、"cat"）
    :param save_dir: 保存图片的文件夹
    :param max_count: 最多下载数量
    """
    # 创建保存文件夹（确保目录存在）
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 必应图片搜索基础URL和请求头（模拟浏览器）
    base_url = "https://www.bing.com/images/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.bing.com/"
    }

    downloaded = 0  # 已下载数量
    offset = 0  # 分页偏移量（每次加载35张左右）

    # 替换为streamlit的进度提示（更贴合界面）
    status_text = st.empty()
    status_text.success(f"开始搜索关键词：{keyword}，最多下载{max_count}张图片...")

    while downloaded < max_count:
        # 构造搜索参数（q是关键词，first是偏移量）
        params = {
            "q": keyword,
            "first": offset,
            "form": "HDRSC2"  # 固定参数，确保返回正确格式
        }
        url = f"{base_url}?{urlencode(params)}"

        try:
            # 发送请求，获取搜索结果页
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取图片标签（必应图片的原图链接在 <a> 标签的 m 属性中）
            img_links = []
            for a_tag in soup.find_all('a', class_='iusc'):
                # m属性是一个JSON字符串，提取其中的"murl"（原图链接）
                m_data = a_tag.get('m')
                if m_data and '"murl":"' in m_data:
                    # 解析JSON字符串中的原图链接
                    murl = m_data.split('"murl":"')[1].split('"')[0]
                    img_links.append(murl)

            if not img_links:
                status_text.error("未找到更多图片，可能已到最后一页")
                break

            # 下载图片
            for img_url in img_links:
                if downloaded >= max_count:
                    break
                try:
                    # 下载图片（添加随机延迟，避免反爬）
                    time.sleep(0.5)
                    img_response = requests.get(img_url, headers=headers, timeout=15)
                    img_response.raise_for_status()

                    # 生成文件名（关键词+序号+原扩展名）
                    ext = img_url.split('.')[-1].split('?')[0]  # 提取扩展名（处理带参数的URL）
                    if len(ext) > 5:  # 避免异常扩展名
                        ext = 'jpg'
                    filename = f"{keyword}_{downloaded + 1}.{ext}"
                    save_path = os.path.join(save_dir, filename)

                    # 保存图片
                    with open(save_path, 'wb') as f:
                        f.write(img_response.content)

                    downloaded += 1
                    status_text.success(f"已下载 {downloaded}/{max_count}：{filename}")

                except Exception as e:
                    st.warning(f"下载失败（{img_url}）：{str(e)[:50]}")  # 用warning避免打断流程

        except Exception as e:
            st.error(f"请求搜索页失败：{str(e)}")
            break

        # 准备下一页（偏移量增加35，必应每页约35张）
        offset += 35
        # 适当延迟，避免频繁请求被拦截
        time.sleep(1)

    st.success(f"下载完成，共下载 {downloaded} 张图片，保存至：{os.path.abspath(save_dir)}")
    return downloaded  # 返回实际下载数量，方便后续判断

#=================管理majian数据库===================
def read_majiang():
    """读取用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM majiang")
        rows = cursor.fetchall()
        information = [{"id": row["id"], "username": row["username"], "socre": row["socre"]} for row in rows]
        return information
    except sqlite3.Error as e:
        st.error(f"读取用户信息出错：{e}")

def write_majiang(username,socre):
    """写入用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO majiang (username, socre) VALUES (?, ?)", (username, socre))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"写入用户信息出错：{e}")

def Updata_majiang(username, socre):
    """更新用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE majiang SET socre=? WHERE username=?", (socre, username))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"更新用户信息出错：{e}")
    finally:
        conn.close()

def init_count_majiang():
    """初始化用户信息表，确保表结构完整"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS majiang
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           socre TEXT NOT NULL
                       )
                       """)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"初始化用户信息表出错：{e}")
    finally:
        conn.close()
def delete_majiang(username):
    """删除用户信息"""
    conn = get_db_connection_count_password()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM majiang WHERE username=?", (username,))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"删除用户信息出错：{e}")
    finally:
        conn.close()