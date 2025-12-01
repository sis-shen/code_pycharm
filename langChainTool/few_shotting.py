# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import FewShotChatMessagePromptTemplate,ChatPromptTemplate
# model = ChatOpenAI(model="gpt-4o-mini")
#
# # 1.准备数据集
# examples = [
#     {"input":"2 🤓 3","output":"222"},
#     {"input": "3 🤓 2", "output": "33"},
# ]
#
# # 准备提示词模板
# prompt_template = ChatPromptTemplate(
#     [
#         ("human", "{input}"),
#         ("ai", "{output}")
#     ]
# )
#
# few_shot_prompt = FewShotChatMessagePromptTemplate(
#     example_prompt=prompt_template,
#     examples=examples
# )
#
# final_template = ChatPromptTemplate(
#     [
#         ("system","你是一名中国的小学数学老师，擅于定义新运算题目，并且每句话前面都会加个小朋友这样的亲切称呼"),
#         few_shot_prompt,
#         ("human","{input}")
#     ]
# )
#
# chain = final_template | model
# print(chain.invoke({"input":"9 🤓 2 是多少?"}).content)

# # ---------------长度选择器
# from langchain_core.example_selectors.length_based import LengthBasedExampleSelector
# from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
# from langchain_openai import ChatOpenAI
#
# examples = [
#     {"input": "happy", "output": "unhappy"},
#     {"input": "big", "output": "small"},
#     {"input": "fast", "output": "slow"},
#     {"input": "light", "output": "dark"},
#     {"input": "strong", "output": "weak"},
#     {"input": "safe", "output": "dangerous"},
# ]
#
# example_prompt = PromptTemplate(
#     input_variables=["input","output"],
#     template="Input:{input} ---> Output:{output}",
# )
#
# # 长度示例选择器
# length_selector = LengthBasedExampleSelector(
#     examples=examples,
#     example_prompt=example_prompt,
#     max_length=25,
# )
#
# # 用于实例化少样本提示的模板
# few_shot_template = FewShotPromptTemplate(
#     example_selector=length_selector,
#     example_prompt=example_prompt,
#     prefix="给出每个输入反义词",
#     suffix="Input:{adjective} ---> Output:",
#     input_variables=["adjective"]
# )
#
# long_usr_input = {"adjective":"非常 非常 非常 非常 非常 非常 非常 非常 非常 非常 非常 非常 非常 非常 长的输入"}
# print(few_shot_template.invoke(long_usr_input).to_messages()[0].content)


# # ---------------语义选择器
# from langchain_core.example_selectors.semantic_similarity import SemanticSimilarityExampleSelector
# from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
#
# examples = [
#     {"input": "happy", "output": "sad"},
#     {"input": "big", "output": "small"},
#     {"input": "fast", "output": "slow"},
#     {"input": "light", "output": "dark"},
#     {"input": "strong", "output": "weak"},
#     {"input": "safe", "output": "dangerous"},
# ]
#
# example_prompt = PromptTemplate(
#     input_variables=["input","output"],
#     template="Input:{input} ---> Output:{output}",
# )
#
# # 语义相似度示例选择器
# similarity_selector = SemanticSimilarityExampleSelector.from_examples(
#     examples=examples,
#     embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
#     vectorstore_cls=Chroma,
#     k=2,
# )
#
# # 用于实例化少样本提示的模板
# few_shot_template = FewShotPromptTemplate(
#     example_selector=similarity_selector,
#     example_prompt=example_prompt,
#     prefix="给出每个输入反义词",
#     suffix="Input:{adjective} ---> Output:",
#     input_variables=["adjective"]
# )
#
# usr_input = {"adjective":"worried"}
# print(few_shot_template.invoke(usr_input).to_messages()[0].content)


# # ---------------MMR选择器
# from langchain_core.example_selectors.semantic_similarity import MaxMarginalRelevanceExampleSelector
# from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
#
# examples = [
#     {"input": "happy", "output": "sad"},
#     {"input": "big", "output": "small"},
#     {"input": "fast", "output": "slow"},
#     {"input": "light", "output": "dark"},
#     {"input": "strong", "output": "weak"},
#     {"input": "safe", "output": "dangerous"},
# ]
#
# example_prompt = PromptTemplate(
#     input_variables=["input","output"],
#     template="Input:{input} ---> Output:{output}",
# )
#
# # 语义相似度示例选择器
# mmr_selector = MaxMarginalRelevanceExampleSelector.from_examples(
#     examples=examples,
#     embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
#     vectorstore_cls=Chroma,
#     k=2,
# )
#
# # 用于实例化少样本提示的模板
# few_shot_template = FewShotPromptTemplate(
#     example_selector=mmr_selector,
#     example_prompt=example_prompt,
#     prefix="给出每个输入反义词",
#     suffix="Input:{adjective} ---> Output:",
#     input_variables=["adjective"]
# )
#
# usr_input = {"adjective":"worried"}
# print(few_shot_template.invoke(usr_input).to_messages()[0].content)

# ---------------NGRAM选择器
from langchain_community.example_selectors.ngram_overlap import NGramOverlapExampleSelector
from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate

examples = [
    {"input": "I see Supdriver flying", "output": "我看到了Supdriver在飞"},
    {"input": "My dog barks", "output": "我的狗叫"},
    {"input": "Supdriver can fly", "output": "Supdriver会飞"},
]

example_prompt = PromptTemplate(
    input_variables=["input","output"],
    template="Input:{input} ---> Output:{output}",
)

# 语义相似度示例选择器
mmr_selector = NGramOverlapExampleSelector(
    examples=examples,
    example_prompt=example_prompt,
    threhold=-1
)

# 用于实例化少样本提示的模板
few_shot_template = FewShotPromptTemplate(
    example_selector=mmr_selector,
    example_prompt=example_prompt,
    prefix="给出每个输入的中文翻译",
    suffix="Input:{raw_text} ---> Output:",
    input_variables=["raw_text"]
)

usr_input = {"raw_text":"Supdriver can fly high"}
print(few_shot_template.invoke(usr_input).to_messages()[0].content)