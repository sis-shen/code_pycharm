# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import HumanMessage,AIMessage
#
# model = ChatOpenAI(model="gpt-4o-mini")
#
# parser = StrOutputParser()
#
# chain = model | parser
#
# messages = [
#     HumanMessage("你好，我是supdriver，请记住我的名字")
# ]
# ai_msg = chain.invoke(messages)
# print(ai_msg)
# messages.append(AIMessage(ai_msg))
# messages.append(HumanMessage("你还记得我的名字吗"))
# ai_msg = chain.invoke(messages)
# print(ai_msg)


# from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import HumanMessage,AIMessage
# from langchain_core.chat_history import BaseChatMessageHistory,InMemoryChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
#
# storage = {}
# # session_id用于区分不同的对话
# def get_sesstion_history(session_id:str)->BaseChatMessageHistory:
#     if session_id not in storage:
#         storage[session_id] = InMemoryChatMessageHistory();
#     return storage[session_id]
#
# model = ChatOpenAI(model="gpt-4o-mini")
# parser = StrOutputParser()
#
# chain = model | parser
#
# # 包装model
# history_model = RunnableWithMessageHistory(chain,get_sesstion_history)
#
# config = {"configurable": {"session_id": "1"}}
#
# result = history_model.invoke(
#     [HumanMessage("你好我是supdriver，请记住我的名字")],
#     config=config
# )
# print(result)
# result = history_model.invoke(
#     [HumanMessage("还记得我的名字吗")],
#     config=config
# )
# print(result)

# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,trim_messages,filter_messages
# from langchain_core.output_parsers import StrOutputParser
#
# model = ChatOpenAI(model="gpt-4o-mini")
#
# parser = StrOutputParser()
#
# messages = [
#     SystemMessage("你的名字是曼巴，当我说man！时，你要回复我 man! ,当我说其它内容时，正常聊天"),
#     HumanMessage("你好，我的名字是supdriver,请记住我的名字"),
#     AIMessage("你好，supdriver！很高兴认识你。我会记住你的名字。有什么我可以帮助你的吗？"),
#     HumanMessage("man!"),
#     AIMessage("man!"),
#     HumanMessage("你觉得24这个数字怎么样，请简短的回答"),
#     AIMessage("24是一个很特别的数字，它在许多领域都有重要意义，比如时间、数学和文化。"),
#     HumanMessage("还记得我是谁吗？")
# ]
#
# trimmer = trim_messages(
#     max_tokens=5,
#     token_counter=len,
#     strategy="last",    # 策略：last为默认值，保留最新消息; first则是保留最早消息
#     include_system=True,    # 是否始终保留系统消息
#     allow_partial=False,    # 是否允许拆分消息
#     start_on="human",   # 指定修剪后第一条消息的类型
# )
#
# chain = trimmer | model
#
# print(trimmer.invoke(messages))

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,SystemMessage,merge_message_runs
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

messages = [
    SystemMessage("你的名字是曼巴，当我说man！时，你要回复我 man! "),
    SystemMessage("当我说其它内容时，正常聊天"),
    HumanMessage("你好"),
    HumanMessage("我的名字是supdriver"),
    HumanMessage("请记住我的名字"),
]

merged_msg = merge_message_runs(messages)

print(merged_msg)
