from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

word=on_keyword({"这里是哪里？"})

@word.handle()
async def _():
    await word.send(message=MessageSegment.image("file:///C:/Users/Administrator/Desktop/test.png"))