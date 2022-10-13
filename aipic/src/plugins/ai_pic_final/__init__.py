from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot import on_command
import sys
from datetime import datetime
import random

sys.path.append("D:/Program/AI_picture/stable-diffusion-webui") ###
from pic_gen import prompt_only_wrapper, prompt_only_wrapper_img_2_img
from nonebot.rule import to_me
import os
from os.path import dirname
import datetime
from nonebot.params import ArgPlainText
from nonebot.params import T_State
import aiohttp
import requests
from io import BytesIO
from PIL import Image

cddir = dirname(__file__) + "/cd"
cdtxt = cddir + "/" + "cd.txt"
heisi_cd = 10

add = on_command("aipic", priority=99, block=True)


# @add.handle()
# async def add_handle(event: GroupMessageEvent, args: Message = CommandArg()):
#     arg = args.extract_plain_text().split()
#     pass

async def get_img(img_url: str) -> bytes:
    '''
    将收到的图片下载下来，并转换成二进制格式
    Args:
        img_url (str): 图片url地址
    Returns:
        bytes: 二进制格式的图片
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as resp:
            result = await resp.content.read()
    if not result:
        return None
    return result


@add.got("nums", prompt="请选择功能\n输入 1 描述转图片\n 输入 2 图片转图片")
async def _(event: GroupMessageEvent, state: T_State, reply: str = ArgPlainText("nums")):
    uid = event.user_id
    state["id"] = uid
    state["mode"] = reply
    if int(reply) == 1:
        await add.send(
            message=MessageSegment.at(state["id"]) + "请输入逗号分隔的英文描述"
        )
    elif int(reply) == 2:
        await add.send(
            message=MessageSegment.at(state["id"]) + "请上传图片（注意是图片不是文件）"
        )
    else:
        await add.finish(
            message=MessageSegment.at(state["id"]) + "请正确选择！"
        )


@add.got("des_or_img")
async def _(event: GroupMessageEvent, state: T_State):
    if not os.path.exists(cddir):
        os.mkdir(cddir)
    if not os.path.exists(cdtxt):
        with open(cdtxt, "w") as cd:
            time_now = datetime.datetime.now()
            cd.write(str(time_now))
            cd.close()
            await add.finish(
                message="创建cd.txt，第一次"
            )
    else:
        cd_time = open(cdtxt, "r").read()
        cd_time = datetime.datetime.strptime(cd_time, "%Y-%m-%d %H:%M:%S.%f")
        now = datetime.datetime.now()
        if int(str((now - cd_time).seconds)) > int(heisi_cd):
            with open(cdtxt, "w") as cd:
                time_now = datetime.datetime.now()
                cd.write(str(time_now))
                cd.close()
            if int(state["mode"]) == 1:
                ###  执行语句
                arg = state["des_or_img"].extract_plain_text()
                uid = event.user_id
                curDTObj = datetime.datetime.now()
                timeStr = curDTObj.strftime("%Y%M%H%M%S")
                filename = timeStr + ".png"
                temp_path = "./temp_pic/"
                abspath = os.path.abspath(temp_path + filename)
                prompt_only_wrapper(str(arg), abspath)
                img_url = "file:///" + abspath
                await add.send(message=(MessageSegment.at(uid) + "关键词是" + str(arg)) + MessageSegment.image(img_url))
                ### 执行语句
            elif int(state["mode"]) == 2:
                for seg in state["des_or_img"]:
                    if seg.type == "image":
                        ###执行语句
                        url = seg.data["url"]
                        response = requests.get(url)
                        input_img = Image.open(BytesIO(response.content))
                        uid = event.user_id
                        curDTObj = datetime.datetime.now()
                        timeStr = curDTObj.strftime("%Y%M%H%M%S")
                        filename = timeStr + ".png"
                        temp_path = "./temp_pic/"
                        abspath = os.path.abspath(temp_path + filename)
                        prompt_only_wrapper_img_2_img(input_img, abspath)
                        img_url = "file:///" + abspath
                        await add.send(message=(MessageSegment.at(uid) + "生成的图片") + MessageSegment.image(img_url))
                        break
                else:
                    await add.finish(message=(MessageSegment.at(state["id"]) + "不是图捏"))
            else:
                uid = event.user_id
                await add.finish(message=(MessageSegment.at(uid) + "寄"))
        else:
            left = int(heisi_cd) - int(str((now - cd_time).seconds))
            uid = event.user_id
            await add.finish(
                message=MessageSegment.at(uid) + "你先别急，系统占用中，剩%d秒" % left
            )

# @add.handle()
# async def _(event:GroupMessageEvent, args: Message = CommandArg()):
#     arg = args.extract_plain_text()
#     curDTObj = datetime.now()
#     timeStr = curDTObj.strftime("%Y%M%H%M%S")
#     filename = timeStr + ".png"
#     temp_path = "D:/Program/qqbot/aipic/temp_pic/"
#     prompt_only_wrapper(str(arg),temp_path + filename)
#     img_url = "file:///" + temp_path + filename
#     await add.send(message=("关键词是" + str(arg)) + MessageSegment.image(img_url))
