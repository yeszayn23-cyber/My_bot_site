import telebot
from telebot import types

# --- حط التوكن تاعك هنا ---
TOKEN = '8000457608:AAEmrrhrKUf1-qRM-JDR1Ux8db3ia_v3zKw'
# --- حط المعرف تاعك (ID) باش تخرجلك لوحة التحكم ---
ADMIN_ID = 8421694319 # معرف التليجرام الخاص بك [cite: 2026-02-13]

bot = telebot.TeleBot(TOKEN)

# تخزين البيانات (في الواقع يفضل قاعدة بيانات، لكن هنا للسهولة في ملفات نصية)
channels = [] # قائمة القنوات
welcome_msg = "مرحباً بك في البوت!" # رسالة الترحيب الافتراضية

# دالة للتحقق من الاشتراك الإجباري
def is_subscribed(user_id):
    for ch in channels:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']:
                return False
        except:
            continue # إذا كان البوت ليس أدمن في القناة يتخطاها
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    # إذا كان المستخدم هو الأدمن
    if user_id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📢 إدارة القنوات", "📝 رسالة الترحيب")
        markup.add("📊 الإحصائيات")
        bot.send_message(message.chat.id, "أهلاً بك يا مطور.. اختر من اللوحة:", reply_markup=markup)
        return

    # للغاشي (المستخدمين)
    if not is_subscribed(user_id):
        markup = types.InlineKeyboardMarkup()
        for ch in channels:
            markup.add(types.InlineKeyboardButton(f"الاشتراك في {ch}", url=f"https://t.me/{ch[1:]}"))
        markup.add(types.InlineKeyboardButton("تحقق من الاشتراك ✅", callback_data="check"))
        bot.send_message(message.chat.id, "⚠️ عذراً، يجب عليك الاشتراك في القنوات أولاً لتشغيل البوت:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, welcome_msg)

# معالج لوحة التحكم للأدمن
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def admin_panel(message):
    global welcome_msg
    if message.text == "📢 إدارة القنوات":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ إضافة قناة", callback_data="add_ch"), 
                   types.InlineKeyboardButton("❌ حذف قناة", callback_data="del_ch"))
        msg = "قائمة القنوات الحالية:\n" + "\n".join(channels) if channels else "لا توجد قنوات حالياً."
        bot.send_message(message.chat.id, msg, reply_markup=markup)
        
    elif message.text == "📝 رسالة الترحيب":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✍️ تعديل", callback_data="edit_welcome"), 
                   types.InlineKeyboardButton("🗑️ حذف", callback_data="reset_welcome"))
        bot.send_message(message.chat.id, f"رسالة الترحيب الحالية:\n\n{welcome_msg}", reply_markup=markup)

# التعامل مع الأزرار (Callback Queries)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "check":
        if is_subscribed(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ شكراً لاشتراكك!")
            bot.edit_message_text(welcome_msg, call.message.chat.id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "❌ مازلت غير مشترك!", show_alert=True)
            
    elif call.data == "add_ch":
        msg = bot.send_message(call.message.chat.id, "أرسل معرف القناة الآن (مثال: @channel):")
        bot.register_next_step_handler(msg, save_channel)
        
    elif call.data == "edit_welcome":
        msg = bot.send_message(call.message.chat.id, "أرسل رسالة الترحيب الجديدة:")
        bot.register_next_step_handler(msg, save_welcome)

def save_channel(message):
    if message.text.startswith('@'):
        channels.append(message.text)
        bot.send_message(message.chat.id, f"✅ تم إضافة {message.text}")
    else:
        bot.send_message(message.chat.id, "❌ خطأ! المعرف يجب أن يبدأ بـ @")

def save_welcome(message):
    global welcome_msg
    welcome_msg = message.text
    bot.send_message(message.chat.id, "✅ تم تحديث رسالة الترحيب.")

bot.infinity_polling()
