from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot import on_command

from nonebot.rule import to_me
import os
from os.path import dirname
import datetime
from nonebot.params import ArgPlainText
from nonebot.params import T_State

cddir = dirname(__file__) + "/cd"
cdtxt = cddir + "/" + "cd.txt"
heisi_cd = 30

add = on_command("aipic___", priority=99, block=True, rule=to_me())


# @add.handle()
# async def add_handle(event: GroupMessageEvent, args: Message = CommandArg()):
#     arg = args.extract_plain_text().split()
#     pass

# @add.handle()
# async def lq_(event:GroupMessageEvent, args: Message = CommandArg()):
#     uid = event.user_id
#     await add.send(
#         message=MessageSegment.at(uid) + "请选择功能\n输入 1 描述转图片\n 输入 2 图片转图片(开发中)"
#     )

@add.got("nums", prompt="请选择功能\n输入 1 描述转图片\n 输入 2 图片转图片(开发中)")
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
            message=MessageSegment.at(state["id"]) + "请上传图片"
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
            await add.send(
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
                img_url = "file:///C:/Users/Administrator/Desktop/test.png"
                await add.send(message=(MessageSegment.at(uid) + "关键词是" + str(arg)) + MessageSegment.image(img_url))
                ###  执行语句
        else:
            left = int(heisi_cd) - int(str((now - cd_time).seconds))
            uid = event.user_id
            await add.finish(
                message=MessageSegment.at(uid) + "你先别急，系统占用中，剩%d秒" % left
            )

    # from nonebot import on_keyword
    # from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
    # from nonebot.adapters.onebot.v11.event import GroupMessageEvent
    # from nonebot.adapters.onebot.v11.message import Message
    # from nonebot.params import CommandArg
    # from nonebot import on_command
    #
    # from nonebot.rule import to_me
    # import os
    # from os.path import dirname
    # import datetime
    #
    # cddir = dirname(__file__) + "/cd"
    # cdtxt = cddir + "/" + "cd.txt"
    # heisi_cd = 30
    #
    # add = on_command("aipic___", priority=99, block=True, rule=to_me())
    #
    # # @add.handle()
    # # async def add_handle(event: GroupMessageEvent, args: Message = CommandArg()):
    # #     arg = args.extract_plain_text().split()
    # #     pass
    #
    # @add.handle()
    # async def lq_():
    #     await add.send(
    #         message="请选择功能\n1. 描述转图片\n 2.图片转图片(开发中)"
    #     )
    #
    # @add.handle()
    # async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    #     if not os.path.exists(cddir):
    #         os.mkdir(cddir)
    #     if not os.path.exists(cdtxt):
    #         with open(cdtxt, "w") as cd:
    #             time_now = datetime.datetime.now()
    #             cd.write(str(time_now))
    #             cd.close()
    #             await add.send(
    #                 message="创建cd.txt，第一次"
    #             )
    #     else:
    #         cd_time = open(cdtxt, "r").read()
    #         cd_time = datetime.datetime.strptime(cd_time, "%Y-%m-%d %H:%M:%S.%f")
    #         now = datetime.datetime.now()
    #         if int(str((now - cd_time).seconds)) > int(heisi_cd):
    #             with open(cdtxt, "w") as cd:
    #                 time_now = datetime.datetime.now()
    #                 cd.write(str(time_now))
    #                 cd.close()
    #             ###  执行语句
    #             arg = args.extract_plain_text()
    #             uid = event.user_id
    #             img_url = "file:///C:/Users/Administrator/Desktop/test.png"
    #             await add.send(message=(MessageSegment.at(uid) + "关键词是" + str(arg)) + MessageSegment.image(img_url))
    #             ###  执行语句
    #         else:
    #             left = int(heisi_cd) - int(str((now - cd_time).seconds))
    #             uid = event.user_id
    #             await add.send(
    #                 message=MessageSegment.at(uid) + "你先别急，系统占用中，剩%d秒" % left
    #             )
