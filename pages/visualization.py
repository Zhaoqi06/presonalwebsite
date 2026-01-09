import streamlit as st
import snap7.client as c
import subprocess
import platform
import os
import queue
import sounddevice as sd
import vosk
import json
import threading
import time
from pathlib import Path

# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")

# =================== Vosk模型配置 ==========================
MODEL_PATH = r"C:\vosk-model-small-cn-0.22"


# 初始化全局Vosk模型
@st.cache_resource
def load_vosk_model():
    """加载Vosk模型并缓存"""
    try:
        if os.path.exists(MODEL_PATH):
            st.info("正在加载Vosk模型...")
            model = vosk.Model(MODEL_PATH)
            return model
        else:
            st.error(f"Vosk模型路径不存在: {MODEL_PATH}")
            return None
    except Exception as e:
        st.error(f"加载Vosk模型失败: {str(e)}")
        return None


# =================== PLC连接类 ==========================
class PLCConnection:
    def __init__(self):
        self.client = None
        self.connected = False
        self.plc_ip = '192.168.0.13'
        self.rack = 0
        self.slot = 1
        self.timeout = 3000

    def connect(self):
        """建立PLC连接"""
        try:
            if self.client is None:
                self.client = c.Client()
                self.client.set_param(c.S7Client.POLL_TIMEOUT, self.timeout)

            if not self.connected:
                self.client.connect(self.plc_ip, self.rack, self.slot)
                self.connected = self.client.get_connected()

            return self.client if self.connected else None
        except Exception as e:
            st.error(f"PLC连接错误: {str(e)}")
            self.connected = False
            return None

    def disconnect(self):
        """断开PLC连接"""
        try:
            if self.client and self.connected:
                self.client.disconnect()
                self.connected = False
                return True
        except Exception as e:
            st.error(f"断开连接时出错: {e}")
        return False


# =================== 初始化Session State ==========================
# 在页面开头初始化所有必要的session state
if 'plc_connection' not in st.session_state:
    st.session_state.plc_connection = PLCConnection()

if 'plc_data' not in st.session_state:
    st.session_state.plc_data = []

if 'voice_command' not in st.session_state:
    st.session_state.voice_command = ""

if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

if 'vosk_model_loaded' not in st.session_state:
    # 尝试加载模型并设置状态
    model = load_vosk_model()
    st.session_state.vosk_model = model
    st.session_state.vosk_model_loaded = model is not None
    if model:
        st.session_state.vosk_model_loaded = True
        st.rerun()  # 重新运行以更新UI


# =================== PLC数据函数 ==========================
def read_plc_data(client, db_number, start, size):
    """读取 PLC DB 块数据"""
    try:
        if client and client.get_connected():
            data = client.db_read(db_number, start, size)
            return data
    except Exception as e:
        st.error(f"数据读取错误: {e}")
    return None


def parse_db_data(byte_array):
    """解析 DB 块数据为整数"""
    if not byte_array:
        return []

    integers = []
    for i in range(0, len(byte_array), 2):
        if i + 1 < len(byte_array):
            value = int.from_bytes(byte_array[i:i + 2], byteorder='big')
            integers.append(value)
    return integers


def execute_command(command, client):
    """执行PLC命令"""
    if not command:
        return

    command_lower = command.lower()

    try:
        if "启动" in command_lower:
            st.success("✅ PLC 启动命令已发送")
            # 实际PLC控制代码
            client.db_write(10, 19, bytes([1]))
            return "启动"
        elif "停止" in command_lower:
            st.success("🛑 PLC 停止命令已发送")
            # 实际PLC控制代码
            client.db_write(10, 19, bytes([0]))
            return "停止"
        else:
            st.warning(f"未知命令: {command}")
            return None
    except Exception as e:
        st.error(f"执行命令失败: {e}")
        return None


