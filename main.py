from time import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import Database
from config import TOKEN

bot = Bot(TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)

database = Database()


class Form(StatesGroup):
    subject = State()
    grade = State()

@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    # проверка препода на наличие в БД
    is_teacher = database.check_teacher(message.from_user.id)

    if is_teacher:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("Получить задание")
        markup.add(btn)
        await message.answer(f"Здравствуйте, {message.from_user.first_name}", reply_markup=markup)

    else:
        markup = types.ReplyKeyboardRemove()
        await message.answer("Добро пожаловать\nСкиньте мне файл задания или фото, а я найду кто поможет вам его решить", reply_markup=markup)

@dispatcher.message_handler(content_types=['photo'])
async def bot_file(message: types.Message):
    is_teacher = database.check_teacher(message.from_user.id)
    if is_teacher:
        global file_id_solution
        file_id_solution = message.photo[0].file_id
        database.add_solution(task_id, file_id_solution, message.from_user.id)
        markup = types.ReplyKeyboardRemove()
        await bot.send_photo(tg_client_id, file_id_solution, reply_markup=markup)
    else:
        global file_id
        file_id = message.photo[0].file_id
        await Form.subject.set()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Биология")
        btn2 = types.KeyboardButton("Математика")
        btn3 = types.KeyboardButton("Химия")
        btn4 = types.KeyboardButton("Информатика")
        markup.add(btn1, btn2, btn3, btn4)
        await message.answer("Отлично, укажите теперь предмет", reply_markup=markup)

@dispatcher.message_handler(content_types=types.ContentTypes.TEXT)
async def bot_message(message: types.Message):
    is_teacher = database.check_teacher(message.from_user.id)
    if is_teacher:
        if message.text == "Получить задание" or message.text == "Пропустить задание":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("Отмена")
            markup.add(btn)   
            await message.answer("Идет поиск...", reply_markup=markup)
            sleep(0.5) # Искусственная задержка (будто загрузка с большой бд), позже - убрать!
            info = database.get_teacher_info(message.from_user.id)
            print(info)
            subject = info[2]
            grade = info[5]
            task = database.get_task(subject, grade)
            print(task)
            global task_id, tg_client_id
            task_id = task[0]
            file_id = task[3]
            tg_client_id = task[6]
            # тут вывод сообщения о задании
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Принять")
            btn2 = types.KeyboardButton("Пропустить задание")
            markup.add(btn1, btn2)
            await message.answer("Задание #" + str(task_id), reply_markup=markup)
            await bot.send_photo(message.chat.id, file_id)

@dispatcher.message_handler(state=Form.subject)
async def process_subject(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['subject'] = message.text
    await Form.next()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("5")
    btn2 = types.KeyboardButton("6")
    btn3 = types.KeyboardButton("7")
    btn4 = types.KeyboardButton("8")
    btn5 = types.KeyboardButton("9")
    btn6 = types.KeyboardButton("10")
    btn7 = types.KeyboardButton("11")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    await message.answer("Выберите класс", reply_markup=markup)

@dispatcher.message_handler(state=Form.grade)
async def process_grade(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['grade'] = message.text
        database.add_task(data["subject"], data["grade"], file_id, message.from_user.id)
        markup = types.ReplyKeyboardRemove()
        await message.answer("Задание создано\nОжидайте решения\n\n" + data["subject"] + ", " + data["grade"] + " класс", reply_markup=markup)
    await state.finish()

# @dispatcher.message_handler(content_types=["text"])
# async def bot_message(message: types.chat_photo):
#     task = ""
#     global grade
#     global subject
#     if message.text == 'Биология' or "Математика" or "Химия" or "Информатика":
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn1 = types.KeyboardButton("5")
#         btn2 = types.KeyboardButton("6")
#         btn3 = types.KeyboardButton("7")
#         btn4 = types.KeyboardButton("8")
#         btn5 = types.KeyboardButton("9")
#         btn6 = types.KeyboardButton("10")
#         btn7 = types.KeyboardButton("11")
#         markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
#         await message.answer("Choose Grade", reply_markup=markup)
#     if message.text == 'Биология':
#         subject = ('Биология')
#     if message.text == 'Математика':
#         subject = ('Математика')
#     if message.text == 'Химия':
#         subject = ('Химия')
#     if message.text == 'Информатика':
#         subject = ('Химия')
#     if message.text == '5':
#         grade = message.text
#         database.add_task(subject, grade, task, message.chat.id)
#         await message.answer("Ждите решения")
#     if message.text == '6':
#         grade = message.text
#         database.add_task(subject, grade, task, message.chat.id)
#         await message.answer("Ждите решения")
#     if message.text == '7':
#         grade = message.text
#         database.add_task(subject, grade, task, message.chat.id)
#         await message.answer("Ждите решения")
#     if message.text == '8':
#         grade = message.text
#         database.add_task(subject, grade, task, message.chat.id)
#         await message.answer("Ждите решения")
#     if message.text == '9':
#         grade = message.text
#         database.add_task(subject, grade, task, message.chat.id)
#         await message.answer("Ждите решения")
#     if message.text == '10':
#         grade = message.text
#         database.add_task(subject, grade, task, message.chat.id)
#         await message.answer("Ждите решения")
#     if message.text == '11':
#         grade = message.text
#         database.add_task(subject, grade, task, message.chat.id)
#         await message.answer("Ждите решения")

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
