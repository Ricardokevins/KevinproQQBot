from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
from services.common import ServiceException
from services.dialogue import get_reply
from nonebot.natural_language import NLPSession, IntentCommand
from nonebot.experimental.plugin import on_command, on_natural_language
from jieba import posseg

__plugin_name__ = '聊天'
__plugin_usage__ = (
    '用法：\n'
)


weather_permission = lambda sender: (not sender.is_privatechat) or sender.is_superuser


@on_command('对话', aliases=('说话', '聊天'), permission=weather_permission)
async def _(session: CommandSession):
    # 若用户对机器人说“天气”，则此变量为 `['']`
    # 若用户对机器人说“天气 香港”，则此变量为 `['香港']`
    # 若用户对机器人说“天气 香港 详细”，则此变量为 `['香港', '详细']`
    args = session.current_arg_text.strip().split(' ')
    print(args)

    query = " ".join(args)
    print(query)
    if not args[0]:
        Ask = await session.aget(key='city', prompt='请问你要说什么呢？', at_sender=True)
    else:
        Ask = query

    try:
        func = get_reply
        result = await func(Ask)
    except ServiceException as e:
        result = e.message

    await session.send(result)

