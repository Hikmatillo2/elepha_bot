import settings
from elephaBot.service.database import *
from telebot import TeleBot
from telebot.types import Message

bot = TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    if check_user_exists(str(message.chat.id)):
        bot.send_message(
            message.chat.id,
            "Вы подписались на рассылку уведомлений от сервиса directorvzagorin.youtrack.cloud!"
        )

@bot.message_handler(content_types=['text'])
def text(message: Message):
    pass
