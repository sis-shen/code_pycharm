from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

# 定义大模型
model = ChatOpenAI(model="gpt-4o-mini")

# 结构输出对象
class SearchResult(BaseModel):
    """结构化搜索结果。"""
    query: str = Field(description="搜索查询")
    findings: str = Field(description="调查结果摘要")

@tool
def web_search(query: str) -> str:
    """
    在网上搜索信息。
    Args:
        query: 搜索查询
    """
    return "西安今天天多云转小雨，气温18-23度，东南风2级，空气质量良好。"

# 手动将工具结果加入消息列表
model_with_search = model.bind_tools([web_search])
messages = [
    HumanMessage("搜索当前最新的西安的天气")
]

ai_msg = model_with_search.invoke(messages)
messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    tool_msg = web_search.invoke(tool_call)
    messages.append(tool_msg)

structured_search_model = model_with_search.with_structured_output(SearchResult)
result = structured_search_model.invoke(messages)
print(result)
