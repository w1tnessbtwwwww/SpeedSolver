from app.cfg.settings import settings
import telebot

class TelegramLogger:
    def __init__(self):
        self.bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
    

    async def info(message: str) -> str:
        ...

    async def error(message: str) -> str:
        ...

    async def warning(message: str) -> str:
        ...
    
    async def fatal(message: str) -> str:
        ...
