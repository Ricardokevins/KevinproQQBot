import requests
from lxml import etree
from datetime import datetime
from nonebot.helpers import send_to_superusers
import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
from services.common import ServiceException
from services.weather import get_current_weather_short
from services.weather import get_current_weather_short, get_current_weather_desc
from nonebot.natural_language import NLPSession, IntentCommand
from nonebot.experimental.plugin import on_command, on_natural_language
import jionlp as jio
import time
__plugin_name__ = '日程 助手'
__plugin_usage__ = (
    '用法：\n'

)

from datetime import datetime
weather_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuser
class WeiBo(object): 
    def run(self): 
        url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6" 
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'} 
        html = etree.HTML(requests.get(url, headers=header).text) 
        rank = html.xpath('//td[@class="td-01 ranktop"]/text()') 
        affair = html.xpath('//td[@class="td-02"]/a/text()') 
        view = html.xpath('//td[@class="td-02"]/span/text()') 
        top = affair[0] 
        affair = affair[1:] 
        Topk = []
        print('{0:<10}\t{1:<40}'.format("top", top)) 
        for i in range(0, len(affair)): 
            # print(rank[i])
            # print(affair[i])
            result = str(rank[i])+'\t'+affair[i]
            Topk.append(result)
            #print("{0:<10}\t{1:{3}<30}\t{2:{3}>20}".format(rank[i], affair[i], chr(12288)))
            #print("{0:<10}\t{1:{3}<30}\t{2:{3}>20}".format(rank[i], affair[i], view[i], chr(12288)))
        return Topk


import os
def get_output():
    import time
    cur_time = time.strftime("%H-%M", time.localtime()) 
    first_path = time.strftime("%Y-%m", time.localtime()) 
    second_path = time.strftime("%m-%d", time.localtime()) 
    def check_mkdir(path):
        import os
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path) 
    basepath = './data/'
    check_mkdir(basepath+first_path)
    check_mkdir(basepath+first_path+"/"+second_path)
    check_mkdir(basepath+first_path+"/"+second_path+"/"+cur_time)
    return first_path+"/"+second_path+"/"+cur_time

def func():
    output_folder = get_output()
    model = WeiBo()
    Top = model.run()
    with open(output_folder+'/'+'Top50weibo'+".txt",mode="w",encoding='utf-8') as f:
        for i in Top:
            f.write(i+'\n')

@nonebot.scheduler.scheduled_job('interval', minutes=1)
async def hh():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    func()






