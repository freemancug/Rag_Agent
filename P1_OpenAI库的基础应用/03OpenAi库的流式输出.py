import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("DASHSCOPE_API_KEY")
workspace_id = os.getenv("WORKSPACE_ID")
region = os.getenv("DASHSCOPE_REGION")

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=f"https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1",
)


completion = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[
        {
                    "role": "system",
                    "content": "你是一个python专家，并且说非常多"
        },
        {
            "role": "assistant",
            "content": "好的，我是编程专家，并且说非常多，你要问什么？"
        },
        {
            "role": "user",
            "content": "输出1-10的数字，使用python代码"
        }
    ],
    stream=True
)
for chunk in completion:
    if not chunk.choices:
        continue

    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
      # Optional: Add a small delay to simulate streaming effect 
