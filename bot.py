import telebot
from telebot.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Токен твоего бота от BotFather
BOT_TOKEN = "ТВОЙ_ТОКЕН_СЮДА"
WEB_APP_URL = "https://abc123.ngrok.io"  # Замени на свой ngrok URL

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    web_app = WebAppInfo(WEB_APP_URL)
    markup.add(InlineKeyboardButton(
        text="📚 Открыть приложение",
        web_app=web_app
    ))

    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "🎓 Добро пожаловать в геймифицированное приложение для изучения теории чисел!\n\n"
        "✨ Здесь тебя ждут:\n"
        "• 📖 Интерактивное обучение\n"
        "• 🎯 Режим экзамена\n"
        "• 🏆 Система достижений\n"
        "• 📊 Отслеживание прогресса\n\n"
        "Нажми кнопку ниже, чтобы начать! 👇",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    markup = InlineKeyboardMarkup()
    web_app = WebAppInfo(WEB_APP_URL)
    markup.add(InlineKeyboardButton(
        text="📚 Открыть приложение",
        web_app=web_app
    ))

    bot.send_message(
        message.chat.id,
        "Используй кнопку ниже для открытия приложения! 👇",
        reply_markup=markup
    )


if __name__ == "__main__":
    print("🚀 Бот запущен!")
    bot.polling()
