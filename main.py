import os
import logging
import asyncio
from flask import Flask, request, render_template_string, make_response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask uygulaması
flask_app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8886446926:AAFUBRKk6qDUvQi1dsneaFQXkUIKBz-sGgg")
BASE_URL = "https://telegram-kasa-bot.onrender.com"
WEB_APP_URL = f"{BASE_URL}?v=2"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")

telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Kasa & Arbitraj PRO v2", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📊 *Kasa & Arbitraj PRO Yönetim Sistemi v2*\n\n"
        "Gelişmiş arayüze erişmek için aşağıdaki butona tıklayabilirsin:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

telegram_app.add_handler(CommandHandler("start", start))

# Tam Donanımlı PRO HTML Arayüzü (Hesaplayıcı, Bahis Takip, Özelleştir)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <title>Kasa & Arbitraj PRO v2</title>
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
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; -webkit-tap-highlight-color: transparent; }
        .tab-btn.active { background-color: #2563eb; color: #ffffff; font-weight: 600; box-shadow: 0 4px 12px rgba(37,99,235,0.3); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body id="bodyRoot" class="pb-32 p-3 max-w-lg mx-auto space-y-4 bg-[#0b0f17] text-slate-100 transition-colors duration-200">

    <!-- Üst Header -->
    <header class="p-3.5 flex items-center justify-between border border-slate-800 bg-[#151c28] rounded-2xl shadow-xl">
        <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-blue-600/20 text-blue-500 border border-blue-500/30 flex items-center justify-center font-bold text-sm">PRO</div>
            <div>
                <h1 class="font-bold text-sm tracking-wide text-white">Kasa & Arbitraj PRO</h1>
                <p class="text-[11px] text-slate-400">Telegram Mini App v2</p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <span id="currencyBadge" class="text-xs px-2.5 py-1.5 bg-blue-500/10 text-blue-400 font-semibold rounded-lg border border-blue-500/20">₺ TRY</span>
        </div>
    </header>

    <!-- Toplam Kasa Kartı -->
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
                <div class="text-[10px] font-semibold text-slate-400 uppercase">NET KÂR</div>
                <div id="displayNetProfit" class="text-xs font-black text-emerald-400 mt-1">+₺0,00</div>
            </div>
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">BONUS</div>
                <div id="displayBonus" class="text-xs font-black text-blue-400 mt-1">₺75,00</div>
            </div>
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">ROI</div>
                <div id="displayROI" class="text-xs font-black text-purple-400 mt-1">%0.00</div>
            </div>
        </div>
    </div>

    <!-- ALT 3'LÜ SEKME NAVİGASYONU -->
    <div class="grid grid-cols-3 gap-1 p-1 bg-slate-900/90 rounded-xl border border-slate-800">
        <button id="tabBtn1" onclick="switchTab('calc')" class="tab-btn active py-2.5 text-[11px] font-semibold rounded-lg text-slate-400 transition flex items-center justify-center gap-1.5">
            <i class="fa-solid fa-calculator"></i> Hesaplayıcı
        </button>
        <button id="tabBtn2" onclick="switchTab('track')" class="tab-btn py-2.5 text-[11px] font-semibold rounded-lg text-slate-400 transition flex items-center justify-center gap-1.5">
            <i class="fa-solid fa-list-check"></i> Bahis Takip
        </button>
        <button id="tabBtn3" onclick="switchTab('settings')" class="tab-btn py-2.5 text-[11px] font-semibold rounded-lg text-slate-400 transition flex items-center justify-center gap-1.5">
            <i class="fa-solid fa-sliders"></i> Özelleştir
        </button>
    </div>

    <!-- TAB 1: HESAPLAYICI (SUREBET + BEKLEYENE EKLE) -->
    <div id="tabCalc" class="tab-content active space-y-3">
        <div class="bg-[#151c28] p-4 rounded-2xl border border-slate-800 space-y-3 shadow-lg">
            <div class="flex justify-between items-center">
                <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-bolt text-amber-400"></i> Surebet Hesaplayıcı
                </h3>
                <span id="arbStatus" class="text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Fırsat Var</span>
            </div>

            <div class="grid grid-cols-2 gap-2">
                <div>
                    <label class="text-[10px] font-semibold text-slate-400 block mb-1">1. Büro Oranı</label>
                    <input type="number" id="calcOdds1" step="0.01" value="2.10" oninput="recalcArb()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
                </div>
                <div>
                    <label class="text-[10px] font-semibold text-slate-400 block mb-1">2. Büro Oranı</label>
                    <input type="number" id="calcOdds2" step="0.01" value="2.05" oninput="recalcArb()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
                </div>
            </div>

            <div>
                <label class="text-[10px] font-semibold text-slate-400 block mb-1">Toplam Yatırılacak Bütçe</label>
                <input type="number" id="calcTotalStake" value="1000" oninput="recalcArb()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white focus:border-blue-500 focus:outline-none">
            </div>

            <div class="p-3 bg-slate-900/80 rounded-xl text-xs space-y-2 border border-slate-800">
                <div class="flex justify-between items-center text-slate-300">
                    <span>1. Büro Stake:</span>
                    <span id="resStake1" class="font-bold text-white">₺506,02</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                    <span>2. Büro Stake:</span>
                    <span id="resStake2" class="font-bold text-white">₺493,98</span>
                </div>
                <div class="flex justify-between items-center pt-2 border-t border-slate-800 font-bold">
                    <span class="text-slate-300">Garanti Net Kâr:</span>
                    <span id="resNetProfit" class="text-emerald-400 font-extrabold">+₺62,65 (%6.27)</span>
                </div>
            </div>

            <button onclick="addCurrentBetToPending()" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl text-xs shadow-lg shadow-blue-600/30 transition flex items-center justify-center gap-2">
                <i class="fa-solid fa-circle-plus"></i> Bu Bahsi Bekleyenlere Ekle
            </button>
        </div>
    </div>

    <!-- TAB 2: BAHİS TAKİP -->
    <div id="tabTrack" class="tab-content space-y-3">
        <!-- Manuel Bahis Ekleme Paneli -->
        <div class="bg-[#151c28] p-4 rounded-2xl border border-slate-800 space-y-3 shadow-lg">
            <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                <i class="fa-solid fa-plus-circle text-blue-400"></i> Manuel Bahis Ekle
            </h3>
            <div class="grid grid-cols-2 gap-2">
                <input type="text" id="manualMatch" placeholder="Maç Adı (Örn: GS - FB)" class="bg-slate-900 border border-slate-700 rounded-xl p-2 text-xs text-white">
                <input type="number" id="manualStake" placeholder="Yatırım Miktarı" class="bg-slate-900 border border-slate-700 rounded-xl p-2 text-xs text-white">
            </div>
            <div class="grid grid-cols-2 gap-2">
                <input type="number" id="manualOdds" step="0.01" placeholder="Oran" class="bg-slate-900 border border-slate-700 rounded-xl p-2 text-xs text-white">
                <input type="text" id="manualNote" placeholder="Not (Opsiyonel)" class="bg-slate-900 border border-slate-700 rounded-xl p-2 text-xs text-white">
            </div>
            <button onclick="addManualBet()" class="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold rounded-xl text-xs border border-slate-700 transition">
                Listeye Kaydet
            </button>
        </div>

        <!-- Bekleyen Bahisler -->
        <div class="bg-[#151c28] p-4 rounded-2xl border border-slate-800 space-y-3 shadow-lg">
            <h3 class="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                <i class="fa-solid fa-clock"></i> Bekleyen Bahisler
            </h3>
            <div id="pendingList" class="space-y-2"></div>
        </div>

        <!-- Sonuçlanan Bahisler -->
        <div class="bg-[#151c28] p-4 rounded-2xl border border-slate-800 space-y-3 shadow-lg">
            <h3 class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                <i class="fa-solid fa-check-circle"></i> Sonuçlanan Bahisler
            </h3>
            <div id="settledList" class="space-y-2"></div>
        </div>
    </div>

    <!-- TAB 3: ÖZELLEŞTİRME VE VERİ İNDİRME -->
    <div id="tabSettings" class="tab-content space-y-3">
        <div class="bg-[#151c28] p-4 rounded-2xl border border-slate-800 space-y-4 shadow-lg">
            <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                <i class="fa-solid fa-gear text-blue-400"></i> Uygulama Tercihleri
            </h3>

            <div class="space-y-2 text-xs">
                <label class="text-slate-400 font-semibold block">Para Birimi Seçimi</label>
                <select id="currencySelect" onchange="changeCurrency()" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                    <option value="TRY">Türk Lirası (₺ TRY)</option>
                    <option value="USDT">Tether ($ USDT)</option>
                </select>
            </div>

            <div class="space-y-2 text-xs">
                <label class="text-slate-400 font-semibold block">Tema Seçimi</label>
                <select id="themeSelect" onchange="changeTheme()" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                    <option value="dark">Modern Koyu (Dark)</option>
                    <option value="midnight">Gece Mavisi (Midnight)</option>
                    <option value="light">Aydınlık (Light)</option>
                </select>
            </div>

            <div class="pt-2 border-t border-slate-800 space-y-2">
                <label class="text-slate-400 font-semibold block text-xs">Veri Dışa Aktarımı</label>
                <div class="grid grid-cols-2 gap-2">
                    <button onclick="exportData('excel')" class="py-2.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 font-bold rounded-xl text-xs border border-emerald-500/30 flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-file-excel"></i> Excel İndir
                    </button>
                    <button onclick="exportData('csv')" class="py-2.5 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 font-bold rounded-xl text-xs border border-blue-500/30 flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-file-csv"></i> CSV İndir
                    </button>
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
                    <label class="text-slate-400 block mb-1 font-semibold">Mevcut Toplam Kasa</label>
                    <input type="number" id="inputBalance" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Hedef Kasa</label>
                    <input type="number" id="inputGoal" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Bekleyen Risk</label>
                    <input type="number" id="inputRisk" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Kayıp Bonusu</label>
                    <input type="number" id="inputBonus" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
            </div>

            <div class="flex gap-2 pt-2 border-t border-slate-800">
                <button onclick="closeBalanceModal()" class="w-1/2 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition">İptal</button>
                <button onclick="saveBalanceModal()" class="w-1/2 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition shadow-lg shadow-blue-600/30">Kaydet</button>
            </div>
        </div>
    </div>

    <!-- SONUÇLANDIRMA MODALI -->
    <div id="settleModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-[#151c28] w-full max-w-sm rounded-2xl border border-slate-800 p-5 space-y-4 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-trophy text-amber-400"></i> Bahis Sonuçlandır
                </h3>
                <button onclick="closeSettleModal()" class="text-slate-400 hover:text-white text-base"><i class="fa-solid fa-xmark"></i></button>
            </div>

            <div class="space-y-3 text-xs">
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Hangi Büro Kazandı / Sonuç?</label>
                    <select id="settleResultType" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                        <option value="büro1">1. Büro Kazandı</option>
                        <option value="büro2">2. Büro Kazandı</option>
                        <option value="kayıp">Komple Kayıp (Lost)</option>
                    </select>
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Kayıp Bonusu Alındı mı?</label>
                    <select id="bonusTakenSelect" onchange="toggleBonusInput()" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                        <option value="hayir">Hayır</option>
                        <option value="evet">Evet, Alındı</option>
                    </select>
                </div>
                <div id="bonusAmountContainer" class="hidden">
                    <label class="text-slate-400 block mb-1 font-semibold">Alınan Kayıp Bonusu Miktarı</label>
                    <input type="number" id="inputBonusVal" value="0" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
            </div>

            <div class="flex gap-2 pt-2 border-t border-slate-800">
                <button onclick="closeSettleModal()" class="w-1/2 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition">İptal</button>
                <button onclick="confirmSettle()" class="w-1/2 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition shadow-lg shadow-emerald-600/30">Sonuçlandır</button>
            </div>
        </div>
    </div>

    <!-- NOT DÜZENLEME MODALI -->
    <div id="noteModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-[#151c28] w-full max-w-sm rounded-2xl border border-slate-800 p-5 space-y-4 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-note-sticky text-blue-400"></i> Bahis Notu Düzenle
                </h3>
                <button onclick="closeNoteModal()" class="text-slate-400 hover:text-white text-base"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div>
                <textarea id="inputNoteText" rows="3" placeholder="Notunuzu buraya yazın..." class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-xs text-white"></textarea>
            </div>
            <button onclick="saveNote()" class="w-full py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs rounded-xl shadow-lg">Notu Kaydet</button>
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
            roi: 0,
            currency: 'TRY'
        };

        let pendingBets = [];
        let settledBets = [];
        let currentSettleIndex = null;
        let currentNoteIndex = null;

        function getSymbol() { return state.currency === 'TRY' ? '₺' : '$'; }
        function fmt(num) { return getSymbol() + num.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }

        function updateUI() {
            document.getElementById('displayBalance').innerText = fmt(state.balance);
            document.getElementById('displayGoal').innerText = fmt(state.goal);
            document.getElementById('displayRisk').innerText = fmt(state.risk);
            document.getElementById('displayNetProfit').innerText = (state.netProfit >= 0 ? '+' : '') + fmt(state.netProfit);
            document.getElementById('displayBonus').innerText = fmt(state.bonus);
            document.getElementById('displayROI').innerText = '%' + state.roi.toFixed(2);
            document.getElementById('currencyBadge').innerText = state.currency === 'TRY' ? '₺ TRY' : '$ USDT';
            renderPending();
            renderSettled();
        }

        function switchTab(tab) {
            document.getElementById('tabCalc').classList.remove('active');
            document.getElementById('tabTrack').classList.remove('active');
            document.getElementById('tabSettings').classList.remove('active');
            document.getElementById('tabBtn1').classList.remove('active');
            document.getElementById('tabBtn2').classList.remove('active');
            document.getElementById('tabBtn3').classList.remove('active');

            if (tab === 'calc') {
                document.getElementById('tabCalc').classList.add('active');
                document.getElementById('tabBtn1').classList.add('active');
            } else if (tab === 'track') {
                document.getElementById('tabTrack').classList.add('active');
                document.getElementById('tabBtn2').classList.add('active');
            } else {
                document.getElementById('tabSettings').classList.add('active');
                document.getElementById('tabBtn3').classList.add('active');
            }
        }

        function recalcArb() {
            const o1 = parseFloat(document.getElementById('calcOdds1').value) || 0;
            const o2 = parseFloat(document.getElementById('calcOdds2').value) || 0;
            const total = parseFloat(document.getElementById('calcTotalStake').value) || 0;

            if (o1 <= 1 || o2 <= 1 || total <= 0) return;

            const arb = (1 / o1) + (1 / o2);
            const s1 = (total * (1 / o1)) / arb;
            const s2 = (total * (1 / o2)) / arb;
            const profit = (s1 * o1) - total;
            const profitPct = (profit / total) * 100;

            document.getElementById('resStake1').innerText = fmt(s1);
            document.getElementById('resStake2').innerText = fmt(s2);

            const profitEl = document.getElementById('resNetProfit');
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

        function addCurrentBetToPending() {
            const o1 = parseFloat(document.getElementById('calcOdds1').value) || 0;
            const o2 = parseFloat(document.getElementById('calcOdds2').value) || 0;
            const total = parseFloat(document.getElementById('calcTotalStake').value) || 0;
            const arb = (1 / o1) + (1 / o2);
            const s1 = (total * (1 / o1)) / arb;
            const s2 = (total * (1 / o2)) / arb;
            const profit = (s1 * o1) - total;

            pendingBets.push({
                title: `Surebet (${o1} & ${o2})`,
                stake: total,
                profit: profit,
                s1: s1, s2: s2, o1: o1, o2: o2,
                note: 'Hesaplayıcıdan Eklendi'
            });

            state.risk += total;
            updateUI();
            switchTab('track');
        }

        function addManualBet() {
            const match = document.getElementById('manualMatch').value || 'Özel Bahis';
            const stake = parseFloat(document.getElementById('manualStake').value) || 0;
            const odds = parseFloat(document.getElementById('manualOdds').value) || 0;
            const note = document.getElementById('manualNote').value || '';

            if (stake <= 0) return;

            pendingBets.push({
                title: match, stake: stake, profit: (stake * odds) - stake,
                s1: stake, s2: 0, o1: odds, o2: 0, note: note
            });

            state.risk += stake;
            document.getElementById('manualMatch').value = '';
            document.getElementById('manualStake').value = '';
            document.getElementById('manualOdds').value = '';
            document.getElementById('manualNote').value = '';
            updateUI();
        }

        function renderPending() {
            const container = document.getElementById('pendingList');
            if (pendingBets.length === 0) {
                container.innerHTML = '<div class="text-xs text-slate-500 text-center py-2">Bekleyen bahis bulunmuyor.</div>';
                return;
            }
            container.innerHTML = pendingBets.map((bet, idx) => `
                <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
                    <div class="flex justify-between items-start">
                        <div>
                            <div class="font-bold text-xs text-white">${bet.title}</div>
                            <div class="text-[10px] text-slate-400">Yatırım: ${getSymbol()}${bet.stake.toFixed(2)} | Not: ${bet.note}</div>
                        </div>
                        <div class="flex gap-1">
                            <button onclick="openNoteModal(${idx})" class="px-2 py-1 bg-slate-800 text-blue-400 rounded text-[10px]"><i class="fa-solid fa-pen"></i></button>
                            <button onclick="openSettleModal(${idx})" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded text-[10px]">Sonuçlandır</button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function renderSettled() {
            const container = document.getElementById('settledList');
            if (settledBets.length === 0) {
                container.innerHTML = '<div class="text-xs text-slate-500 text-center py-2">Sonuçlanan bahis bulunmuyor.</div>';
                return;
            }
            container.innerHTML = settledBets.map(bet => `
                <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 flex justify-between items-center text-xs">
                    <div>
                        <div class="font-bold text-white">${bet.title}</div>
                        <div class="text-[10px] text-slate-400">Durum: <span class="${bet.net >= 0 ? 'text-emerald-400 font-bold' : 'text-rose-400 font-bold'}">${bet.status}</span></div>
                    </div>
                    <div class="text-right">
                        <div class="${bet.net >= 0 ? 'text-emerald-400' : 'text-rose-400'} font-extrabold">${bet.net >= 0 ? '+' : ''}${fmt(bet.net)}</div>
                    </div>
                </div>
            `).join('');
        }

        function openSettleModal(idx) { currentSettleIndex = idx; document.getElementById('settleModal').classList.remove('hidden'); }
        function closeSettleModal() { document.getElementById('settleModal').classList.add('hidden'); currentSettleIndex = null; }
        function toggleBonusInput() {
            const val = document.getElementById('bonusTakenSelect').value;
            document.getElementById('bonusAmountContainer').classList.toggle('hidden', val !== 'evet');
        }

        function confirmSettle() {
            if (currentSettleIndex === null) return;
            const bet = pendingBets[currentSettleIndex];
            const resultType = document.getElementById('settleResultType').value;
            const bonusTaken = document.getElementById('bonusTakenSelect').value;
            const bonusVal = parseFloat(document.getElementById('inputBonusVal').value) || 0;

            state.risk -= bet.stake;
            let netResult = 0;
            let statusText = '';

            if (resultType === 'büro1') { netResult = (bet.s1 * bet.o1) - bet.stake; statusText = '1. Büro Kazandı'; }
            else if (resultType === 'büro2') { netResult = (bet.s2 * bet.o2) - bet.stake; statusText = '2. Büro Kazandı'; }
            else { netResult = -bet.stake; statusText = 'Kayıp'; }

            if (bonusTaken === 'evet' && bonusVal > 0) {
                state.bonus += bonusVal;
                netResult += bonusVal;
            }

            state.balance += netResult;
            state.netProfit += netResult;

            settledBets.push({ title: bet.title, net: netResult, status: statusText });
            pendingBets.splice(currentSettleIndex, 1);
            updateUI();
            closeSettleModal();
        }

        function openNoteModal(idx) {
            currentNoteIndex = idx;
            document.getElementById('inputNoteText').value = pendingBets[idx].note;
            document.getElementById('noteModal').classList.remove('hidden');
        }
        function closeNoteModal() { document.getElementById('noteModal').classList.add('hidden'); currentNoteIndex = null; }
        function saveNote() {
            if (currentNoteIndex !== null) {
                pendingBets[currentNoteIndex].note = document.getElementById('inputNoteText').value;
                renderPending();
            }
            closeNoteModal();
        }

        function openBalanceModal() {
            document.getElementById('inputBalance').value = state.balance;
            document.getElementById('inputGoal').value = state.goal;
            document.getElementById('inputRisk').value = state.risk;
            document.getElementById('inputBonus').value = state.bonus;
            document.getElementById('balanceModal').classList.remove('hidden');
        }
        function closeBalanceModal() { document.getElementById('balanceModal').classList.add('hidden'); }
        function saveBalanceModal() {
            state.balance = parseFloat(document.getElementById('inputBalance').value) || 0;
            state.goal = parseFloat(document.getElementById('inputGoal').value) || 0;
            state.risk = parseFloat(document.getElementById('inputRisk').value) || 0;
            state.bonus = parseFloat(document.getElementById('inputBonus').value) || 0;
            updateUI();
            closeBalanceModal();
        }

        function changeCurrency() { state.currency = document.getElementById('currencySelect').value; updateUI(); }
        function changeTheme() {
            const theme = document.getElementById('themeSelect').value;
            const root = document.getElementById('bodyRoot');
            if (theme === 'light') root.className = "pb-32 p-3 max-w-lg mx-auto space-y-4 bg-slate-100 text-slate-900 transition-colors duration-200";
            else if (theme === 'midnight') root.className = "pb-32 p-3 max-w-lg mx-auto space-y-4 bg-slate-950 text-slate-100 transition-colors duration-200";
            else root.className = "pb-32 p-3 max-w-lg mx-auto space-y-4 bg-[#0b0f17] text-slate-100 transition-colors duration-200";
        }

        function exportData(type) { alert(`Veriler ${type.toUpperCase()} formatında aktarılıyor...`); }

        window.onload = function() { updateUI(); recalcArb(); };
    </script>
</body>
</html>
"""

@flask_app.route("/")
def index():
    response = make_response(render_template_string(HTML_TEMPLATE))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

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
        ext_url = RENDER_EXTERNAL_URL if RENDER_EXTERNAL_URL else BASE_URL
        webhook_url = f"{ext_url}/{BOT_TOKEN}"
        set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={webhook_url}"
        try:
            urllib.request.urlopen(set_webhook_url)
            print("Webhook tanımlandı!")
        except Exception as e:
            print(f"Webhook hatası: {e}")

    asyncio.run(main_setup())

    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
