# ТГ бот регистрации.
import telebot
import database as db
import buttons as bt
from geopy import Nominatim


bot = telebot.TeleBot("6643297345:AAH2Dprar4RgV7PQ4rYd0skrGPdl7cj01m0")
geo = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

selected_lang = {}
texts = {"welcome_message": {"rus": "Здравствуйте.", "eng": "Welcome."},
         "reg_begin": {"rus": "Начало регистрации. Введите имя.", "eng": "Registration start. Enter your name."},
         "name_res": {"rus": "Имя получено, отправьте номер.", "eng": "Name received, send the number."},
         "loc_res": {"rus": "Номер получен, отправьте локацию.", "eng": "Number received, send the location."},
         "send_but": {"rus": "Отправьте по кнопке.", "eng": "Send using the button."},
         "reg_suc": {"rus": "Регистрация успешна.", "eng": "Registration successful."},
         "lang_choose": {"rus": "Добро пожаловать. Выберите удобный для вас язык",
                         "eng": "Welcome. Choose your preferred language"},
         "set_lang": {"rus": "Установлен язык: Русский.", "eng": "Your language has beet set to: English"},
         "wait": {"rus": "Ожидайте дальнейшей доработки", "eng": "Wait next repair"},
         # "": {"rus":"", "eng": ""},

         }


def lang_choice(user_id, keyword):
    user_lang = selected_lang.get(user_id, "rus")
    return texts[keyword][user_lang]


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    check = db.check_in_base(user_id)
    lang_choose = lang_choice(user_id, "lang_choose")
    lang_choose1 = lang_choice(user_id, "wait")
    if check:
        # bot.send_message(user_id, f"Здравствуйте, '{message.from_user.first_name}', выберите удобный для вас язык.",
        # reply_markup=bt.lang())
        bot.send_message(user_id, lang_choose1)
    else:
        bot.send_message(user_id, lang_choose, reply_markup=bt.lang())
        bot.register_next_step_handler(message, begin_registration)


def begin_registration(message):
    user_id = message.from_user.id
    reg_begin = lang_choice(user_id, "reg_begin")
    bot.send_message(user_id, reg_begin)
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    name = message.text
    user_id = message.from_user.id
    name_res = lang_choice(user_id, "name_res")
    bot.send_message(user_id, name_res, reply_markup=bt.num_bt())
    bot.register_next_step_handler(message, get_num, name)


def get_num(message, name):
    user_id = message.from_user.id
    loc_res = lang_choice(user_id, "loc_res")
    send_but = lang_choice(user_id, "send_but")
    if message.contact:
        num = message.contact.phone_number
        bot.send_message(user_id, loc_res, reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, get_loc, name, num)
    else:
        bot.send_message(user_id, send_but, reply_markup=bt.num_bt())
        bot.register_next_step_handler(message, get_num, name)


def get_loc(message, name, num):
    user_id = message.from_user.id
    reg_suc = lang_choice(user_id, "reg_suc")
    send_but = lang_choice(user_id, "send_but")
    if message.location:
        loc = str(geo.reverse(f"{message.location.latitude}", f"{message.location.longitude}"))
        db.registration(user_id, name, num, loc)
        bot.send_message(user_id, reg_suc, reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, send_but, reply_markup=bt.loc_bt())
        bot.register_next_step_handler(message, get_loc, name, num)


@bot.callback_query_handler(lambda call: call.data in ['rus', 'eng'])
def choose_lang(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    selected_lang[user_id] = call.data
    set_lang = lang_choice(user_id, "set_lang")
    if call.data == "rus":
        bot.send_message(chat_id, set_lang, reply_markup=telebot.types.ReplyKeyboardRemove())
    elif call.data == "eng":
        bot.send_message(chat_id, set_lang, reply_markup=telebot.types.ReplyKeyboardRemove())


# def choose_lang(call):
#     chat_id = call.message.chat.id
#     user_id = call.from_user.id
#     selected_lang[user_id] = call.data
#     set_lang = lang_choice(user_id, "set_lang")
#     if call.data == "rus" or call.data == "eng":
#         bot.send_message(chat_id, set_lang, reply_markup=telebot.types.ReplyKeyboardRemove())
#         begin_registration(chat_id)


bot.polling(non_stop=True)
