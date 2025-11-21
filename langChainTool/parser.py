from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import Iterator,List

model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

def split_into_list(input:Iterator[str])->Iterator[List[str]]:
    buffer = ""
    for chunk in input:
        buffer += chunk
        while "。" in buffer:
            stop_index = buffer.index("。")
            yield [buffer[:stop_index].strip()]
            buffer = buffer[stop_index + 1 :]

    yield [buffer.strip()]

chain = model | parser | split_into_list

for chunk in chain.stream("讲一个100汉字的冷笑话，每句话用中文句号分割"):
    print(chunk,end='|')