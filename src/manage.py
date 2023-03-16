import telebot
import dotenv
import requests
import random
import os
import sys
import openai
import logging

from Proxy_List_Scrapper import Scrapper

scrapper = Scrapper(category='NEW', print_err_trace=False)
data = scrapper.getProxies()

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, '../data')
env_path = os.path.join(dir_path, '../.env')

dotenv.load_dotenv(env_path)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] %(message)s')

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Telebot:
    def __init__(self):
        self.token = os.getenv('TOKEN')
        self.openai = openai
        self.openai.api_key = os.getenv("OPENAI_API_KEY")
        self.bot = telebot.TeleBot(self.token)

    def run(self):
        logger.debug('Starting telebot')

        if not self.token:
            logger.debug('No token found. Quit')
            exit(0)

        self.keyboard1 = telebot.types.ReplyKeyboardMarkup()
        self.keyboard1.row('Привет', 'Пока', 'Запись', 'Общаться с ChatGPT')

        self.keyboard2 = telebot.types.ReplyKeyboardMarkup()
        self.keyboard2.row('Сегодня', 'Завтра')
        self.keyboard2.row('Послезавтра', 'Никогда')

        bot = self.bot

        @bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id,
                                  'Привет, ты написал мне /start или пришли фотку или набери любой текст общения',
                                  reply_markup=self.keyboard1)

        @bot.message_handler(content_types=['text'])
        def send_text(message):
            logger.debug(f'Incoming: {message}')

            if message.text.lower() == 'привет':
                self.bot.send_sticker(message.chat.id,
                                      'CAACAgIAAxkBAAN7YFxY3QNyojjn-WRgveU0geWBtG8AAgYNAALXhRoOChznHH7hG6geBA')
            elif message.text.lower() == 'пока':
                self.bot.send_sticker(message.chat.id,
                                      'CAACAgIAAxkBAAMIYFxSa2vkEfTHjeUuo7jXwALV5iwAAgUNAALXhRoOzb8Lm4UPeF4eBA')
            elif message.text.lower() == 'запись':
                self.bot.send_message(message.chat.id, 'Выбери дату', reply_markup=self.keyboard2)
            elif message.text.lower() in ['сегодня', 'завтра', 'послезавтра', 'никогда']:
                self.bot.send_message(message.chat.id, 'Ты записан на %s, чуви! (=' % message.text.lower(),
                                      reply_markup=telebot.types.ReplyKeyboardRemove())
            elif 'прочитать' in message.text.lower():
                text = message.text.lower()
                text = text.replace('прочитать', '')

                self.bot.send_audio(message.chat.id, audio=self.get_audio(text), caption='', title='')
            else:
                try:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=message.text,
                        temperature=0,
                        max_tokens=1000,
                    )

                    self.bot.send_message(message.chat.id, response['choices'][0]['text'],
                                          reply_markup=telebot.types.ReplyKeyboardRemove())
                except BaseException as e:
                    self.bot.send_message(message.chat.id, 'Try again later. Im busy.',
                                          reply_markup=telebot.types.ReplyKeyboardRemove())

        @bot.message_handler(content_types=['sticker'])
        def sticker_id(message):
            logger.debug(f'Incoming sticker: {message}')

        @bot.message_handler(content_types=['photo'])
        def send_photo(message):
            logger.debug(f'Incoming photo: {message}')

            self.bot.send_photo(message.chat.id, photo=open(os.path.join(data_path, 'photo.jpg'), 'rb'),
                                reply_markup=telebot.types.ReplyKeyboardRemove())

        self.bot.infinity_polling()

    def get_random_proxy(self):
        rand = random.choice(data.proxies)

        return {
            'http': 'http://' + rand.ip + ':' + rand.port,
            'https': 'http://' + rand.ip + ':' + rand.port,
        }

    def get_audio(self, text: str):
        try:
            r = requests.get(
                'http://nextup.com/ivona/php/nextup-polly/CreateSpeech/CreateSpeechGet3.php?voice=Maxim&language=ru'
                '-RU&text=' + text,
                proxies=self.get_random_proxy(), timeout=10)

            if r.status_code != 200:
                return self.get_audio(text)

            return r.text
        except BaseException as e:
            return self.get_audio(text)


if __name__ == "__main__":
    Telebot().run()
