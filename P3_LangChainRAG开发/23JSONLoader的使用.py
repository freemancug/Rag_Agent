from langchain_community.document_loaders import json_loader

loader = json_loader.JSONLoader(
    file_path="./data/stu_json_lines.json",
    jq_schema=".name",  # jq表达式，提取json数据中的name字段,
    text_content = False,  # 不将json数据转为文本内容
    json_lines = True  # json文件是否为json lines格式

)

documents = loader.load()
print("documents:", documents)
