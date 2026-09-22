from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()

#创建模型对象  不穿model默认用的是 text-embedding-v1
embedding_model = DashScopeEmbeddings(
    model="text-embedding-v3"
)

#不用invoke stream
# embed_query、embed_documents
print(embedding_model.embed_query("我喜欢你"))
print(embedding_model.embed_documents(["我喜欢你","我稀饭你","“晚上吃啥”"]))
