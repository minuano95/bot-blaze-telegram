import telebot
from functions import main_request, results

# Creating bot 
TOKEN = '5429855911:AAHKI_y_L2dy7pyyapj2dM0oB6eNeSHwPIU'
bot = telebot.TeleBot(TOKEN, parse_mode=None)



@bot.message_handler(commands=['resultado'])
def send_stats(message):
    a = results()
    string = f'''Wins: {a['wins']} \nErros: {a['losses']} \nPrimeira tentativa: {a['prim_tent']} \nPrimeira gale: {a['prim_gale']} \nSegunda gale: {a['seg_gale']} \nBranco: {a['white']} \nPreto: {a['black']} \nVermelho: {a['red']} \nWinrate: {a['porcentagem']}'''
    while True:
        try:
            bot.reply_to(message, text=string)
            break
        except Exception as e:
            print('Erro:', e)

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message('-1001772338760', '\U0001f4c8 \U0001f4c8 Ligando o bot \U0001f4c8 \U0001f4c8')

    main_request(bot)

bot.infinity_polling()
 