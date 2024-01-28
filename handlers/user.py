import datetime
import random

import psycopg2
import telebot

from funcs.datetime_funcs import get_welcome
from funcs.db import get_books_from_db, save_data
from init_bot import bot


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = f"{get_welcome()}! Я книжный бот))\n\n" \
           f"Список команд:\n" \
           f"/get_book - получить книгу на вечер\n" \
           f"/get_my_id - получить мой id\n" \
           f"/get_date - получить сегодняшнюю дату"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["get_book"])
def get_book(message: telebot.types.Message):
    books = get_books_from_db()
    # with open("book.txt", "r", encoding="utf-8") as file: # Тут
    #     books = file.read().split("\n") # Тут
    book = random.choice(books)
    bot.send_message(message.chat.id, text=f'Сегодня вечером стоит почитать "{book[1]}", автор: "{book[2]}"', parse_mode="MarkdownV2")


@bot.message_handler(commands=["get_my_id"])
def get_my_id(message: telebot.types.Message):
    text = f"Мой id: {message.chat.id}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["get_date"])
def get_date(message: telebot.types.Message):
    current_date = datetime.datetime.now()
    text = f"Текущая дата: {current_date.date()}"
    bot.send_message(message.chat.id, text)


@bot.message_handler()
def get_date(message: telebot.types.Message):
    data_text = message.text.split('||')

    if len(data_text) == 1:
        bot.send_message(message.chat.id, "Не было ||")

    elif len(data_text) == 2:
        name = data_text[0]
        author = data_text[1]
        bot.send_message(message.chat.id, f"Название книги: {name}, Автор: {author}")
        save_data(name=name, author=author)
        bot.send_message(message.chat.id, "Данные вставлены")

    else:
        bot.send_message(message.chat.id, "Слишком много ||")

