"""
提示词：用户的提问+向量库中检索到的参考资料
"""
from langchain_community.chat_models import ChatTongyi
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatTongyi(model="qwen3-max")

prompt = ChatPromptTemplate.from_messages(
    [
    ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户问题，参考资料：{context}"),
    ("user", "用户提问：{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 准备一下资料（向量哭的数据）
# add_texts 传入一个list[str]，将文本转为向量存储到向量库中
vector_store.add_texts(["减肥就是要少吃多练","在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来","跑步是很好的运动哦"])  # 这里可以传入一些参考资料，作为向量存储到向量库中

input_text = "怎么减肥？"

# 先从向量库中检索出与用户问题最相关的参考资料
results = vector_store.similarity_search(input_text, k=2)  # k表示返回
print("检索到的参考资料：", results)
reference_text = "["
for result in results:
    reference_text += result.page_content
reference_text += "]"

def print_prompt(full_prompt):
    print("=" * 20, full_prompt.to_string(), "=" * 20)
    return full_prompt

chain = prompt | print_prompt | model | StrOutputParser()
res=chain.invoke({"input": input_text, "context": reference_text})  # 将用户问题和检索到的参考资料传入到chain中
print("最终结果：", res)