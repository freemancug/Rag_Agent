from langchain.agents import create_agent,AgentState
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langgraph.runtime import Runtime
from dotenv import load_dotenv

load_dotenv()
@tool(description="获取体重，返回值是整数，单位千克")
def get_weight() -> int:
    """
    获取体重信息
    """
    return 90  # 假设体重是90千克

@tool(description="获取身高，返回值是整数，单位厘米")
def get_height() -> int:
    """
    获取身高信息
    """
    return 172


agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),  # 智能体的大脑LLM
    tools=[get_weight, get_height],  # 智能体的工具箱
    system_prompt="""你是严格遵循ReAct框架的智能体，必须按「思考→行动→观察→再思考」的流程解决问题，
    且**每轮仅能思考并调用1个工具**，禁止单次调用多个工具。
    并告知我你的思考过程，工具的调用原因，按思考、行动、观察三个结构告知我""", # 智能体的系统消息
)

for chunk in agent.stream(
    {
        "messages": [
            {"role": "user", "content": "计算我的BMI"},
        ]
    },
    stream_mode="values"
):  
    latest_message =chunk["messages"][-1]

    if latest_message.content:
            print(f"{latest_message.type}: {latest_message.content}")  # 用属性访问，不是下标
    if isinstance(latest_message, AIMessage) and latest_message.tool_calls:
        print(f"工具调用： { [tc['name'] for tc in latest_message.tool_calls] }")  # 用属性访问，不是下标
    