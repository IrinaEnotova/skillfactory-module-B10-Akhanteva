import telebot
from config import *
from extensions import *

bot = telebot.TeleBot(TOKEN)

# тест бота
# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'hello')

# обработка комманд /start и /help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Приветствую! \nДанный бот поможет Вам с переводом денежных валют. \n \
\nЧтобы начать работу, введите сообщение в следующем формате: \
\n<Название валюты> \
<В какую валюту перевести> \
<Количество переводимой валюты> \n \
\nЧтобы увидеть список доступных валют, введите /values'
    bot.reply_to(message, text)

# обработчик с доступными валютами
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

# обработчик перевода
@bot.message_handler(content_types=['text',])
def convertMoney(message: telebot.types.Message):
    values = message.text.split(' ')
    if len(values) > 3:
        raise ConversionException('Введено более трех входных параметров! Попробуйте еще раз!')

    target, base, amount = values
    total_base = ExchangeMaker.convertMoney(target, base, amount)

    text = f'Цена {amount} {target} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()