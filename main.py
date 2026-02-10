import telebot
from telebot import types

# Твій токен
API_TOKEN = '8196800585:AAE3UBIw9m37YRJnWBm220DNYs7KnPGa7Ro'

bot = telebot.TeleBot(API_TOKEN)

# Словник для збереження ID останнього повідомлення бота
users_last_msg = {}

# --- КЛАВІАТУРИ (КНОПКИ) ---

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("🎓 ПРОФІЛІ НАВЧАННЯ")
    btn2 = types.KeyboardButton("📞 КОНТАКТИ")
    btn3 = types.KeyboardButton("📍 ЛОКАЦІЯ")
    markup.add(btn1, btn2, btn3)
    return markup

def profiles_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("ІСТОРИКО-ПРАВОВИЙ ПРОФІЛЬ")
    btn2 = types.KeyboardButton("ПРОФІЛЬ ІНОЗЕМНОЇ ФІЛОЛОГІЇ")
    btn3 = types.KeyboardButton("БІОТЕХНОЛОГІЧНИЙ ПРОФІЛЬ")
    btn4 = types.KeyboardButton("МЕДИЧНИЙ ПРОФІЛЬ")
    btn_back = types.KeyboardButton("⬅️ ПОВЕРНУТИСЯ У МЕНЮ")
    markup.add(btn1, btn2, btn3, btn4, btn_back)
    return markup

# --- ФУНКЦІЇ ДОПОМОГИ ---

def delete_messages(chat_id, user_msg_id):
    """Видаляє повідомлення користувача та попереднє повідомлення бота"""
    try:
        bot.delete_message(chat_id, user_msg_id)
    except:
        pass

    if chat_id in users_last_msg:
        try:
            bot.delete_message(chat_id, users_last_msg[chat_id])
        except:
            pass

def send_bot_message(message, text, markup=None, photo_path=None):
    """Універсальна функція відправки"""
    delete_messages(message.chat.id, message.message_id)
    chat_id = message.chat.id
    sent_msg = None

    try:
        if photo_path:
            with open(photo_path, 'rb') as photo:
                sent_msg = bot.send_photo(
                    chat_id, 
                    photo, 
                    caption=text, 
                    reply_markup=markup, 
                    parse_mode='Markdown'
                )
        else:
            sent_msg = bot.send_message(
                chat_id, 
                text, 
                reply_markup=markup, 
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        
        if sent_msg:
            users_last_msg[chat_id] = sent_msg.message_id

    except Exception as e:
        sent_msg = bot.send_message(chat_id, text, reply_markup=markup, parse_mode='Markdown')
        if sent_msg:
            users_last_msg[chat_id] = sent_msg.message_id

# --- ОБРОБНИКИ КОМАНД І ГОЛОВНОГО МЕНЮ ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    delete_messages(message.chat.id, message.message_id)
    
    text = (
        "*Вітаю у боті ТНВК №15!*\n\n"
        "Тут ви можете дізнатися про напрямки навчання, "
        "знайти контакти адміністрації та побудувати маршрут до закладу."
    )
    sent_msg = bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode='Markdown')
    users_last_msg[message.chat.id] = sent_msg.message_id

@bot.message_handler(commands=['help'])
def help_command(message):
    text = (
        "*Допомога*\n\n"
        "Використовуйте кнопки внизу екрану для навігації.\n"
        "Якщо кнопки зникли — введіть команду /start"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "⬅️ ПОВЕРНУТИСЯ У МЕНЮ")
def back_to_main(message):
    send_bot_message(
        message, 
        "*Головне меню*", 
        markup=main_menu()
    )

@bot.message_handler(func=lambda message: message.text == "🎓 ПРОФІЛІ НАВЧАННЯ")
def show_profiles_menu(message):
    send_bot_message(
        message, 
        "Оберіть профіль, який вас цікавить:", 
        markup=profiles_menu()
    )

@bot.message_handler(func=lambda message: message.text == "📞 КОНТАКТИ")
def show_contacts(message):
    text = (
        "*КОНТАКТИ АДМІНІСТРАЦІЇ ТНВК ШМЛ 15*\n\n"
        "*Адміністрація:*\n"
        "🔹 Оксана Романівна – директор;\n"
        "🔹 Краснопольська Ірина Семенівна – заступник директора з навчально-виховної роботи;\n"
        "🔹 Мацьковська Ганна Петрівна – заступник директора з навчально-виховної роботи;\n"
        "🔹 Стульківська Мирослава Дмитрівна – заступник директора з виховної роботи.\n\n"
        "📧 *E-mail:* skhool_15@ukr.net"
    )
    send_bot_message(message, text, markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "📍 ЛОКАЦІЯ")
