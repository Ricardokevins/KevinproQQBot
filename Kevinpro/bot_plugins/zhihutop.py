from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
from services.common import ServiceException
from services.zhihutop import get_zhihuTop
from nonebot.natural_language import NLPSession, IntentCommand
from nonebot.experimental.plugin import on_command, on_natural_language
from jieba import posseg

__plugin_name__ = '聊天'
__plugin_usage__ = (
    '用法：\n'
)


weather_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuser


@on_command('知乎热榜', aliases=('知乎', '热搜'), permission=weather_permission)
async def _(session: CommandSession):
    # 若用户对机器人说“天气”，则此变量为 `['']`
    # 若用户对机器人说“天气 香港”，则此变量为 `['香港']`
    # 若用户对机器人说“天气 香港 详细”，则此变量为 `['香港', '详细']`
    
    try:
        func = get_zhihuTop
        result = await func()
    except ServiceException as e:
        result = e.message
    
    
    for i in result:
        sent = ""
        for j in i:
            sent += '{} : {}  '.format(j,i[j])
                
        await session.send(sent)

