import telebot
from config import exchanges, TOKEN
from extensions import Converter, APIException
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате:\n<имя валюты, цену, которую нужно узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество переводимой валюты>\nУвидить список ввсех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in exchanges.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()