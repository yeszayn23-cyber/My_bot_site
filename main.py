import telebot
from telebot import types

# --- البيانات الأساسية (التوكن والآيدي الخاص بكِ) ---
TOKEN = '8000457608:AAEmrrhrKUf1-qRM-JDR1Ux8db3ia_v3zKw'
ADMIN_ID = 8421694319 
bot = telebot.TeleBot(TOKEN)

# مخزن المعلومات (سيتم تعبئته من داخل التيليجرام)
data = {
    'welcome': "مرحباً بكِ في بوت الله أولاً 🤍",
    'channel': "", 
    'idea': "سيتم كتابة فكرة البوت هنا قريباً."
}

def check_sub(uid):
    if not data['channel']: return True
    try:
        status = bot.get_chat_member(data['channel'], uid).status
        return status in ['creator', 'administrator', 'member']
    except: return True

@bot.message_handler(commands=['admin'], func=lambda m: m.from_user.id == ADMIN_ID)
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📝 وضع رسالة ترحيب", callback_data="set_w"),
        types.InlineKeyboardButton("📢 وضع معرف القناة (@...)", callback_data="set_c"),
        types.InlineKeyboardButton("💡 وضع فكرة البوت", callback_data="set_i")
    )
    bot.send_message(message.chat.id, "🛠 **أهلاً بكِ في لوحة التحكم:**", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("💡 فكرة البوت", "📖 فتح التطبيق")
        bot.send_message(message.chat.id, data['welcome'], reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("اشترك في القناة أولاً 📢", url=f"https://t.me/{data['channel'].replace('@','')}")
        markup.add(btn)
        bot.send_message(message.chat.id, "⚠️ يرجى الاشتراك في القناة لتفعيل البوت.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.from_user.id == ADMIN_ID)
def handle_calls(call):
    prompts = {"set_w": "أرسلي الآن رسالة الترحيب:", "set_c": "أرسلي معرف القناة (مثل @allahfirst):", "set_i": "أرسلي نص فكرة البوت:"}
    msg = bot.send_message(call.message.chat.id, prompts[call.data])
    bot.register_next_step_handler(msg, globals()[f"save_{call.data.split('_')[1]}"])

def save_w(m): data['welcome'] = m.text; bot.send_message(m.chat.id, "✅ تم الحفظ")
def save_c(m): data['channel'] = m.text; bot.send_message(m.chat.id, "✅ تم الربط")
def save_i(m): data['idea'] = m.text; bot.send_message(m.chat.id, "✅ تم الحفظ")

@bot.message_handler(func=lambda m: m.text == "💡 فكرة البوت")
def show_idea(m): bot.send_message(m.chat.id, data['idea'])

bot.polling()
