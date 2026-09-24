from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableSerializable
from dotenv import load_dotenv
import os

load_dotenv()
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人,可以作诗"), 
        MessagesPlaceholder(variable_name="history"),
        ("human", "你好，帮我写一首唐诗"),  
    ]  
)


history_date=[

    ("human", "你来写一首唐诗"),
    ("ai", "床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "好诗再来一个"),
    ("ai", "锄禾日当午，汗滴禾下土。谁知盘中餐，粒粒皆辛苦。")
]


model=ChatTongyi(model="qwen3-max", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY") )

# 组成链,要求每一个组件都是Runnable接口的子类
chain: RunnableSerializable = chat_prompt_template | model

# 通过链去调用invoke或stream
# res = chain.invoke(input={"history": history_date})
# print(res.content)

# 通过stream流式输出
for chunk in chain.stream(input={"history": history_date}):
    print(chunk.content, end="",flush=True)  # 流式输出
