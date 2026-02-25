import telebot
from telebot import types
import urllib.parse
bot = telebot.TeleBot('8345945744:AAGXc1Bl7nIFKQPTv_NciD39A1cGu0t2r-Q')
bot.set_my_commands([
    types.BotCommand("k", "K1ll Card"),
    types.BotCommand("profile", "Check Profile Info"),
    types.BotCommand("br", "B3 Auth"),
    types.BotCommand("chk", "Str!pe Auth"),
    types.BotCommand("plans", "Check Plans"),
    types.BotCommand("buy", "Buy Plan"),
    types.BotCommand("cmds", "Check Commands"),
    types.BotCommand("faq", "frequently asked questions"),
    types.BotCommand("make_payment", "Buy Plan")
])
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name or "User"
    welcome_text = (
        f"👋 <b>Hello, {user_name}!</b>\n\n"
        "I am your Multi-Tool Assistant. Here is what I can do:\n\n"
        "🛠 <b>Tools:</b> /chk, /br, /k\n"
        "👤 <b>Account:</b> /profile, /plans\n"
        "ℹ️ <b>Info:</b> /faq, /buy"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML" )


@bot.message_handler(commands=['k'])
def k(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🚀 Upgrade to Premium", callback_data="view_plans"))
    
    response_text = (
        "<b>Premium Killer Gateway</b> requires a paid plan.\n\n"
        "💳 <b>Your current plan:</b> Free\n\n"
        "To upgrade your plan and unlock this gateway, please use the /plans command or click below."
    )
    
    bot.send_message(
        message.chat.id, 
        f"{response_text}", 
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "N/A"
    
    profile_text = (
        "👤 <b>User Profile</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"<b>Name:</b> {first_name}\n"
        f"<b>Username:</b> {username}\n"
        f"<b>User ID:</b> <code>{user_id}</code>\n"
        "<b>Plan:</b> <pre>Free Tier</pre>\n"
        "<b>Credits:</b> 0\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💡 <i>Want more access? Use /plans to upgrade.</i>"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💎 Upgrade Now", callback_data="view_plans"))
    
    bot.send_message(
        message.chat.id, 
        profile_text, 
        parse_mode="HTML", 
        reply_markup=markup
    )



@bot.message_handler(commands=['br'])
def br(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💎 Get Premium Access", callback_data="view_plans"))
    
    denied_text = (
        "🚫 <b>Access Restricted</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "The <b>(/br)</b> gateway is a premium feature.\n\n"
        "👤 <b>Your Status:</b> <code>Free User</code>\n"
        "🔒 <b>Requirement:</b> <code>Premium Plan</code>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💡 <i>Premium users get unlimited access to all gateways, faster speeds, and 24/7 support.</i>"
    )
    
    bot.send_message(
        message.chat.id, 
        denied_text, 
        parse_mode="HTML", 
        reply_markup=markup
    )



@bot.message_handler(commands=['chk'])
def chk(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💎 Get Premium Access", callback_data="view_plans"))
    
    denied_text = (
        "🚫 <b>Access Restricted</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "The <b>(/chk)</b> gateway is a premium feature.\n\n"
        "👤 <b>Your Status:</b> <code>Free User</code>\n"
        "🔒 <b>Requirement:</b> <code>Premium Plan</code>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💡 <i>Premium users get unlimited access to all gateways, faster speeds, and 24/7 support.</i>"
    )
    
    bot.send_message(
        message.chat.id, 
        denied_text, 
        parse_mode="HTML", 
        reply_markup=markup
    )






@bot.message_handler(commands=['plans', 'buy'])
def plans(message):
    owner_username = "ITz_Hitesh" 
    
    p50_msg = urllib.parse.quote("Hello! I want to buy the 1000 Credits Plan ($50).")
    p65_msg = urllib.parse.quote("Hello! I want to buy the 2050 Credits Plan ($65).")
    p100_msg = urllib.parse.quote("Hello! I want to buy the 4159 Credits Plan ($100).")
    p150_msg = urllib.parse.quote("Hello! I want to buy the Unlimited 5k Credits Plan ($150).")

    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_1 = types.InlineKeyboardButton("💳 Buy 1000 Credits ($50)", url=f"https://t.me/{owner_username}?text={p50_msg}")
    btn_2 = types.InlineKeyboardButton("💳 Buy 2050 Credits ($65)", url=f"https://t.me/{owner_username}?text={p65_msg}")
    btn_3 = types.InlineKeyboardButton("💳 Buy 4159 Credits ($100)", url=f"https://t.me/{owner_username}?text={p100_msg}")
    btn_4 = types.InlineKeyboardButton("♾️ Buy 5k Credits ($150)", url=f"https://t.me/{owner_username}?text={p150_msg}")
    
    markup.add(btn_1, btn_2, btn_3, btn_4)

    # 4. Your specific text layout
    plan_text = (
        "<b>Available Plans</b>\n\n"
        "⏳ <b>25 DAYS PLANS</b>\n"
        " \n"
        " ► 1000 Credits - PLAN 50$\n"
        " ► 2050 Credits - PLAN 65$\n"
        " ► 4159 Credits - PLAN 100$\n\n"
        "<b>𝗨𝗻𝗹𝗶𝗺𝗶𝘁𝗲𝗱 𝗣𝗹𝗮𝗻</b>\n\n"
        "♾️ <b>DAYS PLANS</b>\n"
        " ► 5k Credits - PLAN 150$\n\n"
        "<b>Credits Usage</b>\n\n"
        "  ► CC K!ls - 5 Credits\n"
        "  ► CC Checker - 2 Credits\n\n"
        "⚠️ Read FAQs and Rules Before Purchasing - /faq\n"
        "💵 Click /make_payment to proceed"
    )

    bot.send_message(message.chat.id, plan_text, parse_mode="HTML", reply_markup=markup)


@bot.message_handler(commands=['cmds'])
def cmds(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💎 View Premium Plans", callback_data="view_plans"))
    
    commands_text = (
        "📜 <b>Bot Command Menu</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "🛠 <b>Tools & Gateways</b>\n"
        "├ /chk - <i>Single Checker</i>\n"
        "├ /br - <i>Bulk Roller (Premium)</i>\n"
        "└ /k - <i>Killer Gateway (Premium)</i>\n\n"
        "👤 <b>User Management</b>\n"
        "├ /profile - <i>Check your status</i>\n"
        "├ /plans - <i>Pricing & Features</i>\n"
        "└ /buy - <i>Purchase access</i>\n\n"
        "ℹ️ <b>Information</b>\n"
        "├ /faq - <i>Common Questions</i>\n"
        "└ /cmds - <i>Show this menu</i>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "👇 <b>Need full access? Click below!</b>"
    )
    
    bot.send_message(
        message.chat.id, 
        commands_text, 
        parse_mode="HTML", 
        reply_markup=markup
    )

@bot.message_handler(commands=['faq'])
def faq(message):
    owner_username = "ITz_Hitesh"
    support_msg = urllib.parse.quote("Hello! I have a question regarding the bot.")

    markup = types.InlineKeyboardMarkup()
    btn_support = types.InlineKeyboardButton("👨‍💻 Contact Support", url=f"https://t.me/{owner_username}?text={support_msg}")
    markup.add(btn_support)

    faq_text = (
        "❓ <b>Frequently Asked Questions</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "<b>1️⃣ How do I get Premium?</b>\n"
        "Go to /plans, select your preferred plan, and contact the owner to complete the payment.\n\n"
        "<b>2️⃣ Which payment methods are accepted?</b>\n"
        "We currently accept <b>BTC, LTC, and USDT (TRC20)</b>. For other methods, contact support.\n\n"
        "<b>3️⃣ Why is /k or /br not working?</b>\n"
        "These are <b>Premium Gateways</b>. You must have an active subscription to use them. Check your status in /profile.\n\n"
        "<b>4️⃣ How long does activation take?</b>\n"
        "Once payment is confirmed, activation is usually instant or within 30 minutes.\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "<b>Still have questions?</b> Click below to chat with us!"
    )

    bot.send_message(
        message.chat.id, 
        faq_text, 
        parse_mode="HTML", 
        reply_markup=markup
    )

@bot.message_handler(commands=['make_payment'])
def make_payment(message):
    owner_username = "ITz_Hitesh"
    paid_msg = urllib.parse.quote("Hello! I have just sent the payment. Please verify my transaction.")

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_paid = types.InlineKeyboardButton("✅ I have Sent Payment", url=f"https://t.me/{owner_username}?text={paid_msg}")
    btn_cancel = types.InlineKeyboardButton("❌ Cancel", callback_data="cancel_payment")
    markup.add(btn_paid, btn_cancel)

    payment_text = (
        "💳 <b>Payment Information</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "To upgrade your account, please send the exact amount to one of the addresses below:\n\n"
        
        "🟠 <b>Bitcoin (BTC):</b>\n"
        "<code>bc1qynrz73p4jtlvuhdrn2csk2mrmcc32leg25yv09</code>\n\n"
        
        "🔵 <b>Litecoin (LTC):</b>\n"
        "<code>Ladcekr66VtmT2VayJM4YS4rL5M4KxFU1b</code>\n\n"
        
        "🟢 <b>USDT (TRC20):</b>\n"
        "<code>TDPfzdGBkkXfuTgbPp7NcUKgK1qenzvt3i</code>\n\n"
        
        "━━━━━━━━━━━━━━━━━━\n"
        "⚠️ <b>Important:</b>\n"
        "1. Send only the supported coin to its network.\n"
        "2. After sending, click the button below to send a screenshot/hash to the owner."
    )

    bot.send_message(
        message.chat.id, 
        payment_text, 
        parse_mode="HTML", 
        reply_markup=markup
    )


if __name__ == '__main__':
    bot.polling()
    print("Bot is running...")