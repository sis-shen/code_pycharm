# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage,SystemMessage
# from langchain_core.output_parsers import StrOutputParser
# # 定义大模型
# model = ChatOpenAI(model="deepseek-chat",openai_api_base="https://api.deepseek.com/v1")
#
# # 定义消息列表
# messages = [
#     SystemMessage(content="translate the following from English into Chinese"),
#     HumanMessage(content="hi I'm Supdriver~")
# ]
#
# # 调用大模型,并使用链式执行 model->parser->output
# parser = StrOutputParser()
# chain = model | parser
# print(chain.invoke(messages))

# from langchain.chat_models.base import init_chat_model
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.messages import HumanMessage,SystemMessage
# model = init_chat_model(model="deepseek-chat",model_provider="deepseek")
#
# messages = [
#     SystemMessage("Response in Chinese"),
#     HumanMessage("What's your name,Response in Chinese")
# ]
#
# chain = model | StrOutputParser()
# print(chain.invoke(messages))

from langchain.chat_models.base import init_chat_model
from langchain_core.runnables.config import RunnableConfig

configurable_model = init_chat_model(
    model="gpt-5-mini",
    temperature=0,
    configurable_fields=("model", "model_provider", "temperature",
                         "max_tokens"),
    config_prefix="pre_first",
)
runnable_config = RunnableConfig({
    "configurable":{
        "pre_first_model":"deepseek-chat",
        "pre_first_model_provider":"deepseek",
        "pre_first_temperature":0.5
    }
})

print(configurable_model.invoke("what's your name,response in chinese",config=runnable_config).content)