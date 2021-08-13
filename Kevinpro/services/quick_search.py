import threading
import time
import math
import datetime
import multiprocessing as mp

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

def get_scorer(name, param):
    query,query_list,answer_list = param
    max_sim = -1
    for idx in range(len(query_list)):
        cur_sim = get_score(query_list[idx], query)
        if cur_sim > max_sim:
            max_sim = cur_sim
            best_match_q = query_list[idx]
            best_match_a = answer_list[idx]
    return (max_sim, best_match_q,best_match_a)
        

def multi_process_tag(query,query_list,answer_list):
    num_cores = int(mp.cpu_count())
    print("本地计算机有: " + str(num_cores) + " 核心")
    pool = mp.Pool(num_cores)
    
    param_dict = {}
    start = 0
    end =  len(query_list)
    step = int((end - start)/num_cores)
    print("per Task Step: ",step)
    for i in range(num_cores):
        param_dict['task{}'.format(i)]= (query,query_list[start:start+step],answer_list[start:start+step])
        start = start+step
    param_dict['task{}'.format(num_cores)]= (query,query_list[start:],answer_list[start:])
    start_t = datetime.datetime.now()
    results = [pool.apply_async(get_scorer, args=(name, param)) for name, param in param_dict.items()]
    results = [p.get() for p in results]
    total = 0
    my_result = []
    
    max_sim = -1

    for i in results:
        score,q,a = i
        if score > max_sim:
            max_sim = score
            best_match_q = q
            best_match_a = a

    

    end_t = datetime.datetime.now()
    elapsed_sec = (end_t - start_t).total_seconds()
    print("多进程计算 共消耗: " + "{:.2f}".format(elapsed_sec) + " 秒")
    return best_match_a

    