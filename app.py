import requests
import telebot
import json

TOKEN = '5843177964:AAHVUYtZX00lX_Bumu8IXufuyZ9WNL7buX0'

bot = telebot.TeleBot(TOKEN)

keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB'
}

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
    target, base, amount = message.text.split(' ')
    request = requests.get(f'https://v6.exchangerate-api.com/v6/bc707e8c44ea94453d11304a/pair/{keys[target]}/{keys[base]}/{amount}')
    total_base = json.loads(request.content)['conversion_result']
    text = f'Цена {amount} {target} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()