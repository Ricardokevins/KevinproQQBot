f = open("./2021-08/08-20/09-14/Top50Zhihu.txt",encoding="utf-8")
lines = f.readlines()
Top = [i.strip() for i in lines]
from pattern_event_triples import ExtractEvent
for i in Top:
    content = i.split('\t')[1]
    handler = ExtractEvent()
    events, spos = handler.phrase_ip(content)
    spos = [i for i in spos if i[0] and i[2]]
    print('svos', spos)