# =================== 语音识别函数 ==========================
def record_and_recognize():
    """录音并识别语音"""
    # 确保模型已加载
    if not st.session_state.get('vosk_model_loaded', False):
        st.error("❌ Vosk模型未加载，请在模型设置页面加载模型")
        return None

    try:
        # 设置录音参数
        samplerate = 16000
        blocksize = 8000
        duration = 5  # 录音5秒

        # 创建队列和识别器
        q = queue.Queue()

        def callback(indata, frames, time, status):
            if status:
                print(f"音频状态: {status}")
            q.put(bytes(indata))

        # 创建识别器
        model = st.session_state.vosk_model
        rec = vosk.KaldiRecognizer(model, samplerate)

        # 开始录音
        st.info("🎤 正在录音...请说「启动」或「停止」")
        st.session_state.is_recording = True

        with sd.RawInputStream(samplerate=samplerate, blocksize=blocksize,
                               dtype='int16', channels=1, callback=callback):

            start_time = time.time()
            last_update = start_time

            # 录音循环
            while time.time() - start_time < duration and st.session_state.is_recording:
                # 获取音频数据
                data = q.get()

                # 处理音频
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        st.session_state.is_recording = False
                        return text
                else:
                    # 显示部分结果
                    partial_result = json.loads(rec.PartialResult())
                    partial_text = partial_result.get("partial", "")

                    # 每1秒更新一次部分结果
                    if time.time() - last_update > 1.0 and partial_text:
                        print(f"识别中: {partial_text}")
                        last_update = time.time()

            # 录音结束，获取最终结果
            final_result = json.loads(rec.FinalResult())
            text = final_result.get("text", "")
            st.session_state.is_recording = False
            return text

    except Exception as e:
        st.error(f"录音识别错误: {e}")
        st.session_state.is_recording = False
        return None


# =================== 主界面 ==========================
st.set_page_config(page_title="智能打磨分拣系统", layout="wide")

# 侧边栏导航
st.sidebar.title("导航栏")
nav = st.sidebar.radio("选择页面", ["省技能大赛", "模型设置", "音频测试"])

if nav == "省技能大赛":
    # 主标题
    st.markdown("""
        <style>
        .main-title {
            font-size: 2.2rem;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
        }
        </style>
        <div class="main-title">智能打磨分拣系统可视化</div>
    """, unsafe_allow_html=True)

    st.divider()

    # PLC连接状态区域
    col1, col2 = st.columns([3, 1])

    with col1:
        # PLC连接状态
        plc_conn = st.session_state.plc_connection
        client = plc_conn.connect()

        if client:
            st.success("✅ PLC 已连接", icon="✅")

            # 读取PLC数据
            if st.button("📥 读取PLC数据", type="primary"):
                with st.spinner("正在读取数据..."):
                    db_data = read_plc_data(client, 12, 14, 34)
                    if db_data:
                        st.session_state.plc_data = parse_db_data(db_data)
                        st.success("数据读取成功！")
                    else:
                        st.warning("读取数据失败")

            # 显示PLC数据
            if st.session_state.plc_data:
                st.subheader("📊 PLC数据监控")

                # 创建三列显示数据
                cols = st.columns(3)
                for idx, value in enumerate(st.session_state.plc_data):
                    with cols[idx % 3]:
                        st.metric(
                            label=f"DB12.DBW{14 + idx * 2}",
                            value=value,
                            delta="正常" if value > 0 else "异常",
                            delta_color="normal" if value > 0 else "inverse"
                        )
        else:
            st.error("❌ PLC 连接失败")
            if st.button("🔄 重新连接"):
                st.rerun()

    with col2:
        # 语音控制面板
        st.subheader("🎤 语音控制")

        # 显示Vosk模型状态
        if st.session_state.get('vosk_model_loaded', False):
            st.success("✅ Vosk模型已加载")
        else:
            st.warning("⚠️ Vosk模型未加载")
            if st.button("立即加载模型", key="load_model_home"):
                model = load_vosk_model()
                if model:
                    st.session_state.vosk_model = model
                    st.session_state.vosk_model_loaded = True
                    st.success("✅ 模型加载成功!")
                    st.rerun()
                else:
                    st.error("❌ 模型加载失败")

        # 语音识别按钮
        if st.button("开始语音识别", type="secondary", icon="🎤", use_container_width=True):
            if st.session_state.get('vosk_model_loaded', False):
                # 如果正在录音，则停止
                if st.session_state.is_recording:
                    st.session_state.is_recording = False
                    st.info("录音已停止")
                else:
                    # 开始录音识别
                    result = record_and_recognize()

                    if result:
                        st.session_state.voice_command = result
                        st.success(f"✅ 识别结果: {result}")

                        # 执行命令
                        if client:
                            execute_command(result, client)
                    else:
                        st.warning("未识别到有效语音")
            else:
                st.error("❌ 请先加载Vosk模型")

        # 显示录音状态
        if st.session_state.is_recording:
            st.warning("⏺️ 正在录音...")

        # 显示上次语音命令
        if st.session_state.voice_command:
            st.info(f"上次语音命令: {st.session_state.voice_command}")

    # 手动控制区域
    st.divider()
    st.subheader("🕹️ 手动控制")

    manual_col1, manual_col2 = st.columns(2)

    with manual_col1:
        if st.button("🚀 启动系统", type="primary", use_container_width=True):
            if client:
                execute_command("启动", client)
            else:
                st.error("PLC未连接")

    with manual_col2:
        if st.button("⏹️ 停止系统", type="secondary", use_container_width=True):
            if client:
                execute_command("停止", client)
            else:
                st.error("PLC未连接")

