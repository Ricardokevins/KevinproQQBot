import jieba
from wordcloud import WordCloud
# 构建并配置词云对象w
w = WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc')

# 对来自外部文件的文本进行中文分词，得到string
f = open('./2021-08\\08-20\\21-45\\Top50Zhihu.txt',encoding='utf-8')
#f = open('./2021-08\\08-20\\21-45\\Top50weibo.txt',encoding='utf-8')
#txt = f.read()
lines = f.readlines()
f2 = open('stopword.txt','r',encoding='utf-8')
stopwordlist = [i.strip() for i in f2.readlines()]

filterd = []
for index,i in enumerate(lines):
    content = i.strip().split('\t')[1]
    freq = int((70 - index)/10)
    #freq = 1
    txtlist = jieba.lcut(content)
    for l in range(freq):
        for word in txtlist:
            if word not in stopwordlist:
                filterd.append(word)


string = " ".join(filterd)

# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)

# 将词云图片导出到当前文件夹
w.to_file('test.png')