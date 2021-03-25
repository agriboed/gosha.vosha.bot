import telebot
import dotenv
import os

if __name__ == "__main__":
    dotenv.load_dotenv()

    token = os.getenv('TOKEN')

    if not token:
        print('No token found. Quit')
        exit(0)

    bot = telebot.TeleBot(token)

    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('Привет', 'Пока', 'Запись')

    keyboard2 = telebot.types.ReplyKeyboardMarkup()
    keyboard2.row('Сегодня', 'Завтра')
    keyboard2.row('Послезавтра', 'Никогда')


    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


    @bot.message_handler(content_types=['text'])
    def send_text(message):
        print(message)

        if message.text.lower() == 'привет':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAN7YFxY3QNyojjn-WRgveU0geWBtG8AAgYNAALXhRoOChznHH7hG6geBA')
        elif message.text.lower() == 'пока':
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAMIYFxSa2vkEfTHjeUuo7jXwALV5iwAAgUNAALXhRoOzb8Lm4UPeF4eBA')
        elif message.text.lower() == 'запись':
            bot.send_message(message.chat.id, 'Выбери дату', reply_markup=keyboard2)
        elif message.text.lower() in ['сегодня', 'завтра', 'послезавтра', 'никогда']:
            bot.send_message(message.chat.id, 'Ты записан на %s, чуви! (=' % message.text.lower(),
                             reply_markup=telebot.types.ReplyKeyboardRemove())


    @bot.message_handler(content_types=['sticker'])
    def sticker_id(message):
        print(message)


    bot.polling()
