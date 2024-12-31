import datetime
from app.cfg.settings import settings

from app.utils.logger.logger import Logger

import telebot

from app.utils.result import Result, err, success

class TelegramLogger(Logger):
    def __init__(self, 
                 token: str = settings.TELEGRAM_API_TOKEN, 
                 chat_id: str = settings.TELEGRAM_CHAT_ID):
        self._bot = telebot.TeleBot(token)
        self._chat_id = chat_id


    def send_log(self, template: str) -> Result[None]:
        try:
            self._bot.send_message(self._chat_id, template, parse_mode="Markdown")
            return success()
        except:
            return err("Произошла ошибка")

    def info(self, message: str):
        template = f"""❗**INFO**❗\n
{message}\n
Date: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""
        
        sending = self.send_log(template)
        

    def error(self, message: str) -> str:
        template = f"""🚨 **ERROR** 🚨\n
{message}\n
Date: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""
        
        sending = self.send_log(template)
        
    def warning(self, message: str) -> str:
        template = f"""⚠️ **WARNING** ⚠️\n 
{message}\n
Date: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""
        
        sending = self.send_log(template)
        
    def fatal(self, message: str) -> str:
        template = f"""🆘 **FATAL** 🆘\n 
{message}\n
Date: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
"""
        
        sending = self.send_log(template)

logger: TelegramLogger = TelegramLogger()