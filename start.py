import time
import os
from bs4 import BeautifulSoup as bs
import requests
import telebot
import urllib
from telebot import types
import re
import json
token = "1994181034:AAFeq7fdxnZdgCPZ7g300f60jJpmWdafl4k"
bot = telebot.TeleBot(token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Загрузить файл на anonfiles')

url = 'https://api.anonfiles.com/upload'
def file(message):
 if message.content_type == "document":
  try:
   chat_id = message.chat.id
   url = 'https://api.anonfiles.com/upload'
   file_info = bot.get_file(message.document.file_id)
   downloaded_file = bot.download_file(file_info.file_path)
   ss = message.document.file_name
   src = '' + message.document.file_name;
   with open(src, 'wb') as new_file:
    new_file.write(downloaded_file)
   bot.send_message(message.chat.id, f"[ЗАГРУЖАЕМ] {ss}")
   files = {'file': (ss, open(ss, 'rb')),}
   r = requests.post(url, files=files)
   resp = json.loads(r.text)

   if resp['status']:
    urlshort = resp['data']['file']['url']['short']
    urllong = resp['data']['file']['url']['full']
    bot.send_message(message.chat.id,f'[УСПЕШНО] Ваш файл был успешно загружен:\nFull URL: {urllong}\nShort URL: {urlshort}',  reply_markup=keyboard1)
    os.remove(src)
   else:
    message = resp['error']['message']
    errtype = resp['error']['type']
    bot.send_message(message.chat.id, f'[ОШИБКА] {message}\n{errtype}',  reply_markup=keyboard1)
    os.remove(src)
  except Exception as e:
   bot.send_message(message.chat.id, e,  reply_markup=keyboard1)
 else:
  bot.reply_to(message, "Это не документ",  reply_markup=keyboard1)

@bot.message_handler(commands=['start'])
def handle_docs_photo(message):
 bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}', reply_markup=keyboard1)

@bot.message_handler(content_types=["text"])
def send_message(message):
 if message.text == "Загрузить файл на anonfiles":
  bot.send_message(message.chat.id,"Отправьте файл.")
  bot.register_next_step_handler(message, file)

if __name__ == '__main__':
 bot.polling(none_stop=True)
