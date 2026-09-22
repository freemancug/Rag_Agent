# from langchain_core.prompts import PromptTemplate
# from langchain_community.llms.tongyi import Tongyi
# from dotenv import load_dotenv
# import os

# load_dotenv()

# prompt_template=PromptTemplate.from_template(
#     "我的邻居姓{last_name}，刚生了{gender},你帮我起个名字，简单回答。"
# )
# #调用.format()方法注入信息即可
# prompt_text=prompt_template.format(last_name="张",gender="女儿")

# model=Tongyi(model="qwen-max")
# res=model.invoke(input=prompt_text)
# print(res)



from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{last_name}，刚生了{gender}，你帮我起个名字，简单回答。"
)

# prompt_text = prompt_template.format(
#     last_name="张",
#     gender="女儿"
# )

# DeepSeek 大语言模型
model = ChatOpenAI(
    model="deepseek-v4-pro",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

chain=prompt_template | model
# 调用大语言模型
res = chain.invoke(input={
    "last_name": "张",
    "gender": "女儿"
})

print(res.content)
