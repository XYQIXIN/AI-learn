# LangChain 实现 RAG — 学习笔记

## 整体流程

```
文档加载 → 文本分割 → 向量化存储 → 相似度检索 → 对话式问答
```

---

## Step 1: 文档加载

### 代码
```python
import os
# 解决 Windows 中文环境下的编码问题
loader = TextLoader(
    os.path.join(os.path.dirname(__file__), '../藜麦.txt'),
    encoding='utf-8'
)
documents = loader.load()
```

> **踩坑记录**：Windows 中文环境下 TextLoader 默认用 GBK 编码，报错 `UnicodeDecodeError`。解决：显式指定 `encoding='utf-8'`，并用 `__file__` 拼绝对路径避免运行目录不一致。

### 知识点

| 组件 | 作用 |
|------|------|
| `TextLoader` | 加载纯文本文件（.txt） |
| `documents` | 返回 `List[Document]`，每个元素有 `.page_content`（正文）和 `.metadata`（来源等元数据） |

### 其他常用 Loader
```python
# PDF 文件
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("paper.pdf")

# 网页
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com")

# Markdown
from langchain_community.document_loaders import UnstructuredMarkdownLoader
loader = UnstructuredMarkdownLoader("readme.md")
```

---

## Step 2: 文本分割

### 代码
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=128,      # 每个 chunk 的最大字符数
    chunk_overlap=50,    # 相邻 chunk 重叠字符数，保持上下文连贯
    separators=["\n\n", "\n", "。", "！", "？", "//"]  # 按优先级依次尝试分割
)

texts = text_splitter.create_documents(
    [documents[0].page_content],
    metadatas=[documents[0].metadata]   # 保留来源信息，方便追溯
)
```

### 参数建议

| 参数 | 含义 | 建议 |
|------|------|------|
| `chunk_size` | 每块最大字符数 | 中文场景 128~512；英文可更大。取决于 embedding 模型上限 |
| `chunk_overlap` | 块间重叠量 | 通常设为 chunk_size 的 10%~50%，避免关键信息被切断 |
| `separators` | 分隔符优先级 | 从粗到细：段落 → 换行 → 标点 |

### 为什么传 metadata
分割后每个 chunk 都会自动带上来源信息，方便检索时追溯原文：
```python
# texts[0].metadata → {"source": "藜麦.txt"}
```

---

## Step 3: 向量化与存储

### 代码
```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"  # 国内镜像，避免 huggingface 超时

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为文本生成向量表示用于文本检索"
)

db = Chroma.from_documents(documents=texts, embedding=embeddings)
```

> **踩坑记录**：`HuggingFaceEmbeddings`（非 Bge 版）不接受 `query_instruction` 参数，换 `HuggingFaceBgeEmbeddings` 才行。另外 huggingface.co 在国内直连超时，用 `HF_ENDPOINT=https://hf-mirror.com` 镜像。

<!-- v1.0 升级提示：
  `HuggingFaceBgeEmbeddings` 在 langchain 0.2.2+ 已标记废弃。
  v1.0 推荐安装 `langchain-huggingface` 包，使用：
  from langchain_huggingface import HuggingFaceEmbeddings
  embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
  同时去掉 query_instruction（新版本自动处理 BGE 模型的 query prefix）。
-->

### 组件说明

| 组件 | 作用 |
|------|------|
| `HuggingFaceBgeEmbeddings` | 将文本转为向量（BGE 中文模型） |
| `Chroma` | 轻量级向量数据库，内存/本地均可 |
| `from_documents()` | 一步完成：向量化文档 → 存入数据库 |

### 常用 Embedding 模型
```python
# BGE 中文系列（推荐）
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5"   # small 轻量 / large 效果好
)

# OpenAI Embedding（需 API）
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# M3E 中文模型
embeddings = HuggingFaceBgeEmbeddings(model_name="moka-ai/m3e-small")
```

### 其他向量数据库
```python
# FAISS — Facebook 的高效向量检索
from langchain_community.vectorstores import FAISS
db = FAISS.from_documents(documents, embedding)

# Chroma 默认存在内存，如需持久化：
db = Chroma.from_documents(documents, embedding, persist_directory="./chroma_db")
```

---

## Step 4: 相似度检索

### 代码
```python
search_result = db.similarity_search("藜一般在几月播种？")

print("=== 检索结果 ===")
for i, doc in enumerate(search_result):
    print(f"[{i+1}] {doc.page_content[:200]}...")
```

### 检索方法对比

