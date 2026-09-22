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
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？你能干什么？"},
    ],
    stream=True
)
for chunk in completion:
    if not chunk.choices:
        continue

    content = chunk.choices[0].delta.content

    if content:
        print(content, end="", flush=True)
# print(completion.choices[0].message.content)