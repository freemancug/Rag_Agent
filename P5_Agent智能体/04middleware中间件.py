from langchain.agents import create_agent,AgentState
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain_core.messages import AIMessage
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model,wrap_model_call,wrap_tool_call
from langgraph.runtime import Runtime
from dotenv import load_dotenv

load_dotenv()
@tool(description="查询天气,传入城市名称字符串，返回字符串天气信息")
def get_weather(city: str) -> str:
    """
    获取天气信息
    """
    return f"城市{city}今天天气晴朗，温度25度。"

""""
1.agent执行前
2.agent执行后
3.model执行前
4.model执行后
5.工具执行中
6.模型执行中
"""

@before_agent
def log_before_agent(state: AgentState,runtime:Runtime) -> None:
    # agent执行前会调用这个函数并传入state和runtime对象
    print(f'[before_agent]agent启动，并附带{len(state["messages"])}条消息')

@after_agent
def log_after_agent(state: AgentState,runtime:Runtime) -> None:
    print(f'[after_agent]agent结束，并附带{len(state["messages"])}条消息')

@before_model
def log_before_model(state: AgentState,runtime:Runtime) -> None:
    print(f'[before_model]模型即将调用，并附带{len(state["messages"])}条消息')

@after_model
def log_after_model(state: AgentState,runtime:Runtime) -> None:
    print(f'[after_model]模型模型结束，并附带{len(state["messages"])}条消息')

@wrap_model_call
def model_call_hook(request ,handler):
    print("模型调用啦")
    return handler(request)

@wrap_tool_call
def monitor_tool(request,handler):
    print(f"工具执行：{request.tool_call['name']}")
    print(f"工具执行传入参数：{request.tool_call['args']}")
    return handler(request)




agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),  # 智能体的大脑LLM
    tools=[get_weather],  # 智能体的工具箱  
    middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model, model_call_hook, monitor_tool],  # 中间件列表
)

res = agent.invoke({"messages": [{"role": "user", "content": "请告诉我深圳的天气,如何穿衣"}]})  # 调用智能体进行对话

print("************\n",res)  # 输出智能体的回答