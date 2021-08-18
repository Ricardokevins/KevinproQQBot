import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import bs4
class crawl:
	def page_kuai(page):
	    ua = UserAgent()
	    headers={'User-Agent':ua.random}
	    html=requests.get('https://www.kuaidaili.com/free/inha/'+str(page),headers=headers)#删除作者参数  ,verify=False
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
                            #r.lpush('IP',IP)
		                    print("可yong+1"+IP)
		                except :
		                    print("false")
		            except Exception:
		                pass
	    else:
	        print('********************被墙*************************')

#用来测试代理池里面代理IP是否可用
import redis
import requests
import time
class test:
	def test_IP(r):# 从列表的尾部取出一个ip
		while r.llen('IP') >12 :
			try:
				ip=str(r.rpop('IP'),encoding='utf-8')# redis导出的数据都是bytes类型的，所以我们必须将其str化，必须加enconding参数
				proxies = {'http': ip}# 测试ip有没有用
				try:
					html=requests.get("http://www.baidu.com",proxies=proxies,timeout=6)
					if html.status_code == 200:
						r.lpush('IP',ip)
						print('valid IP')
				except :
					print('丢弃无用的ip')
				time.sleep(3)
			except :
				print("IP池枯竭")
			#time.sleep(20)


import redis
import time

 
if __name__ == '__main__':
	count_1=16
	count_2=17
	
	R = None
	for i in range(count_1,count_2):
		crawl.page_kuai(i,R)
		time.sleep(2)
		count_1=count_2
		count_2+=1
		test.test_IP(R)