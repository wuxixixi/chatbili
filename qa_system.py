import os
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.chat_models import QianfanChatEndpoint
from analysis import load_analysis_documents

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 初始化 Qianfan LLM
model_name = "ERNIE-Bot-turbo"  # 替换为实际使用的模型名称
llm_qianfan = QianfanChatEndpoint(model=model_name, streaming=True)

# 初始化 Qianfan Embeddings
qianfan_ak = os.getenv("QIANFAN_AK")
qianfan_sk = os.getenv("QIANFAN_SK")

embeddings = QianfanEmbeddingsEndpoint(
    qianfan_ak=qianfan_ak,
    qianfan_sk=qianfan_sk,
)

def build_retriever():
    """
    加载分析文档，构建向量数据库并返回检索器
    """
    analysis_docs = load_analysis_documents()
    vectordb = Chroma.from_documents(analysis_docs, embeddings)
    retriever = vectordb.as_retriever()
    return retriever

def get_qa_chain():
    """
    构建并返回 RAG 问答链
    """
    retriever = build_retriever()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm_qianfan,
        chain_type="stuff",
        retriever=retriever
    )
    return qa_chain
