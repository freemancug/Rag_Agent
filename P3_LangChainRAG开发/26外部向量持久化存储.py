from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader, JSONLoader, TextLoader,PyPDFLoader
from dotenv import load_dotenv
import os,json
load_dotenv()

# chromadb向量数据库(轻量级的向量数据库) 需要安装chromadb库
vector_store = Chroma(
    collection_name="test",   #当前向量存储起个名字，类似数据库的表名称
    embedding_function=DashScopeEmbeddings(),
    persist_directory=os.getenv("PERSIST_DIRECTORY")   #指定数据存放的文件夹路径
)

print("向量存储库路径:",os.getenv("PERSIST_DIRECTORY"))

loader=CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",  # 指定本条数据的来源是哪里
)

documents = loader.load()
for document in documents:
    print("document:", document)

# # 向量存储的 新增、删除、检索
# vector_store.add_documents(
#     documents=documents,
#     ids=["id"+str(i) for i in range(1, len(documents)+1)]
    
# )  # 被新增的文档，类型：list[Document]

# # 删除  传入[id,id,...]  
# vector_store.delete(
#     ids=["id1","id2"]
# )
#检索 返回类型list[Document]
results = vector_store.similarity_search(
    query="Pythoon是不是简单易学呀",  # 检索的内容
    k=3,  # 返回的文档数量
    filter={"source": "黑马程序员"}  # 过滤条件，指定source列为info.csv的文档
)
for result in results:
    print("result:", result)