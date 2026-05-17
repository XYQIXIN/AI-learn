# 配置模型部分
import os
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

os.environ['DEEPSEEK_API_KEY'] = 'sk-xxx'
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

Settings.llm = OpenAILike(
    model="deepseek-chat",
    api_key=os.environ['DEEPSEEK_API_KEY'],
    api_base="https://api.deepseek.com/v1",
    temperature=0.1,
    is_chat_model=True,
)

model_path = r"C:\Users\A\.cache\huggingface\hub\models--BAAI--bge-small-zh-v1.5\snapshots\7999e1d3359715c523056ef9478215996d62a620"
Settings.embed_model = HuggingFaceEmbedding(model_name=model_path)

print("LLM + Embedding 配置完毕")
print(f" LLM: Deepseek(deepseek-v4-flash)")
print(f" Embedding: BAAI/bge-small-zh-v1.5(本地运行)")

# 加载文档
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader

loader = SimpleDirectoryReader(
    input_dir=os.path.join(os.path.dirname(__file__), "data"),
    file_extractor={".pdf": PyMuPDFReader()},
)
documents = loader.load_data()
print(f"成功加载 {len(documents)} 个文档")
for doc in documents:
    fname = doc.metadata.get('file_name', 'unknown')
    print(f" - {fname} ({len(doc.text):,})字符")

# 文档切分
from llama_index.core.node_parser import SentenceSplitter
splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50,
)
nodes = splitter.get_nodes_from_documents(documents)
print(f"切分完成 {len(documents)}个文档 -> {len(nodes)} 个 chunk")

print()
print("--- 前两个 chunk 预览 ---")
for i, node in enumerate(nodes[:2]):
    print(f"\n[Chunk {i+1}]({len(node.text)} 字符):")
    print(node.text[:200])
    print("...")

# 构建向量索引
import faiss
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.faiss import FaissVectorStore
d = 512
faiss_index = faiss.IndexFlatL2(d)
vector_store = FaissVectorStore(faiss_index=faiss_index)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
vector_index = VectorStoreIndex(nodes, storage_context=storage_context)

print(f"向量索引构建完成")
print(f" 向量数量：{len(nodes)}")
print(f" 向量维度：{d}")

# 基础问答
query_engine = vector_index.as_query_engine(similarity_top_k=3)

question = "世运电路2023年上半年实现营业收入多少?"
response = query_engine.query(question)

print(f"Q: {question}")
print(f"A: {response}")
print()
print(f"回答基于 {len(response.source_nodes)}个检索到的 chunk")

# DEBUG查看检索结果
from llama_index.core.retrievers import VectorIndexRetriever
retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3)

question = "同仁堂安宫牛黄丸的市场价格"
retrieved_nodes = retriever.retrieve(question)

print(f"问题: {question}")
print(f"检索到 {len(retrieved_nodes)} 个 chunk:")

for i, node in enumerate(retrieved_nodes):
    print(f"\n{'='*60}")
    print(f"chunk {i+1}: | 相似度得分: {node.score:.4f}(越小越相似)")
    print(f"{'='*60}")
    print(node.node.text[:400])

# 带记忆的多轮对话
from llama_index.core.memory import ChatMemoryBuffer
memory = ChatMemoryBuffer.from_defaults(token_limit=5000)

chat_engine = vector_index.as_chat_engine(
    chat_mode='context',
    memory=memory,
    system_prompt="你是一个基于检索结果回答问题的助手。如果检索不到相关信息,就诚实地说不知道。",
)

q1 = "世运电路2023年上半年实现营业收入多少?"
response1 = chat_engine.chat(q1)
print(f">> 用户{q1}")
print(f">> 助手{response1}")
print()

q2 = "它同比增长了多少?"
response2 = chat_engine.chat(q2)
print(f">> 用户{q2}")
print(f">> 助手{response2}")

# Agent模块
import nest_asyncio
nest_asyncio.apply()

from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core import SummaryIndex

def vector_query(query:str) -> str:
    engine = vector_index.as_query_engine(similarity_top_k=3)
    return engine.query(query)

vector_tool = FunctionTool.from_defaults(
    name = "precise_search",
    fn = vector_query,
    description="对文档进行向量检索,适合回答具体事实性问题,例如：[××营业收入多少?] [××价格多少]"
)

summary_index = SummaryIndex(nodes)
summary_engine = summary_index.as_query_engine(response_mode="tree_summarize")

summary_tool = QueryEngineTool.from_defaults(
    name = 'summary',
    query_engine=summary_engine,
    description="对文档进行概括总结,适合回答整体性问题,例如：[总结一下××] [这篇文章讲了什么]"
)

print("工具箱准备完毕：")
print(" 1. precise_search - 精确检索（查具体问题）")
print(" 2. summary - 全文总结（查整体问题）")

# Agent 运行
from llama_index.core.agent import ReActAgent

agent = ReActAgent(
    tools=[vector_tool, summary_tool],
    llm=Settings.llm,
    verbose=True
)

import asyncio

async def run_agent_tests():
    print("=" * 60)
    print("测试1:整体性问题(预期用 summary)")
    print("=" * 60)
    handler = agent.run("总结一下兴证电子")
    response = await handler
    print()
    print("最终回答：")
    print(response)
    print()

    print("=" * 60)
    print("测试2:具体问题(预期用 precise_search)")
    print("=" * 60)
    handler = agent.run("世运电路2023年同比增长多少")
    response = await handler
    print()
    print("最终回答：")
    print(response)

asyncio.run(run_agent_tests())
