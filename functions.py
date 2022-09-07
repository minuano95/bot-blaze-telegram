import csv
import json
import requests
import logging
import telebot
import sqlite3
from time import sleep
from datetime import datetime
# from notifypy import Notify
from pushbullet import Pushbullet


def results():
    conn = sqlite3.connect('count.sql')
    cursor = conn.cursor()
    wins = cursor.execute('SELECT SUM(vit) FROM Registros').fetchone()[0]
    losses = cursor.execute('SELECT SUM(loss) FROM Registros').fetchone()[0]
    prim_tent = cursor.execute('SELECT SUM(primTent) FROM Registros').fetchone()[0]
    prim_gale = cursor.execute('SELECT SUM(primGale) FROM Registros').fetchone()[0]
    seg_gale = cursor.execute('SELECT SUM(segGale) FROM Registros').fetchone()[0]
    white = cursor.execute('SELECT SUM(branco) FROM Registros').fetchone()[0]
    black = cursor.execute('SELECT SUM(preto) FROM Registros').fetchone()[0]
    red = cursor.execute('SELECT SUM(verm) FROM Registros').fetchone()[0]
    porcentagem = round((wins - losses) / wins * 100, 2)

    conn.close()

    return {'wins': wins, 'losses': losses, 'prim_tent': prim_tent, 'prim_gale': prim_gale, 'seg_gale': seg_gale, 'white': white, 'black': black,
            'red': red, 'porcentagem': porcentagem}


def count(time, win:int, loss:int, prim_tent:int, prim_gale:int, seg_gale:int, white:int, red:int, black:int):
    conn = sqlite3.connect('count.sql')
    cursor = conn.cursor()
    string = f'''INSERT INTO Registros (time, vit, loss, primTent, primGale, segGale, branco, preto, verm)
                VALUES ("{time}", {win}, {loss}, {prim_tent}, {prim_gale}, {seg_gale}, {white}, {black}, {red})'''
    cursor.execute(string)
    conn.commit()
    conn.close()


# desktop notification settings
def desktop_notification(message):
    notification = Notify()
    notification.title = 'Blaze'
    notification.message = message
    notification.icon = r'C:\Users\User\Downloads\python projects\blaze_bot\blaze-icon.png'
    notification.send()

# phone notifications
def bot_msg(title, message):
    pb = Pushbullet('o.9mKgLukDRUkGzzaWN9DIC0aqy3ixNHKj')
    pb.push_note(title, message)

