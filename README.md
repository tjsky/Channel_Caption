# Channel_Caption
自动给Telegram频道消息增加签名，方便频道主实现宣传功能。带有排除关键词功能，以免错改其他bot的消息。

![](https://img.tjsky.net/2024/11/3ab85c5ef15491f1cd5282bc652b3105.png)


## 前期准备
1. 去 @BotFather 申请一个机器人。
2. 获得 Bot 的 API Token。
3. 管理员权限：给 Bot 频道管理员权限，主要是编辑消息的权限。


## 拉取并修改配置
1. `git clone https://github.com/tjsky/Channel_Caption.git`
2. `cd Channel_Caption`
3. `pip install -r requirements.txt`
4. 将`config.example.json`改名为`config.json`使用你喜欢的编辑器编辑内部的相关部分。
 - BOT_TOKEN：从botfather那里得到
 - CHANNEL_SIGNATURES：频道ID（是一个负数），冒号后是需要发送的内容（支持markdown格式）
 - IGNORED_KEYWORDS：不做签名的关键词，当消息含有这些关键词时，不会对消息去签名
 - REACTION_ENABLED：是否开启反应功能（消息下的那个表情反应）
 - DEFAULT_REACTIONS：随机使用的额反应（bot每条消息只能点一个反应）
## 运行
1. 测试运行：`python main.py`
2. 正式运行：最好还是用类似 PM2、supervisor 之类的进程管理工具，来实现不间断运行、自动重启、失效重启等功能。
如果你用的面板服，比如宝塔和1panel，他们有官方开发的守护进程工具用那个也行。

## 更新
- 初版发布
- 尝试解决签名后原始消息格式消失的问题；增加反应功能
