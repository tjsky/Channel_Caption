# Channel_Caption
自动给Telegram频道消息增加签名

![](https://img.tjsky.net/2024/11/3ab85c5ef15491f1cd5282bc652b3105.png)


## 前期准备
1. 去 @BotFather 申请一个机器人。
2. 获得 Bot 的 API Token。
3. 管理员权限：给 Bot 频道管理员权限，主要是编辑消息的权限。


## 拉取并修改配置
1. `git clone https://github.com/tjsky/Channel_Caption.git`
2. `cd Channel_Caption`
3. `pip install -r requirements.txt`
4. 使用你喜欢的编辑器编辑main.py内的相关部分。
```python
# 设置 Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# 支持多频道不同签名，冒号前是频道的ID，后面是签名的内容，支持MARKDOWN格式
CHANNEL_SIGNATURES = {
    -1001234567890: "\n\n---\n来自 [频道 A](https://t.me/channelA)",  # 签名内容，支持MARKDOWN格式
    -1002345678901: "\n\n---\n来自 [频道 B](https://t.me/channelB)",
}
```

## 运行
1. 测试运行：`python -m main`
2. 正式运行：最好还是用类似 PM2、supervisor 之类的进程管理工具，来实现不间断运行、自动重启、失效重启等功能。
如果你用的面板服，比如宝塔和1panel，他们有官方开发的守护进程工具用那个也行。
