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

# Tam Kapsamlı PRO HTML & CSS & JS Arayüzü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Kasa & Arbitraj PRO</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 50: '#eff6ff', 100: '#dbeafe', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8' },
                        darkbg: '#0b0f17',
                        cardbg: '#151c28',
                        cardborder: '#212d40'
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #0b0f17; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; -webkit-tap-highlight-color: transparent; }
        .tab-btn.active { background-color: #2563eb; color: #ffffff; font-weight: 600; shadow: 0 4px 12px rgba(37,99,235,0.3); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body class="pb-28 p-3 max-w-lg mx-auto space-y-4">

    <!-- Üst Header -->
    <header class="p-3.5 flex items-center justify-between border border-slate-800 bg-[#151c28] rounded-2xl shadow-xl">
        <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-blue-600/20 text-blue-500 border border-blue-500/30 flex items-center justify-center font-bold text-sm">TMA</div>
            <div>
                <h1 class="font-bold text-sm tracking-wide text-white">Kasa & Arbitraj PRO</h1>
                <p class="text-[11px] text-slate-400">Telegram Mini App Engine</p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <button onclick="exportToExcel()" class="text-xs px-2.5 py-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 font-semibold rounded-lg border border-emerald-500/30 flex items-center gap-1.5 transition">
                <i class="fa-solid fa-file-excel"></i> Excel İndir
            </button>
            <span class="text-xs px-2 py-1 bg-slate-800 text-slate-300 font-semibold rounded-lg border border-slate-700">₺ TRY</span>
        </div>
    </header>

    <!-- Toplam Kasa Kartı (Bakiye Düzenleme Modallı) -->
    <div class="bg-[#151c28] p-5 rounded-2xl border border-slate-800 shadow-xl space-y-4 relative overflow-hidden">
        <div class="flex justify-between items-start">
            <div class="space-y-1">
                <div class="text-[11px] font-semibold text-slate-400 tracking-wider flex items-center gap-1.5">
                    <i class="fa-solid fa-wallet text-slate-400"></i> TOPLAM KASA
                </div>
                <div class="text-3xl font-black text-white tracking-tight flex items-center gap-2">
                    <span id="displayBalance">₺10.000,00</span>
                </div>
            </div>
            <button onclick="openBalanceModal()" class="text-xs bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-xl border border-slate-700/80 flex items-center gap-1.5 font-medium transition active:scale-95">
                <i class="fa-solid fa-pen-to-square text-blue-400"></i> Düzenle
            </button>
        </div>

        <div class="grid grid-cols-2 gap-2 pt-3 border-t border-slate-800/80 text-xs">
            <div>
                <span class="text-slate-400 block text-[11px]">Hedef:</span>
                <span id="displayGoal" class="font-bold text-slate-200">₺20.000,00</span>
            </div>
            <div class="text-right">
                <span class="text-slate-400 block text-[11px]">Bekleyen Risk:</span>
                <span id="displayRisk" class="font-bold text-amber-400">₺300,00</span>
            </div>
        </div>

        <div class="grid grid-cols-3 gap-2 pt-3 border-t border-slate-800/80 text-center">
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">NET KÂR/ZARAR</div>
                <div id="displayNetProfit" class="text-xs font-black text-emerald-400 mt-1">+₺0,00</div>
            </div>
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">KAYIP BONUSU</div>
                <div id="displayBonus" class="text-xs font-black text-blue-400 mt-1">₺75,00</div>
            </div>
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">ROI DEĞERİ</div>
                <div id="displayROI" class="text-xs font-black text-purple-400 mt-1">%0.00</div>
            </div>
        </div>
    </div>

    <!-- Sekme Navigasyonu -->
    <div class="grid grid-cols-2 gap-1.5 p-1 bg-slate-900/80 rounded-xl border border-slate-800">
        <button id="tabBtn1" onclick="switchTab('arb')" class="tab-btn active py-2 text-xs font-semibold rounded-lg text-slate-400 transition">
            Arbitraj (Surebet)
        </button>
        <button id="tabBtn2" onclick="switchTab('kelly')" class="tab-btn py-2 text-xs font-semibold rounded-lg text-slate-400 transition">
            Kelly / Oran Stake
        </button>
    </div>

    <!-- TAB 1: ARB / SUREBET HESAPLAYICI -->
    <div id="tabArb" class="tab-content active space-y-3">
        <div class="bg-[#151c28] p-4 rounded-2xl border border-slate-800 space-y-3 shadow-lg">
            <div class="flex justify-between items-center">
                <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-bolt text-amber-400"></i> 2 Yönlü Surebet Matriksi
                </h3>
                <span id="arbStatus" class="text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Fırsat Var</span>
            </div>

            <div class="grid grid-cols-2 gap-2">
                <div>
                    <label class="text-[10px] font-semibold text-slate-400 block mb-1">1. Büro Oranı</label>
                    <input type="number" id="arbOdds1" step="0.01" value="2.10" oninput="recalcArb()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
                </div>
                <div>
                    <label class="text-[10px] font-semibold text-slate-400 block mb-1">2. Büro Oranı</label>
                    <input type="number" id="arbOdds2" step="0.01" value="2.05" oninput="recalcArb()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
                </div>
            </div>

            <div>
                <label class="text-[10px] font-semibold text-slate-400 block mb-1">Toplam Yatırılacak Bütçe (TRY)</label>
                <input type="number" id="arbTotalStake" value="1000" oninput="recalcArb()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
            </div>

            <div class="p-3 bg-slate-900/80 rounded-xl text-xs space-y-2 border border-slate-800">
                <div class="flex justify-between items-center text-slate-300">
                    <span>1. Büro Stake:</span>
                    <span id="arbStake1" class="font-bold text-white">₺506,02</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                    <span>2. Büro Stake:</span>
                    <span id="arbStake2" class="font-bold text-white">₺493,98</span>
                </div>
                <div class="flex justify-between items-center pt-2 border-t border-slate-800 font-bold">
                    <span class="text-slate-300">Garanti Net Kâr:</span>
                    <span id="arbProfit" class="text-emerald-400 font-extrabold">+₺62,65 (%6.27)</span>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: KELLY / ORAN STAKE HESAPLAYICI -->
    <div id="tabKelly" class="tab-content space-y-3">
        <div class="bg-[#151c28] p-4 rounded-2xl border border-slate-800 space-y-3 shadow-lg">
            <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                <i class="fa-solid fa-calculator text-blue-400"></i> Kelly Kriteri & Risk Yönetimi
            </h3>

            <div>
                <label class="text-[10px] font-semibold text-slate-400 block mb-1">Bahis Oranı (Odds)</label>
                <input type="number" id="kellyOdds" step="0.01" value="2.20" oninput="recalcKelly()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
            </div>

            <div>
                <label class="text-[10px] font-semibold text-slate-400 block mb-1">Tahmini Kazanma İhtimali (%)</label>
                <input type="number" id="kellyWinProb" value="55" oninput="recalcKelly()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
            </div>

            <div class="p-3 bg-slate-900/80 rounded-xl text-xs space-y-2 border border-slate-800">
                <div class="flex justify-between items-center text-slate-300">
                    <span>Önerilen Kelly Kasa Oranı:</span>
                    <span id="kellyFraction" class="font-bold text-blue-400">%17.50</span>
                </div>
                <div class="flex justify-between items-center pt-2 border-t border-slate-800 font-bold">
                    <span class="text-slate-300">Önerilen Stake (TRY):</span>
                    <span id="kellyStake" class="text-emerald-400 font-extrabold">₺1.750,00</span>
                </div>
            </div>
        </div>
    </div>

    <!-- BAKİYE DÜZENLEME MODALI -->
    <div id="balanceModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-[#151c28] w-full max-w-sm rounded-2xl border border-slate-800 p-5 space-y-4 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-blue-500"></i> Kasa Parametreleri
                </h3>
                <button onclick="closeBalanceModal()" class="text-slate-400 hover:text-white text-base"><i class="fa-solid fa-xmark"></i></button>
            </div>

            <div class="space-y-3 text-xs">
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Mevcut Toplam Kasa (TRY)</label>
                    <input type="number" id="inputBalance" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Hedef Kasa (TRY)</label>
                    <input type="number" id="inputGoal" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Bekleyen Risk (TRY)</label>
                    <input type="number" id="inputRisk" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Kayıp Bonusu (TRY)</label>
                    <input type="number" id="inputBonus" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
            </div>

            <div class="flex gap-2 pt-2 border-t border-slate-800">
                <button onclick="closeBalanceModal()" class="w-1/2 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition">İptal</button>
                <button onclick="saveBalanceModal()" class="w-1/2 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-lg shadow-blue-600/30">Kaydet</button>
            </div>
        </div>
    </div>

    <script>
        const tg = window.Telegram?.WebApp;
        if (tg) tg.expand();

        let state = {
            balance: 10000,
            goal: 20000,
            risk: 300,
            netProfit: 0,
            bonus: 75,
            roi: 0
        };

        function fmt(num) {
            return '₺' + num.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }

        function updateUI() {
            document.getElementById('displayBalance').innerText = fmt(state.balance);
            document.getElementById('displayGoal').innerText = fmt(state.goal);
            document.getElementById('displayRisk').innerText = fmt(state.risk);
            document.getElementById('displayNetProfit').innerText = (state.netProfit >= 0 ? '+' : '') + fmt(state.netProfit);
            document.getElementById('displayBonus').innerText = fmt(state.bonus);
            document.getElementById('displayROI').innerText = '%' + state.roi.toFixed(2);
        }

        function switchTab(tab) {
            document.getElementById('tabArb').classList.remove('active');
            document.getElementById('tabKelly').classList.remove('active');
            document.getElementById('tabBtn1').classList.remove('active');
            document.getElementById('tabBtn2').classList.remove('active');

            if (tab === 'arb') {
                document.getElementById('tabArb').classList.add('active');
                document.getElementById('tabBtn1').classList.add('active');
            } else {
                document.getElementById('tabKelly').classList.add('active');
                document.getElementById('tabBtn2').classList.add('active');
            }
        }

        function openBalanceModal() {
            document.getElementById('inputBalance').value = state.balance;
            document.getElementById('inputGoal').value = state.goal;
            document.getElementById('inputRisk').value = state.risk;
            document.getElementById('inputBonus').value = state.bonus;
            document.getElementById('balanceModal').classList.remove('hidden');
        }

        function closeBalanceModal() {
            document.getElementById('balanceModal').classList.add('hidden');
        }

        function saveBalanceModal() {
            state.balance = parseFloat(document.getElementById('inputBalance').value) || 0;
            state.goal = parseFloat(document.getElementById('inputGoal').value) || 0;
            state.risk = parseFloat(document.getElementById('inputRisk').value) || 0;
            state.bonus = parseFloat(document.getElementById('inputBonus').value) || 0;
            updateUI();
            recalcKelly();
            closeBalanceModal();
        }

        function recalcArb() {
            const o1 = parseFloat(document.getElementById('arbOdds1').value) || 0;
            const o2 = parseFloat(document.getElementById('arbOdds2').value) || 0;
            const total = parseFloat(document.getElementById('arbTotalStake').value) || 0;

            if (o1 <= 1 || o2 <= 1 || total <= 0) return;

            const arb = (1 / o1) + (1 / o2);
            const s1 = (total * (1 / o1)) / arb;
            const s2 = (total * (1 / o2)) / arb;
            const profit = (s1 * o1) - total;
            const profitPct = (profit / total) * 100;

            document.getElementById('arbStake1').innerText = fmt(s1);
            document.getElementById('arbStake2').innerText = fmt(s2);

            const profitEl = document.getElementById('arbProfit');
            const statusEl = document.getElementById('arbStatus');

            if (arb < 1) {
                profitEl.className = "text-emerald-400 font-extrabold";
                profitEl.innerText = '+' + fmt(profit) + ' (%' + profitPct.toFixed(2) + ')';
                statusEl.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20";
                statusEl.innerText = "Fırsat Var";
            } else {
                profitEl.className = "text-rose-400 font-extrabold";
                profitEl.innerText = fmt(profit) + ' (%' + profitPct.toFixed(2) + ')';
                statusEl.className = "text-[10px] px-2 py-0.5 rounded font-bold bg-rose-500/10 text-rose-400 border border-rose-500/20";
                statusEl.innerText = "Arbitraj Yok";
            }
        }

        function recalcKelly() {
            const odds = parseFloat(document.getElementById('kellyOdds').value) || 0;
            const prob = (parseFloat(document.getElementById('kellyWinProb').value) || 0) / 100;

            if (odds <= 1 || prob <= 0) return;

            const b = odds - 1;
            const q = 1 - prob;
            let f = (b * prob - q) / b;

            if (f < 0) f = 0;

            const stake = state.balance * f;

            document.getElementById('kellyFraction').innerText = '%' + (f * 100).toFixed(2);
            document.getElementById('kellyStake').innerText = fmt(stake);
        }

        function exportToExcel() {
            alert('Kasa hareketleri Excel formatında aktarılıyor...');
        }

        window.onload = function() {
            updateUI();
            recalcArb();
            recalcKelly();
        };
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
