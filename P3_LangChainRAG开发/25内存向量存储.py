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
    source_column="source",  # 指定哪一列作为文档内容
)

documents = loader.load()
print(documents[0])
