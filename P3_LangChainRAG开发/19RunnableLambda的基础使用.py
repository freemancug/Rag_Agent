from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
import os

load_dotenv()
# 创建所需的解析器
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

# 创建模型实例
model = ChatTongyi(model="qwen3-max", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY") )

# 第一个提示词模版
fisrt_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname},刚生了{gender},请帮忙起名子，仅生成一个名字，并告知我名字，不要额外信息。"
)

# 第二个提示词模版
second_prompt = PromptTemplate.from_template(
    "姓名：{name},请帮我解析含义。"
)

# my_func = RunnableLambda(lambda ai_message: {"name": ai_message.content})

# chain = fisrt_prompt | model | my_func | second_prompt | model | str_parser

chain = fisrt_prompt | model | (lambda ai_message: {"name": ai_message.content}) | second_prompt | model | str_parser

for chunk in chain.stream(input={"lastname": "张", "gender": "女"}):
    print(chunk, end="",flush=True)  # 流式输出


