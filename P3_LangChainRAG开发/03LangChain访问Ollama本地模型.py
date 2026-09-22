from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()

model = OllamaLLM(model="qwen:4b")

res=model.invoke("你好，帮我写一首诗。")
print(res)