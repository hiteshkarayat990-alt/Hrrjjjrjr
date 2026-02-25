import os
import json
import qrcode
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters, ConversationHandler
)
import asyncio
import logging

# ================= CONFIG =================
BOT_TOKEN = "8746668065:AAEWM2PZh8XdquEb_6gB4AAU16-NxkDrlVU"
ADMIN_ID = 6493020320
ADMIN_USERNAME = "ITz_Hitesh"
GROUP_LINK = "https://t.me/+wSZCqe1cVctiMjY1"
UPI_ID = "hiteshkarayat49@oksbi"
NAME = "Hitesh Group"

QR_PATH = "qr.png"
LOGO_FILE = "phonepe.png"   # optional
USERS_FILE = "users.json"

pending_users = {}

# ================= LOGGING =================
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ================= QR GENERATE =================
def generate_qr():
    upi = f"upi://pay?pa={UPI_ID}&pn={NAME}&cu=INR"
    qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(upi)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    if os.path.exists(LOGO_FILE):
        try:
            logo = Image.open(LOGO_FILE).resize((80, 80))
            w, h = img.size
            img.paste(logo, ((w-80)//2, (h-80)//2))
        except Exception as e:
            logging.error(f"Logo paste failed: {e}")
    img.save(QR_PATH)

# ================= STORAGE =================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_user(uid):
    users = load_users()
    if uid not in users:
        users.append(uid)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    keyboard = [
        [InlineKeyboardButton("💰 Buy Premium", callback_data="buy")],
        [InlineKeyboardButton("💵 Price Details", callback_data="price")],
        [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_USERNAME}")]
    ]
    text = (
        "👋 Welcome to Premium Bot!\n\n"
        "Kya aap Premium lena chahte hain? 💸\n\n"
        "💎 GROUP ENTRY PRICE\n"
        "₹99 (Lifetime)\n\n"
        "📩 Payment karke screenshot bot ko bhejo\n"
        "🔥 DAILY 1K+ videos\n"
        f"👤 Admin: @{ADMIN_USERNAME}\n\n"
        "👇 Buttons se choose karo 👇"
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ================= CALLBACK =================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    try:
        if q.data == "buy":
            generate_qr()
            with open(QR_PATH, "rb") as f:
                await context.bot.send_photo(
                    q.message.chat_id,
                    photo=f,
                    caption=(
                        "💸 Payment QR\n\n"
                        f"UPI ID: {UPI_ID}\n"
                        "Amount Pay According To Your category \n\n"
                        "Payment ke baad 👇 button dabaye"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("📸 I've Paid", callback_data="paid")]]
                    )
                )
        elif q.data == "price":
            await context.bot.send_message(
                q.message.chat_id,
                "📢 AGAR AAP GROUP ME JOIN HONA CHAHATE HO TO PAYMENT KARNA PADEGA\n\n"
                "Adult+18 → ₹79\n"
                "Choti bachi → ₹199\n"
                "M@m son sis → ₹99\n\n"
                "All category vid@eo → ₹249\n\n"
                "50k+ videos lifetime entry\n"
                "Agar payment kar sakte ho tabhi reply dena sir..?"
            )
        elif q.data == "paid":
            pending_users[q.from_user.id] = True
            await context.bot.send_message(q.from_user.id, "📸 Ab payment ka screenshot bhejo")
        elif q.data.startswith("confirm"):
            uid = int(q.data.split(":")[1])
            await context.bot.send_message(uid, f"✅ Payment Approved\n\n👉 {GROUP_LINK}")
            await q.edit_message_caption("✔ Payment Approved")
        elif q.data.startswith("reject"):
            uid = int(q.data.split(":")[1])
            await context.bot.send_message(uid, "❌ Payment Rejected. Admin se contact karo.")
            await q.edit_message_caption("❌ Payment Rejected")
    except Exception as e:
        logging.error(f"Callback error: {e}")

# ================= SCREENSHOT =================
async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in pending_users:
        return
    keyboard = [[
        InlineKeyboardButton("✔ Confirm", callback_data=f"confirm:{uid}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject:{uid}")
    ]]
    await context.bot.send_photo(
        ADMIN_ID,
        update.message.photo[-1].file_id,
        caption=f"📩 Payment from {update.effective_user.first_name} ({uid})",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await context.bot.send_message(uid, "⏳ Admin verification pending")

# ================= BROADCAST =================
WAIT_BROADCAST = 1

async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("📢 Broadcast ke liye message / photo / video bhejo")
    return WAIT_BROADCAST

async def broadcast_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_users()
    sent = 0
    blocked = []

    tasks = []

    for uid in users:
        try:
            if update.message.text:
                tasks.append(context.bot.send_message(uid, update.message.text))
            elif update.message.photo:
                tasks.append(context.bot.send_photo(uid, update.message.photo[-1].file_id, caption=update.message.caption or ""))
            elif update.message.video:
                tasks.append(context.bot.send_video(uid, update.message.video.file_id, caption=update.message.caption or ""))
            sent += 1
        except Exception as e:
            blocked.append(uid)
            logging.error(f"Broadcast error for {uid}: {e}")

    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)

    await context.bot.send_message(
        ADMIN_ID,
        f"✅ Broadcast Done\nSent: {sent}\nBlocked: {len(blocked)}"
    )
    return ConversationHandler.END

# ================= RUN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    conv = ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast_start)],
        states={WAIT_BROADCAST: [MessageHandler(filters.ALL, broadcast_send)]},
        fallbacks=[]
    )
    app.add_handler(conv)

    print("🔥 Baba ka script start ho gaya")
    app.run_polling()

if __name__ == "__main__":
    main()