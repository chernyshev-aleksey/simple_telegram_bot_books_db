import datetime
import random

import psycopg2
import telebot
from telebot.custom_filters import StateFilter
from telebot.handler_backends import StatesGroup, State

from funcs.datetime_funcs import get_welcome
from funcs.db import get_books_from_db, save_data, save_book, add_category_to_book, get_all_categories
from init_bot import bot
from keyboards import gen_category_keyboard, get_category_kb


class MyStates(StatesGroup):
    # Just name variables differently
    wait_title_book = State()
    wait_author = State()
    wait_category = State()
    wait_inline_category = State()


def zip_categories(_categories):
    result = {}

    for _category in _categories:
        if _category[0] in result:
            result[_category[0]]['category'].append(_category[1])
        else:
            result[_category[0]] = {
                'category': [_category[1]],
                'name': _category[2],
                'title_book': _category[0]
            }

    r = []

    for key in result.keys():
        r.append(result[key])

    return r


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = f"{get_welcome()}! Я книжный бот))\n\n" \
           f"Список команд:\n" \
           f"/get_book - получить книгу на вечер\n" \
           f"/get_my_id - получить мой id\n" \
           f"/get_date - получить сегодняшнюю дату\n" \
           f"/add_book - добавить произведение"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["get_book"])
def get_book(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        text="Выберете тип поиска",
        reply_markup=gen_category_keyboard()
    )


@bot.callback_query_handler(func=lambda call: True)
def first_inline(call: telebot.types.CallbackQuery):
    if call.data == "category":
        categories = get_all_categories()

        if len(categories) > 5:
            categories = categories[:5]

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

        bot.send_message(
            text="Выберите жанр книги, чтобы было проще найти для тебя лучшую книгу",
            reply_markup=get_category_kb(categories),
            chat_id=call.message.chat.id,
        )

    elif call.data == "random":
        books = get_books_from_db()
        book = random.choice(books)

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

        bot.send_message(call.message.chat.id, text=f'Сегодня вечером стоит почитать "{book[0]}", автор: "{book[2]}", жанр: "{book[1]}"',
                         parse_mode="MarkdownV2")

    else:
        print(call.data)
        books = get_books_from_db(call.data)

        books = zip_categories(books)

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

        book = random.choice(books)

        bot.send_message(call.message.chat.id,
                         text=f'Сегодня вечером стоит почитать {book["title_book"]}, автор: {book["name"]}, жанры: {", ".join(book["category"])}',
                         parse_mode="MarkdownV2")


# @bot.message_handler(commands=["get_book"])
# def get_book(message: telebot.types.Message):
#     books = get_books_from_db()
#     # with open("book.txt", "r", encoding="utf-8") as file: # Тут
#     #     books = file.read().split("\n") # Тут
#     book = random.choice(books)
#     bot.send_message(message.chat.id, text=f'Сегодня вечером стоит почитать "{book[1]}", автор: "{book[2]}"',
#                      parse_mode="MarkdownV2")


@bot.message_handler(commands=["get_my_id"])
def get_my_id(message: telebot.types.Message):
    text = f"Мой id: {message.chat.id}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["get_date"])
def get_date(message: telebot.types.Message):
    current_date = datetime.datetime.now()
    text = f"Текущая дата: {current_date.date()}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["add_book"])
def command_add_book(message: telebot.types.Message):
    bot.send_message(message.chat.id, text="Супер! Напиши, пожалуйста, название книги")
    bot.set_state(message.from_user.id, MyStates.wait_title_book, message.chat.id)


@bot.message_handler(state=MyStates.wait_title_book)
def set_title(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['title'] = message.text

    bot.send_message(message.chat.id, text="Супер! Напиши, пожалуйста, автора книги")
    bot.set_state(message.from_user.id, MyStates.wait_author, message.chat.id)


@bot.message_handler(state=MyStates.wait_author)
def set_title(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['author'] = message.text

    bot.send_message(message.chat.id, text="Супер! Напиши, пожалуйста, жанр книги")
    bot.set_state(message.from_user.id, MyStates.wait_category, message.chat.id)


@bot.message_handler(state=MyStates.wait_category, commands=["end"])
def set_title(message: telebot.types.Message):
    bot.delete_state(message.from_user.id, message.chat.id)

    text = f"{get_welcome()}! Я книжный бот))\n\n" \
           f"Список команд:\n" \
           f"/get_book - получить книгу на вечер\n" \
           f"/get_my_id - получить мой id\n" \
           f"/get_date - получить сегодняшнюю дату\n" \
           f"/add_book - добавить произведение"
    bot.send_message(message.chat.id, text)


@bot.message_handler(state=MyStates.wait_category)
def set_title(message: telebot.types.Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if 'second' in data:
            add_category_to_book(
                book_id=data['book_id'],
                category=message.text
            )
        else:
            book_id = save_book(
                title=data['title'],
                author=data['author'],
                category=message.text
            )
            data['book_id'] = book_id

        bot.send_message(message.chat.id, text="Супер! Напиши, пожалуйста, дополнительную категорию книги, нажми /end чтобы завершить ввод категорий")

        data['second'] = True


# @bot.message_handler()
# def add_gook(message: telebot.types.Message):
#     data_text = message.text.split(' || ')
#
#     if len(data_text) == 1:
#         bot.send_message(message.chat.id, "Не было ||")
#
#     elif len(data_text) == 2:
#         name = data_text[0]
#         author = data_text[1]
#         bot.send_message(message.chat.id, f"Название книги: {name}, Автор: {author}")
#         save_data(name=name, author=author)
#         bot.send_message(message.chat.id, "Данные вставлены")
#
#     else:
#         bot.send_message(message.chat.id, "Слишком много ||")

bot.add_custom_filter(StateFilter(bot))
