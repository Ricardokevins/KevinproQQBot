# KevinproQQBot

基于NoneBot的实现的QQ机器人，欢迎PR，提交新的插件



本项目的主要入门链接：[使用 nonebot 搭建 qq 群聊机器人 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/340849952)

本项目自然语言处理内核：[Ricardokevins/Kevinpro-NLP-demo: 个人的NLP实践demo，包含了分类，对话机器人，文本摘要，关系抽取以及对抗训练，知识蒸馏等pytorch实现 (github.com)](https://github.com/Ricardokevins/Kevinpro-NLP-demo)



主要框架：

```
gocqhttp                          -------- QQ消息的捕获
Kevinpro                          -------- 接受捕获的消息并处理
	bot_plugins                   -------- 插件实现
		dialogue.py               -------- 对话算法
		ping.py                   -------- 测试用
		weather.py                -------- 查询天气
		zhihutop.py               -------- 获取知乎热榜
	services                      --------为插件提供支持
		...略
	bot.py                        -------- 主函数
	bot_config.py                 -------- 配置文件
	
```



# 已经实现：

1. 获取天气
2. 简单的英文对话
3. 获取知乎Top10热搜

![image-20210811134933323](README.assets/image-20210811134933323.png)



# 待实现

1. 更多的NLP算法迁移和融合
2. 更加智能的问答，包括中文支持
3. 引入图片等资源