from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import CommandArg
from nonebot import on_command

add=on_command("add",priority=99,block=True)

@add.handle()
async def add_handle(event: GroupMessageEvent, args: Message = CommandArg()):
    arg = args.extract_plain_text().split()
    pass


def can_cal(args):
    for num in range(0,len(args)):
        try:
            if(float(args[num])<-100000 or float(args[num])>100000):
                return False
        except ValueError:
            return False
    return True

def cal_1(arg):
    count=len(arg)
    sum=0
    for num in range(0,count):
        sum+=float(arg[num])
    return sum

@add.handle()
async def _(event:GroupMessageEvent, args: Message = CommandArg()):
    arg=args.extract_plain_text().split()
    if len(arg)==0:
        await add.finish("没有数字也不会算啊...")
    elif len(arg)==1:
        await add.finish("只有一个数字...")
    elif (len(arg)>=2) and (len(arg)<=10):
        if can_cal(arg):
            await add.finish(f"算出来了!答案是:{cal_1(arg)}")
        else:
            await add.finish("算不过来了!")
    else:
        await add.finish("算不过来了!")