# from datetime import datetime
# text = '2021-08-17 14:30:00'
# y = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
# #a1 = datetime.datetime.strptime(a,"%d/%m/%Y %H:%M:%S")
# print(y)
# z = datetime.now()
# diff = y - z
# print(diff)
# print(type(diff))
# print(diff.days)

# print(diff.seconds)

import jionlp as jio
import time
text = '1分钟后叫我'
res = jio.parse_time(text, time_base=time.time())
print(res)
