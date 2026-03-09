import ffmpeg
import os
import tempfile
from datetime import datetime
from pathlib import Path
import streamlit as st
import zipfile
import shutil
import function as fc
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")


# 使用 selectbox 实现导航
nav = st.sidebar.selectbox("导航栏", ["视频转GIF", "视频调速","M4A转MP3","批量找图","MOV转MP4"])

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
                        success = fc.mp4_to_gif_high_quality(
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
                    success = fc.adjust_video_speed_improved(video_path, output_filename, speed_factor)

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
    # Streamlit 页面设置
    st.set_page_config(page_title="M4A→MP3转换器", page_icon="🎵", layout="centered")
    st.title("M4A 转 MP3 工具")
    st.markdown("采用 **320kbps CBR** + **`-q:a 0`** 最高质量参数，最大限度保留音质。")
    if not fc.check_ffmpeg():
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
                    success = fc.ffmpeg_m4a_to_mp3_best(tmp_input_path, output_path)
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
                        success = fc.ffmpeg_m4a_to_mp3_best(tmp_input_path, output_path)
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
                    st.session_state.downloaded_count = fc.bing_image_downloader(
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
                    # 下载后清理文件
                    on_click=lambda: (
                        shutil.rmtree(st.session_state.output_dir, ignore_errors=True),
                        os.remove(st.session_state.zip_path) if os.path.exists(st.session_state.zip_path) else None,
                        st.session_state.update(downloaded_count=0, output_dir="", zip_path="")
                    )
                )
    elif st.session_state.downloaded_count == 0 and st.session_state.output_dir != "":
        st.warning("未下载到任何图片，请更换关键词或减少查找数量重试！")

elif nav == "MOV转MP4":
    st.header("MOV转MP4格式！")

    import subprocess
    import re
    import logging
    from tqdm import tqdm

    # 配置日志
    logging.basicConfig(level=logging.INFO)

    def get_video_duration(input_path):
        """获取视频总时长（秒），用于进度计算"""
        try:
            cmd = [
                'ffmpeg', '-i', input_path,
                '-f', 'null', '-',
                '-hide_banner', '-loglevel', 'error',
                '-stats'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            # 匹配时长（如 Duration: 00:01:23.45, start: 0.000000, bitrate: ...）
            duration_pattern = re.compile(r'Duration: (\d+:\d+:\d+\.\d+)')
            match = duration_pattern.search(result.stderr)
            if match:
                time_str = match.group(1)
                h, m, s = time_str.split(':')
                return int(h) * 3600 + int(m) * 60 + float(s)
        except Exception as e:
            logging.error(f"获取视频时长失败：{str(e)}")
        return None

    def convert_mov_to_mp4(
            input_path,
            output_path,
            video_bitrate="5M",  # 视频比特率（默认5Mbps，可改如"10M"）
            resolution=None,  # 分辨率（如"1920x1080"，None则保持原分辨率）
            fps=None,  # 帧率（如30，None则保持原帧率）
            audio_bitrate="128k"  # 音频比特率
    ):
        """转换单个MOV文件为MP4"""
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            logging.error(f"输入文件不存在：{input_path}")
            return False

        # 检查输入是否为MOV文件
        if not input_path.lower().endswith('.mov'):
            logging.error(f"非MOV文件，跳过：{input_path}")
            return False

        # 创建输出文件夹（如果不存在）
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # 获取视频总时长（修复total_duration未定义问题）
        total_duration = get_video_duration(input_path)

        # 构建ffmpeg命令
        cmd = [
            'ffmpeg',
            '-i', input_path,  # 输入文件
            '-vcodec', 'libx264',  # 视频编码（MP4主流编码）
            '-acodec', 'aac',  # 音频编码
            '-b:v', video_bitrate,  # 视频比特率
            '-b:a', audio_bitrate,  # 音频比特率
            '-strict', 'experimental',  # 兼容部分音频格式
            '-y'  # 覆盖已有文件
        ]

        # 添加分辨率参数（如果指定）
        if resolution:
            cmd.extend(['-s', resolution])

        # 添加帧率参数（如果指定）
        if fps:
            cmd.extend(['-r', str(fps)])

        # 输出文件
        cmd.append(output_path)

        try:
            # 执行ffmpeg命令并捕获输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1  # 行缓冲，实时获取输出
            )

            # 正则表达式：匹配ffmpeg输出中的时间（如 time=00:01:23.45）
            time_pattern = re.compile(r'time=(\d+:\d+:\d+\.\d+)')
            progress_bar = None

            # 实时解析输出，更新进度条
            for line in process.stdout:
                match = time_pattern.search(line)
                if match and total_duration:
                    # 解析当前时间（转为秒）
                    time_str = match.group(1)
                    h, m, s = time_str.split(':')
                    current_seconds = int(h) * 3600 + int(m) * 60 + float(s)
                    progress = min(100, current_seconds / total_duration * 100)

                    # 初始化进度条
                    if not progress_bar:
                        progress_bar = tqdm(total=100, unit='%', desc=os.path.basename(input_path))
                    # 更新进度条
                    progress_bar.update(progress - progress_bar.n)

            # 等待进程结束
            process.wait()

            # 关闭进度条
            if progress_bar:
                progress_bar.close()

            # 检查转换是否成功
            if process.returncode == 0:
                logging.info(f"转换成功：{output_path}")
                return True
            else:
                logging.error(f"转换失败（返回码：{process.returncode}）：{input_path}")
                return False

        except Exception as e:
            logging.error(f"转换出错：{str(e)}，文件：{input_path}")
            return False

    def batch_convert(input_path, output_dir, **kwargs):
        """批量转换（输入为文件或文件夹）"""
        if os.path.isfile(input_path):
            # 单个文件处理
            filename = os.path.basename(input_path)
            output_filename = os.path.splitext(filename)[0] + '.mp4'
            output_path = os.path.join(output_dir, output_filename)
            return convert_mov_to_mp4(input_path, output_path,** kwargs)
        elif os.path.isdir(input_path):
            # 文件夹批量处理（只处理MOV文件）
            success_count = 0
            fail_count = 0
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith('.mov'):
                        input_file = os.path.join(root, file)
                        # 保持原文件夹结构输出
                        relative_path = os.path.relpath(root, input_path)
                        output_subdir = os.path.join(output_dir, relative_path)
                        output_file = os.path.join(output_subdir, os.path.splitext(file)[0] + '.mp4')
                        if convert_mov_to_mp4(input_file, output_file, **kwargs):
                            success_count += 1
                        else:
                            fail_count += 1
            logging.info(f"批量转换完成：成功{success_count}个，失败{fail_count}个")
            return success_count > 0
        else:
            logging.error(f"输入路径无效：{input_path}")
            return False

    # ========== 新增Streamlit交互逻辑（适配前端使用） ==========
    # 1. 文件上传
    uploaded_file = st.file_uploader("选择MOV文件", type=['mov'], key="mov2mp4")

    # 2. 转换参数配置
    st.subheader("转换参数")
    col1, col2 = st.columns(2)
    with col1:
        video_bitrate = st.text_input("视频比特率", value="5M", help="如5M/10M，数值越大画质越好")
        resolution = st.text_input("分辨率（选填）", placeholder="如1920x1080，留空保持原分辨率")
    with col2:
        fps = st.number_input("帧率（选填）", min_value=1, max_value=60, value=None, placeholder="留空保持原帧率")
        audio_bitrate = st.text_input("音频比特率", value="128k", help="如128k/192k")

    # 3. 转换逻辑
    if uploaded_file is not None:
        # 保存上传的MOV文件到临时路径
        temp_mov = tempfile.NamedTemporaryFile(delete=False, suffix='.mov')
        temp_mov.write(uploaded_file.getbuffer())
        temp_mov.close()

        # 输出路径
        output_mp4 = os.path.join(tempfile.gettempdir(), f"{os.path.splitext(uploaded_file.name)[0]}.mp4")

        # 转换按钮
        if st.button("开始转换", type="primary"):
            with st.spinner("正在转换..."):
                # 整理参数（过滤空值）
                convert_kwargs = {
                    "video_bitrate": video_bitrate,
                    "audio_bitrate": audio_bitrate
                }
                if resolution.strip():
                    convert_kwargs["resolution"] = resolution.strip()
                if fps:
                    convert_kwargs["fps"] = fps

                # 执行转换
                success = convert_mov_to_mp4(temp_mov.name, output_mp4,** convert_kwargs)

                if success:
                    st.success("转换成功！")
                    # 预览视频
                    st.video(output_mp4)
                    # 下载按钮
                    with open(output_mp4, "rb") as f:
                        st.download_button(
                            label="下载MP4文件",
                            data=f,
                            file_name=f"{os.path.splitext(uploaded_file.name)[0]}.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("转换失败，请检查文件或参数！")

            # 清理临时文件
            os.unlink(temp_mov.name)
            if os.path.exists(output_mp4):
                os.unlink(output_mp4)