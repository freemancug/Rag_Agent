from pathlib import Path
from langchain_community.document_loaders import CSVLoader


print("文件是否存在：", Path("./data/stu.csv").exists())


loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
    csv_args={"delimiter":","}
)

# 批量加载.load() -> list[Document]  [Document, Document, ...]
documents = loader.load()

print(documents)