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

async def add_signature(update: Update, context):
    message = update.channel_post
    if not message:
        return

    # 获取当前频道的签名
    chat_id = message.chat_id
    signature = CHANNEL_SIGNATURES.get(chat_id)
    if not signature:
        return  

    # 检测是否是成组的媒体，比如多张图片组成的相册
    if message.media_group_id:
        if context.chat_data.get("last_media_group_id") == message.media_group_id:
            return  

        # 记下媒体组 ID
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

    # 如果是单一消息（非媒体组）
    elif message.text:
        new_text = message.text + signature
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message.message_id,
            text=new_text,
            parse_mode=ParseMode.MARKDOWN,
        )
        
    elif message.photo or message.video or message.document:
        
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

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, add_signature))
    application.run_polling()

if __name__ == "__main__":
    main()
