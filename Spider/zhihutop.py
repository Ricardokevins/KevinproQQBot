import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import bs4

def get_proxy(page):
    ua = UserAgent()
    headers={'User-Agent':ua.random}
    print("============ Getting {} page ============ ".format(page))
    html=requests.get('https://www.kuaidaili.com/free/inha/'+str(page),headers=headers)#删除作者参数  ,verify=False
    enable_list = []
    if html.status_code == 200:
        #print(html.text)
        Soup=BeautifulSoup(html.text,'lxml')
        tbody=Soup.find('tbody')
        if isinstance(tbody,bs4.element.Tag):
            tr_list=tbody.find_all('tr')
            for tr in tr_list:
                try:
                    IP_adress=tr.find('td').get_text()
                    IP_port=tr.find('td',attrs={'data-title':"PORT"}).get_text()
                    IP="http://"+IP_adress+":"+IP_port
                    proxies={'http':IP}
                    #print(proxies)
                    try:
                        response = requests.get('http://www.baidu.com', proxies=proxies,timeout=10)#########
                        enable_list.append(proxies)
                    except :
                        print("false")
                except Exception:
                    pass
    else:
        print('********************被墙*************************')
    return enable_list

def save_hot_list() -> None:
    # 请求头
    ua = UserAgent()
	
    # headers = {
    #     #'User-Agent': 'osee2unifiedRelease/4318 osee2unifiedReleaseVersion/7.7.0 Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    #     'User-Agent':"Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) (Engine, like URL) Mobile/12B440 MicroMessenger/6.0.1 NetType/3G+",
    #     'Host': 'api.zhihu.com',
    # }
    # 请求参数
    params = (
        ('limit', '50'),
        ('reverse_order', '0'),
    )
    # 发送请求
    # proxies = {
    # "http": "http://127.0.0.1:7890",
    # }


    #proxies = {'http': None, 'https': None}
    flag = 1
    page = 1
    while flag:
        #proxies_list = get_proxy(page)
        proxies_list = ['jj']
        page = page + 1
        page = page % 18
        if len(proxies_list) == 0:
            continue
        #print("Hit ===================")
        for proxies in proxies_list:
            #headers={'User-Agent':ua.random,'Host': 'api.zhihu.com','Cookie':"HuCV4KQJJGyIlkNSLLKM1HE5svztuRw6zGcx9Bf2SL4"}
            headers={'User-Agent':ua.random,'Host': 'api.zhihu.com'}
            # print(proxies)
            # print(headers)
            #IP="http://"+"127.0.0.1"+":"+"7890"
            #proxies={'http':IP}
            proxies = {'http': None, 'https': None}
            response = requests.get(
                'https://zhihu.com/topstory/hot-list', proxies=proxies,headers=headers, params=params)
            test_data = response.json()
            if 'data' in test_data:
                items = test_data['data']
                flag = 0
                break
            else:
                print(test_data)
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
        
    print(rows)
    return rows


save_hot_list()