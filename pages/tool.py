import ffmpeg
import os
import tempfile
from datetime import datetime
from pathlib import Path
import streamlit as st
import subprocess
import zipfile
import shutil
import requests
import time
from urllib.parse import urlencode
from bs4 import BeautifulSoup
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")


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


# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏", ["视频转GIF", "视频调速","M4A转MP3","批量找图"])

if nav == "视频转GIF":
    st.title("视频转GIF工具")

    uploaded_file = st.file_uploader("选择视频文件", type=['mp4', 'avi', 'mov', 'mkv'])

    if uploaded_file is not None:
        # 保存上传的文件
        video_path = f"temp_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 显示视频预览
        st.video(uploaded_file)

        col1, col2 = st.columns(2)
        with col1:
            start_time = st.number_input("开始时间（秒）", 0, 300, 0)
        with col2:
            end_time = st.number_input("结束时间（秒）", 0, 300, 10)

        col3, col4 = st.columns(2)
        with col3:
            fps = st.slider("GIF帧率", 1, 30, 10)
        with col4:
            scale_width = st.slider("宽度（像素）", 160, 1280, 480)

        if st.button("转换为GIF"):
            if end_time <= start_time:
                st.error("结束时间必须大于开始时间")
            else:
                with st.spinner("正在转换..."):
                    try:
                        # 计算持续时间
                        duration = end_time - start_time

                        # 生成GIF文件名
                        gif_filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"

                        # 使用高质量转换函数
                        success = mp4_to_gif_high_quality(
                            video_path,
                            gif_filename,
                            start_time=start_time,
                            duration=duration,
                            fps=fps,
                            scale_width=scale_width
                        )

                        if success:
                            # 显示结果
                            st.success("高质量GIF转换成功！")
                            st.image(gif_filename)

                            # 提供下载
                            with open(gif_filename, "rb") as file:
                                st.download_button(
                                    label="下载GIF",
                                    data=file,
                                    file_name=gif_filename,
                                    mime="image/gif"
                                )
                        else:
                            st.error("转换失败")

                    except Exception as e:
                        st.error(f"转换失败：{str(e)}")
                    finally:
                        # 清理临时文件
                        if os.path.exists(video_path):
                            os.remove(video_path)
                        if os.path.exists(gif_filename):
                            os.remove(gif_filename)

elif nav == "视频调速":
    st.title("视频调速工具")
    uploaded_file = st.file_uploader("选择视频文件", type=['mp4', 'avi', 'mov', 'mkv'])

    if uploaded_file is not None:
        # 保存上传的文件
        video_path = f"temp_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 显示原始视频
        st.video(uploaded_file)

        # 显示视频信息
        try:
            probe = ffmpeg.probe(video_path)
            video_streams = [stream for stream in probe['streams'] if stream['codec_type'] == 'video']
            if video_streams:
                video_info = video_streams[0]
                duration = float(probe['format']['duration'])
                st.info(f"视频时长: {duration:.2f}秒 | 分辨率: {video_info['width']}x{video_info['height']} | 格式: {video_info['codec_name']}")
        except:
            pass

        speed_factor = st.slider("播放速度", 0.1, 5.0, 1.0, 0.1)

        if st.button("调整速度"):
            with st.spinner("正在处理..."):
                try:
                    # 生成新文件名
                    output_filename = f"speed_adjusted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

                    # 使用优化后的视频调速函数
                    success = adjust_video_speed_improved(video_path, output_filename, speed_factor)

                    if success:
                        # 显示结果
                        st.success(f"处理成功！速度调整为 {speed_factor}x")
                        st.video(output_filename)

                        # 提供下载
                        with open(output_filename, "rb") as file:
                            st.download_button(
                                label="下载视频",
                                data=file,
                                file_name=output_filename,
                                mime="video/mp4"
                            )
                    else:
                        st.error("视频调速处理失败")

                except Exception as e:
                    st.error(f"处理失败：{str(e)}")
                finally:
                    # 清理临时文件
                    if os.path.exists(video_path):
                        os.remove(video_path)
                    if os.path.exists(output_filename):
                        os.remove(output_filename)
