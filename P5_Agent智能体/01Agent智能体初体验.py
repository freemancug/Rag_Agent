from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool(description="获取天气信息")
def get_weather()->str:
    """
    获取天气信息
    """
    return "明天深圳的天气晴，最高气温30度，最低气温25度。"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),  # 智能体的大脑LLM
    tools=[get_weather],  # 智能体的工具箱
    system_prompt="你是一个聊天助手，可以回答用户问题。",  # 智能体的系统消息
)

res =agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "明天深圳的天气如何？"},
        ]
    }
)  # 调用智能体进行对话

for msg in res["messages"]:
    print(f"{msg.type}: {msg.content}")  # 用属性访问，不是下标
