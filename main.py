import streamlit as st
from data_collection import gather_bilibili_data
from analysis import analyze_and_store
from qa_system import get_qa_chain

# 初始化数据库
from database import initialize_database

# 运行初始化
initialize_database()

def main():
    st.title("Bilibili 视频数据分析与问答系统")

    st.header("1. 数据收集")
    video_url = st.text_input("请输入 Bilibili 视频的 URL：")
    if st.button("获取并存储视频信息"):
        if video_url:
            try:
                gather_bilibili_data([video_url])
                st.success("视频信息已成功获取并存储到数据库中。")
                # 调用分析函数
                with st.spinner("正在分析视频信息..."):
                    analyze_and_store()
                st.success("视频信息已成功分析并存储。")
            except Exception as e:
                st.error(f"获取或存储视频信息时出错: {e}")
        else:
            st.warning("请输入一个有效的 Bilibili 视频 URL。")

    st.header("2. 问答系统")
    user_query = st.text_input("请输入您的问题：")
    if st.button("提交问题"):
        if user_query:
            try:
                qa_chain = get_qa_chain()
                with st.spinner("正在生成回答..."):
                    answer = qa_chain.run(user_query)
                st.success("回答生成成功！")
                st.write(answer)
            except Exception as e:
                st.error(f"生成回答时出错: {e}")
        else:
            st.warning("请输入一个问题。")

if __name__ == "__main__":
    main()
