from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from dotenv import load_dotenv
import os

load_dotenv()

prompt = PromptTemplate.from_template("你是一个AI助手")
model = ChatTongyi(model="qwen3-max", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"))
chain = prompt | model
print(type(chain))  # <class 'langchain_core.runnables.chain.Chain'>

chain1 = prompt | model | prompt | model
print(type(chain1))  # <class 'langchain_core.runnables.chain.Chain