from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader=TextLoader("./data/Python基础语法.txt", encoding="utf-8")  
docs=loader.load() 

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,  # 每个文档块的最大长度    
    chunk_overlap=50,  # 文档块之间的重叠长度
    separators=["\n\n","\n","。","！","？",".","!","?"," ",""], # 分割符列表，按顺序尝试使用
    length_function=len  # 计算文档块长度的函数
)
splited_documents=text_splitter.split_documents(docs)  # 将文档拆分为多个文档块
print("文档块数量：", len(splited_documents))
for document in splited_documents:
    print("="*20)
    print(document)
    print("="*20)
