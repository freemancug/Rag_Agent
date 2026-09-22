from langchain_community.llms.tongyi import Tongyi
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("DASHSCOPE_API_KEY")
# Tongyi.api_key = "YOUR_API_KEY"
model = Tongyi(model="qwen-max")

res=model.stream(input="你好，帮我写一首诗。")
for chunk in res:
    print(chunk, end="",flush=True)
    

# from langchain_ollama import OllamaLLM
# from dotenv import load_dotenv


# model = OllamaLLM(model="qwen3:4b")

# res=model.stream(input="你好，帮我写一首诗。")
# for chunk in res:
#     print(chunk, end="",flush=True)



# from langchain_openai import ChatOpenAI
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

# res = model.stream(input="你好，帮我写一首情诗。100字以内。")
# for chunk in res:
#     print(chunk.content, end="",flush=True)
