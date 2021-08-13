from aiocache import cached
import requests
import pandas as pd
import time
import os
# follow https://zhuanlan.zhihu.com/p/362213028

query = []
answer = []
import json
load_f =  open("./data/QA.json",'r',encoding='utf-8')
load_dict = json.load(load_f)
pairs_dict = load_dict['data']  
for i in pairs_dict:
    for j in i['paragraphs']:
        query.append(j['qas'][0]['question'])
        answer.append(j['qas'][0]['answers'][0]['text'])

option_corpus = ['./data/chatterbot.tsv','./data/xiaohuangji.tsv','./data/qingyun.tsv']
for i in option_corpus:
    f = open(i,'r',encoding='utf-8')
    lines = f.readlines()
    for k in lines:
        q = k.split('\t')[0]
        a = k.split('\t')[1]
        query.append(q)
        answer.append(a)

print("Corpus Size : {}".format(len(query)))
import jieba

import jieba.analyse
import jieba
import jieba.analyse
import numpy as np





def extract_keyword(s):
    s = s.replace(' ','')
    return [i for i in s]

def get_score(s1,s2):
    keywords_x = extract_keyword(s1)
    keywords_y = extract_keyword(s2)

    # jaccard相似度计算
    intersection = len(list(set(keywords_x).intersection(set(keywords_y))))
    union = len(list(set(keywords_x).union(set(keywords_y))))
    # 除零处理
    sim = float(intersection)/union if union != 0 else 0
    return sim



from tqdm import tqdm
def search(question):
    max_sim = -1
    for i in tqdm(range(len(query))):
        cur_sim = get_score(query[i], question)
        if cur_sim > max_sim:
            max_sim = cur_sim
            best_match_q = query[i]
            best_match_a = answer[i]
    print(max_sim)
    print("匹配问题: " + best_match_q + " == 回答: " + best_match_a)
    if max_sim <= 0.4:
        best_match_a = "我暂时无法回答这个问题"
    
    #return "匹配问题: " + best_match_q + " == 回答: " + best_match_a
    return best_match_a

from services.quick_search import multi_process_tag
def get_quick_search(question):
    return multi_process_tag(question,query,answer)

async def fetch_NJUbot(que):
    try:
        res = search(que)
    except HTTPError as e:
        logger.exception(e)
        raise ServiceException('API 服务目前不可用')
    return res

@cached(ttl=60) # 结果缓存 60 秒
async def get_NJUbot(que):
    return (await fetch_NJUbot(que))


