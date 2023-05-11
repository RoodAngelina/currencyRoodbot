import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Введите запрос в следующем формате:\n <название валюты> \
<в какую валюту перевести> <сумма переводимой валюты>\nЧтобы посмотреть список \
доступных валют, введите команду /values.'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert_(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')

        if len(values_) != 3:
            raise ConvertionException('Должно быть три параметра.')

        quote, base, amount = values_
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}.')
    else:
        result = round(float(total_base) * float(amount), 2)
        text = f'Цена {amount} {quote} в {base} - {result}'
        bot.send_message(message.chat.id, text)

bot.polling()
