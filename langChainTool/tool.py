# from langchain_core.tools import tool
#
# @tool
# def multiply(a:int,b :int)->int:
#     """ 两个整数相乘
#
#     Args:
#         a: 第一个整数
#         b: 第二个整数
#     """
#     return a * b
#
# @tool
# def add(a:int,b :int)->int:
#     """ 两个整数相加
#
#     Args:
#         a: 第一个整数
#         b: 第二个整数
#     """
#     return a + b
#
# # 已经可以对工具进行调用了
#
# print(multiply.invoke({"a": 2, "b": 3})) # 输出:6
# print(multiply.name)
# print(multiply.description)
# print(multiply.args)

#------------------
# from pydantic import BaseModel,Field
#
# class AddInput(BaseModel):
#     """两个整数相加求和"""
#     a: int = Field(..., description="First Integer")
#     b: int = Field(..., description="Second Integer")
#
# class MulInput(BaseModel):
#     """两数相乘求积"""
#     a: int = Field(..., description="First Integer")
#     b: int = Field(..., description="Second Integer")
#
# from langchain.tools import tool
#
# @tool(args_schema=AddInput)
# def add(a:int, b:int)->int:
#     return a+b
#
# @tool(args_schema=MulInput)
# def mul(a:int, b:int)->int:
#     return a*b
#-----------------

# from typing_extensions import Annotated
# from langchain.tools import tool
#
# @tool
# def add(
#     a:Annotated[int, ..., "First integer"],
#     b: Annotated[int, ..., "Second integer"]
# ):
#     """两数相加"""
#     return a+b

#-----------------
# from langchain_core.tools.structured import StructuredTool
#
# def multiply(a:int,b :int)->int:
#     """ 两个整数相乘
#
#     Args:
#         a: 第一个整数
#         b: 第二个整数
#     """
#     return a * b
#
# mul_tool = StructuredTool.from_function(func=multiply)
#
# print(mul_tool.invoke({"a": 2, "b": 3})) # 输出:6
# print(mul_tool.name)
# print(mul_tool.description)
# print(mul_tool.args)

# ---------

from pydantic import BaseModel,Field
from typing import Tuple,List

class MulInput(BaseModel):
    """两数相乘求积"""
    a: int = Field(..., description="First Integer")
    b: int = Field(..., description="Second Integer")

def mul(a:int, b:int)->Tuple[int,List[int]]:
    nums = [a,b]
    content = f"{nums}相乘的结果为{a*b}"
    return content,nums
from langchain_core.tools import StructuredTool

mul_tool = StructuredTool.from_function(
    func=mul,
    name="Calculator",
    description="两数相乘求积",
    args_schema=MulInput,
    response_format="content_and_artifact"
)

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,ToolMessage
from langchain_tavily import TavilySearch



model = ChatOpenAI(model="deepseek-chat",openai_api_base="https://api.deepseek.com/v1")
model_with_tool =model.bind_tools([mul_tool])

messages = [
    HumanMessage("3乘5等于多少")
]
ai_msg = model_with_tool.invoke(messages)

messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    selected_tool = {
        "Calculator":mul_tool
    }
    tool_msg = selected_tool[tool_call["name"]].invoke(tool_call)
    messages.append(tool_msg)

print(messages)
result = model_with_tool.invoke(messages)
print(result)
print(result.content)