| 方法 | 参数 | 说明 |
|------|------|------|
| `similarity_search(q, k=4)` | 查询文本、返回数量 | 最常用，余弦相似度 |
| `similarity_search_with_score(q)` | 查询文本 | 返回 `(文档, 分数)`，分数越低越相似 |
| `max_marginal_relevance_search(q, k=3)` | 查询文本、返回数量 | MMR 算法，结果更多样，避免重复 |

### 高级示例
```python
# 带分数的检索
results = db.similarity_search_with_score("藜麦怎么播种？")
for doc, score in results:
    print(f"[score={score:.4f}] {doc.page_content[:100]}...")

# MMR 检索（多样性优先）
results = db.max_marginal_relevance_search("藜麦怎么播种？", k=3)
```

### 自定义检索器
```python
retriever = db.as_retriever(
    search_type="mmr",           # 可选: "similarity", "mmr", "similarity_threshold"
    search_kwargs={
        "k": 5,
        "score_threshold": 0.5   # 仅 similarity_threshold 模式生效
    }
)
```

---

## Step 5: 对话式问答

### 代码
```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

# 1. 配置 LLM
llm = ChatOpenAI(
    model="deepseek-chat",       # DeepSeek 的对话模型
    temperature=0,               # 0=确定性输出，1=创造性输出
    api_key="sk-你的key",
    base_url="https://api.deepseek.com/v1"
)

# 2. 创建检索器
retriever = db.as_retriever()

# 3. 创建记忆组件（保存对话历史，实现多轮对话）
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 4. 构建问答链（必须用 from_llm，不能用构造函数）
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

# 5. 提问
result = qa.invoke({"question": "藜怎么防治虫害？"})
print("问题:", result.get("question"))
print("回答:", result.get("answer"))
```

> **踩坑记录**：新版 LangChain 不再支持 `ConversationalRetrievalChain(llm=...)` 直接传参，会报 `Extra inputs are not permitted`。必须用 `ConversationalRetrievalChain.from_llm(...)`。

<!--
v1.0 升级提示：
  `ConversationalRetrievalChain` 和 `ConversationBufferMemory` 在 v1.0 中已被 LCEL 风格替代。
  新的推荐写法如下（仅作参考，当前代码仍然可用）：

  from langchain.chains import create_history_aware_retriever, create_retrieval_chain
  from langchain.chains.combine_documents import create_stuff_documents_chain
  from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

  # Step A: 构建"感知历史"的检索器
  contextualize_prompt = ChatPromptTemplate.from_messages([
      MessagesPlaceholder("chat_history"),
      ("human", "{input}"),
  ])
  history_aware_retriever = create_history_aware_retriever(
      llm, retriever, contextualize_prompt
  )

  # Step B: 构建 QA 链
  qa_prompt = ChatPromptTemplate.from_messages([
      ("system", "基于提供的上下文回答用户问题：\n\n{context}"),
      MessagesPlaceholder("chat_history"),
      ("human", "{input}"),
  ])
  stuff_chain = create_stuff_documents_chain(llm, qa_prompt)

  # Step C: 组装完整的 RAG 链
  rag_chain = create_retrieval_chain(history_aware_retriever, stuff_chain)

  # 调用方式
  result = rag_chain.invoke({"input": "藜怎么防治虫害？", "chat_history": []})
-->

### 组件说明

| 组件 | 作用 |
|------|------|
| `ChatOpenAI` | 调用 OpenAI 兼容 API（DeepSeek、千帆等） |
| `as_retriever()` | 把向量数据库变成标准检索器接口 |
| `ConversationBufferMemory` | 存储对话历史，实现多轮对话记忆 |
| `ConversationalRetrievalChain` | 串联检索 + LLM 生成 |

### 各平台 API 配置速查
```python
# DeepSeek 官方
ChatOpenAI(model="deepseek-chat", api_key="sk-xxx",
           base_url="https://api.deepseek.com/v1")

# 百度千帆（DeepSeek 模型）
ChatOpenAI(model="deepseek-v3", api_key="xxx",
           base_url="https://qianfan.baidubce.com/v2/")

# OpenAI
ChatOpenAI(model="gpt-4o", api_key="sk-xxx")

# 阿里通义千问
ChatOpenAI(model="qwen-turbo", api_key="xxx",
           base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
```

### Prompt 自定义
```python
from langchain_core.prompts import PromptTemplate

custom_template = """你是一个农业专家，擅长回答农作物相关问题。
请严格根据以下参考资料回答。如果资料中没有相关信息，请如实说"参考文档未提及"。

参考资料：
{context}

用户问题：{question}
回答："""

qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={
        "prompt": PromptTemplate(
            input_variables=["context", "question"],
            template=custom_template
        )
    }
)
```

