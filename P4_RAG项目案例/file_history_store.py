
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
import os,json
from typing import Sequence

# message_to_dict:单个消息对象(BaseMessage类实例)->字典对象
# message_from_dict:字典对象转为单个消息对象(BaseMessage类实例)，[字典,字典,...]->[消息，消息,...]
# AImessage、HumanMessage、SystemMessage等类都是BaseMessage的子类

# 实现通过会话id获取对应的InMemoryChatMessageHistory类对象
def get_history(session_id):
    return FileChatMessageHistory(session_id, storage_path="./chat_history")  # 每个会话id对应一个文件，存储在./chat_history文件夹下

class FileChatMessageHistory(BaseChatMessageHistory):
    """将消息存储在文件中"""

    def __init__(self,session_id, storage_path):
        self.session_id = session_id  # 会话ID
        self.storage_path = storage_path #不同会话id的存储文件，所在的文件夹路径
        # 完整的文件路径，存储文件名为session_id.json
        self.file_path = os.path.join(self.storage_path, f"{self.session_id}.json")
        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)   

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequeence序列 类似list、tuple，都是有序的集合
        all_messages = list(self.messages)  # 获取当前已有的消息列表
        all_messages.extend(messages)  # 将新消息添加到列表中

        # 将数据同步写入本地文件中

        # 类对象写入文件 -> 一堆二进制

        # 问了方便，可以将BaseMessage类消息转为字典（借助json模块以json字符串写入文件）
        # 官方message_to_dict:单个消息对象（BaseMessage类实例）->字典对象
        # new_messages= []
        # for message in messages:
        #     new_messages.append(message_to_dict(message))

        new_messages = [message_to_dict(message) for message in all_messages]  # 列表推导式，等价于上面for循环
        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=4)  # 将字典列表写入文件，json.dump()将Python对象转为json字符串并写入文件
    @property   #@property装饰器将方法变为成员属性用，调用时无需加括号
    def messages(self)-> list[BaseMessage]:
        # 当前文件内：list[字典]
        # 如果文件存在，则从文件中加载消息，否则返回空列表
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)  # 读取文件内容并解析为Python对象（列表）
                # 将字典列表转为BaseMessage类实例列表
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []
    def clear(self)->None:
        # 清空消息列表
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)  # 将空列表写入文件，清空消息列表

    

    
