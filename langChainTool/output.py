# from langchain_openai import ChatOpenAI
# from typing import Optional,Union
# from pydantic import BaseModel,Field
#
# class JokeSchema(BaseModel):
#     """给用户讲一个笑话"""
#
#     setup: str = Field(description="这个笑话的开头")
#     punchline:str = Field(description="这个笑话的妙语")
#     rating:Optional[int] = Field(description="这个笑话的打分，满分10分", default=None)
# class ConversationalSchema(BaseModel):
#     """以聊天对话的方式回应，用闲聊的语气"""
#
#     response: str = Field(description="对用户问候的回应")
#
# class FinalResponse(BaseModel):
#     final_output: Union[JokeSchema, ConversationalSchema]
#
# model = ChatOpenAI(model="gpt-4o-mini")
# structured_model = model.with_structured_output(FinalResponse)
#
# print(structured_model.invoke("给我讲一个关于牛顿与苹果的笑话"))
# print(structured_model.invoke("你好，你是谁"))

#--------------
# from langchain_openai import ChatOpenAI
# from typing import Optional
# from typing_extensions import TypedDict,Annotated
#
# class JokeSchema(TypedDict):
#     """给用户讲一个笑话"""
#     setup: Annotated[str,...,"这个笑话的开头"]
#     punchline: Annotated[str,...,"这个笑话的妙语"]
#     rating: Annotated[Optional[int],None, "从0到10给这个笑话的好笑程度打分"]
#
#
# model = ChatOpenAI(model="gpt-4o-mini")
# structured_model = model.with_structured_output(JokeSchema, include_raw=True)
#
# result = structured_model.invoke("给我讲一个关于牛顿与苹果的笑话")
# print(result)

#------------

# from langchain_openai import ChatOpenAI
#
# json_schema = {
#     "title": "joke",
#     "description": "给⽤⼾讲⼀个笑话。",
#     "type": "object",
#     "properties": {
#         "setup": {
#             "type": "string",
#             "description": "这个笑话的开头",
#         },
#         "punchline": {
#             "type": "string",
#             "description": "这个笑话的妙语",
#         },
#         "rating": {
#             "type": "integer",
#             "description": "从1到10分，给这个笑话评分",
#             "default": None,
#         },
#     },
#     "required": ["setup", "punchline"],
#  }
#
#
# model = ChatOpenAI(model="gpt-4o-mini")
# structured_model = model.with_structured_output(json_schema)
#
# result = structured_model.invoke("给我讲一个关于牛顿与苹果的笑话")
# print(result)


#-----------------
# from typing import Optional
# from pydantic import BaseModel, Field
# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
#
# model = ChatOpenAI(model="gpt-4o-mini")
# class Person(BaseModel):
#     """一个人的信息。"""
#     #注意：
#     #1。每个字段都是Optional“可选的”-允许 LLM 在不知道答案时输出 None。#2。每个字段都有一个description“描述”一LLM使用这个描述。
#     #有一个好的描述可以帮助提高提敢结果。
#     name: Optional[str] = Field(default=None, description="这个人的名字")
#     hair_color:Optional[str] = Field(default=None, description="如果知道这个人头发的颜色")
#     skin_color:Optional[str] = Field(default=None,description="如果知道这个人的肤色")
#     height_in_meters: Optional[str] = Field(default=None, description="以米为单位的高度")
#
# structured_model = model.with_structured_output(schema=Person)
# messages = [
#     SystemMessage(content="你是一个提取信息的专家，只从文本中提取相关信息。如果您不知道要提取的属性的值，属性值返回null"),
#     HumanMessage(content="史密斯身高6英尺，金发。")
# ]
# result = structured_model.invoke(messages)
# print(result)
#
# messages.append(result)
# result = structured_model.invoke("约翰身高1.8米，是一位长着白发的黑人老人")
# print(result)



#---------------------------

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from typing import Optional
from pydantic import BaseModel,Field
from langchain_core.prompts import PromptTemplate

class JokeSchema(BaseModel):
    """给用户讲一个笑话"""

    setup: str = Field(description="这个笑话的开头")
    punchline:str = Field(description="这个笑话的妙语")
    rating:Optional[int] = Field(description="这个笑话的打分，满分10分", default=None)

parser = PydanticOutputParser(pydantic_object=JokeSchema)

prompt = PromptTemplate(
    template="{query}\nAnswer in this following template\n{template}",
    input_variables=["query"],
    partial_variables={"template":parser.get_format_instructions()}
)

model = ChatOpenAI(model="gpt-4o-mini")

chain = prompt | model | parser
print(chain.invoke({"query":"给我讲一个关于牛顿与苹果的笑话"}))
