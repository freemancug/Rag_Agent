from  langchain_core.prompts import PromptTemplate,FewShotPromptTemplate,ChatPromptTemplate


"""
PromptTemplate:PromptTemplate->StringPromptTemplate->BasePromptTemplate->RunnableSerializable->Runnable
FewShotPromptTemplate: FewShotPromptTemplate->StringPromptTemplate->BasePromptTemplate->RunnableSerializable->Runnable
ChatPromptTemplate:ChatPromptTemplate->BaseChatPromptTemplate->BasePromptTemplate->RunnableSerializable->Runnable
"""


template = PromptTemplate.from_template("我的邻居姓{last_name}，刚生了{gender}，你帮我起个名字，简单回答。")
res=template.format(last_name="张", gender="男孩")
print(res,type(res))


res2=template.invoke(input={"last_name":"张","gender":"男孩"})
print(res2,type(res2))