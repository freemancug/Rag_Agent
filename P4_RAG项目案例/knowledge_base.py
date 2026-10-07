"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def check_md5(md5_str:str):
    """
    检查传入的md5字符串是否已经被处理过了
    retrn: True表示已经处理过了，False表示没有处理过
    """
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在，那肯定没有处理过md5，直接返回False
        open(config.md5_path, "w", encoding="utf-8").close()
        return False
    else:
        with open(config.md5_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == md5_str:
                    return True
            return False

def save_md5(md5_str:str):
    """
    将传入的md5字符串，记录到文件中保存
    """
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")

def get_string_md5(input_str:str):
    """
    获取传入字符串的md5值字符串
    """
    #将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=config.encoding)
    md5 = hashlib.md5()
    md5.update(str_bytes)
    return md5.hexdigest()


class KnowledgeBaseService:
    """
    知识库服务类
    """
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)  #确保向量存储目录存在
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model ="text-embedding-v4"),
            persist_directory=config.persist_directory  
        )   #向量存储的实例Chroma向量库对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,   #分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap, #连接文本段之间的字符重叠长度
            separators=config.separators, #分割自然段落段的分隔符列表
            length_function=len #使用Python自带的len函数统计文本长度
        )  #文本分割器对象
    def upload_by_str(self,data:str, file_name):
        """
        将传入的字符串，进行向量化，存入向量数据库中
        """
        # 先得到传入字符串的md5值
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"

        
        if len(data) > config.max_split_char_number:
            # 如果传入的字符串长度大于阈值，则进行文本分割
             # 对每个分割后的文本进行向量化并存入向量数据库
            knowledge_chunks:list[str] = self.splitter.split_text(data)                   
        else:
            # 如果传入的字符串长度不大于阈值，则直接进行向量化并存入向量数据库
            knowledge_chunks:list[str]=[data]
        metadata = {
                    "source": file_name,
                    "creat_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "operator": "小夏"
        }
        self.chroma.add_texts(
                knowledge_chunks,
                metadatas=[metadata for _ in knowledge_chunks]       
        )
        save_md5(md5_hex)
        return "[成功]内容已经存入知识库中"
if __name__ == "__main__":
    service = KnowledgeBaseService()
    r=service.upload_by_str("周杰轮222", "testfile")
    print(r)