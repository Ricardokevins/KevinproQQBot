from aiocache import cached

from Seq2Seq.test import BotAPI


async def fetch_reply(uri: str) -> str:
    try:
        res = BotAPI(uri)
    except HTTPError as e:
        logger.exception(e)
        raise ServiceException('API 服务目前不可用')
    return res

@cached(ttl=60) # 结果缓存 60 秒
async def get_reply(city: str) -> str:
    return (await fetch_reply(city))


