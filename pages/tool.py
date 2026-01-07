import streamlit as st
import os
from datetime import datetime
import ffmpeg
import subprocess
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
nav = st.sidebar.selectbox("导航栏", ["视频转GIF", "视频调速"])

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
