import requests
from lxml import etree


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
    cur_time = time.strftime("%H", time.localtime()) 
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


output_folder = get_output()
model = WeiBo()
Top = model.run()

with open(output_folder+'/'+'Top50weibo'+".txt",mode="w",encoding='utf-8') as f:
    for i in Top:
        f.write(i+'\n')

from pattern_event_triples import ExtractEvent
for i in Top:
    content = i.split('\t')[1]
    handler = ExtractEvent()
    events, spos = handler.phrase_ip(content)
    spos = [i for i in spos if i[0] and i[2]]
    print('svos', spos)