elif nav == "模型设置":
    st.title("Vosk模型设置")

    # 显示当前模型路径
    st.info(f"当前模型路径: {MODEL_PATH}")

    # 检查路径是否存在
    if os.path.exists(MODEL_PATH):
        st.success(f"✅ 模型文件夹存在")
        # 列出文件夹内容
        files = os.listdir(MODEL_PATH)
        st.write(f"📁 文件夹内容 ({len(files)}个文件):")
        for file in files[:10]:  # 只显示前10个文件
            st.write(f"  - {file}")
        if len(files) > 10:
            st.write(f"  ... 还有{len(files) - 10}个文件")
    else:
        st.error(f"❌ 模型文件夹不存在")
        st.markdown("""
        **请按照以下步骤操作:**
        1. 访问 https://alphacephei.com/vosk/models
        2. 下载: `vosk-model-small-cn-0.22.zip`
        3. 解压到: `C:\\vosk-model-small-cn-0.22`
        """)

    # 模型状态显示
    st.divider()
    st.subheader("模型状态")

    if st.session_state.get('vosk_model_loaded', False):
        st.success("✅ 模型已加载到内存")
    else:
        st.warning("⚠️ 模型未加载")

    # 加载模型按钮
    if st.button("加载Vosk模型", type="primary", key="load_model_btn"):
        with st.spinner("正在加载模型..."):
            model = load_vosk_model()
            if model:
                st.session_state.vosk_model = model
                st.session_state.vosk_model_loaded = True
                st.success("✅ 模型加载成功!")
                st.rerun()  # 刷新页面以更新状态
            else:
                st.error("❌ 模型加载失败")
                st.session_state.vosk_model_loaded = False

    # 卸载模型按钮
    if st.button("卸载Vosk模型", key="unload_model_btn"):
        st.session_state.vosk_model = None
        st.session_state.vosk_model_loaded = False
        st.info("模型已从内存卸载")
        st.rerun()

    # 模型信息
    st.divider()
    st.subheader("模型信息")

    if st.session_state.get('vosk_model_loaded', False):
        st.success("✅ 模型准备就绪")
        st.write("模型可以用于语音识别")
    else:
        st.error("❌ 模型未加载，无法使用语音识别功能")

elif nav == "音频测试":
    st.title("音频设备测试")

    # 列出音频设备
    st.subheader("音频设备列表")
    try:
        devices = sd.query_devices()
        device_info = []
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:  # 只显示输入设备
                device_info.append({
                    "ID": i,
                    "设备名": device['name'],
                    "输入通道": device['max_input_channels'],
                    "默认采样率": device['default_samplerate']
                })

        if device_info:
            st.dataframe(device_info)
        else:
            st.warning("未找到输入设备（麦克风）")

        # 选择输入设备
        default_input = sd.default.device[0] if sd.default.device else 0
        selected_device = st.selectbox(
            "选择输入设备",
            options=range(len(devices)),
            format_func=lambda x: f"{x}: {devices[x]['name']}",
            index=default_input
        )

    except Exception as e:
        st.error(f"无法获取音频设备: {e}")

    # 测试麦克风
    st.subheader("麦克风测试")

    if st.button("测试录音"):
        try:
            samplerate = 16000
            duration = 3

            st.info(f"正在录音 {duration} 秒...")

            # 设置输入设备
            sd.default.device = selected_device

            # 录音
            recording = sd.rec(int(duration * samplerate),
                               samplerate=samplerate,
                               channels=1,
                               dtype='float32')

            # 等待录音完成
            sd.wait()

            st.success("✅ 录音完成!")

            # 显示波形图
            st.line_chart(recording)

        except Exception as e:
            st.error(f"录音失败: {e}")

    # 测试Vosk识别
    st.subheader("语音识别测试")

    if st.button("测试语音识别"):
        if not st.session_state.get('vosk_model_loaded', False):
            st.error("请先在模型设置页面加载模型")
        else:
            result = record_and_recognize()
            if result:
                st.success(f"✅ 识别结果: {result}")
                st.session_state.voice_command = result
            else:
                st.warning("未识别到语音")

# 页脚
st.divider()
st.caption("智能打磨分拣系统 v1.0 | 省技能大赛项目 | 使用Vosk离线语音识别")