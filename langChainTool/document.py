# from langchain_community.document_loaders.pdf import PyPDFLoader
#
# file_path = "./docs/面经.pdf"
# loader = PyPDFLoader(file_path)
#
# docs = loader.load()
#
# print("第一页的元数据")
# print(docs[0].metadata)
# print("第一页的内容")
# print(docs[0].page_content)

from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader

file_path = "./docs/面经.md"
loader = UnstructuredMarkdownLoader(file_path, mode="elements")

docs = loader.load()

print("查看页数")
print(len(docs))
print("第一页的元数据")
print(docs[0].metadata)