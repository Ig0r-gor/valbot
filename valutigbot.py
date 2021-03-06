# ValutigBot
import telebot
from config import money, TOKEN, moneykey
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def botstart(message: telebot.types.Message):
    text = 'Приветствую! Это бот для пересчета валют по актуальному курсу. Для начала работы введите команду боту в следующем формате: \n \
<имя валюты для перевода>  <в какую валюту перевести> \
<количество переводимой валюты> \n Список доступных валют: /money \nПодсказка: /help '
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def bothelp(message: telebot.types.Message):
    text = 'Формат запроса боту: \n \
<имя валюты для перевода>  <в какую валюту перевести> \
<количество переводимой валюты> \n Например: доллар рубль 10 \nСписок доступных валют: /money'
    bot.reply_to(message, text)

@bot.message_handler(commands=['money'])
def botmoney(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in money.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def botconvert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Ошибка с количеством параметров')

        base, quote, amount = values
        for key in moneykey:
            if base in moneykey[key]:
                base = key
            elif quote in moneykey[key]:
                quote = key
        total_base = MoneyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Возникли проблемы с обработкой\n{e}')
    else:
        text = f'Цена {amount} {base} составляет {round(total_base, 2)} {quote}'
        bot.send_message(message.chat.id, text)
        
# bot.polling(none_stop=True)
bot.polling()
