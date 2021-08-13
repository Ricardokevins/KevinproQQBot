from aiocache import cached
import requests
import pandas as pd
import time
import os
# follow https://zhuanlan.zhihu.com/p/362213028

def save_hot_list() -> None:
    # 请求头
    headers = {
        'User-Agent': 'osee2unifiedRelease/4318 osee2unifiedReleaseVersion/7.7.0 Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Host': 'api.zhihu.com',
    }
    # 请求参数
    params = (
        ('limit', '50'),
        ('reverse_order', '0'),
    )
    # 发送请求
    # proxies = {
    # "http": "http://127.0.0.1:7890",
    # }
    proxies = {'http': None, 'https': None}
    response = requests.get(
        'https://zhihu.com/topstory/hot-list', proxies=proxies,headers=headers, params=params)

    items = response.json()['data']
    rows = []

    # 遍历全部热榜，取出几个属性
    for rank, item in enumerate(items, start=1):
        target = item.get('target')
        title = target.get('title')
        answer_count = target.get('answer_count')
        hot = int(item.get('detail_text').split(' ')[0])
        follower_count = target.get('follower_count')
        question_url = target.get('url').replace(
            'api', 'www').replace('questions', 'question')
        if rank >= 10:
            continue
        rows.append({
            '排名': rank,
            '标题': title,
            '回答数': answer_count,
            '关注数': follower_count,
            '热度(万)': hot,
        })
        
    
    return rows



async def fetch_zhihuTop():
    try:
        res = save_hot_list()
    except HTTPError as e:
        logger.exception(e)
        raise ServiceException('API 服务目前不可用')
    return res

@cached(ttl=60) # 结果缓存 60 秒
async def get_zhihuTop():
    return (await fetch_zhihuTop())


