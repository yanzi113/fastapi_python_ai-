from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from time import sleep
from sse_starlette.sse import EventSourceResponse
from langchain_openai import ChatOpenAI
app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}
class Item(BaseModel):
        name: str

@app.post("/testpost")
async def create_item(item: Item):
        msg = f'后端收到消息： {item.name}'
        print(msg)
        return {'param': msg}

#  SSE相关代码
class StreamData(BaseModel):
    data: str

    # glm4 Model
glm4_model = ChatOpenAI(
        model_name="gLm-4-air",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4",
        openai_api_key="839815e495bcc411b3005d0a8f8ff15f.sM3vvPVaJLv1y998",
        streaming=True,
        verbose=True,
    )
# @app.post("/stream")
# async def stream_run(
#         data: StreamData,
# ):
#     print('收到前端数据：{}' .format(data.data))
#     # 定义一个简单的生成器
#     def generator(StreamData):
#         yield 'data: start'
#         sleep(1)
#         yield 'data: 服务器收到前端{}'.format(data.data)
#         sleep(1)
#         yield 'data: end'
#
#     return EventSourceResponse(generator(data))

@app.post("/stream")
async def stream_run(
    data: StreamData
):
    print('收到前端数据： {}'.format(data.data))

    def glm4_talk(data:StreamData):
        for chunk in glm4_model.stream(data.data):
            print('-------------')
            print(chunk.content)
            yield chunk.content
    # 接收到输入的数据，开始事件流发送
    return EventSourceResponse(glm4_talk(data))

@app.get("/test")
def read_root():
    return {"param" : "你好！：这里是后端"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)

