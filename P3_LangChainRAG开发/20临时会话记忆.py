from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

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
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

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
    res =conversation_chain.invoke({"input": "小明有2个猫"}, session_config)
    print("第一次执行，",res)
    res =conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    print("第二次执行，",res)
    res =conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第三次执行，",res)