# from langchain_core.prompts import PromptTemplate
#
# prompt_template = PromptTemplate.from_template("Say twice the following sentence. {text_sentence}")
#
# print(prompt_template.invoke({"text_sentence": "man!"}))
#
# print(prompt_template.invoke({"text_sentence": "HAHA!"}))

from langchain_core.prompts import ChatPromptTemplate

# 1. 创建模板，这里是消息列表，有一个系统消息和一个用户消息
prompt_template = ChatPromptTemplate(
    [
        ("system", "Say twice the following sentence. {text_sentence}"),
        ("user", "{user_input}")
    ]
)

# 实例化模板，但还不是消息列表类型
msg_val = prompt_template.invoke(
    {
        "text_sentence":"man!",
        "user_input":"HAHA!"
    }
)
# 3.转换成消息队列
messages = msg_val.to_messages()
print(messages)
from langchain_openai import ChatOpenAI
model = ChatOpenAI()
print()