from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from dotenv import load_dotenv
import os,json
from typing import Sequence

# message_to_dict:单个消息对象(BaseMessage类实例)->字典对象
# message_from_dict:字典对象转为单个消息对象(BaseMessage类实例)，[字典,字典,...]->[消息，消息,...]
# AImessage、HumanMessage、SystemMessage等类都是BaseMessage的子类
load_dotenv()

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

    

    

# 创建模型实例
model = ChatTongyi(model="qwen3-max", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY") )

# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回应用户问题。对话历史：{chat_history},用户问题：{input}，请回答。"
# )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回应用户问题,对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)

def print_prompt(full_prompt):
    print("=" * 20, full_prompt.to_string(), "=" * 20)
    return full_prompt

str_parser = StrOutputParser()

base_chain = prompt | print_prompt | model | str_parser

store = {}      # key就是session，value就是InMemoryChatMessageHistory对象

# 实现通过会话id获取对应的InMemoryChatMessageHistory类对象
def get_history(session_id):
    return FileChatMessageHistory(session_id, storage_path="./chat_history")  # 每个会话id对应一个文件，存储在./chat_history文件夹下

# 创建一个新的链，对原有链增强功能：自动获取会话历史，并将其传入到原有链中，附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,    #被增强的原有chain
    get_history, #通过会话id获取对应的InMemoryChatMessageHistory类对象
    input_messages_key="input",  # 表示用户输入在模版中的占位符
    history_messages_key="chat_history" # 表示用户历史消息在模版中的占位符
)

if __name__ == "__main__":
    #固定资格，添加LangChina的配置，为当前程序配置所属的session_id，方便在同一个会话中进行多轮对话
    session_config = {
        "configurable":{
            "session_id": "user_001"}
    }
    # res =conversation_chain.invoke({"input": "小明有2个猫"}, session_config)
    # print("第一次执行，",res)
    # res =conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    # print("第二次执行，",res)
    res =conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第三次执行，",res)
