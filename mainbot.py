import telebot
from telebot import types
from secondary import Database
from random import randint
import pyttsx3

db = Database('bot-quest-chat')
token = '5241140610:AAE0p3jKou26mLqmRBzxh8LhGbZ-OvwvjyA'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  item1 = types.KeyboardButton('Начать Квест')
  markup.add(item1)
  item2 = types.KeyboardButton('Поиск Собеседника')
  markup.add(item2)
  bot.send_message(message.chat.id, 'Привет, {0.first_name}! Выбери одну из функций, чтобы продолжить.'.format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['menu'])
def menu(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  item1 = types.KeyboardButton('Начать Квест')
  markup.add(item1)
  item2 = types.KeyboardButton('Поиск Собеседника')
  markup.add(item2)
  bot.send_message(message.chat.id, 'Меню'.format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['stop'])
def stop(message):
  chat_info = db.get_active_chat(message.chat.id)
  if chat_info != False:
    db.del_chat(chat_info[0])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Начать Квест')
    markup.add(item1)
    item2 = types.KeyboardButton('Поиск Собеседника')
    markup.add(item2)
    bot.send_message(chat_info[1], 'Собеседник покинул чат', reply_markup=markup)
    bot.send_message(message.chat.id, 'Вы вышли из чата', reply_markup=markup)
  else:
    bot.send_message(message.chat.id, 'Вы не состоите в чате', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
  if message.chat.type == 'private':
    if message.text == 'Поиск Собеседника':
      markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
      item1 = types.KeyboardButton('Остановить Поиск')
      markup.add(item1)
      chat_two = db.get_chat() # Забираем первого человека в очереди
      if db.create_chat(message.chat.id, chat_two) == False:
        db.add_queue(message.chat.id)
        bot.send_message(message.chat.id, 'Идет поиск собеседника', reply_markup=markup)
      else:
        mess = 'Собеседник найден! Чтобы закончить диалог, напишите /stop'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('/stop')
        markup.add(item1)
        bot.send_message(message.chat.id, mess, reply_markup=markup)
        bot.send_message(chat_two, mess, reply_markup=markup)

    
    elif message.text == 'Остановить Поиск':
      db.del_queue(message.chat.id)
      bot.send_message(message.chat.id, 'Поиск остановлен, напишите /menu')


    elif message.text == 'Начать Квест':

      text_to_speech = pyttsx3.init()
      RU_VOICE_ID = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'
      text_to_speech.setProperty('voice', RU_VOICE_ID)

      def ttsq(src, teext):
          text_to_speech.save_to_file(teext, src)
          text_to_speech.runAndWait()
          voice = open(src, 'rb')
          return voice

      user = message.chat.id
      states = {}
      inventories = {}
      states[user] = 0
      inventories[user] = []
      def process_state(user, state, inventory):

        kb = types.InlineKeyboardMarkup()
        if state == 0:
          kb.add(types.InlineKeyboardButton(text="Пойти направо", callback_data="1"))
          kb.add(types.InlineKeyboardButton(text="Пойти налево", callback_data="2"))
          bot.send_message(user, "Вы оказались в темном подземелье, перед вами два прохода.", reply_markup=kb)
          src = 'dungeon' + '.oga'
          voice = ttsq(src, "Вы оказались в темном подземелье, перед вами два прохода.")
          bot.send_audio(message.chat.id, voice)
        if state == 1:
          kb.add(types.InlineKeyboardButton(text="Переплыть", callback_data="1"))
          kb.add(types.InlineKeyboardButton(text="Вернуться", callback_data="2"))
          bot.send_message(user, "Перед вами большое подземное озеро, а вдали виднеется маленький остров.", reply_markup=kb)
          src = 'biglake' + '.oga'
          voice = ttsq(src, "Перед вами большое подземное озеро, а вдали виднеется маленький остров.")
          bot.send_audio(message.chat.id, voice)

        if state == 2:
            bot.send_message(user, "Вы выиграли.")
            src = 'win' + '.oga'
            voice = ttsq(src, "Вы выиграли.")
            bot.send_audio(message.chat.id, voice)
      def process_answer(user, answer):
          if states[user] == 0:
              if answer == "1":
                  states[user] = 1
              else:
                  if "key" in inventories[user]:
                      bot.send_message(user, "Перед вами закрытая дверь. Вы пробуете открыть ее ключем, и дверь поддается. Кажется, это выход.")
                      src = 'keyandoor' + '.oga'
                      voice = ttsq(src, "Перед вами закрытая дверь. Вы пробуете открыть ее ключем, и дверь поддается. Кажется, это выход.")
                      bot.send_audio(message.chat.id, voice)
                      states[user] = 2
                  else:
                      bot.send_message(user, "Перед вами закрытая дверь, и, кажется, без ключа ее не открыть. Придется вернуться обратно.")
                      src = 'closeddoor' + '.oga'
                      voice = ttsq(src, "Перед вами закрытая дверь, и, кажется, без ключа ее не открыть. Придется вернуться обратно.")
                      bot.send_audio(message.chat.id, voice)
                      states[user] = 0
          elif states[user] == 1:
              if answer == "2":
                  bot.send_message(user, "И правда, не стоит штурмовать неизвестные воды. Возвращаемся назад...")
                  src = 'shturm' + '.oga'
                  voice = ttsq(src, 'И правда, не стоит штурмовать неизвестные воды. Возвращаемся назад...')
                  bot.send_audio(message.chat.id, voice)
                  states[user] = 0
              else:
                  bot.send_message(user, "Вы пробуете переплыть озеро...")
                  src = 'tryingtoswim' + '.oga'
                  voice = ttsq(src, "Вы пробуете переплыть озеро...")
                  bot.send_audio(message.chat.id, voice)
                  chance = randint(0, 100)
                  if chance < 30:
                      bot.send_message(user, "Вода оказалось теплой, а в сундуке на острове вы нашли старый ключ. Стоит вернутся обратно.")
                      src = 'warmwater' + '.oga'
                      voice = ttsq(src, "Вода оказалось теплой, а в сундуке на острове вы нашли старый ключ. Стоит вернутся обратно.")
                      bot.send_audio(message.chat.id, voice)
                      inventories[user].append("key")
                      states[user] = 0
                  else:
                      bot.send_message(user, "На середине озера вас подхватывают волны и возвращают обратно.")
                      src = 'halfoflake' + '.oga'
                      voice = ttsq(src, "На середине озера вас подхватывают волны и возвращают обратно.")
                      bot.send_audio(message.chat.id, voice)
                      states[user] = 1
          process_state(user, states[user], inventories[user])
      bot.send_message(user, "Добро пожаловать в игру!")
      process_state(user, states[user], inventories[user])
      @bot.callback_query_handler(func=lambda call: True)
      def user_answer(call):
        user = call.message.chat.id
        process_answer(user, call.data)
    
    
    else:
      if db.get_active_chat(message.chat.id) != False:
        chat_info = db.get_active_chat(message.chat.id)
        bot.send_message(chat_info[1], message.text)
      else:
        bot.send_message(message.chat.id, 'Вы не начали диалог')


bot.polling(non_stop=True)