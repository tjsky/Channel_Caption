from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, MessageHandler, filters

# 设置 Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# 签名内容，支持MARKDOWN格式
SIGNATURE = "\n\n---\n来源： [我的频道](https://t.me/your_channel)"

async def add_signature(update: Update, context):
    # 监控消息
    message = update.channel_post
    if not message:
        return

    # 文字消息
    if message.text:
        new_text = message.text + SIGNATURE
        await context.bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=message.message_id,
            text=new_text,
            parse_mode=ParseMode.MARKDOWN,
        )
    # 图片、视频、文件消息
    elif message.caption:
        # 防止签名超出 Telegram 限制（开通TG会员可到2048个字符，请同步修改1024到2048）
        new_caption = message.caption + SIGNATURE
        if len(new_caption) > 1024:
            new_caption = message.caption[:1024 - len(SIGNATURE)] + SIGNATURE

        await context.bot.edit_message_caption(
            chat_id=message.chat_id,
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
