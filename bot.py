import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
DB_PATH = os.environ.get("DATABASE_PATH", "zyvarqo.db")

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛍 Marketplace", callback_data="marketplace"),
         InlineKeyboardButton("🧰 Services", callback_data="services")],
        [InlineKeyboardButton("👤 My Account", callback_data="account"),
         InlineKeyboardButton("📦 My Orders", callback_data="orders")],
        [InlineKeyboardButton("🎁 Referrals", callback_data="referrals"),
         InlineKeyboardButton("💬 Support", callback_data="support")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, username, first_name) VALUES (?, ?, ?)",
            (user.id, user.username, user.first_name)
        )
    await update.message.reply_text(
        f"Welcome to Zyvarqo, {user.first_name}! 🚀\n\n"
        "Explore products and services, manage your requests, or contact our team.",
        reply_markup=main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use /start to open the main menu. Choose Support to send our team a message."
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    messages = {
        "marketplace": "🛍 Marketplace\n\nOur product catalogue is being prepared. Please check back soon.",
        "services": "🧰 Services\n\nOur services directory is being prepared. Please check back soon.",
        "account": "👤 Your account\n\nYou are registered with Zyvarqo. More account features are coming soon.",
        "orders": "📦 My Orders\n\nYou don't have any orders recorded yet.",
        "referrals": "🎁 Referrals\n\nYour personal referral programme is coming soon. Please don't share payment or login details.",
        "support": "💬 Support\n\nReply to this message with your question. Our team will review it.",
    }
    if query.data == "support":
        context.user_data["awaiting_support"] = True
    await query.edit_message_text(messages.get(query.data, "Please choose an option."), reply_markup=main_menu())

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_support"):
        user = update.effective_user
        message = update.message.text
        context.user_data["awaiting_support"] = False
        if ADMIN_ID:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Zyvarqo support message from {user.full_name} "
                     f"(Telegram ID: {user.id}, username: @{user.username or 'none'}):\n\n{message}"
            )
            await update.message.reply_text("Thank you. Your message has been sent to Zyvarqo support.")
        else:
            await update.message.reply_text(
                "Thanks for contacting Zyvarqo. Support messaging is not connected yet."
            )
    else:
        await update.message.reply_text("Please use /start to open the Zyvarqo menu.")

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ADMIN_ID or update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("This command is for the bot administrator.")
        return
    with sqlite3.connect(DB_PATH) as db:
        count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    await update.message.reply_text(f"Zyvarqo admin summary\nRegistered users: {count}")

def main():
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Zyvarqo Assistant is running.")
    app.run_polling()

if __name__ == "__main__":
    main()
