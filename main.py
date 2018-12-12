import ast
import telebot
from telebot import types
from choice import choice_main, location_search
import re

from telebot import apihelper
apihelper.proxy = {'https': 'https://WZtV0U:2jDt7A@196.19.9.73:8000'}


sm = u'\U0001F603'

def forgetEverything(bot):
    bot.pay = False
    bot.lat = None
    bot.lon = None
    bot.r = 50000
    bot.waitingForNumber = False
    bot.finished = False


class MyBot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.pay = False
        self.lat = None
        self.lon = None
        self.r = 50000
        self.waitingForNumber = False
        self.finished = False

def tryToFinish(message):
    if bot.finished:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
        keyboard.add(types.KeyboardButton('/Начать сначала'))
        bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


# bot = telebot.TeleBot('780629738:AAFfVHwMAc0fILjtEK1pwiQ-dZFG3yqMFZM')
bot = MyBot('780629738:AAFfVHwMAc0fILjtEK1pwiQ-dZFG3yqMFZM')

@bot.message_handler(commands=['start', 'Начать'])
def handle_start(message):
    forgetEverything(bot)
    bot.send_message(message.chat.id, "Привет! Я помогу найти вам событие по вашим интересам. "
                                      "Вы желаете посмотреть все события или только события, "
                                      "расположенные рядом с вами?")


@bot.message_handler(regexp='\D*прив\D*|\D*Прив\D*|\D*здрав\D*|\D*Здрав\D*')
def handle_start(message):
    forgetEverything(bot)
    bot.send_message(message.chat.id, "Привет! Я помогу найти вам событие по вашим интересам. "
                                        "Вы желаете посмотреть все события или только события, "
                                        "расположенные рядом с вами?")


@bot.message_handler(regexp='\D*рядом\D*|\D*Рядом\D*')
def request_location(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Мне необходимо ваше местоположение", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    bot.send_message(message.chat.id, 'Подождите...Ищем события... ')
    try:
        ast.literal_eval(str(message.location))["latitude"]
        loc = True
    except:
        loc = False
    if loc:
        bot.lat = (ast.literal_eval(str(message.location))["latitude"])
        bot.lon = (ast.literal_eval(str(message.location))["longitude"])
    answer = location_search(bot.lat, bot.lon, bot.r)
    if answer is not None:
        for i in range(len(answer)):
            message1 = "#" + str(i + 1) + "\n" + answer[i]["title"] + "\n" + answer[i][
                "content"] + "\n" + "Начало события" + \
                       answer[i][
                           "start"] + "\n" + "Конец события" + answer[i]["end"] + "\n" + answer[i]["url"]
        bot.finished = True
    else:
        message1 = 'По Вашему запросу событий в радиусе %i не найдено. Вы можете ввести новый радиус или начать сначала.' % (bot.r,)
        bot.waitingForNumber = True
    bot.send_message(message.chat.id, message1)
    tryToFinish(message)


re_int = re.compile('\d+')
@bot.message_handler(regexp='\D*\d+\D*')
def handle_start(message):
    if not bot.waitingForNumber:
        return
    bot.waitingForNumber = False
    new_radius = int(re_int.search(message.text).group())
    print(new_radius)
    bot.r = new_radius
    location(message)

    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    # keyboard.add(types.KeyboardButton('/Начать сначала'))
    # bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*все\D*|\D*Все\D*')
def handle_start(message):
    bot.send_message(message.chat.id, "Вы предпочитаете платное или бесплатное событие?")


@bot.message_handler(regexp='\D*бесплатн\D*|\D*Бесплатн\D*')
def handle_start(message):
    message.text = 'Бесплатно'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*платн\D*|\D*Платн\D*')
def handle_start(message):
    bot.send_message(message.chat.id, "Какую категорию событий вы ищите? Это могут быть квесты, концерты, "
                                      "стендап шоу, фестивали, образовательные программы, выставки, ярмаки, "
                                      "развлечения для детей, постоянные выставки.")


@bot.message_handler(regexp='\D*квест\D*|\D*Квест\D*')
def handle_start(message):
    message.text = 'Продолжительность квеста'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*концерт\D*|\D*Концерт\D*')
def handle_start(message):
    message.text = 'Концерты'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*стендап\D*|\D*Стендап\D*|\D*стэндап\D*|\D*Стэндап\D*')
def handle_start(message):
    message.text = 'Стендап'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*фестивал\D*|\D*Фестивал\D*')
def handle_start(message):
    message.text = 'Фестивали'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*ярмарк\D*|\D*Ярмарк\D*')
def handle_start(message):
    message.text = 'Ярмарки'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*постоян\D*|\D*Постоян\D*')
def handle_start(message):
    message.text = 'Постоянные'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*выставк\D*|\D*Выставк\D*')
def handle_start(message):
    message.text = 'Выставки'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*знани\D*|\D*Знани\D*|\D*лекци\D*|\D*Лекци\D*|\D*образован\D*|\D*Образован\D*')
def handle_start(message):
    message.text = 'Знания'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*дет\D*|\D*Дет\D*|\D*ребен\D*|\D*Ребен\D*|\D*ребён\D*|\D*Ребён\D*')
def handle_start(message):
    message.text = 'Дети'
    text = message.text
    bot.send_message(message.chat.id, 'Подождите...Ищем события...')
    dermo = choice_main(text)
    for i in range(len(dermo)):
        mes = "#" + str(i + 1) + "\n" + dermo[i]["title"] + "\n" + " " + dermo[i][
            "content"] + "\n" + "Смотреть больше:" + dermo[i]["url"]
        bot.send_message(message.chat.id, mes)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=1)
    keyboard.add(types.KeyboardButton('/Начать сначала'))
    bot.send_message(message.chat.id, sm + 'Мы всегда рады помочь Вам!', reply_markup=keyboard)


@bot.message_handler(regexp='\D*')
def handle_start(message):
    bot.send_message(message.chat.id, "Я не понимаю вас.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
