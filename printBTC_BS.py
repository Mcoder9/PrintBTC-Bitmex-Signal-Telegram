import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime
from time import sleep


class PrintbtcBitmexSignal():
    PrintbtcBSbot = 'https://api.telegram.org/bot5410478068:AAGBOIfRr53c-upmDyJpLbjVTAokYpPVSi0'
    PrintbtcBS_chatid = '-1001328221163'
    trackTime = []
    scheduleTiming = ['00','14','16']


    def getDayTime(self):
        worldtimeAPI = 'http://worldtimeapi.org/api/timezone/America/New_York'
        while True:
            resp = requests.get(worldtimeAPI)
            if resp.status_code == 200:
                respinfo = resp.json()
                unixTime = int(respinfo['unixtime'])
                dateTime = respinfo['datetime']
                day = datetime.utcfromtimestamp(unixTime).strftime('%a')
                time = dateTime.split('T')[1].split(':')[0]
                return day,time

    def getTicker(self):
        tickerURL = 'http://tslatrading.com/crypto/index.php'
        resp = requests.get(tickerURL)
        soup = BeautifulSoup(resp.content, 'lxml')
        tickersURLs = [tickerURL+x.get('href') for x in soup.select('td>a[target="_blank"]',limit=300)] # get ticker href and make full URL by adding parent URL part
        return tickersURLs

    def getSignal(self):
        tickersURLs = self.getTicker()
        while True:
            randomTicker = random.choice(tickersURLs)
            resp = requests.get(randomTicker)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'lxml')
                try:
                    getText = soup.find('pre').getText()
                    signalText = '\n'.join([x for x in getText.splitlines()[:-1]])
                except: signalText = None
                if signalText:
                    return signalText

    def sendToPrintbtcBS(self,signalText):
        parameters = {"chat_id" : self.PrintbtcBS_chatid,"text" : signalText,}
        requests.get(self.PrintbtcBSbot + "/sendMessage", data = parameters)


    def run(self):
        day,time = self.getDayTime()
        print(self.trackTime)
        print(day,time)
        if not time in self.trackTime:
            if time in self.scheduleTiming:
                signalText = self.getSignal()
                self.sendToPrintbtcBS(signalText)

                self.trackTime.append(time)
                print(f'Sent signal at for {self.trackTime}')
            if len(self.trackTime) == 3:
                self.trackTime = []

bot = PrintbtcBitmexSignal()
while True:
    bot.run()
    sleep(3)
