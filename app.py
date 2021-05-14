import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет. Это бот, который поможет узнать нынешний курс интересующей вас валюты.\n ' \
           'Формат записи данных: \n<имя валюты> <в какую валюту перевести> <количество переводимой' \
           ' валюты>\n Увидеть список всех доступных валют: /values\n Помощь с записью данных: /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы ответ был более корректный, требуется ввести комманду боту в следующем формате: ' \
           '\n<имя валюты, цену которой хотите узнать> пробел <имя валюты, в которой надо узнать ' \
           'цену первой валюты> пробел <количество первой валюты>\n(имя валюты писать словом,' \
           ' взятым из списка доступных валют, с маленькой буквы и никак иначе)\n' \
           'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = f'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите 3 параметра запроса или команду!')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} \n >>> {round(total_base, 3)}'
        bot.send_message(message.chat.id, text)


bot.polling()