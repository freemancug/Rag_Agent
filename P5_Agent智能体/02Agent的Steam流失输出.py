from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
@tool(description="获取股票价格，传入股票名称，返回字符串信息")
def get_price(name:str) -> str:
    """
    获取价格信息
    """
    return f"股票{name}的价格是2元。"

@tool(description="获取股票信息，传入股票名称，返回字符串信息")
def get_info(name:str) -> str:
    """
    获取股票信息
    """
    return f"股票{name}，是一家A股上市公司，专注于IT职业教育。"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),  # 智能体的大脑LLM
    tools=[get_price, get_info],  # 智能体的工具箱
    system_prompt="你是一个智能助手，可以回答股票相关问题，记住请告知我思考过程，让我知道你为什么调用某个工具。",  # 智能体的系统消息
)

for chunk in agent.stream(
    {
        "messages": [
            {"role": "user", "content": "传智教育股价多少，并介绍一下"},
        ]
    },
    stream_mode="values"
):  
    print(chunk)  # 输出智能体的回答