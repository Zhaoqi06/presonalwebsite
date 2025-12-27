import streamlit as st
import os
from datetime import datetime

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("请先登录")
    st.switch_page("pages/login.py")
# 隐藏默认导航/水印
st.markdown("""
            <style>
            .css-14xtw13,.css-1v3fvcr{display:none !important;}
            </style>
              """, unsafe_allow_html=True)

if "刘钊齐" == st.session_state["username"]:
    st.title("欢迎进入管理页面")
    st.divider()
    nav = st.sidebar.selectbox("导航栏",["首页", "数学教学"])
    if nav == "首页":
        st.header("分布通知")
        with st.form("input_form"):
            title_input = st.text_input("标题")
            text_input = st.text_area("文本")
            time_input = st.date_input("时间")
            submit_btn = st.form_submit_button("提交")
        if submit_btn:
            if not title_input or not text_input or not time_input:
                st.error("请填写完整的信息")
            else:
                card_file_path = "document\card_file.txt"
                with open(card_file_path,'a',encoding = "utf-8") as f:
                    f.write("标题:"+title_input+"\n")
                    f.write("文本:"+text_input+"\n")
                    f.write(f"时间:{time_input}\n")
                    f.write("\n")
                    st.success("分布成功！")
                    f.close()
        st.divider()
        st.header("删除通知")

        with st.form("delete_form"):
            title_input = st.text_input("标题")
            time_input = st.date_input("时间")
            submit_btn = st.form_submit_button("提交")

        if submit_btn:
            card_file_path = "document\card_file.txt"
            time_input_str = time_input.strftime("%Y-%m-%d")
            try:
                # 1. 读取文件所有内容
                with open(card_file_path, 'r', encoding="utf-8") as f:
                    lines = f.readlines()
                # 问题3、5修正：避免遍历中删除元素，先记录需要保留的行
                new_lines = []
                i = 0
                while i < len(lines):
                    # 匹配标题和日期（使用转换后的字符串）
                    if (title_input in lines[i]) and (i + 2 < len(lines)) and (time_input_str in lines[i + 2]):
                        # 匹配成功：跳过这3行（即不添加到new_lines，等同于删除）
                        i += 3  # 跳过i、i+1、i+2
                    else:
                        # 匹配失败：保留当前行，i递增1
                        new_lines.append(lines[i])
                        i += 1

                # 问题4修正：将修改后的内容写回文件（w模式覆盖原文件）
                with open(card_file_path, 'w', encoding="utf-8") as f:
                    f.writelines(new_lines)

                st.success("通知删除成功！")
                f.close()

            except FileNotFoundError:
                st.error(f"错误：找不到文件 {card_file_path}，请检查文件路径是否正确")
            except IndexError:
                st.error("错误：文件内容格式异常，未找到对应的日期行")
            except Exception as e:
                st.error(f"删除失败：{str(e)}")


else:
    st.error("非管理员人员不能进入该页面")



    #with card1:
        #st.subheader("行课通知")
        #st.write("由于授课结构调整，本次会有短期行课安排，行课时间为2025/12/22日开始的每周六下午，具体时间听从安排。")
        #st.write("行课内容为 数学必修一 必修二 必修三 必修四 必修五 选修4-5.各位同学提前准备！")
