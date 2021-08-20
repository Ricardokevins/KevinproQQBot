from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
from services.common import ServiceException
from services.NJUQA import get_NJUbot
from nonebot.natural_language import NLPSession, IntentCommand
from nonebot.experimental.plugin import on_command, on_natural_language
from jieba import posseg

__plugin_name__ = '问答'
__plugin_usage__ = (
    '用法：问答，使用NJU问答语料\n'
)


weather_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuser


@on_command('问答', aliases=('问'), permission=weather_permission)
async def _(session: CommandSession):
    # 若用户对机器人说“天气”，则此变量为 `['']`
    # 若用户对机器人说“天气 香港”，则此变量为 `['香港']`
    # 若用户对机器人说“天气 香港 详细”，则此变量为 `['香港', '详细']`
    args = session.current_arg_text.strip().split(' ')
    print(args)
    query = " ".join(args)

    if not args[0]:
        Ask = await session.aget(key='city', prompt='请问你问什么？', at_sender=True)
    else:
        Ask = query

    try:
        func = get_NJUbot
        result = await func(Ask)
    except ServiceException as e:
        result = e.message
    await session.send(result)

from aiocqhttp import MessageSegment
# @on_command('setu', aliases=('富婆','色图', '老婆', '老婆图', '萝莉'))
# async def setu(session: CommandSession):
#     seq = MessageSegment.image("file:///D:\\KevinproPython\\workspace\\KevinproQQBot\\Kevinpro\\8531.png")
#     print(seq)
#     await session.send(seq)

Base_path = "file:///D:\\KevinproPython\\workspace\\KevinproQQBot\\Kevinpro\\{}"
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import requests
import time
import urllib
from lxml import etree
from aiocqhttp import MessageSegment
import requests


class GetPic:
    def __init__(self):
        self.session = requests.session()

    def get_Pic(self):
        res = self.session.get("http://api.mtyqx.cn/api/random.php", verify=False)

        # 保存图片
        with open("{}.png".format('8531'), "wb") as f:
            f.write(res.content)
        return True

@on_command('setu', aliases=('富婆','色图', '老婆', '老婆图', '萝莉'))
async def setu(session: CommandSession):
    Pic = GetPic()
    import os
    print(os.path.exists("{}.png".format('8531')))
    if Pic.get_Pic():
        seq = MessageSegment.image(Base_path.format('8531.png'))
        await session.send(seq)
