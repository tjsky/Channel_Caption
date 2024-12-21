from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters

# 设置 Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# 支持多频道不同签名，冒号前是频道的ID
CHANNEL_SIGNATURES = {
    -1001234567890: "\n\n---\n来自 [频道 A](https://t.me/channelA)",  # 签名内容，支持MARKDOWN格式
    -1002345678901: "\n\n---\n来自 [频道 B](https://t.me/channelB)",
}

# 定义忽略添加签名的关键词列表
IGNORED_KEYWORDS = ["#互推", "Powered by", "By：", "订阅频道", "加入群聊"]

# 检查消息是不是含有忽略词的
def contains_ignored_keywords(text):
    return any(keyword in text for keyword in IGNORED_KEYWORDS)

async def add_signature(update: Update, context):
    message = update.channel_post
    if not message:
        return

    # 获取消息当前签名
    chat_id = message.chat_id
    signature = CHANNEL_SIGNATURES.get(chat_id)
    if not signature:
        return  

    # 检测是否包含忽略的关键词
    if message.text and contains_ignored_keywords(message.text):
        return  

    if message.caption and contains_ignored_keywords(message.caption):
        return  

    # 是媒体组中的消息吗？
    if message.media_group_id:

        if context.chat_data.get("last_media_group_id") == message.media_group_id:
            return  


        context.chat_data["last_media_group_id"] = message.media_group_id

        # 确保新的签名不超过 Telegram 限制（非会员 1024 字符，会员 2048 字符）
        new_caption = (message.caption or "") + signature
        if len(new_caption) > 1024:
            new_caption = (message.caption or "")[:1024 - len(signature)] + signature

        await context.bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message.message_id,
            caption=new_caption,
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    # 单一消息
    elif message.text:
        new_text = message.text + signature
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message.message_id,
            text=new_text,
            parse_mode=ParseMode.MARKDOWN,
        )
    elif message.photo or message.video or message.document:
        new_caption = (message.caption or "") + signature
        if len(new_caption) > 1024:
            new_caption = (message.caption or "")[:1024 - len(signature)] + signature
        await context.bot.edit_message_caption(
            chat_id=chat_id,
            message_id=message.message_id,
            caption=new_caption,
            parse_mode=ParseMode.MARKDOWN,
        )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, add_signature))
    application.run_polling()

if __name__ == "__main__":
    main()
