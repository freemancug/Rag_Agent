from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("DASHSCOPE_API_KEY")
# Tongyi.api_key = "YOUR_API_KEY"
model = ChatTongyi(model="qwen3-max")

#准备消息列表
messages=[
    SystemMessage(content="你是一个边塞诗人"),
    HumanMessage(content="帮我写一首唐诗。")  ,
    AIMessage(content="锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。") ,   
    HumanMessage(content="按照你上一个回复的格式，在写一首唐诗。")        
]

res=model.stream(input=messages)
for chunk in res:
    print(chunk.content, end="",flush=True)
    




# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage  
# from dotenv import load_dotenv
# import os

# load_dotenv()

# model = ChatOpenAI(
#     model="deepseek-v4.1-flash",
#     api_key=os.getenv("DASHSCOPE_API_KEY"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#     temperature=0.7,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2
# )

# #准备消息列表
# messages=[
#     SystemMessage(content="你是一个边塞诗人，100字以内。"),
#     HumanMessage(content="你好，帮我写一首情诗。100字以内。")              
# ]
# res = model.stream(input=messages)
# for chunk in res:
#     print(chunk.content, end="",flush=True)
