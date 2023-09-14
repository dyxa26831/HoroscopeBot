import telebot  # Библиотека для создания сайта
from telebot import types  # Библиотека для создания кнопок
from bs4 import BeautifulSoup  # Библиотека для парсинга сайта
import requests  # Библиотека для определения url сайта

bot = telebot.TeleBot(
    "6321806515:AAGlx36W6DDeUH4jXO1GElm5XME-6q57_70"
)  # Инициализация токена бота


global orgs
orgs = {
    "Телец": "taurus",
    "Весы": "libra",
    "Стрелец": "sagittarius",
    "Козерог": "capricorn",
    "Лев": "leo",
    "Скорпион": "scorpio",
    "Близнецы": "gemini",
    "Рыбы": "pisces",
    "Рак": "cancer",
    "Водолей": "aquarius",
    "Дева": "virgo",
    "Овен": "aries",
}  # Словарь для добавление кнопок и определения сайта


def button():
    global markup
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # Инициализация кнопки
    global a
    a = []
    for key in orgs:  # Добавление текста в кнопку
        a.append(types.KeyboardButton(key))
    markup.add(*a, row_width=2)


@bot.message_handler(commands=["start"])
def start(message):
    button()
    bot.send_message(
        message.chat.id,
        "Давай узнаем твой гороскоп на сегодня, кто ты по знаку зодиака?",
        reply_markup=markup,
    )  # Отправка сообщения


@bot.message_handler(content_types=["text"])
def sendHoroscope(message):
    button()
    if message.text in orgs:  # Защита от неправильного ввода
        horoscope = orgs[message.text]
        url = f"https://horo.mail.ru/prediction/{horoscope}/today/"  # Инициализация сайта для парсинга
        response = requests.get(url)  # Получения сайта
        bs = BeautifulSoup(response.text, "lxml")  # Получение всего контента на сайте
        temp = bs.find(
            "div", "article__item article__item_alignment_left article__item_html"
        )  # Получения нужного контента на сайте
        bot.send_message(message.chat.id, text=temp.text)  # Отправка сообщения
    else:  # Защита от неправильного ввода
        bot.send_message(
            message.chat.id,
            "Вы указали не гороскоп, нажмите на одну из кнопок",
            reply_markup=markup,
        )


bot.polling(none_stop=True)  # Функция для начала работы бота
