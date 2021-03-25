import telebot
import dotenv
import os
import requests
import random
from Proxy_List_Scrapper import Scrapper

scrapper = Scrapper(category='NEW', print_err_trace=False)
data = scrapper.getProxies()

if __name__ == "__main__":
    dotenv.load_dotenv()

    token = os.getenv('TOKEN')

    if not token:
        print('No token found. Quit')
        exit(0)

    bot = telebot.TeleBot(token)

    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('Привет', 'Пока', 'Запись', 'Прочитать текст')

    keyboard2 = telebot.types.ReplyKeyboardMarkup()
    keyboard2.row('Сегодня', 'Завтра')
    keyboard2.row('Послезавтра', 'Никогда')


    def get_random_proxy():
        rand = random.choice(data.proxies)
        test = rand

        return {
            'http': 'http://' + rand.ip + ':' + rand.port,
            'https': 'http://' + rand.ip + ':' + rand.port,
        }


    def get_audio(text):
        try:
            r = requests.get(
                'http://nextup.com/ivona/php/nextup-polly/CreateSpeech/CreateSpeechGet3.php?voice=Maxim&language=ru-RU&text=' + text,
                proxies=get_random_proxy(), timeout=10)

            if r.status_code != 200:
                return get_audio(text)

            return r.text
        except BaseException as e:
            return get_audio(text)


    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id,
                         'Привет, ты написал мне /start или пришли фотку или набери "прочитать <любой текст здесь>"',
                         reply_markup=keyboard1)


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
        elif 'прочитать' in message.text.lower():
            text = message.text.lower()
            text = text.replace('прочитать', '')

            bot.send_audio(message.chat.id, audio=get_audio(text), caption='', title='')


    @bot.message_handler(content_types=['sticker'])
    def sticker_id(message):
        print(message)


    @bot.message_handler(content_types=['photo'])
    def send_photo(message):
        print(message)
        bot.send_photo(message.chat.id, photo=open('./photo.jpg', 'rb'),
                       reply_markup=telebot.types.ReplyKeyboardRemove())


    bot.polling()
