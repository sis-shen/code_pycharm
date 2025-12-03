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

# from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
# from langchain_text_splitters import CharacterTextSplitter
#
# file_path = "./docs/面经.md"
# loader = UnstructuredMarkdownLoader(file_path)
#
# docs = loader.load()
#
# text_spliter = CharacterTextSplitter(
#     separator="\n\n" ,       # 选择分隔符
#     chunk_size=100,
#     chunk_overlap=20,
#     length_function=len,
#     is_separator_regex=False
# )
#
# texts = text_spliter.split_documents(docs)
#
# for doc in docs[:10]:
#     print('*'*10)
#     print(doc)


from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore


file_path = "./docs/面经.md"
loader = UnstructuredMarkdownLoader(file_path)

docs = loader.load()

text_spliter = CharacterTextSplitter(
    separator="\n\n" ,       # 选择分隔符
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False
)

docs = text_spliter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
store = InMemoryVectorStore(embedding=embeddings)

ids = store.add_documents(documents=docs)

results = store.similarity_search(query="Linux的特性",k=2)

for doc in results:
    print("*"*40)
    print(doc.page_content)


# doc_vector = embeddings.embed_documents(str_arr)
#
# print(f"文档数量为：{len(docs)}，生成了{len(doc_vector)}个向量的列表")
# print(f"第一个文档向量维度：{len(doc_vector[0])}")
# print(f"第二个文档向量维度：{len(doc_vector[1])}")