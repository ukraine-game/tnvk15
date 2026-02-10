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
    """Видаляє лише текст, не чіпаючи клавіатуру"""
    try:
        bot.delete_message(chat_id, user_msg_id)
    except:
        pass

    if chat_id in users_last_msg:
        try:
            bot.delete_message(chat_id, users_last_msg[chat_id])
        except:
            pass

# --- ОБРОБНИКИ КОМАНД І ГОЛОВНОГО МЕНЮ ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    delete_messages(message.chat.id, message.message_id)
    text = (
        "*Вітаю у боті ТНВК №15!*\n\n"
        "Тут ви можете дізнатися про напрямки навчання, "
        "знайти контакти адміністрації та побудувати маршрут."
    )
    sent_msg = bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode='Markdown')
    users_last_msg[message.chat.id] = sent_msg.message_id

@bot.message_handler(func=lambda message: message.text == "⬅️ ПОВЕРНУТИСЯ У МЕНЮ")
def back_to_main(message):
    delete_messages(message.chat.id, message.message_id)
    sent_msg = bot.send_message(message.chat.id, "*Головне меню*", reply_markup=main_menu(), parse_mode='Markdown')
    users_last_msg[message.chat.id] = sent_msg.message_id

@bot.message_handler(func=lambda message: message.text == "🎓 ПРОФІЛІ НАВЧАННЯ")
def show_profiles_menu(message):
    delete_messages(message.chat.id, message.message_id)
    sent_msg = bot.send_message(message.chat.id, "Оберіть профіль навчання:", reply_markup=profiles_menu(), parse_mode='Markdown')
    users_last_msg[message.chat.id] = sent_msg.message_id

@bot.message_handler(func=lambda message: message.text == "📞 КОНТАКТИ")
def show_contacts(message):
    delete_messages(message.chat.id, message.message_id)
    text = (
        "*КОНТАКТИ АДМІНІСТРАЦІЇ ТНВК ШМЛ 15*\n\n"
        "🔹 Оксана Романівна – директор;\n"
        "🔹 Краснопольська Ірина Семенівна – заст. директора;\n"
        "🔹 Мацьковська Ганна Петрівна – заст. директора;\n"
        "🔹 Стульківська Мирослава Дмитрівна – заст. директора.\n\n"
        "📧 *E-mail:* skhool_15@ukr.net"
    )
    # Відправляємо контакти і ОБОВ'ЯЗКОВО main_menu()
    sent_msg = bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode='Markdown')
    users_last_msg[message.chat.id] = sent_msg.message_id

@bot.message_handler(func=lambda message: message.text == "📍 ЛОКАЦІЯ")
def show_location(message):
    delete_messages(message.chat.id, message.message_id)
    
    lat, lon = 49.544480, 25.628073
    inline_markup = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(
        text="🗺 Побудувати маршрут (Google Maps)", 
        url=f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
    )
    inline_markup.add(url_btn)

    text = (
        "*ТНВК Школа-ліцей №15 імені Лесі Українки*\n\n"
        "📍 *Адреса:* м. Тернопіль, вул. Лесі Українки, 23\n\n"
        "Натисніть кнопку нижче для маршруту."
    )
    # Відправляємо повідомлення з кнопкою-посиланням ТА одночасно оновлюємо нижнє меню
    sent_msg = bot.send_message(message.chat.id, text, reply_markup=main_menu(), parse_mode='Markdown')
    # Додатково кріпимо Inline-кнопку до цього ж повідомлення
    bot.edit_message_reply_markup(message.chat.id, sent_msg.message_id, reply_markup=inline_markup)
    
    users_last_msg[message.chat.id] = sent_msg.message_id

# --- ОБРОБНИКИ ПРОФІЛІВ ---
# (Аналогічно додаємо видалення повідомлень та підтримку меню)

@bot.message_handler(func=lambda message: message.text in ["ІСТОРИКО-ПРАВОВИЙ ПРОФІЛЬ", "ПРОФІЛЬ ІНОЗЕМНОЇ ФІЛОЛОГІЇ", "БІОТЕХНОЛОГІЧНИЙ ПРОФІЛЬ", "МЕДИЧНИЙ ПРОФІЛЬ"])
def handle_profiles(message):
    delete_messages(message.chat.id, message.message_id)
    
    # Визначаємо текст залежно від вибору
    responses = {
        "ІСТОРИКО-ПРАВОВИЙ ПРОФІЛЬ": "*ІСТОРИКО-ПРАВОВИЙ ПРОФІЛЬ*\n\nНаш випускник знатиме еволюцію правових систем...",
        "ПРОФІЛЬ ІНОЗЕМНОЇ ФІЛОЛОГІЇ": "*ПРОФІЛЬ ІНОЗЕМНОЇ ФІЛОЛОГІЇ*\n\nЗнатиме граматику (B1–B2) та мовленнєвий етикет...",
        "БІОТЕХНОЛОГІЧНИЙ ПРОФІЛЬ": "*БІОТЕХНОЛОГІЧНИЙ ПРОФІЛЬ*\n\nВмітиме створювати алгоритми та 3D моделі...",
        "МЕДИЧНИЙ ПРОФІЛЬ": "*МЕДИЧНИЙ ПРОФІЛЬ*\n\nЗнатиме біологію та фізику діагностики..."
    }
    
    text = responses.get(message.text, "Інформація оновлюється...")
    
    try:
        with open('tnvk15.jpg', 'rb') as photo:
            sent_msg = bot.send_photo(message.chat.id, photo, caption=text, reply_markup=profiles_menu(), parse_mode='Markdown')
    except:
        sent_msg = bot.send_message(message.chat.id, text, reply_markup=profiles_menu(), parse_mode='Markdown')
    
    users_last_msg[message.chat.id] = sent_msg.message_id

# --- ОБРОБНИК НЕВІДОМОГО КОНТЕНТУ ---

@bot.message_handler(content_types=['text', 'photo', 'video', 'sticker', 'video_note', 'voice', 'location', 'contact'])
def unknown_content(message):
    # Не видаляємо повідомлення користувача тут, щоб він бачив, на що бот свариться
    bot.reply_to(
        message, 
        "Вибачте, я не розумію цей запит. Будь ласка, скористайтеся кнопками меню.\n"
        "Якщо кнопки зникли — напишіть /start"
    )

if __name__ == '__main__':
    bot.infinity_polling()
