import telebot
import time

import requests
from bs4 import BeautifulSoup

import threading

#확인
msgbackup = ""
def startcheck():
    global msgbackup
    source = requests.get("http://ncov.mohw.go.kr/index_main.jsp").text
    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("a.num")
    
    index = 0
    for key in hotKeys:
        index += 1
        if index == 1:
            msg = "코로나19(혹은 신종코로나바이러스, 우한폐렴)의 확진자 정보입니다.\n확진:" + key.text
        if index == 2:
            msg = msg + "\n퇴원: " + key.text      
        if index == 3:
            msg = msg + "\n사망: " + key.text
        
            if msgbackup == msg:
                temp = ""
            else:
                url = "https://api.telegram.org/bot1090552511:AAFeEQs9ApNxaZRYFOoMA1JjcA5jJS3yRFA/sendMessage?chat_id=-1001498453101&text=" + msg
                r = requests.post(url)
                msgbackup = msg
    timer = threading.Timer(3600, startcheck)
    timer.start()

#타이머시작
startcheck()

#챗봇
bot_token = '1090552511:AAFeEQs9ApNxaZRYFOoMA1JjcA5jJS3yRFA'

bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['crona'])
def send_welcome(message):

    source = requests.get("http://ncov.mohw.go.kr/index_main.jsp").text
    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("a.num")
    
    index = 0
    for key in hotKeys:
        index += 1
        if index == 1:
            msg = "코로나19(혹은 신종코로나바이러스, 우한폐렴)의 확진자 정보입니다.\n확진:" + key.text
        if index == 2:
            msg = msg + "\n퇴원: " + key.text      
        if index == 3:
            msg = msg + "\n사망: " + key.text

        if index >= 3:
            bot.reply_to(message,msg)
            break


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,'/crona - 현재 코로나19 확진자의 목록을 보여줍니다. (질병관리본부 홈페이지에 등재된 내용 기준으로 제공되며, 정확히 확인되지 않은 환자의 경우 표시되지 않습니다.)')

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
    