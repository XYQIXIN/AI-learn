import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# step1：文档加载
from langchain_community.document_loaders import TextLoader

loader = TextLoader(os.path.join(os.path.dirname(__file__), './藜麦.txt'), encoding='utf-8')
documents = loader.load()

#step2： 文本分割
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=128, #每个chunk 的最大字符数
    chunk_overlap=50, #每个chunk 之间的重叠字符数（能够保持上下文连贯）
    separators=['\n\n', '\n', "。 ", "! ", "? ", "//"] #分隔符优先级
)

texts = text_splitter.create_documents(    #把文档分割成多个chunks
    [documents[0].page_content],
    metadatas=[documents[0].metadata]       #保留文档元数据
)

#step 3: 向量化与存储
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma 

# 配置embedding 模型参数
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
#创建embedding 模型
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为文本生成向量表示用于文本检索"
)
#加载数据到 chroma 数据库
db = Chroma.from_documents(
    documents=texts,
    embedding=embeddings
)

#step4: 相似度检索
search_result = db.similarity_search("藜一般在几月播种？")

print("===检索结果===")
for i, doc in enumerate(search_result):
    print(f"[{i+1}] {doc.page_content[:200]}...")

#step5: 对话式问答
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "deepseek-v4-flash",
    temperature=0,
    api_key= "sk-xxxx",
    base_url="https://api.deepseek.com"
)
# 创建索引器
retriever = db.as_retriever()
#创建记忆组件（保存对话历史，实现多轮对话）
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
#构建问答链
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

result = qa.invoke({"question": "藜怎么防治虫害？"})
print("问题:", result.get("question"))
print("回答:", result.get("answer"))