# basic api request
def request():
    try:
        while True:
            req = requests.get('https://blaze.com/api/roulette_games/recent', headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            if req.status_code == 200:
                break
        output = json.loads(req.text)
        list_past_results = [{'cor': row['color'], 'numero': row['roll']} for row in output]
        return list_past_results
    except: pass

# main function
def main_request(bot_telegram):
    while True:
        
        list_past_results = request()
        if list_past_results[0]['cor'] == list_past_results[1]['cor']: # and list_past_results[1]['cor'] == list_past_results[2]['cor']:
            return apostar(list_past_results, bot_telegram)

        print('Request feito:', datetime.now())
        sleep(10)

# 
def apostar(lista, bot_telegram):

    white = 0
    black = 0
    red = 0

    # Checkin the color you're gonna bet
    if lista[0]['cor'] == 2:
        # desktop_notification('Apostar no vermelho e no branco')
        # bot_msg('Blaze', 'Apostar no vermelho e no branco.')
        while True:
            try:
                bot_telegram.send_message('-1001772338760', '\U0001f534 \U0001f534 \U0001f534 \U0001f534 \nApostar no vermelho e cobrir o branco. \n\u26aa \u26aa \u26aa \u26aa')
                break
            except Exception as e:
                print('Erro:', e)

    if lista[0]['cor'] == 1:
        # desktop_notification('Apostar no preto e no branco')       
        # bot_msg('Blaze', 'Apostar no preto e no branco.')
        while True:
            try:
                bot_telegram.send_message('-1001772338760', '\u26ab \u26ab \u26ab \u26ab \nApostar no preto e cobrir o branco. \n\u26aa \u26aa \u26aa \u26aa')
                break
            except Exception as e:
                print('Erro:', e)

    win = 0
    loss = 0
    prim_tent = 0
    prim_gale = 0
    seg_gale = 0


    # checking if you won
    while True:
        new_list = request()
        if lista != new_list:
            list = new_list
            break

    if list[0]['cor'] != list[1]['cor']:
        prim_tent += 1
        # desktop_notification('WIIINNNN')
        # bot_msg('Blaze','WIIINNN')
        while True:
            try:
                bot_telegram.send_message('-1001772338760', '\u2705 \u2705 \u2705 \u2705 \nWIIINNN\n\u2705 \u2705 \u2705 \u2705')
                if list[0]['cor'] == 0: white += 1
                if list[0]['cor'] == 1: red += 1
                else: black +=1
                break
            except Exception as e:
                print('Erro:', e)
        win += 1
        print('WIINN')
    else:
        # desktop_notification('Vamos para a primeira gale. \nDobre a aposta e repita a cor')
        # bot_msg('Blaze', 'Vamos para a primeira gale. \nDobre a aposta e repita a cor')
        while True:
            try:
                bot_telegram.send_message('-1001772338760', '\u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \nVamos para a primeira gale. \nDobre a aposta e repita a cor \n\u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f')
                break
            except Exception as e:
                print('Erro:', e)
        print('Primeira gale')

        sleep(1)
        while True:
            new_list = request()
            if list != new_list:
                list = new_list
                break

        if list[0]['cor'] != list[1]['cor']:
            prim_gale += 1
            # desktop_notification('WIIINNNN')
            # bot_msg('Blaze', 'WIIINNN')
            while True:
                try:
                    bot_telegram.send_message('-1001772338760', '\u2705 \u2705 \u2705 \u2705 \nWIIINNN \n\u2705 \u2705 \u2705 \u2705')
                    if list[0]['cor'] == 0: white += 1
                    if list[0]['cor'] == 1: red += 1
                    else: black += 1
                    break
                except Exception as e:
                    print('Erro:', e)
            win += 1
            print('WINN')
            
        else:
            sleep(1)
            # desktop_notification('Vamos para a segunda gale. \nDobre a aposta e repita a cor.')
            # bot_msg('Blaze', 'Vamos para a segunda gale. \nDobre a aposta e repita a cor.')
            while True:
                try:
                    bot_telegram.send_message('-1001772338760', '\u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \nVamos para a segunda gale. \nDobre a aposta e repita a cor. \n\u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f \u26a0\ufe0f')
                    break
                except Exception as e:
                    print('Erro:', e)
            print('Segunda gale')

            while True:
                new_list = request()
                if list != new_list:
                    list = new_list
                    break

            if list[0]['cor'] != list[1]['cor']:
                # desktop_notification('WIIINNNN')
                # bot_msg('Blaze', 'WIIINNN')
                while True:
                    try:
                        bot_telegram.send_message('-1001772338760', '\u2705 \u2705 \u2705 \u2705 \nWIIINNN \n\u2705 \u2705 \u2705 \u2705')
                        if list[0]['cor'] == 0: white += 1
                        if list[0]['cor'] == 1: red += 1
                        else: black += 1
                        break
                    except Exception as e:
                        print('Erro:', e)
                seg_gale += 1
                win += 1
                print('WINN')
            else:
                # desktop_notification('Loss')
                # bot_msg('Blaze', 'Loss')
                while True:
                    try:
                        bot_telegram.send_message('-1001772338760', '\u274c \u274c \u274c \u274c \nLoss \n\u274c \u274c \u274c \u274c')
                        break
                    except Exception as e:
                        print('Erro:', e)
                loss += 1
                print('loss')

    sleep(2)
    time = datetime.now()
    count(time, win, loss, prim_tent, prim_gale, seg_gale, white, red, black)

    while True:
        new_list = request()
        if list != new_list:
            main_request(bot_telegram)


# Cor 2 = Preto | Cor 1 = Vermelho | Cor 0 - Branco