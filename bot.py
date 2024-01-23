import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет, я бот для конвертации валют. \n' \
    'Список доступных валют можно посмотреть здесь /values \n' \
    ' Чтобы начать работу введите команду в следующем формате:\n' \
    '<Наименование валюты>\
    <В какую валюту перевести> \
    <Колличество переводной валюты> \n' \
    'Пример: доллар евро 1'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "/help - все запросы бота  \n" \
           "/start - начало работы с ботом \n" \
           "/values - список доступных валют \n"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
     try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException(f"Некорректное колличество параметров. Переменных должно быть 3")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
     except ConvertionException as e:
         bot.reply_to(message, f"Ошибка пользователя\n{e}")
     except Exception as e:
         bot.replay_to(message, f'Не удаловь обработать команду\n{e}')
     else:
         total_base = float(total_base)
         amount = int(amount)
         result = total_base*amount
         text = f'Конвертируем \n {amount} {quote} = {result} {base} '
         bot.send_message(message.chat.id, text)


bot.polling()
