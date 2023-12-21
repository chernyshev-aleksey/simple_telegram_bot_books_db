import telebot

from init_bot import bot


@bot.message_handler(func=lambda _: True)
def unknown_command(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Неизвестная команда")
