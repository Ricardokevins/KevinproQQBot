import jieba
from wordcloud import WordCloud
# 构建并配置词云对象w
def gen(types):
    w = WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc')

    # 对来自外部文件的文本进行中文分词，得到string
    f = open('./data/Top50{}.txt'.format(types),encoding='utf-8')
    #f = open('./2021-08\\08-20\\21-45\\Top50weibo.txt',encoding='utf-8')
    #txt = f.read()
    lines = f.readlines()
    f2 = open('./data/stopword.txt','r',encoding='utf-8')
    stopwordlist = [i.strip() for i in f2.readlines()]

    filterd = []
    for index,i in enumerate(lines):
        content = i.strip().split('\t')[1]
        freq = int((70 - index)/10)
        #freq = 1
        txtlist = jieba.lcut(content)
        for l in range(freq):
            for word in txtlist:
                if word not in stopwordlist:
                    filterd.append(word)


    string = " ".join(filterd)

    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(string)
    # 将词云图片导出到当前文件夹
    w.to_file('./data/{}.png'.format(types))




from aiocqhttp import MessageSegment
# @on_command('setu', aliases=('富婆','色图', '老婆', '老婆图', '萝莉'))
# async def setu(session: CommandSession):
#     seq = MessageSegment.image("file:///D:\\KevinproPython\\workspace\\KevinproQQBot\\Kevinpro\\8531.png")
#     print(seq)
#     await session.send(seq)

Base_path = "file:///D:\\KevinproPython\\workspace\\KevinproQQBot\\Kevinpro\\data\\{}"
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import requests
import time
import urllib
from lxml import etree
from aiocqhttp import MessageSegment
import requests

@on_command('知乎热榜图', aliases=('知乎词云'))
async def setu(session: CommandSession):
    gen("Zhihu")
    seq = MessageSegment.image(Base_path.format('Zhihu.png'))
    await session.send(seq)



@on_command('微博热榜图', aliases=('微博词云'))
async def setu(session: CommandSession):
    gen("weibo")
    seq = MessageSegment.image(Base_path.format('weibo.png'))
    await session.send(seq)