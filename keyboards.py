from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_category_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("По жанру", callback_data="category"),
                    InlineKeyboardButton("Случайную", callback_data="random"))
    return markup


def get_category_kb(categories):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for category in categories:
        markup.add(InlineKeyboardButton(text=category[1], callback_data=category[1]))

    return markup
