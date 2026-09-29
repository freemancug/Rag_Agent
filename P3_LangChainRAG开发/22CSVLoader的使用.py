from pathlib import Path
from langchain_community.document_loaders import CSVLoader


print("文件是否存在：", Path("./data/stu.csv").exists())


loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
    csv_args={
        "delimiter":",",
        "quotechar": '"',
        # 如果数据原本有表头，就不要下面的代码，如果没有可以使用
        # "fieldnames": ["name", "age", "gender", "hobby"]
    }
)

# 批量加载.load() -> list[Document]  [Document, Document, ...]
# documents = loader.load()

# for document in documents:
#     print("文档类型：", type(document))
#     print("文档内容：", document.page_content)
#     print("文档元数据：", document.metadata)

for document in loader.lazy_load():
    print("文档类型：", type(document))
    print("文档内容：", document.page_content)
    print("文档元数据：", document.metadata)


# print(documents)