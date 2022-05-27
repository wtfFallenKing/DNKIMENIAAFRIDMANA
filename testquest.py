from telebot import TeleBot, types
from random import randint

token = '5241140610:AAE0p3jKou26mLqmRBzxh8LhGbZ-OvwvjyA'

states = {}
inventories = {}
bot = TeleBot(token)

@bot.message_handler(commands=["start"])
def start_game(message):
    user = message.chat.id

    states[user] = 0
    inventories[user] = []

    bot.send_message(user, "Добро пожаловать в игру!")

    process_state(user, states[user], inventories[user])

@bot.callback_query_handler(func=lambda call: True)
def user_answer(call):
    user = call.message.chat.id
    process_answer(user, call.data)

def process_state(user, state, inventory):
    kb = types.InlineKeyboardMarkup()

    if state == 0:
        kb.add(types.InlineKeyboardButton(text="пойти направо", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="пойти налево", callback_data="2"))

        bot.send_message(user, "Вы в оказались в темном подземелье, перед вами два прохода.", reply_markup=kb)

    if state == 1:
        kb.add(types.InlineKeyboardButton(text="переплыть", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="вернуться", callback_data="2"))

        bot.send_message(user, "Перед вами большое подземное озеро, а вдали виднеется маленький остров.", reply_markup=kb)

    if state == 2:
        bot.send_message(user, "Вы выиграли.")

def process_answer(user, answer):
    if states[user] == 0:
        if answer == "1":
            states[user] = 1
        else:
            if "key" in inventories[user]:
                bot.send_message(user,
                                 "Перед вами закрытая дверь. Вы пробуете открыть ее ключем, и дверь поддается. Кажется, это выход.")
                states[user] = 2
            else:
                bot.send_message(user, "Перед вами закрытая дверь, и, кажется, без ключа ее не открыть. Придется вернуться обратно.")
                states[user] = 0

    elif states[user] == 1:
        if answer == "2":
            bot.send_message(user,
                             "И правда, не стоит штурмовать неизвестные воды. Возвращаемся назад...")
            states[user] = 0
        else:
            bot.send_message(user,
                             "Вы пробуете переплыть озеро...")

            chance = randint(0, 100)
            if chance < 30:
                bot.send_message(user,
                                 "Вода оказалось теплой, а в сундуке на острове вы нашли старый ключ. Стоит вернутся обратно.")
                inventories[user].append("key")
                states[user] = 0
            else:
                bot.send_message(user,
                                 "На середине озера вас подхватывают волны и возвращают обратно.")
                states[user] = 1

    process_state(user, states[user], inventories[user])

bot.polling(none_stop=True)