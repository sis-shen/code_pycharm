# from langchain_core.prompts import PromptTemplate
#
# prompt_template = PromptTemplate.from_template("Say twice the following sentence. {text_sentence}")
#
# print(prompt_template.invoke({"text_sentence": "man!"}))
#
# print(prompt_template.invoke({"text_sentence": "HAHA!"}))

# from langchain_core.prompts import ChatPromptTemplate
#
# # 1. 创建模板，这里是消息列表，有一个系统消息和一个用户消息
# prompt_template = ChatPromptTemplate(
#     [
#         ("system", "Say {repeat_time} times everything that follows after"),
#         ("user", "{user_input}")
#     ]
# )
#
# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
#
# # 2.组成链式调用
# parser = StrOutputParser()
# model = ChatOpenAI(model="gpt-4o-mini")
# chain = prompt_template | model | parser
# print(chain.invoke(
#     {
#         "repeat_time": "3",
#         "user_input": "HAHA!"
#     }
# ))


from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from  langchain_core.messages import HumanMessage,AIMessage

# 1. 创建模板，这里是消息列表，有一个系统消息和一个用户消息
prompt_template = ChatPromptTemplate(
    [
        ("system", "回答世界地理问题"),
        # MessagesPlaceholder("msgs")
        ("placeholder", "{msgs}") # 两种表述是等价的
    ]

)

param_msgs = [
    HumanMessage("亚洲第一大国是谁？"),
    AIMessage("是印度，因为它人杰地灵，人口最多"),
    HumanMessage("那俄罗斯为什么不是亚洲第一大国？")
]

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# 2.组成链式调用
parser = StrOutputParser()
model = ChatOpenAI(model="gpt-4o-mini")
chain = prompt_template | model | parser
print(chain.invoke(
    {
        "msgs": param_msgs,
    }
))