from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatTongyi(model="qwen3-max", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY") )
prompt = PromptTemplate.from_template("" \
"我邻居姓：{lastname},刚生了{gender},请起名，仅告知我名字无需其它内容。"
)
# StrOutputParser可以将AiMessage对象解析为str类型,可以加入chain作为组件存在（Runnable接口的子类）
parser = StrOutputParser()
# PromptValue, str, or list of BaseMessages
chain = prompt | model | parser | model | parser

res:str=chain.invoke(input={"lastname": "张", "gender": "男"})
print(res)
print(type(res))  # <class 'str'>