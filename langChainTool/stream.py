# from langchain_core import
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")


async def async_output():
    print("开始异步调用")
    async for chunk in model.astream("讲一个100个汉字字的冷笑话"):
        print(chunk.content, end="|")

import asyncio
asyncio.run(async_output())