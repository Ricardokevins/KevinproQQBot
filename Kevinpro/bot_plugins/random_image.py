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
    if Pic.get_Pic():
        seq = MessageSegment.image(Base_path.format('8531.png'))
        await session.send(seq)
