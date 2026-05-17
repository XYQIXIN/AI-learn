"""
LangChain v1.0 风格 RAG 实现
对比原始版本的主要变化：
  1. Embedding: HuggingFaceBgeEmbeddings → langchain_huggingface.HuggingFaceEmbeddings
  2. 对话链: ConversationalRetrievalChain → create_history_aware_retriever + create_retrieval_chain (LCEL)
  3. 记忆:   ConversationBufferMemory → 手动管理 chat_history 列表
"""
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# ========== Step 1: 文档加载 ==========
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    os.path.join(os.path.dirname(__file__), "./藜麦.txt"),
    encoding="utf-8",
)
documents = loader.load()

# ========== Step 2: 文本分割 ==========
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=128,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "!", "?", "//"],
)

texts = text_splitter.create_documents(
    [documents[0].page_content],
    metadatas=[documents[0].metadata],
)

# ========== Step 3: 向量化与存储 ==========
# 与原版共用 embedding 方式，复用已缓存的模型，避免重新下载
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为文本生成向量表示用于文本检索",
)

db = Chroma.from_documents(documents=texts, embedding=embeddings)

# ========== Step 4: 相似度检索 ==========
search_result = db.similarity_search("藜一般在几月播种？")

print("=== 检索结果 ===")
for i, doc in enumerate(search_result):
    print(f"[{i+1}] {doc.page_content[:200]}...")

# ========== Step 5: 对话式问答 (v1.0 LCEL 风格) ==========
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 配置 LLM
llm = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key="sk-xxxx",
    base_url="https://api.deepseek.com",
)

# 2. 检索器
retriever = db.as_retriever()

# 3. "感知历史"的检索器 —— 根据对话历史改写出更好的检索 query
contextualize_prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    (
        "system",
        "根据聊天历史，将用户当前的问题改写为一个独立的、无需上下文就能理解的检索查询。"
        "如果用户的问题已经独立完整，直接原样返回即可。",
    ),
])
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_prompt
)

# 4. 基于文档生成答案的链
qa_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一个农业专家，严格根据以下参考资料回答问题。"
        "如果资料中没有相关信息，请如实说'参考文档未提及'。"
        "\n\n参考资料:\n{context}",
    ),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
stuff_chain = create_stuff_documents_chain(llm, qa_prompt)

# 5. 组装完整的 RAG 链
rag_chain = create_retrieval_chain(history_aware_retriever, stuff_chain)

# 6. 提问（chat_history 由调用方手动维护，不再依赖 ConversationBufferMemory）
chat_history = []

result = rag_chain.invoke({"input": "藜怎么防治虫害？", "chat_history": chat_history})
print("\n问题:", result.get("input"))
print("回答:", result.get("answer"))
