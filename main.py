import os
import logging
import asyncio
from flask import Flask, request, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask uygulaması
flask_app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8886446926:AAFUBRKk6qDUvQi1dsneaFQXkUIKBz-sGgg")
WEB_APP_URL = "https://telegram-kasa-bot.onrender.com"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")

telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Kasa & Arbitraj PRO", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📊 *Kasa & Arbitraj PRO Yönetim Sistemi*\n\n"
        "Gelişmiş arayüze erişmek için aşağıdaki butona tıklayabilirsin:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

telegram_app.add_handler(CommandHandler("start", start))

# PRO HTML & Tailwind Arayüzü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Kasa & Arbitraj PRO</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root { --bg-color: #0f172a; --card-bg: #1e293b; --accent: #3b82f6; --text-main: #f8fafc; --text-muted: #94a3b8; }
        body { background-color: var(--bg-color); color: var(--text-main); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .card { background-color: var(--card-bg); }
    </style>
</head>
<body class="pb-24 p-4 max-w-lg mx-auto space-y-4">
    <header class="p-4 flex items-center justify-between border border-slate-800 card rounded-2xl shadow-lg">
        <div class="flex items-center gap-2">
            <span class="text-2xl">⚡</span>
            <div>
                <h1 class="font-bold text-base leading-tight">Kasa & Arbitraj PRO</h1>
                <p class="text-xs text-slate-400">Telegram Mini App Engine</p>
            </div>
        </div>
        <span class="text-xs px-2.5 py-1 bg-blue-500/20 text-blue-400 font-semibold rounded-full border border-blue-500/30">PRO</span>
    </header>

    <!-- Toplam Kasa Kartı ve Bakiye Düzenleme -->
    <div class="card p-5 rounded-2xl border border-slate-800 shadow-xl space-y-4 relative overflow-hidden">
        <div class="flex justify-between items-start">
            <div>
                <div class="text-xs font-medium text-slate-400">TOPLAM KASA</div>
                <div class="text-3xl font-extrabold text-white mt-1 cursor-pointer flex items-center gap-2" onclick="toggleEditBalance()">
                    <span id="displayBalance">₺10.000,00</span>
                    <span class="text-xs font-normal text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">Düzenle ✏️</span>
                </div>
            </div>
        </div>

        <!-- Gizli Düzenleme Alanı -->
        <div id="editBalanceBox" class="hidden pt-2 border-t border-slate-700 space-y-2">
            <label class="text-xs text-slate-400 block">Yeni Kasa Bakiyesini Gir:</label>
            <div class="flex gap-2">
                <input type="number" id="newBalanceInput" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-sm text-white" placeholder="10000">
                <button onclick="saveBalance()" class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-semibold transition">Kaydet</button>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-2 pt-2 border-t border-slate-800/80 text-xs">
            <div>
                <span class="text-slate-400 block">Hedef:</span>
                <span class="font-bold text-slate-200">₺20.000,00</span>
            </div>
            <div>
                <span class="text-slate-400 block">Bekleyen Risk:</span>
                <span class="font-bold text-amber-400">₺300,00</span>
            </div>
        </div>

        <div class="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 text-center">
            <div class="bg-slate-900/50 p-2 rounded-xl">
                <div class="text-[10px] text-slate-400">NET KÂR/ZARAR</div>
                <div class="text-xs font-bold text-emerald-400 mt-0.5">+₺0,00</div>
            </div>
            <div class="bg-slate-900/50 p-2 rounded-xl">
                <div class="text-[10px] text-slate-400">KAYIP BONUSU</div>
                <div class="text-xs font-bold text-blue-400 mt-0.5">₺75,00</div>
            </div>
            <div class="bg-slate-900/50 p-2 rounded-xl">
                <div class="text-[10px] text-slate-400">ROI DEĞERİ</div>
                <div class="text-xs font-bold text-purple-400 mt-0.5">%0.00</div>
            </div>
        </div>
    </div>

    <!-- Surebet Hesaplayıcı Modülü -->
    <div class="card p-4 rounded-xl border border-slate-800 space-y-3">
        <h3 class="text-sm font-bold flex items-center gap-1.5">⚡ 2 Yönlü Surebet Hesaplayıcı</h3>
        <div class="grid grid-cols-2 gap-2">
            <div>
                <label class="text-[11px] text-slate-400 block mb-1">1. Büro Oranı</label>
                <input type="number" id="calcOdds1" step="0.01" value="2.10" oninput="calculateSurebet()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-sm text-white">
            </div>
            <div>
                <label class="text-[11px] text-slate-400 block mb-1">2. Büro Oranı</label>
                <input type="number" id="calcOdds2" step="0.01" value="2.05" oninput="calculateSurebet()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-sm text-white">
            </div>
        </div>
        <div>
            <label class="text-[11px] text-slate-400 block mb-1">Toplam Bütçe (TRY)</label>
            <input type="number" id="calcTotalStake" value="1000" oninput="calculateSurebet()" class="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-sm text-white">
        </div>
        <div class="p-3 bg-slate-900 rounded-lg text-xs space-y-1.5 border border-slate-800">
            <div class="flex justify-between"><span>Büro 1 Stake:</span> <span id="resStake1" class="font-bold text-white">0.00 TRY</span></div>
            <div class="flex justify-between"><span>Büro 2 Stake:</span> <span id="resStake2" class="font-bold text-white">0.00 TRY</span></div>
            <div class="flex justify-between pt-1 border-t border-slate-800"><span>Garanti Net Kâr:</span> <span id="resNetProfit" class="font-extrabold text-emerald-400">+0.00 TRY</span></div>
        </div>
    </div>

    <script>
        const tg = window.Telegram?.WebApp;
        if (tg) tg.expand();

        function toggleEditBalance() {
            const box = document.getElementById('editBalanceBox');
            box.classList.toggle('hidden');
        }

        function saveBalance() {
            const val = parseFloat(document.getElementById('newBalanceInput').value);
            if (!isNaN(val)) {
                document.getElementById('displayBalance').innerText = '₺' + val.toLocaleString('tr-TR', {minimumFractionDigits: 2});
                toggleEditBalance();
            }
        }

        function calculateSurebet() {
            const o1 = parseFloat(document.getElementById('calcOdds1').value) || 0;
            const o2 = parseFloat(document.getElementById('calcOdds2').value) || 0;
            const totalStake = parseFloat(document.getElementById('calcTotalStake').value) || 0;
            if (o1 <= 1 || o2 <= 1 || totalStake <= 0) return;
            const arbPercent = (1/o1) + (1/o2);
            const stake1 = (totalStake * (1/o1)) / arbPercent;
            const stake2 = (totalStake * (1/o2)) / arbPercent;
            const netProfit = (stake1 * o1) - totalStake;
            document.getElementById('resStake1').innerText = stake1.toFixed(2) + ' TRY';
            document.getElementById('resStake2').innerText = stake2.toFixed(2) + ' TRY';
            document.getElementById('resNetProfit').innerText = '+' + netProfit.toFixed(2) + ' TRY';
        }
        window.onload = calculateSurebet;
    </script>
</body>
</html>
"""

@flask_app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@flask_app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json(force=True)
    update = Update.de_json(json_update, telegram_app.bot)
    
    async def process():
        await telegram_app.process_update(update)

    asyncio.run(process())
    return "OK", 200

if __name__ == "__main__":
    async def main_setup():
        await telegram_app.initialize()
        import urllib.request
        ext_url = RENDER_EXTERNAL_URL if RENDER_EXTERNAL_URL else WEB_APP_URL
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
