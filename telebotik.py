from aiogram import Bot, Dispatcher, executor, types
from database import Database
import telebot
import sqlite3

bot = Bot("token")
dispatcher = Dispatcher(bot)

database = Database()


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    #проверяем idпользователя на соответствие с id преподователя
    # conn = sqlite3.connect(r 'list.db')
    # cur = conn.cursor()
    # cur.execute("SELECT teachers_ids FROM list_of_id;")#бд тестовая
    # all_id = cur.fetchall()
    # id =list()
    # for i in all_id:
    #     id.append(int(i[0]))
    # all_id = id
    # if not(message.chat.id in all_id):
    #     import igor #в случае несоответствия перенаправляем на интерфейс ученика
    await message.answer("добро пожалловать в бота")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("да")
    btn2 = types.KeyboardButton("no")
    markup.add(btn, btn2)

    await message.answer("{message.from_user.first_name},это вы?", reply_markup=markup)


@dispatcher.message_handler(content_types=["text"])
#дальше частичная(без бд)реализация интерфейса преподователя
# async def bot_message(message: types.Message):
#     if message.text == "да":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn = types.KeyboardButton("онлайн")
#         markup.add(btn)
#         await message.answer("добро пожалловать в бота", reply_markup=markup)
#     if message.text == "no":
#         await message.answer("перенаправляю")
#         import igor
#     if message.text == "онлайн":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn = types.KeyboardButton("офлайн")
#         markup.add(btn)
#         await message.answer("на линии", reply_markup=markup)
#дальше следует соединение с преподователя

executor.start_polling(dispatcher)