---

## 完整代码

```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# ========== Step 1: 文档加载 ==========
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    os.path.join(os.path.dirname(__file__), '../藜麦.txt'),
    encoding='utf-8'
)
documents = loader.load()

# ========== Step 2: 文本分割 ==========
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=128,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "//"]
)
texts = text_splitter.create_documents(
    [documents[0].page_content],
    metadatas=[documents[0].metadata]
)

# ========== Step 3: 向量化与存储 ==========
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma

model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}

embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为文本生成向量表示用于文本检索"
)
db = Chroma.from_documents(documents=texts, embedding=embeddings)

# ========== Step 4: 检索 ==========
search_result = db.similarity_search("藜一般在几月播种？")
print("=== 检索结果 ===")
for i, doc in enumerate(search_result):
    print(f"[{i+1}] {doc.page_content[:200]}...")

# ========== Step 5: 问答 ==========
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0,
    api_key="sk-你的key",
    base_url="https://api.deepseek.com/v1"
)

retriever = db.as_retriever()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)

result = qa.invoke({"question": "藜怎么防治虫害？"})
print("问题:", result.get("question"))
print("回答:", result.get("answer"))
```

---

## 补充知识

### 1. LLMChain — 手动控制的问答

比 `ConversationalRetrievalChain` 更灵活，但需自己处理检索结果：

```python
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="根据以下上下文回答问题。\n上下文：{context}\n问题：{question}\n回答："
)

llm = ChatOpenAI(model="deepseek-chat", api_key="xxx", base_url="https://api.deepseek.com/v1")
chain = LLMChain(llm=llm, prompt=prompt)

context = "藜麦是一种营养丰富的作物..."
result = chain.invoke({"context": context, "question": "藜麦什么时候播种？"})
print(result["text"])
```

### 2. PromptTemplate — 提示词模板

```python
from langchain_core.prompts import PromptTemplate

# 简单模板
prompt = PromptTemplate.from_template("用一句话解释：{topic}")

# 带角色的模板
prompt = PromptTemplate(
    input_variables=["question"],
    template="你是农业专家，简洁回答：{question}"
)
print(prompt.format(question="藜麦怎么种？"))
```

### 3. ChatPromptTemplate — 对话式模板

```python
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是一个专业的农业专家。"),
    HumanMessagePromptTemplate.from_template("请问：{question}")
])

messages = chat_prompt.format_messages(question="藜麦什么时候播种？")
```

### 4. 完全本地运行（无需 API）

```python
# Ollama 本地大模型
from langchain_community.llms import Ollama
llm = Ollama(model="llama3")

# HuggingFace 本地模型
from langchain_community.llms import HuggingFaceHub
llm = HuggingFaceHub(repo_id="google/flan-t5-large", task="text-generation")
```

---

## 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `UnicodeDecodeError` | Windows 默认 GBK 编码 | `TextLoader(..., encoding='utf-8')` |
| `Error loading ../file` | 运行目录不是脚本所在目录 | 用 `os.path.join(os.path.dirname(__file__), ...)` |
| `Extra inputs are not permitted` | `ConversationalRetrievalChain` 直接传参 | 改用 `.from_llm(...)` |
| `query_instruction` 报错 | 用了 `HuggingFaceEmbeddings` 而非 Bge 版 | 换成 `HuggingFaceBgeEmbeddings` |
| huggingface 连接超时 | 国内网络限制 | `os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"` |
| 检索结果不相关 | chunk_size 不合理 | 调小 chunk_size，或换更好的 embedding 模型 |
| API 调用失败 | Key 或 base_url 不对 | 检查平台后台确认配置 |
| GPU 内存不足 | 模型太大 | 换 `bge-small` 而非 `bge-large` |

---

## v1.0 迁移备忘

当前代码基于 LangChain 0.3.x，可正常运行。如果需要升级到 **LangChain v1.0** 风格，以下是要改的地方（改不改都行，看你自己）：

| 组件 | 当前写法 | v1.0 写法 |
|------|----------|-----------|
| Embedding | `from langchain_community.embeddings import HuggingFaceBgeEmbeddings` | `from langchain_huggingface import HuggingFaceEmbeddings` |
| 对话链 | `ConversationalRetrievalChain.from_llm(...)` | `create_history_aware_retriever` + `create_retrieval_chain` |
| 记忆 | `ConversationBufferMemory(...)` | `BaseChatMessageHistory` 或直接在链中管理 `chat_history` |

详细示例见 Step 5 中的 `<!-- v1.0 升级提示 -->` 注释块。**当前代码完全可用，升级是可选动作。**
