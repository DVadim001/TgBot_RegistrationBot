from telebot import types


def num_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num = types.KeyboardButton("Отправить номер", request_contact=True)
    kb.add(num)
    return kb


def loc_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    loc = types.KeyboardButton("Отправить локацию", request_location=True)
    kb.add(loc)
    return kb


def lang():
    # Создаём пространство для кнопок
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаём сами кнопки
    rus = types.InlineKeyboardButton(text="Русский", callback_data="rus")
    eng = types.InlineKeyboardButton(text="English", callback_data="eng")
    # Добавляем кнопки в пространство
    kb.add(rus, eng)
    return kb
