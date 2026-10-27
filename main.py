import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask uygulaması
flask_app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8886446926:AAFUBRKk6qDUvQi1dsneaFQXkUIKBz-sGgg")
WEB_APP_URL = "https://kasa-hesaplayici.onrender.com"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")

# Global Telegram application nesnesi
telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Kasa Takip Mini App", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📊 *Arbitraj Kasa Takip Sistemi*\n\n"
        "İşlem yapmak için aşağıdaki butona tıklayabilirsin:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

telegram_app.add_handler(CommandHandler("start", start))

@flask_app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, telegram_app.bot)
    
    async def process():
        await telegram_app.process_update(update)

    asyncio.run(process())
    return "OK", 200

@flask_app.route("/")
def index():
    return "Bot Webhook Sunucusu Aktif!", 200

if __name__ == "__main__":
    async def main_setup():
        await telegram_app.initialize()
        import urllib.request
        # Render otomatik URL vermezse fallback olarak burayı kullanabiliriz
        ext_url = RENDER_EXTERNAL_URL if RENDER_EXTERNAL_URL else "https://telegram-kasa-bot.onrender.com"
        webhook_url = f"{ext_url}/{BOT_TOKEN}"
        set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}"
        try:
            urllib.request.urlopen(set_webhook_url)
            print("Webhook başarıyla Telegram'a tanımlandı!")
        except Exception as e:
            print(f"Webhook tanımlama hatası: {e}")

    asyncio.run(main_setup())

    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