elif nav == "M4A转MP3":

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


    # Streamlit 页面设置
    st.set_page_config(page_title="M4A→MP3转换器", page_icon="🎵", layout="centered")
    st.title("M4A 转 MP3 工具")
    st.markdown("采用 **320kbps CBR** + **`-q:a 0`** 最高质量参数，最大限度保留音质。")

    # 检查 FFmpeg 是否可用
    def check_ffmpeg():
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except:
            return False


    if not check_ffmpeg():
        st.error("⚠️ 未检测到 FFmpeg，请安装并将其加入系统 PATH。")
        st.info("""
        **Windows**: 下载 [FFmpeg](https://ffmpeg.org/download.html) → 解压 → 将 `bin` 目录添加到环境变量 PATH。
        **macOS**: `brew install ffmpeg`
        **Linux**: `sudo apt install ffmpeg`
        """)
        st.stop()

    mode = st.sidebar.radio("选择功能", ["📁 单文件转换", "📂 批量文件夹转换"])

    if mode == "📁 单文件转换":
        st.subheader("上传单个 M4A 文件并转换为 MP3")
        uploaded_file = st.file_uploader("选择 M4A 文件", type=['m4a', 'mp4'], key="single")
        if uploaded_file is not None:
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_input:
                tmp_input.write(uploaded_file.getbuffer())
                tmp_input_path = tmp_input.name
            output_filename = f"{Path(uploaded_file.name).stem}.mp3"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            col1, col2 = st.columns(2)
            with col1:
                st.audio(tmp_input_path, format="audio/m4a")
            if st.button("开始转换", type="primary"):
                with st.spinner("转换中，请稍候..."):
                    success = ffmpeg_m4a_to_mp3_best(tmp_input_path, output_path)
                if success:
                    st.success("✅ 转换完成！")
                    with col2:
                        st.audio(output_path, format="audio/mp3")
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="📥 下载 MP3",
                            data=f,
                            file_name=output_filename,
                            mime="audio/mpeg"
                        )
            try:
                os.unlink(tmp_input_path)
                os.unlink(output_path)
            except:
                pass


    elif mode == "📂 批量文件夹转换":
        st.subheader("批量转换多个 M4A 文件")
        # 多文件上传控件
        uploaded_files = st.file_uploader(

            "选择多个 M4A 文件",
            type=['m4a', 'mp4'],
            accept_multiple_files=True,
            key="batch_files"
        )

        if uploaded_files:
            st.info(f"已选择 {len(uploaded_files)} 个文件")
            # 显示文件列表
            for f in uploaded_files:
                st.write(f"📄 {f.name}")

            # 开始转换按钮
            if st.button("开始批量转换", type="primary"):
                # 创建临时目录存放输出文件
                output_dir = tempfile.mkdtemp()
                success_count = 0
                fail_count = 0
                # 进度显示
                progress_bar = st.progress(0, text="准备转换...")
                status_text = st.empty()
                log_placeholder = st.empty()
                log_messages = []
                total = len(uploaded_files)
                for idx, uploaded_file in enumerate(uploaded_files):
                    # 更新进度
                    progress = (idx + 1) / total
                    progress_bar.progress(progress, text=f"正在转换：{uploaded_file.name}")
                    status_text.info(f"进度：{idx + 1}/{total}")
                    # 保存上传文件到临时路径
                    suffix = Path(uploaded_file.name).suffix
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_input:
                        tmp_input.write(uploaded_file.getbuffer())
                        tmp_input_path = tmp_input.name
                    # 输出文件路径
                    output_filename = f"{Path(uploaded_file.name).stem}.mp3"
                    output_path = os.path.join(output_dir, output_filename)
                    # 执行转换
                    try:
                        success = ffmpeg_m4a_to_mp3_best(tmp_input_path, output_path)
                    except Exception as e:
                        success = False
                        st.error(f"转换 {uploaded_file.name} 时出错：{str(e)}")
                    # 清理输入临时文件
                    os.unlink(tmp_input_path)
                    if success:
                        success_count += 1
                        log_messages.append(f"✅ {uploaded_file.name} → MP3")
                    else:
                        fail_count += 1
                        log_messages.append(f"❌ {uploaded_file.name} 转换失败")
                    log_placeholder.code("\n".join(log_messages[-5:]))
                progress_bar.empty()
                status_text.empty()
                # 汇总结果
                if fail_count == 0:
                    st.success(f"🎉 全部转换成功！共 {success_count} 个文件。")
                else:
                    st.warning(f"转换完成。成功 {success_count} 个，失败 {fail_count} 个。")
                # 提供打包下载
                if success_count > 0:
                    zip_path = os.path.join(tempfile.gettempdir(),
                                            f"converted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
                    with zipfile.ZipFile(zip_path, 'w') as zipf:
                        for filename in os.listdir(output_dir):
                            if filename.endswith('.mp3'):
                                file_path = os.path.join(output_dir, filename)
                                zipf.write(file_path, arcname=filename)
                    with open(zip_path, "rb") as f:
                        st.download_button(
                            label="📥 下载全部转换后的 MP3 (ZIP)",
                            data=f,
                            file_name=os.path.basename(zip_path),
                            mime="application/zip"
                        )
    st.markdown("---")
    st.caption("转换引擎：FFmpeg 原生 MP3 编码器 | 参数：-b:a 320k -q:a 0")

if nav == "批量找图":
    # 初始化会话状态（保存关键信息，避免页面重渲染丢失）
    if "downloaded_count" not in st.session_state:
        st.session_state.downloaded_count = 0  # 实际下载的图片数量
    if "output_dir" not in st.session_state:
        st.session_state.output_dir = ""  # 图片保存的临时目录
    if "zip_path" not in st.session_state:
        st.session_state.zip_path = ""  # 压缩包路径

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


    st.header("批量找图工具")
    col1, col2 = st.columns(2)
    with col1:
        search_keyword = st.text_input("搜索关键词", placeholder="请输入要查找的图片关键词（如：风景、猫咪）")
    with col2:
        max_count = st.number_input("查找数量", min_value=1, max_value=200, value=10)

    # 提交按钮逻辑
    if st.button("提交", type="primary"):
        if not search_keyword.strip():
            st.error("请输入有效的搜索关键词！")
        else:
            try:
                st.success("提交成功")
                with st.spinner("查找中，请稍后..."):
                    # 重置会话状态（避免旧数据干扰）
                    st.session_state.output_dir = tempfile.mkdtemp(prefix=f"{search_keyword}_imgs_")
                    # 调用下载函数并保存下载数量到会话状态
                    st.session_state.downloaded_count = bing_image_downloader(
                        keyword=search_keyword,
                        save_dir=st.session_state.output_dir,
                        max_count=max_count
                    )
                # 清空压缩包路径（新提交后重置）
                st.session_state.zip_path = ""
            except Exception as e:
                st.error(f"程序运行出错：{str(e)}")

    # ========== 核心修复：基于会话状态显示按钮 ==========
    if st.session_state.downloaded_count > 0:
        # 生成压缩包按钮（点击后保存压缩包路径到会话状态）
        if st.button("生成压缩包", type="primary") and st.session_state.zip_path == "":
            zip_filename = f"{search_keyword}的图片.zip"
            st.session_state.zip_path = os.path.abspath(zip_filename)
            # 生成压缩包
            shutil.make_archive(os.path.splitext(zip_filename)[0], "zip", st.session_state.output_dir)
            st.success("压缩包生成成功！")

        # 只要压缩包路径存在，就显示下载按钮（不受页面重渲染影响）
        if st.session_state.zip_path and os.path.exists(st.session_state.zip_path):
            with open(st.session_state.zip_path, "rb") as zip_file:
                st.download_button(
                    label="下载ZIP",
                    data=zip_file,
                    file_name=os.path.basename(st.session_state.zip_path),
                    mime="application/zip",
                    # 下载后清理文件（可选）
                    on_click=lambda: (
                        shutil.rmtree(st.session_state.output_dir, ignore_errors=True),
                        os.remove(st.session_state.zip_path) if os.path.exists(st.session_state.zip_path) else None,
                        st.session_state.update(downloaded_count=0, output_dir="", zip_path="")
                    )
                )
    elif st.session_state.downloaded_count == 0 and st.session_state.output_dir != "":
        st.warning("未下载到任何图片，请更换关键词或减少查找数量重试！")