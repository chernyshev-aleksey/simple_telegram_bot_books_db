from handlers import register_handlers
from init_bot import bot

if __name__ == "__main__":
    register_handlers()
    print("Бот запущен")
    bot.infinity_polling()
