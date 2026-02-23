!pip install pyTelegramBotAPI

import telebot
from telebot import types

# --- البيانات الخاصة بك ---
TOKEN = '8000457608:AAEmrrhrKUf1-qRM-JDR1Ux8db3ia_v3zKw'
ADMIN_ID = 8421694319  # معرف التليجرام الخاص بك [cite: 2026-02-13]

bot = telebot.TeleBot(TOKEN)

# تخزين البيانات في الذاكرة (للقنوات والترحيب)
data = {
    'channels': [],
    'welcome_msg': "مرحباً بك في البوت! راني خدام بيك يا خويا."
}

# دالة للتحقق من الاشتراك الإجباري
def check_sub(user_id):
    for ch in data['channels']:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            continue
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    # إذا كان المستخدم هو أنت (الأدمن)
    if user_id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📢 القنوات", "📝 الترحيب")
        bot.send_message(message.chat.id, "أهلاً بك يا مطور.. تحكم في بوتك الآن:", reply_markup=markup)
        return

    # للمستخدمين العاديين
    if not check_sub(user_id):
        markup = types.InlineKeyboardMarkup()
        for ch in data['channels']:
            markup.add(types.InlineKeyboardButton(f"اشترك هنا {ch}", url=f"https://t.me/{ch[1:]}"))
        markup.add(types.InlineKeyboardButton("تم الاشتراك ✅", callback_data="verify"))
        bot.send_message(message.chat.id, "⚠️ لازم تشترك في القنوات أولاً باش يخدم البوت:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, data['welcome_msg'])

# لوحة التحكم (للأدمن فقط)
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def admin_actions(message):
    if message.text == "📢 القنوات":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ إضافة قناة", callback_data="add"),
                   types.InlineKeyboardButton("❌ حذف الكل", callback_data="clear"))
        current = "\n".join(data['channels']) if data['channels'] else "لا توجد قنوات."
        bot.send_message(message.chat.id, f"قنوات الاشتراك الحالي:\n{current}", reply_markup=markup)
        
    elif message.text == "📝 الترحيب":
        msg = bot.send_message(message.chat.id, "أرسل رسالة الترحيب الجديدة:")
        bot.register_next_step_handler(msg, update_welcome)

def update_welcome(message):
    data['welcome_msg'] = message.text
    bot.send_message(message.chat.id, "✅ تم تحديث رسالة الترحيب بنجاح.")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "add":
        msg = bot.send_message(call.message.chat.id, "أرسل معرف القناة (مثال: @mychannel):")
        bot.register_next_step_handler(msg, save_ch)
    elif call.data == "clear":
        data['channels'] = []
        bot.answer_callback_query(call.id, "تم حذف جميع القنوات")
    elif call.data == "verify":
        if check_sub(call.from_user.id):
            bot.edit_message_text(data['welcome_msg'], call.message.chat.id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "❌ مازلت ماشتركتش!", show_alert=True)

def save_ch(message):
    if message.text.startswith('@'):
        data['channels'].append(message.text)
        bot.send_message(message.chat.id, f"✅ تمت إضافة {message.text}")
    else:
        bot.send_message(message.chat.id, "❌ خطأ! لازم المعرف يبدأ بـ @")

print(">>> البوت خدام ضرك.. روح جربو في تليجرام!")
bot.infinity_polling()
