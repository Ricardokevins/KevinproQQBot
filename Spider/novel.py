# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import random
base_path =  'https://m.diershubao.org'
# if __name__ == "__main__":
#     
#     target = 'https://m.diershubao.org/0_13/index_2.html#all'
#     req = requests.get(url = target)
    
#     print(req.encoding) #查看网页返回的字符集类型
#     print(req.apparent_encoding) #自动判断字符集类型
#     req.encoding = 'gbk'
#     html = req.text
#     div_bf = BeautifulSoup(html)
#     div = div_bf.find_all('div', class_ = 'info_chapters')
#     print(len(div))
#     a_bf = BeautifulSoup(str(div[0]))
#     a = a_bf.find_all('a')
#     #print(a)
#     target = {}
#     for each in a:
#         if each.get('href') != None:
#             if each.string in target:
#                 print(each.string, base_path + each.get('href'))
#             else:
#                 target[each.string] = base_path + each.get('href')
#         time.sleep(random.randint(1,10)/10)
#     print(target)

# if __name__ == "__main__":
#     target = 'https://m.diershubao.org/0_13/4954.html'
#     req = requests.get(url = target)
#     print(req.encoding) #查看网页返回的字符集类型
#     print(req.apparent_encoding) #自动判断字符集类型
#     req.encoding = 'GB18030'
#     req.encoding = 'gbk'
#     #req.encoding = 'utf-8'
#     html = req.text
#     #print(html.decode('utf-8'))
#     bf = BeautifulSoup(html)
#     texts = bf.find_all('div', class_ = 'novelcontent') 
#     #print(texts[0])
#     f = open('novel/result.txt','w',encoding='utf-8')
#     #print(texts[0])
#     f.write(texts[0].text.replace('\xa0'*8,'\n\n')+ '\n')

def getNovel(target):
    req = requests.get(url = target)
    req.encoding = 'gbk'
    #req.encoding = 'utf-8'
    html = req.text
    #print(html.decode('utf-8'))
    bf = BeautifulSoup(html)
    texts = bf.find_all('div', class_ = 'novelcontent') 
    #print(texts[0])
    #print(texts[0].text.replace('\xa0'*8,'\n\n')[:15])
    return texts[0].text.replace('\xa0'*8,'\n\n')

def write2file(text,file):
    f = open('novel/chaoshi/{}.txt'.format(file),'w',encoding='utf-8')
    #print(texts[0])
    f.write(text + '\n')

def getFromNext():
    target = 'https://m.diershubao.org/0_13/4954.html'
    target = "https://m.diershubao.org/0_13/4960.html"
    target = "https://m.diershubao.org/0_13/5393.html"
    cached_text = []
    while 1:
        print(target)
        req = requests.get(url = target)
        #req.encoding = 'GB18030'
        req.encoding = 'gbk'
        #req.encoding = 'utf-8'
        html = req.text
        #print(html.decode('utf-8'))
        
        bf = BeautifulSoup(html,features="html.parser")
        # texts = bf.find_all('div', class_ = 'novelcontent') 
        texts = bf.find_all('div', class_ = 'page_chapter') 


        a_bf = BeautifulSoup(str(texts[0]))
        a = a_bf.find_all('a')
        result = getNovel(target)
        cached_text.append(result)
        for each in a:
            if each.string == "下一页" or each.string == "下一章":
                target = base_path + each.get('href')
            if each.string == "下一章":
                Novel = "\n".join(cached_text)
                temp = bf.find_all('div', class_ = 'nr_function') 
                title_temp = BeautifulSoup(str(temp[0]))
                title = title_temp.find_all('h1')[0].string
                write2file(Novel,title)
                cached_text = []
            
            
        time.sleep(random.randint(1,20)/10)
    # f = open('novel/result.txt','w',encoding='utf-8')
    # f.write(texts[0].text.replace('\xa0'*8,'\n\n')+ '\n')

getFromNext()
