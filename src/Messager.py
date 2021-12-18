from telegram.bot import Bot
from telegram import ParseMode


class Messager():
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id=chat_id,
                              text=message,
                              parse_mode=ParseMode.MARKDOWN_V2)

    def send_file(self, chat_id, document):
        self.bot.send_document(chat_id=chat_id,
                               document=document)
