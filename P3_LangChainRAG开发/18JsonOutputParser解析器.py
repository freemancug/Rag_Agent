from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
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
    "我邻居姓：{lastname},刚生了{gender},请帮忙起名子，并以json格式返回"
    "要求key是name，value就是起的名字。请严格遵守格式要求"
)

# 第二个提示词模版
second_prompt = PromptTemplate.from_template(
    "姓名：{name},请帮我解析含义。"
)

chain = fisrt_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream(input={"lastname": "张", "gender": "男"}):
    print(chunk, end="",flush=True)  # 流式输出


