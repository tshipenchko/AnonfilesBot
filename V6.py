from .. import loader, utils
from telethon import types, TelegramClient

import re

rgxLi = r'([один|два|три|четыре|пять|шесть|семь|восемь|девять|десять]+)'
xLi = {'ноль':'0','один':'1','два':'2','три':'3','четыре':'4','пять':'5','шесть':'6','семь':'7','восемь':'8','девять':'9','десять':'10'}

# def literal(link, result):
#     dict = {'ноль':0,'один':1,'два':2,'три':3,
#             'четыре':4,'пять':5,'шесть':6,
#             'семь':7,'восемь':8,'девять':9}
#     r = dict.get(result.group(0))
#     link = link.replace(result.group(0),str(r))
#     return link
 
def exercise(link,result):
    r = eval(result[1:-1])
    link = link.replace(result,str(round(r)))
    return link
      
def calculatorBtc(link):
    resultEx = re.findall(r'\(\S+?\)', link)
    if not resultEx:
        return link
    if resultEx:
        for i in resultEx:
            link = exercise(link,i)
    return link
    
@loader.tds
class YourMod(loader.Module):
    """Привет"""
    strings = {"name": "BTC"}
    bot_ids = [159405177]
  
    async def client_ready(self, client, db):
        self.client: TelegramClient = client
        self.db = db
        self.logs = []

    async def btclogscmd(self, m):
        await utils.answer(m, "/n".join(self.logs or ["логов нет чел"]))

    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return     
        try:
            user_mess = message.raw_text
            if message.out or message.from_id in self.bot_ids:
                return  # свои сообщения не ловим, это бессмысленно))
            if re.search(r'BTC_CHANGE_BOT\?start=', user_mess): 
                m = re.search(r'c_\S+', user_mess)
                if(re.search(r'\(',m.group(0))!=None or re.search(rgxLi,m.group(0))!=None):
                    mm=m.group(0)
                    for i,j in xLi.items():
                        if i in m.group(0):
                            mm = re.sub(i,j, mm)      
                    l = calculatorBtc(mm)
                else:
                    l = m.group(0)
                await self.client.send_message('BTC_CHANGE_BOT', '/start ' + l)
                self.logs.append(l)

        except Exception as e:
            print(str(e))
            await self.client.send_message('me',str(e) )
