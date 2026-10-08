md5_path="D:\\github_test\\Rag_Agent\\P4_RAG项目案例\\md5.txt"
encoding="utf-8"
collection_name="rag"
persist_directory="D:\\github_test\\Rag_Agent\\P4_RAG项目案例\\chroma_db"
chunk_size=1000
chunk_overlap=100 
separators=["\n\n", "\n", ".", "!", "?", ".",",","！","？", " ", ""]
max_split_char_number =1000 #文本分割的阈值


#
similarity_threshold = 1 #检索返回匹配的文档数量

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"


# session id 配置
session_config = {
        "configurable": {
            "session_id": "uuser_001"
        }
    }