def show_location(message):
    # 1. Видаляємо старі повідомлення
    delete_messages(message.chat.id, message.message_id)
    
    # 2. Дані локації
    lat = 49.54448018231034
    lon = 25.62807305074633
    
    # 3. Створюємо кнопку посилання (Inline)
    inline_markup = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(
        text="🗺 Побудувати маршрут (Google Maps)", 
        url=f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    )
    inline_markup.add(url_btn)

    text = (
        "*ТНВК Школа-ліцей №15 імені Лесі Українки*\n\n"
        "📍 *Адреса:* м. Тернопіль, вул. Лесі Українки, 23\n\n"
        "Натисніть кнопку нижче, щоб автоматично прокласти маршрут від вашого поточного місця знаходження до школи."
    )
    
    # 4. Відправляємо лише одне повідомлення з Inline-кнопкою
    sent_msg = bot.send_message(message.chat.id, text, reply_markup=inline_markup, parse_mode='Markdown')
    users_last_msg[message.chat.id] = sent_msg.message_id


# --- ОБРОБНИКИ ПРОФІЛІВ ---

@bot.message_handler(func=lambda message: message.text == "ІСТОРИКО-ПРАВОВИЙ ПРОФІЛЬ")
def profile_history(message):
    text = (
        "*ІСТОРИКО-ПРАВОВИЙ ПРОФІЛЬ*\n\n"
        "*НАШ ВИПУСКНИК ЗНАТИМЕ*\n"
        "— Еволюцію правових систем та ключові історичні події.\n"
        "— Основи міжнародного права та роль лідерів.\n\n"
        "*ВМІТИМЕ*\n"
        "— Аналізувати документи та аргументувати в дебатах.\n"
        "— Досліджувати кейси та створювати есе.\n\n"
        "*ЗМОЖЕ*\n"
        "— Захищати права та вирішувати конфлікти.\n"
        "— Підготуватися до НМТ та обрати професію."
    )
    send_bot_message(message, text, markup=profiles_menu(), photo_path='tnvk15.jpg')

@bot.message_handler(func=lambda message: message.text == "ПРОФІЛЬ ІНОЗЕМНОЇ ФІЛОЛОГІЇ")
def profile_philology(message):
    text = (
        "*ПРОФІЛЬ ІНОЗЕМНОЇ ФІЛОЛОГІЇ*\n\n"
        "*НАШ ВИПУСКНИК ЗНАТИМЕ*\n"
        "— Граматику (B1–B2), лексику та культурні особливості.\n"
        "— Цифровий та мовленнєвий етикет.\n\n"
        "*ВМІТИМЕ*\n"
        "— Говорити, слухати, читати та писати іноземними мовами.\n\n"
        "*ЗМОЖЕ*\n"
        "— Подорожувати без бар’єрів та навчатися за кордоном.\n"
        "— Успішно скласти НМТ."
    )
    send_bot_message(message, text, markup=profiles_menu(), photo_path='tnvk15.jpg')

@bot.message_handler(func=lambda message: message.text == "БІОТЕХНОЛОГІЧНИЙ ПРОФІЛЬ")
def profile_biotech(message):
    text = (
        "*БІОТЕХНОЛОГІЧНИЙ ПРОФІЛЬ*\n\n"
        "*НАШ ВИПУСКНИК ЗНАТИМЕ*\n"
        "— Роботу програміста, логіку формул та кібербезпеку.\n\n"
        "*ВМІТИМЕ*\n"
        "— Створювати алгоритми, 3D моделі та знаходити помилки.\n\n"
        "*ЗМОЖЕ*\n"
        "— Створювати цифрові продукти та опановувати нові технології (AI, VR)."
    )
    send_bot_message(message, text, markup=profiles_menu(), photo_path='tnvk15.jpg')

@bot.message_handler(func=lambda message: message.text == "МЕДИЧНИЙ ПРОФІЛЬ")
def profile_medical(message):
    text = (
        "*МЕДИЧНИЙ ПРОФІЛЬ*\n\n"
        "*НАШ ВИПУСКНИК ЗНАТИМЕ*\n"
        "— Біологію, медицину, хімію та фізику діагностики.\n\n"
        "*ВМІТИМЕ*\n"
        "— Працювати з обладнанням, проводити аналізи та дослідження.\n\n"
        "*ЗМОЖЕ*\n"
        "— Надавати домедичну допомогу та готуватися до медичного вишу."
    )
    send_bot_message(message, text, markup=profiles_menu(), photo_path='tnvk15.jpg')

# Обробник будь-якого іншого контенту
@bot.message_handler(content_types=['text', 'photo', 'video', 'sticker', 'video_note', 'voice', 'location', 'contact'])
def unknown_content(message):
    bot.reply_to(
        message, 
        "Вибачте, я не розумію цей запит. Будь ласка, скористайтеся кнопками меню.\n"
        "Якщо виникли проблеми, напишіть /help"
    )

if __name__ == '__main__':
    print("Бот запущено...")
    bot.infinity_polling()
