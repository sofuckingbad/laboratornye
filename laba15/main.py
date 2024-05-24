import telebot
from telebot import types
import sqlite3

API_TOKEN = '6806076796:AAEZTeDDb0UTYx2HaF2Jq0_AbYNA1WoyEME'

bot = telebot.TeleBot(API_TOKEN)


def create_connection():
    return sqlite3.connect('schedule.db')


def get_schedule_by_ids(start_id, end_id):
    conn = create_connection()
    cursor = conn.cursor()

    query = '''
        SELECT day, time, subject, room, teacher FROM schedule 
        WHERE id BETWEEN ? AND ? 
        ORDER BY id
    '''

    cursor.execute(query, (start_id, end_id))
    schedule = cursor.fetchall()
    conn.close()
    return schedule


def format_schedule_by_ids(start_id, end_id):
    schedule = get_schedule_by_ids(start_id, end_id)
    if not schedule:
        return "Расписание не найдено."

    formatted = ""
    current_day = ""
    for day, time, subject, room, teacher in schedule:
        if day != current_day:
            if current_day:
                formatted += "\n"
            current_day = day
            formatted += f"{day.capitalize()}:\n"
        formatted += f"{time} - {subject} {room} - {teacher}\n"
    return formatted


def get_current_week_schedule():
    return format_schedule_by_ids(1, 15)


def get_next_week_schedule():
    return format_schedule_by_ids(16, 27)


def get_schedule_by_day(day):
    conn = create_connection()
    cursor = conn.cursor()

    query = '''
        SELECT time, subject, room, teacher FROM schedule 
        WHERE day = ? AND id BETWEEN 1 AND 15 
        ORDER BY id
    '''

    cursor.execute(query, (day,))
    schedule = cursor.fetchall()
    conn.close()
    return schedule


def format_schedule_by_day(day):
    schedule = get_schedule_by_day(day)
    if not schedule:
        return f"Расписание на {day.capitalize()} не найдено."

    formatted = f"{day.capitalize()}:\n"
    for time, subject, room, teacher in schedule:
        formatted += f"{time} - {subject} {room} - {teacher}\n"
    return formatted


# Keyboards
main_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .add(types.KeyboardButton("Расписание на текущую неделю"))
    .add(types.KeyboardButton("Расписание на следующую неделю"))
    .add(types.KeyboardButton("Расписание по дням"))
    .add(types.KeyboardButton("/help"))
)

days_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .add(types.KeyboardButton("Понедельник"))
    .add(types.KeyboardButton("Вторник"))
    .add(types.KeyboardButton("Среда"))
    .add(types.KeyboardButton("Четверг"))
    .add(types.KeyboardButton("Пятница"))
    .add(types.KeyboardButton("Назад"))
)

help_keyboard = (
    types.ReplyKeyboardMarkup(resize_keyboard=True)
    .add(types.KeyboardButton("/kstu"))
    .add(types.KeyboardButton("/week"))
    .add(types.KeyboardButton("/vk"))
    .add(types.KeyboardButton("/info"))
    .add(types.KeyboardButton("/exam"))
    .add(types.KeyboardButton("/classroom"))
    .add(types.KeyboardButton("Назад"))
)


# Bot Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Чем могу вам помочь? Используйте /help если у вас возникли вопросы?", reply_markup=main_keyboard)


@bot.message_handler(func=lambda message: message.text.lower() == "назад")
def handle_back(message):
    bot.send_message(message.chat.id, "Чем могу вам помочь? Используйте /help если у вас возникли вопросы?", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text.lower() == "/info")
def send_dean_office_schedule(message):
    bot.send_message(message.chat.id, "График работы отдела по работе студентами:")
    # Путь к изображению
    image_path = "info.jpg"
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(func=lambda message: message.text.lower() == "/exam")
def send_dean_office_schedule(message):
    bot.send_message(message.chat.id, "Расписание экзаменов:"
                                      "Защита информации -"
                                      "Разработка пользовательского интерфейса -"
                                      "Экономика предприятия -")

@bot.message_handler(func=lambda message: message.text.lower() == "/classroom")
def send_dean_office_schedule(message):
    bot.send_message(message.chat.id, "Ссылка на гугл класс по РПИ: https://classroom.google.com/c/NjMzNDMxNjAxNzc0")

@bot.message_handler(func=lambda message: message.text.lower() == "расписание на текущую неделю")
def handle_current_week_schedule(message):
    schedule = get_current_week_schedule()
    bot.send_message(message.chat.id, schedule)


@bot.message_handler(func=lambda message: message.text.lower() == "расписание на следующую неделю")
def handle_next_week_schedule(message):
    schedule = get_next_week_schedule()
    bot.send_message(message.chat.id, schedule)

@bot.message_handler(func=lambda message: message.text.lower() == "/help")
def handle_day_schedule(message):
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=help_keyboard)


@bot.message_handler(func=lambda message: message.text.lower() == "расписание по дням")
def handle_day_schedule(message):
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=days_keyboard)

@bot.message_handler(func=lambda message: message.text.lower() in ["понедельник", "вторник", "среда", "четверг", "пятница"])
def handle_specific_day_schedule(message):
    day = message.text.lower()
    schedule = format_schedule_by_day(day)
    bot.send_message(message.chat.id, schedule)


@bot.message_handler(commands=['help'])
def handle_help(message):
    help_message = """
Привет! Я бот для удобного просмотра расписания в институте.

/start - начать взаимодействие с ботом
/help - получить справку о боте и доступных командах
/kstu - получить ссылку на официальный сайт КНИТУ
    """

    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['kstu'])
def kstu_handler(message):
    bot.send_message(message.chat.id, 'Ссылка на оффициальный сайт Университета: https://www.kstu.ru/')


@bot.message_handler(func=lambda message: message.text.lower() == "рпи")
def handle_day_schedule(message):
    bot.send_message(message.chat.id, "Ссылка на документ со сданными\несданными лабораторными по РПИ: "
                                      "https://docs.google.com/spreadsheets/d/1Rnk7hPwJLK3exHXOBOhmKLdUxs4RLajE4pQBPxdK0WA/edit#gid=1407818257", reply_markup=help_keyboard)


@bot.message_handler(func=lambda message: message.text.lower() == "дай совет")
def handle_day_schedule(message):
    bot.send_message(message.chat.id, "Если хотите успешно сдать сессию, то не стоит копить долги на конец семестра")


@bot.message_handler(func=lambda message: message.text.lower() == "когда зачётная неделя")
def handle_day_schedule(message):
    bot.send_message(message.chat.id, "С 3 по 8 июня")


@bot.message_handler(commands=['week'])
def kstu_handler(message):
    bot.send_message(message.chat.id, 'Сейчас нечётная неделя')

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id, "Извините, я вас не понял. Попробуйте снова.")

bot.infinity_polling()

