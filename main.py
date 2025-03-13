from telegram import Update,ReactionTypeEmoji
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden
import logging
import json
import random
from formatter import MessageFormatter


# 初始化日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 加载配置
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
CHANNEL_SIGNATURES = {int(k): v for k, v in config["CHANNEL_SIGNATURES"].items()}
IGNORED_KEYWORDS = config["IGNORED_KEYWORDS"]
REACTION_ENABLED = config.get("REACTION_ENABLED", True)  # 是否启用反应功能
DEFAULT_REACTIONS = config.get("DEFAULT_REACTIONS", ["👍", "❤️", "🎉"])

# 检查忽略关键词
def contains_ignored_keywords(text):
    return any(keyword.lower() in text.lower() for keyword in IGNORED_KEYWORDS)

async def add_signature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.channel_post
        if not message:
            return

        chat_id = message.chat_id
        signature = CHANNEL_SIGNATURES.get(chat_id)
        if not signature:
            return

        # 检查忽略关键词
        content = message.text or message.caption
        if content and contains_ignored_keywords(content):
            return

        # 处理媒体组消息
        if message.media_group_id:
            if context.chat_data.get("last_media_group_id") == message.media_group_id:
                return
            context.chat_data["last_media_group_id"] = message.media_group_id
            await _add_reactions(context, chat_id, message.message_id)
        else:
            await _add_reactions(context, chat_id, message.message_id)

        # 格式转换处理
        processed_content = MessageFormatter.convert_to_markdown_v2(
            content,
            entities=message.entities or message.caption_entities
        )

        # 添加签名
        if message.text:  # 文本消息4096字
            max_length = 4096
            new_text = MessageFormatter.add_signature(processed_content, signature, max_length)
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message.message_id,
                text=new_text,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        else:  # 媒体消息最长1024字
            max_length = 1024
            new_caption = MessageFormatter.add_signature(processed_content, signature, max_length)
            await context.bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message.message_id,
                caption=new_caption,
                parse_mode=ParseMode.MARKDOWN_V2
            )

        # 添加默认反应
        if REACTION_ENABLED and message.message_id:
            await _add_reactions(context, chat_id, message.message_id)

    except BadRequest as e:
        if "Can't parse entities" in str(e):
            logger.error(f"格式解析失败: {e}\n原始内容: {content}")
        elif "Message not modified" in str(e):
            logger.debug("消息无变化无需更新")
        else:
            logger.error(f"API请求错误: {e}")
    except Forbidden as e:
        logger.critical(f"权限不足: {e}")
    except Exception as e:
        logger.error(f"未处理异常: {e}", exc_info=True)

# 添加反应
async def _add_reactions(context, chat_id, message_id):
    try:
        if not REACTION_ENABLED or not DEFAULT_REACTIONS:
            return

        # 随机选择单个反应
        selected_emoji = random.choice(DEFAULT_REACTIONS)
        
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[ReactionTypeEmoji(emoji=selected_emoji)],  
            is_big=False
        )
        logger.debug(f"已添加随机反应 {selected_emoji}")

    except BadRequest as e:
        if "invalid reaction type" in str(e).lower():
            logger.error(f"检测到无效表情，请检查配置: {e}")
        elif "Reactions are disabled" in str(e):
            logger.warning(f"频道 {chat_id} 禁用反应功能")
        elif "ReactionTypeEmoji" in str(e):
            logger.error(f"表情类型不合法: {e}")
        elif "message not found" in str(e):
            logger.error("目标消息不存在")
        else:
            logger.error(f"反应添加请求错误: {e}")
    except Forbidden as e:
        logger.critical(f"权限不足无法添加反应: {e}")
    except Exception as e:
        logger.error(f"添加反应时未处理异常: {e}", exc_info=True)
    except IndexError:
        logger.error("反应列表为空，请检查DEFAULT_REACTIONS配置")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, add_signature))
    application.run_polling()

if __name__ == "__main__":
    main()
    random.seed()
