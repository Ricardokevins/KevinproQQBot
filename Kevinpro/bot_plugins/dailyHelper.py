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
class dailytask():
    def __init__(self,task,time):
        self.task = task
        self.time = time

    def compaire_time(self):
        y = datetime.now()
        x = datetime.strptime(self.time, '%Y-%m-%d %H:%M:%S')
        diff = y - x
        print(self.task,diff.seconds)
        if diff.seconds <= 600:
            return 1
        else:
            return 0

def load():
    Tasks = []
    f = open('./data/daliy.txt','r',encoding='utf-8')
    lines = f.readlines()
    for i in lines:
        if "==" not in i:
            continue
        data = i.strip()
        task = data.split('==')[0]
        time = data.split('==')[1]
        T = dailytask(task,time)
        Tasks.append(T)
    return Tasks

def dump(Tasks):
    f = open('./data/daliy.txt','w',encoding='utf-8')
    for i in Tasks:
        f.write(i.task + "==" + i.time + '\n')
    f.close()
        
weather_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuser

@nonebot.scheduler.scheduled_job('interval', seconds=5)
async def ww():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    Tasks = load()
    print("Hit")
    TbeD = []
    for t in Tasks:
        if t.compaire_time() == 1:
            try:
                await send_to_superusers(bot,message= t.task)
            except CQHttpError:
                pass
        else:
            TbeD.append(t)
    dump(TbeD)

@on_command('所有日程',  permission=weather_permission)
async def oo(session: CommandSession):
    Tasks = load()
    bot = nonebot.get_bot()
    if len(Tasks) == 0:
        try:
            await send_to_superusers(bot,message= '暂无待办日程')
        except CQHttpError:
                pass
    else:
        for i in Tasks:
            await send_to_superusers(bot,message= i.task + ' ' + i.time)

@on_command('日程移除',  permission=weather_permission)
async def pp(session: CommandSession):
    Tasks = load()
    args = session.current_arg_text.strip().split(' ', 1)
    if not args[0]:
        task = await session.aget(key='task', prompt='请问要移除哪个？', at_sender=True)
    else:
        task = args[0]
    print(task)
    if task != '0' and int(task) <= len(Tasks):
        del Tasks[int(task)-2]
    dump(Tasks)

@on_command('日程', aliases=('提醒', '助手'), permission=weather_permission)
async def _(session: CommandSession):
    # 若用户对机器人说“天气”，则此变量为 `['']`
    # 若用户对机器人说“天气 香港”，则此变量为 `['香港']`
    # 若用户对机器人说“天气 香港 详细”，则此变量为 `['香港', '详细']`
    args = session.current_arg_text.strip().split(' ', 1)
    if not args[0]:
        task = await session.aget(key='task', prompt='请问要提醒啥？', at_sender=True)
    else:
        task = args[0]
    
    Tasks = load()
    res = jio.parse_time(task, time_base=time.time())
    temp = dailytask(task,res['time'][0])
    print(task,res['time'][0])
    Tasks.append(temp)
    dump(Tasks)

