import streamlit as st
import os
st.set_page_config(page_title="首页", layout="wide")
# 拦截未登录用户
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")
st.title(f"欢迎回来!{st.session_state['username']}")
st.write("单丝不成线、独木不成林！共建开放包容之路，共赢共同发展之果！")
#----------------------------------------------------------------------------
st.divider()
col1,col2,col3,col4,col5,col6 = st.columns([1.5,1.7,1.2,1.2,1,1.2])
# 添加退出登录功能
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
 # 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
docx_file_path = os.path.join(script_dir, "..", "document", "notifications.docx")
docx_file_path = os.path.normpath(docx_file_path)

    # 从 docx 文件读取通知内容
titles = []
texts = []
times = []

try:
    if os.path.exists(docx_file_path):
        doc = Document(docx_file_path)

            # 遍历文档中的所有段落
        i = 0
        while i < len(doc.paragraphs):
            para = doc.paragraphs[i]

                # 查找标题段落
            if para.text.startswith("标题:"):
                title = para.text[3:].strip()  # 去掉"标题:"前缀
                titles.append(title)

                    # 查找下一个文本段落
                if i + 1 < len(doc.paragraphs):
                    content_para = doc.paragraphs[i + 1]
                    if content_para.text.startswith("文本:"):
                        text = content_para.text[3:].strip()
                        texts.append(text)
                    else:
                        texts.append("")  # 如果没有找到文本段落，添加空字符串
                else:
                    texts.append("")

                    # 查找下一个时间段落
                if i + 2 < len(doc.paragraphs):
                    time_para = doc.paragraphs[i + 2]
                    if time_para.text.startswith("时间:"):
                        time = time_para.text[3:].strip()
                        times.append(time)
                    else:
                        times.append("")  # 如果没有找到时间段落，添加空字符串
                else:
                    times.append("")

                    # 跳过当前通知块（标题、内容、时间、分隔线共4段）
                i += 4
                continue
            else:
                i += 1
    else:
        st.info("暂无通知")
except Exception as e:
    st.error(f"读取通知文件失败：{str(e)}")

    # 显示通知卡片
    # 获取三个列表中最短的长度，避免索引越界
    min_length = min(len(titles), len(texts), len(times))
    for i in range(min_length):
        card_name = "card" + str(i + 1)
        card = st.container(border=True)
        with card:
            st.subheader(titles[i])
            st.write(texts[i])
            st.write(f"时间：{times[i]}")
