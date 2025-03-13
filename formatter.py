from telegram.helpers import escape_markdown
import re

class MessageFormatter:
    @staticmethod
    def convert_to_markdown_v2(original_text, entities=None):
        # 需要转义的特殊字符（Markdown V2）
        MARKDOWN_CHARS = r'_*[]()~`>#+-=|{}.!'

        if not original_text:
            return ""

        
        escaped = original_text.translate(
            str.maketrans({char: f'\\{char}' for char in MARKDOWN_CHARS})
        )

        
        converted = re.sub(r'<b>(.*?)</b>', r'\g<1>', escaped)  # 临时移除标签
        converted = re.sub(r'<i>(.*?)</i>', r'\g<1>', converted)
        converted = re.sub(r'<a href="(.*?)">(.*?)</a>', 
                         lambda m: f'[{escape_markdown(m.group(2), version=2)}]({escape_markdown(m.group(1), version=2)})', 
                         converted)

        
        if entities:
            converted = MessageFormatter._apply_entities(converted, entities)

        
        final_escaped = converted.translate(
            str.maketrans({char: f'\\{char}' for char in MARKDOWN_CHARS})
        )

        return final_escaped

    @staticmethod
    def _apply_entities(text, entities):
        formatted = []
        last_pos = 0
        for entity in sorted(entities, key=lambda x: x.offset):
            
            formatted.append(text[last_pos:entity.offset])
            
            segment = text[entity.offset : entity.offset+entity.length]
            
            if entity.type == "bold":
                formatted.append(f"*{segment}*")
            elif entity.type == "italic":
                formatted.append(f"_{segment}_")
            elif entity.type == "code":
                formatted.append(f"`{segment}`")
            elif entity.type == "pre":
                formatted.append(f"```{segment}```")
            elif entity.type == "underline":
                formatted.append(f"__{segment}__")
            elif entity.type == "strikethrough":
                formatted.append(f"~{segment}~")
            elif entity.type == "spoiler":
                formatted.append(f"||{segment}||")
            elif entity.type == "text_link":
                # URL单独转义
                escaped_url = escape_markdown(entity.url, version=2)
                formatted.append(f"[{segment}]({escaped_url})")
            else:
                formatted.append(segment)
            
            last_pos = entity.offset + entity.length
        
        formatted.append(text[last_pos:])
        return "".join(formatted)
    
    @staticmethod
    def add_signature(content, signature, max_length):
        # 签名单独转义
        MARKDOWN_CHARS = r'_*[]()~`>#+-=|{}.!'
        signature_escaped = signature.translate(
            str.maketrans({char: f'\\{char}' for char in MARKDOWN_CHARS})
        )
    
        combined = f"{content}\n{signature_escaped}"
    
        if len(combined.encode('utf-8')) > max_length:
            available = max_length - len(signature_escaped.encode('utf-8')) - 4  # 最后留出...的字节数
            trimmed = content.encode('utf-8')[:available].decode('utf-8', 'ignore').rstrip()
            return f"{trimmed}...{signature_escaped}"
        return combined