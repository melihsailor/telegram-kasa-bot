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
WEB_APP_URL = f"{BASE_URL}?v=5"
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")

telegram_app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Surebet PRO v5", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📊 *Surebet Kasa & Arbitraj PRO v5*\n\n"
        "Gelişmiş arayüze erişmek için aşağıdaki butona tıklayabilirsin:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

telegram_app.add_handler(CommandHandler("start", start))

# PRO HTML & CSS & JS Arayüzü v5 (Surebet Odaklı)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <title>Surebet Kasa & Arbitraj PRO v5</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; -webkit-tap-highlight-color: transparent; transition: all 0.3s ease; }
        .tab-btn.active { background-color: var(--accent, #2563eb); color: #ffffff; font-weight: 600; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        .theme-tma { --bg: #0f172a; --card: #1e293b; --border: #334155; --accent: #2563eb; }
        .theme-cyberpunk { --bg: #09090b; --card: #18181b; --border: #27272a; --accent: #ec4899; }
        .theme-gold { --bg: #0c0a09; --card: #1c1917; --border: #292524; --accent: #d97706; }
        .theme-emerald { --bg: #022c22; --card: #064e3b; --border: #047857; --accent: #059669; }

        body { background-color: var(--bg); color: #f8fafc; }
        .theme-card { background-color: var(--card); border-color: var(--border); }
    </style>
</head>
<body id="bodyRoot" class="theme-tma pb-36 p-3 max-w-lg mx-auto space-y-4">

    <!-- Header -->
    <header class="p-3.5 flex items-center justify-between border theme-card rounded-2xl shadow-xl">
        <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30 flex items-center justify-center font-bold text-sm">v5</div>
            <div>
                <h1 class="font-bold text-sm tracking-wide text-white">Surebet & Arbitraj PRO</h1>
                <p class="text-[11px] text-slate-400">Çift Büro Stake Motoru</p>
            </div>
        </div>
        <div class="flex items-center gap-2">
            <span id="currencyBadge" class="text-xs px-2.5 py-1.5 bg-blue-500/10 text-blue-400 font-semibold rounded-lg border border-blue-500/20">₺ TRY</span>
        </div>
    </header>

    <!-- Banka Çekim (%10 Kâr) Kartı -->
    <div class="bg-gradient-to-r from-amber-500/20 via-yellow-500/10 to-amber-500/20 p-3.5 rounded-2xl border border-amber-500/30 flex justify-between items-center shadow-lg">
        <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center text-sm font-bold">🏦</div>
            <div>
                <div class="text-[11px] font-bold text-amber-300">Kenara Atılacak Bakiye (%10)</div>
                <div class="text-[10px] text-slate-300">Günlük Net Kâr Çekim Payı</div>
            </div>
        </div>
        <div id="bankWithdrawAmount" class="text-sm font-black text-amber-400">₺0,00</div>
    </div>

    <!-- Zaman Bazlı İstatistik Kartları (Günlük, Haftalık, Aylık) -->
    <div class="grid grid-cols-3 gap-2">
        <div class="theme-card p-2.5 rounded-xl border text-center space-y-1 shadow">
            <span class="text-[10px] text-slate-400 font-bold block">GÜNLÜK KÂR</span>
            <div id="statDaily" class="text-xs font-black text-emerald-400">+₺0,00</div>
        </div>
        <div class="theme-card p-2.5 rounded-xl border text-center space-y-1 shadow">
            <span class="text-[10px] text-slate-400 font-bold block">HAFTALIK KÂR</span>
            <div id="statWeekly" class="text-xs font-black text-emerald-400">+₺0,00</div>
        </div>
        <div class="theme-card p-2.5 rounded-xl border text-center space-y-1 shadow">
            <span class="text-[10px] text-slate-400 font-bold block">AYLIK KÂR</span>
            <div id="statMonthly" class="text-xs font-black text-emerald-400">+₺0,00</div>
        </div>
    </div>

    <!-- Toplam Kasa Kartı ve Hedef İlerleme Çubuğu -->
    <div class="theme-card p-5 rounded-2xl border shadow-xl space-y-4 relative overflow-hidden">
        <div class="flex justify-between items-start">
            <div class="space-y-1">
                <div class="text-[11px] font-semibold text-slate-400 tracking-wider flex items-center gap-1.5">
                    <i class="fa-solid fa-wallet text-slate-400"></i> TOPLAM KASA
                </div>
                <div class="text-3xl font-black text-white tracking-tight flex items-center gap-2">
                    <span id="displayBalance">₺10.000,00</span>
                </div>
            </div>
            <button onclick="openBalanceModal()" class="text-xs bg-slate-800/80 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-xl border border-slate-700/80 flex items-center gap-1.5 font-medium transition">
                <i class="fa-solid fa-pen-to-square text-blue-400"></i> Düzenle
            </button>
        </div>

        <!-- Hedef İlerleme Çubuğu -->
        <div class="space-y-1.5">
            <div class="flex justify-between text-[11px] font-semibold">
                <span class="text-slate-400">Kasa Hedefi İlerlemesi</span>
                <span id="goalProgressPct" class="text-blue-400 font-bold">%50.0</span>
            </div>
            <div class="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                <div id="goalProgressBar" class="h-full bg-gradient-to-r from-blue-600 to-indigo-500 rounded-full transition-all duration-500" style="width: 50%;"></div>
            </div>
            <div class="flex justify-between text-[10px] text-slate-400 pt-0.5">
                <span>Başlangıç: <strong id="displayStartBal" class="text-slate-200">₺10.000,00</strong></span>
                <span>Hedef: <strong id="displayGoal" class="text-slate-200">₺20.000,00</strong></span>
            </div>
        </div>

        <div class="grid grid-cols-3 gap-2 pt-3 border-t border-slate-800/80 text-center">
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">NET KÂR</div>
                <div id="displayNetProfit" class="text-xs font-black text-emerald-400 mt-1">+₺0,00</div>
            </div>
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">BEKLEYEN RİSK</div>
                <div id="displayRisk" class="text-xs font-black text-amber-400 mt-1">₺0,00</div>
            </div>
            <div class="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/50">
                <div class="text-[10px] font-semibold text-slate-400 uppercase">BONUS</div>
                <div id="displayBonus" class="text-xs font-black text-blue-400 mt-1">₺0,00</div>
            </div>
        </div>
    </div>

    <!-- Tıklanabilir Büro Bazlı Cüzdan Dağılımı -->
    <div class="theme-card p-4 rounded-2xl border space-y-3 shadow-lg">
        <div class="flex justify-between items-center">
            <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                <i class="fa-solid fa-building-columns text-blue-400"></i> Büro Bakiyeleri (Cüzdanlar)
            </h3>
            <button onclick="addNewBookie()" class="text-[10px] px-2 py-1 bg-blue-600/20 text-blue-400 font-bold rounded-lg border border-blue-500/30">+ Büro Ekle</button>
        </div>
        <div id="bookiesContainer" class="grid grid-cols-2 gap-2"></div>
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

    <!-- TAB 1: SUREBET HESAPLAYICI -->
    <div id="tabCalc" class="tab-content active space-y-3">
        <div class="theme-card p-4 rounded-2xl border space-y-3 shadow-lg">
            <div class="flex justify-between items-center">
                <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                    <i class="fa-solid fa-bolt text-amber-400"></i> Surebet Çapraz Hesaplayıcı
                </h3>
                <span id="arbStatus" class="text-[10px] px-2 py-0.5 rounded font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Fırsat Var</span>
            </div>

            <div class="grid grid-cols-2 gap-2">
                <div>
                    <label class="text-[10px] font-semibold text-slate-400 block mb-1">1. Büro Adı & Oranı</label>
                    <div class="flex gap-1">
                        <input type="text" id="calcB1Name" value="Bet365" class="w-1/2 bg-slate-900 border border-slate-700/80 rounded-xl p-2 text-xs font-bold text-white">
                        <input type="number" id="calcOdds1" step="0.01" value="2.10" oninput="recalcArb()" class="w-1/2 bg-slate-900 border border-slate-700/80 rounded-xl p-2 text-xs font-bold text-white">
                    </div>
                </div>
                <div>
                    <label class="text-[10px] font-semibold text-slate-400 block mb-1">2. Büro Adı & Oranı</label>
                    <div class="flex gap-1">
                        <input type="text" id="calcB2Name" value="1xBet" class="w-1/2 bg-slate-900 border border-slate-700/80 rounded-xl p-2 text-xs font-bold text-white">
                        <input type="number" id="calcOdds2" step="0.01" value="2.05" oninput="recalcArb()" class="w-1/2 bg-slate-900 border border-slate-700/80 rounded-xl p-2 text-xs font-bold text-white">
                    </div>
                </div>
            </div>

            <div>
                <label class="text-[10px] font-semibold text-slate-400 block mb-1">Toplam Yatırılacak Bütçe</label>
                <input type="number" id="calcTotalStake" value="1000" oninput="recalcArb()" class="w-full bg-slate-900 border border-slate-700/80 rounded-xl p-2.5 text-xs font-bold text-white">
            </div>

            <div class="p-3 bg-slate-900/80 rounded-xl text-xs space-y-2 border border-slate-800">
                <div class="flex justify-between items-center text-slate-300">
                    <span id="labelB1Stake">1. Büro Stake (Miktar):</span>
                    <span id="resStake1" class="font-bold text-white">₺506,02</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                    <span id="labelB2Stake">2. Büro Stake (Miktar):</span>
                    <span id="resStake2" class="font-bold text-white">₺493,98</span>
                </div>
                <div class="flex justify-between items-center pt-2 border-t border-slate-800 font-bold">
                    <span class="text-slate-300">Garanti Net Kâr:</span>
                    <span id="resNetProfit" class="text-emerald-400 font-extrabold">+₺62,65 (%6.27)</span>
                </div>
            </div>

            <button onclick="addCurrentBetToPending()" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl text-xs shadow-lg shadow-blue-600/30 transition flex items-center justify-center gap-2">
                <i class="fa-solid fa-circle-plus"></i> Bu Surebet Bahsini Bekleyenlere Ekle
            </button>
        </div>
    </div>

    <!-- TAB 2: BAHİS TAKİP (ÇİFT BÜRO AYRI STAKE GİRİŞİ) -->
    <div id="tabTrack" class="tab-content space-y-3">
        <!-- Manuel Çapraz Bahis Ekleme Paneli -->
        <div class="theme-card p-4 rounded-2xl border space-y-3 shadow-lg">
            <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                <i class="fa-solid fa-plus-circle text-blue-400"></i> Manuel Surebet Ekle (Ayrı Oran & Miktarlar)
            </h3>
            <input type="text" id="manualMatch" placeholder="Maç Adı (Örn: Galatasaray - Fenerbahçe)" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2 text-xs text-white">
            
            <div class="grid grid-cols-2 gap-2">
                <div>
                    <label class="text-[9px] text-slate-400 block mb-0.5">1. Büro / Oran / Miktar</label>
                    <input type="text" id="manB1" placeholder="Büro Adı" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-1.5 text-xs text-white mb-1">
                    <div class="flex gap-1">
                        <input type="number" id="manO1" step="0.01" placeholder="Oran" class="w-1/2 bg-slate-900 border border-slate-700 rounded-xl p-1.5 text-xs text-white">
                        <input type="number" id="manS1" placeholder="Miktar" class="w-1/2 bg-slate-900 border border-slate-700 rounded-xl p-1.5 text-xs text-white">
                    </div>
                </div>
                <div>
                    <label class="text-[9px] text-slate-400 block mb-0.5">2. Büro / Oran / Miktar</label>
                    <input type="text" id="manB2" placeholder="Büro Adı" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-1.5 text-xs text-white mb-1">
                    <div class="flex gap-1">
                        <input type="number" id="manO2" step="0.01" placeholder="Oran" class="w-1/2 bg-slate-900 border border-slate-700 rounded-xl p-1.5 text-xs text-white">
                        <input type="number" id="manS2" placeholder="Miktar" class="w-1/2 bg-slate-900 border border-slate-700 rounded-xl p-1.5 text-xs text-white">
                    </div>
                </div>
            </div>

            <input type="text" id="manualNote" placeholder="Not (Opsiyonel)" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2 text-xs text-white">

            <button onclick="addManualBet()" class="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold rounded-xl text-xs border border-slate-700 transition">
                Çapraz Bahsi Listeye Kaydet
            </button>
        </div>

        <!-- Bekleyen Bahisler -->
        <div class="theme-card p-4 rounded-2xl border space-y-3 shadow-lg">
            <h3 class="text-xs font-bold text-amber-400 flex items-center gap-1.5">
                <i class="fa-solid fa-clock"></i> Bekleyen Surebetler
            </h3>
            <div id="pendingList" class="space-y-2"></div>
        </div>

        <!-- Sonuçlanan Bahisler -->
        <div class="theme-card p-4 rounded-2xl border space-y-3 shadow-lg">
            <h3 class="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                <i class="fa-solid fa-check-circle"></i> Sonuçlanan Surebetler (Detay, Geri Al & Sil)
            </h3>
            <div id="settledList" class="space-y-2"></div>
        </div>
    </div>

    <!-- TAB 3: ÖZELLEŞTİRME & VERİ SIFIRLAMA -->
    <div id="tabSettings" class="tab-content space-y-3">
        <div class="theme-card p-4 rounded-2xl border space-y-4 shadow-lg">
            <h3 class="text-xs font-bold text-white flex items-center gap-1.5">
                <i class="fa-solid fa-gear text-blue-400"></i> Uygulama Tercihleri
            </h3>

            <div class="space-y-2 text-xs">
                <label class="text-slate-400 font-semibold block">Tema Seçimi</label>
                <select id="themeSelect" onchange="changeTheme()" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                    <option value="theme-tma">Telegram Dark (Klasik TMA Mavisi)</option>
                    <option value="theme-cyberpunk">Cyberpunk Neon (Yeşil & Pembe)</option>
                    <option value="theme-gold">Dark Gold (Prestij Altın)</option>
                    <option value="theme-emerald">Emerald Green (Kasa Yeşili)</option>
                </select>
            </div>

            <div class="space-y-2 text-xs">
                <label class="text-slate-400 font-semibold block">Ana Para Birimi</label>
                <select id="currencySelect" onchange="changeCurrency()" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                    <option value="TRY">Türk Lirası (₺ TRY)</option>
                    <option value="USD">Amerikan Doları ($ USD)</option>
                    <option value="EUR">Euro (€ EUR)</option>
                </select>
            </div>

            <div class="pt-2 border-t border-slate-800 space-y-2">
                <label class="text-slate-400 font-semibold block text-xs">Veri Yönetimi & Sıfırlama</label>
                <div class="grid grid-cols-2 gap-2">
                    <button onclick="exportData('excel')" class="py-2.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 font-bold rounded-xl text-xs border border-emerald-500/30 flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-file-excel"></i> Excel İndir
                    </button>
                    <button onclick="confirmResetAll()" class="py-2.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 font-bold rounded-xl text-xs border border-rose-500/30 flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-trash-can"></i> Her Şeyi Sıfırla
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- BAKİYE & HEDEF DÜZENLEME MODALI -->
    <div id="balanceModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="theme-card w-full max-w-sm rounded-2xl border p-5 space-y-4 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-blue-5