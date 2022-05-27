import pyttsx3
import telebot
from telebot import types
import time
import os

token = '5241140610:AAE0p3jKou26mLqmRBzxh8LhGbZ-OvwvjyA'
bot = telebot.TeleBot(token)

text_to_speech = pyttsx3.init()
RU_VOICE_ID = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'
text_to_speech.setProperty('voice', RU_VOICE_ID)

@bot.message_handler(commands=["start"])
def bot_messages(message):
  bot.send_message(message.chat.id, 'Привет! Чем я могу вам помочь? :)')

@bot.message_handler(content_types=['text'])
def bot_messages(message):
  text = message.text.lower()
  if 'произнеси' in text and text.split()[0] == 'произнеси':
    src = str(message.chat.id) + str(message.message_id) + '_answer.oga'
    text_to_speech.save_to_file(text[9:], src)
    text_to_speech.runAndWait()
    time.sleep(1)
    voice = open(src, 'rb')
    bot.send_audio(message.chat.id, voice)

bot.polling(non_stop=True, timeout=0)