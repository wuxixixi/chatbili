import os
import json
from database import get_db_connection
from langchain.docstore.document import Document
from langchain_community.llms import QianfanLLMEndpoint

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 从环境变量获取千帆平台的凭证
QIANFAN_AK = os.getenv("QIANFAN_AK")
QIANFAN_SK = os.getenv("QIANFAN_SK")
model_name = "ERNIE-Bot-turbo"  # 替换为实际使用的模型名称

# 初始化 Qianfan LLM 并传递凭证
llm_qianfan = QianfanLLMEndpoint(
    model=model_name,
    streaming=True,
    qianfan_ak=QIANFAN_AK,
    qianfan_sk=QIANFAN_SK,
)

def analyze_and_store():
    """
    从数据库读取视频信息，使用 Qianfan LLM 提炼有价值的信息，并存储到 analysis_results 表中
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT bvid, title, description, desc_v2, dynamic FROM videos")
            video_rows = cursor.fetchall()
            for row in video_rows:
                bvid, title, desc, desc_v2, dynamic = row
                # 组合需要分析的内容
                analysis_content = f"""
                视频标题: {title}
                描述: {desc}
                详细描述: {desc_v2}
                动态: {dynamic}
                请提炼出对科研、论文写作有价值的信息：
                """
                # 调用 Qianfan LLM 进行信息提炼
                summary = llm_qianfan(analysis_content)
                # 将提炼结果存储到 analysis_results 表中
                cursor.execute(
                    "INSERT INTO analysis_results (video_id, analysis_text) VALUES (?, ?)",
                    (bvid, summary)
                )
                conn.commit()
                print(f"视频 {bvid} 的分析结果已存储。")
    except Exception as e:
        print(f"分析与存储时出错: {e}")

def load_analysis_documents():
    """
    从 analysis_results 表中加载分析文本，并转换为 Document 对象
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT video_id, analysis_text FROM analysis_results")
            analysis_rows = cursor.fetchall()
            analysis_docs = []
            for row in analysis_rows:
                vid, atext = row
                doc = Document(page_content=atext, metadata={'video_id': vid})
                analysis_docs.append(doc)
            return analysis_docs
    except Exception as e:
        print(f"加载分析文档时出错: {e}")
        return []
