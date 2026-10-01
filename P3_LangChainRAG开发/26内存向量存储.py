from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader, JSONLoader, TextLoader,PyPDFLoader
from dotenv import load_dotenv
import os,json
load_dotenv()

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)



loader=CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",  # 指定本条数据的来源是哪里
)

documents = loader.load()


# 向量存储的 新增、删除、检索
vector_store.add_documents(
    documents=documents,
    ids=["id"+str(i) for i in range(1, len(documents)+1)]
    
)  # 被新增的文档，类型：list[Document]

# 删除  传入[id,id,...]  
vector_store.delete(
    ids=["id1","id2"]
)
#检索 返回类型list[Document]
results = vector_store.similarity_search(
    query="Pythoon是不是简单易学呀",  # 检索的内容
    k=3,  # 返回的文档数量
)
for result in results:
    print("result:", result)