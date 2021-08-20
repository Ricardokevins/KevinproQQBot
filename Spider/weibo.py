import requests
from lxml import etree
def save_hot_list() -> None:
    # 请求头
    headers = {
        'User-Agent': 'osee2unifiedRelease/4318 osee2unifiedReleaseVersion/7.7.0 Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        #'User-Agent':"Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) (Engine, like URL) Mobile/12B440 MicroMessenger/6.0.1 NetType/3G+",
        'Host': 'api.zhihu.com',
    }
    #headers={'User-Agent':headers,'Host': 'api.zhihu.com'}
    # 请求参数
    params = (
        ('limit', '50'),
        ('reverse_order', '0'),
    )
    # 发送请求

    proxies = {'http': None, 'https': None}
    
    response = requests.get(
        'https://zhihu.com/topstory/hot-list', proxies=proxies,headers=headers, params=params)
    #print(response.json())
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


        rows.append(str(rank)+"\t"+title)

    return rows


class WeiBo(object): 
    def run(self): 
        proxies = {'http': None, 'https': None}
        url = "https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6" 
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'} 
        html = etree.HTML(requests.get(url, headers=header,proxies=proxies).text) 
        rank = html.xpath('//td[@class="td-01 ranktop"]/text()') 
        affair = html.xpath('//td[@class="td-02"]/a/text()') 
        view = html.xpath('//td[@class="td-02"]/span/text()') 
        top = affair[0] 
        affair = affair[1:] 
        Topk = []
        #print('{0:<10}\t{1:<40}'.format("top", top)) 
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

    check_mkdir(first_path)
    check_mkdir(first_path+"/"+second_path)
    check_mkdir(first_path+"/"+second_path+"/"+cur_time)
    return first_path+"/"+second_path+"/"+cur_time

import time
from apscheduler.schedulers.blocking import BlockingScheduler

def run():
    output_folder = get_output()

    model = WeiBo()
    Top = model.run()
    with open(output_folder+'/'+'Top50weibo'+".txt",mode="w",encoding='utf-8') as f:
        for i in Top:
            f.write(i+'\n')
    Top = save_hot_list()
    with open(output_folder+'/'+'Top50Zhihu'+".txt",mode="w",encoding='utf-8') as f:
        for i in Top:
            f.write(i+'\n')

run()
def dojob():
    #创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    #添加任务,时间间隔2S
    scheduler.add_job(run, 'interval', minutes=30, id='weibo_top')
    scheduler.start()
dojob()





