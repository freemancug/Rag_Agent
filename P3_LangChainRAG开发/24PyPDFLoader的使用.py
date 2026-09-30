from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    "./data/pdf2.pdf",
    mode = "single",  #默认是"page"，按页加载，每个页面形成一个Document文档对象，"single"按整个pdf加载，形成一个Document文档对象
    password = "itheima"  # pdf文件的密码，如果有的话
    )
i=0
for document in loader.lazy_load():
    i+=1
    print("文档内容：", document)
    print("="*20,i)