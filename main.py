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
            </div>

            <div class="flex gap-2 pt-2 border-t border-slate-800">
                <button onclick="closeBalanceModal()" class="w-1/2 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-semibold text-xs">İptal</button>
                <button onclick="saveBalanceModal()" class="w-1/2 py-2.5 rounded-xl bg-blue-600 text-white font-semibold text-xs shadow-lg">Kaydet</button>
            </div>
        </div>
    </div>

    <!-- BÜRO EKLE / DÜZENLE MODALI -->
    <div id="bookieModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="theme-card w-full max-w-sm rounded-2xl border p-5 space-y-4 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-building-columns text-blue-400"></i> Büro Bakiye Düzenle
                </h3>
                <button onclick="closeBookieModal()" class="text-slate-400 hover:text-white text-base"><i class="fa-solid fa-xmark"></i></button>
            </div>

            <div class="space-y-3 text-xs">
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Büro Adı</label>
                    <input type="text" id="inputBookieName" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Büro Bakiyesi</label>
                    <input type="number" id="inputBookieBalance" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold">
                </div>
            </div>

            <div class="flex gap-2 pt-2 border-t border-slate-800">
                <button onclick="deleteCurrentBookie()" class="w-1/3 py-2.5 rounded-xl bg-rose-600/20 text-rose-400 font-semibold text-xs border border-rose-500/30">Sil</button>
                <button onclick="saveBookieModal()" class="w-2/3 py-2.5 rounded-xl bg-blue-600 text-white font-semibold text-xs shadow-lg">Kaydet</button>
            </div>
        </div>
    </div>

    <!-- SONUÇLANDIRMA MODALI -->
    <div id="settleModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="theme-card w-full max-w-sm rounded-2xl border p-5 space-y-4 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-trophy text-amber-400"></i> Surebet Sonuçlandır
                </h3>
                <button onclick="closeSettleModal()" class="text-slate-400 hover:text-white text-base"><i class="fa-solid fa-xmark"></i></button>
            </div>

            <div class="space-y-3 text-xs">
                <div>
                    <label class="text-slate-400 block mb-1 font-semibold">Hangi Büro Kazandı?</label>
                    <select id="settleResultType" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2.5 text-white font-bold"></select>
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
                <button onclick="closeSettleModal()" class="w-1/2 py-2.5 rounded-xl bg-slate-800 text-slate-300 font-semibold text-xs">İptal</button>
                <button onclick="confirmSettle()" class="w-1/2 py-2.5 rounded-xl bg-emerald-600 text-white font-semibold text-xs shadow-lg">Surebet Sonuçlandır</button>
            </div>
        </div>
    </div>

    <!-- SONUÇLANAN BAHİS DETAY, GERİ AL, SİL & NOT MODALI -->
    <div id="detailModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="theme-card w-full max-w-sm rounded-2xl border p-5 space-y-4 shadow-2xl">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-circle-info text-blue-400"></i> Surebet Detayı & Yönetimi
                </h3>
                <button onclick="closeDetailModal()" class="text-slate-400 hover:text-white text-base"><i class="fa-solid fa-xmark"></i></button>
            </div>

            <div id="detailContent" class="space-y-2 text-xs text-slate-300"></div>

            <div class="space-y-1">
                <label class="text-[11px] text-slate-400 font-semibold block">Bahis Notu</label>
                <textarea id="detailNoteText" rows="2" class="w-full bg-slate-900 border border-slate-700 rounded-xl p-2 text-xs text-white"></textarea>
            </div>

            <div class="grid grid-cols-3 gap-1.5 pt-2 border-t border-slate-800 text-xs">
                <button onclick="revertSettledBet()" class="py-2 rounded-xl bg-amber-600/20 text-amber-400 border border-amber-500/30 font-bold">Geri Al</button>
                <button onclick="saveDetailNote()" class="py-2 rounded-xl bg-blue-600 text-white font-bold">Not Kaydet</button>
                <button onclick="deleteSettledBet()" class="py-2 rounded-xl bg-rose-600/20 text-rose-400 border border-rose-500/30 font-bold">Tamamen Sil</button>
            </div>
        </div>
    </div>

    <script>
        const tg = window.Telegram?.WebApp;
        if (tg) tg.expand();

        let state = {
            balance: 10000,
            startBalance: 10000,
            goal: 20000,
            risk: 0,
            netProfit: 0,
            bonus: 0,
            currency: 'TRY',
            dailyProfit: 0,
            weeklyProfit: 0,
            monthlyProfit: 0
        };

        let bookies = [
            { name: 'Bet365', balance: 5000 },
            { name: '1xBet', balance: 5000 }
        ];

        let pendingBets = [];
        let settledBets = [];

        let currentSettleIndex = null;
        let currentDetailIndex = null;
        let currentBookieIndex = null;

        function getSymbol() { 
            if (state.currency === 'USD') return '$';
            if (state.currency === 'EUR') return '€';
            return '₺';
        }
        function fmt(num) { return getSymbol() + num.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }

        function updateUI() {
            document.getElementById('displayBalance').innerText = fmt(state.balance);
            document.getElementById('displayStartBal').innerText = fmt(state.startBalance);
            document.getElementById('displayGoal').innerText = fmt(state.goal);
            document.getElementById('displayRisk').innerText = fmt(state.risk);
            document.getElementById('displayNetProfit').innerText = (state.netProfit >= 0 ? '+' : '') + fmt(state.netProfit);
            document.getElementById('displayBonus').innerText = fmt(state.bonus);
            document.getElementById('currencyBadge').innerText = `${getSymbol()} ${state.currency}`;

            // İlerleme Çubuğu
            const progressPct = Math.min(100, Math.max(0, ((state.balance - state.startBalance) / (state.goal - state.startBalance)) * 100));
            document.getElementById('goalProgressPct').innerText = '%' + (isNaN(progressPct) ? 0 : progressPct.toFixed(1));
            document.getElementById('goalProgressBar').style.width = (isNaN(progressPct) ? 0 : progressPct) + '%';

            // Banka Çekim Tutarı (%10)
            const bankCut = state.dailyProfit > 0 ? state.dailyProfit * 0.10 : 0;
            document.getElementById('bankWithdrawAmount').innerText = fmt(bankCut);

            // Günlük, Haftalık, Aylık İstatistikler
            document.getElementById('statDaily').innerText = (state.dailyProfit >= 0 ? '+' : '') + fmt(state.dailyProfit);
            document.getElementById('statWeekly').innerText = (state.weeklyProfit >= 0 ? '+' : '') + fmt(state.weeklyProfit);
            document.getElementById('statMonthly').innerText = (state.monthlyProfit >= 0 ? '+' : '') + fmt(state.monthlyProfit);

            renderBookies();
            renderPending();
            renderSettled();
        }

        function switchTab(tab) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

            if (tab === 'calc') { document.getElementById('tabCalc').classList.add('active'); document.getElementById('tabBtn1').classList.add('active'); }
            else if (tab === 'track') { document.getElementById('tabTrack').classList.add('active'); document.getElementById('tabBtn2').classList.add('active'); }
            else { document.getElementById('tabSettings').classList.add('active'); document.getElementById('tabBtn3').classList.add('active'); }
        }

        function renderBookies() {
            const container = document.getElementById('bookiesContainer');
            container.innerHTML = bookies.map((b, idx) => `
                <div onclick="openBookieModal(${idx})" class="p-2.5 bg-slate-900 rounded-xl border border-slate-800 flex justify-between items-center cursor-pointer hover:border-blue-500/50 transition">
                    <span class="text-xs font-bold text-slate-300">${b.name}</span>
                    <span class="text-xs font-black text-white">${fmt(b.balance)}</span>
                </div>
            `).join('');
        }

        function openBookieModal(idx) {
            currentBookieIndex = idx;
            document.getElementById('inputBookieName').value = bookies[idx].name;
            document.getElementById('inputBookieBalance').value = bookies[idx].balance;
            document.getElementById('bookieModal').classList.remove('hidden');
        }
        function closeBookieModal() { document.getElementById('bookieModal').classList.add('hidden'); }
        function saveBookieModal() {
            if (currentBookieIndex !== null) {
                bookies[currentBookieIndex].name = document.getElementById('inputBookieName').value;
                bookies[currentBookieIndex].balance = parseFloat(document.getElementById('inputBookieBalance').value) || 0;
                updateBookieTotal();
                updateUI();
            }
            closeBookieModal();
        }
        function deleteCurrentBookie() {
            if (currentBookieIndex !== null) {
                bookies.splice(currentBookieIndex, 1);
                updateBookieTotal();
                updateUI();
            }
            closeBookieModal();
        }
        function addNewBookie() {
            bookies.push({ name: `Büro ${bookies.length + 1}`, balance: 0 });
            openBookieModal(bookies.length - 1);
        }
        function updateBookieTotal() {
            state.balance = bookies.reduce((acc, b) => acc + b.balance, 0);
        }

        function recalcArb() {
            const b1 = document.getElementById('calcB1Name').value || '1. Büro';
            const b2 = document.getElementById('calcB2Name').value || '2. Büro';
            const o1 = parseFloat(document.getElementById('calcOdds1').value) || 0;
            const o2 = parseFloat(document.getElementById('calcOdds2').value) || 0;
            const total = parseFloat(document.getElementById('calcTotalStake').value) || 0;

            document.getElementById('labelB1Stake').innerText = `${b1} Stake (Miktar):`;
            document.getElementById('labelB2Stake').innerText = `${b2} Stake (Miktar):`;

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
            const b1 = document.getElementById('calcB1Name').value || '1. Büro';
            const b2 = document.getElementById('calcB2Name').value || '2. Büro';
            const o1 = parseFloat(document.getElementById('calcOdds1').value) || 0;
            const o2 = parseFloat(document.getElementById('calcOdds2').value) || 0;
            const total = parseFloat(document.getElementById('calcTotalStake').value) || 0;
            const arb = (1 / o1) + (1 / o2);
            const s1 = (total * (1 / o1)) / arb;
            const s2 = (total * (1 / o2)) / arb;

            pendingBets.push({
                title: `Surebet (${b1} & ${b2})`,
                b1: b1, b2: b2, o1: o1, o2: o2,
                s1: s1, s2: s2, stake: total,
                note: 'Hesaplayıcıdan Eklendi'
            });

            state.risk += total;
            updateUI();
            switchTab('track');
        }

        function addManualBet() {
            const match = document.getElementById('manualMatch').value || 'Özel Surebet';
            const b1 = document.getElementById('manB1').value || '1. Büro';
            const o1 = parseFloat(document.getElementById('manO1').value) || 0;
            const s1 = parseFloat(document.getElementById('manS1').value) || 0;
            const b2 = document.getElementById('manB2').value || '2. Büro';
            const o2 = parseFloat(document.getElementById('manO2').value) || 0;
            const s2 = parseFloat(document.getElementById('manS2').value) || 0;
            const note = document.getElementById('manualNote').value || '';

            const totalStake = s1 + s2;
            if (totalStake <= 0) return;

            pendingBets.push({
                title: match, b1: b1, b2: b2, o1: o1, o2: o2,
                s1: s1, s2: s2, stake: totalStake, note: note
            });

            state.risk += totalStake;
            updateUI();
            switchTab('track');
        }

        function renderPending() {
            const container = document.getElementById('pendingList');
            if (pendingBets.length === 0) {
                container.innerHTML = '<div class="text-xs text-slate-500 text-center py-2">Bekleyen surebet bulunmuyor.</div>';
                return;
            }
            container.innerHTML = pendingBets.map((bet, idx) => `
                <div class="p-3 bg-slate-900 rounded-xl border border-slate-800 space-y-2">
                    <div class="flex justify-between items-start">
                        <div>
                            <div class="font-bold text-xs text-white">${bet.title}</div>
                            <div class="text-[10px] text-slate-300">1) ${bet.b1}: ${fmt(bet.s1)} @ ${bet.o1}</div>
                            <div class="text-[10px] text-slate-300">2) ${bet.b2}: ${fmt(bet.s2)} @ ${bet.o2}</div>
                            <div class="text-[10px] text-slate-400 pt-1">Toplam Yatırım: ${fmt(bet.stake)} | Not: ${bet.note}</div>
                        </div>
                        <button onclick="openSettleModal(${idx})" class="px-2.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-lg text-[10px]">Sonuçlandır</button>
                    </div>
                </div>
            `).join('');
        }

        function renderSettled() {
            const container = document.getElementById('settledList');
            if (settledBets.length === 0) {
                container.innerHTML = '<div class="text-xs text-slate-500 text-center py-2">Sonuçlanan surebet bulunmuyor.</div>';
                return;
            }
            container.innerHTML = settledBets.map((bet, idx) => `
                <div onclick="openDetailModal(${idx})" class="p-3 bg-slate-900 rounded-xl border border-slate-800 flex justify-between items-center text-xs cursor-pointer hover:bg-slate-800/80 transition">
                    <div>
                        <div class="font-bold text-white">${bet.title}</div>
                        <div class="text-[10px] text-slate-400">Sonuç: <span class="text-blue-400 font-bold">${bet.winner}</span></div>
                    </div>
                    <div class="text-right">
                        <div class="${bet.net >= 0 ? 'text-emerald-400' : 'text-rose-400'} font-extrabold">${bet.net >= 0 ? '+' : ''}${fmt(bet.net)}</div>
                        <div class="text-[9px] text-slate-500">Yönet / Geri Al ➔</div>
                    </div>
                </div>
            `).join('');
        }

        function openSettleModal(idx) {
            currentSettleIndex = idx;
            const bet = pendingBets[idx];
            const select = document.getElementById('settleResultType');
            select.innerHTML = `
                <option value="b1">${bet.b1} Kazandı (Alınacak: ${fmt(bet.s1 * bet.o1)})</option>
                <option value="b2">${bet.b2} Kazandı (Alınacak: ${fmt(bet.s2 * bet.o2)})</option>
                <option value="lost">Her İki Taraf Da Kaybetti (Lost)</option>
            `;
            document.getElementById('settleModal').classList.remove('hidden');
        }

        function closeSettleModal() { document.getElementById('settleModal').classList.add('hidden'); }
        function toggleBonusInput() {
            const val = document.getElementById('bonusTakenSelect').value;
            document.getElementById('bonusAmountContainer').classList.toggle('hidden', val !== 'evet');
        }

        function confirmSettle() {
            if (currentSettleIndex === null) return;
            const bet = pendingBets[currentSettleIndex];
            const res = document.getElementById('settleResultType').value;
            const bonusTaken = document.getElementById('bonusTakenSelect').value;
            const bonusVal = parseFloat(document.getElementById('inputBonusVal').value) || 0;

            state.risk -= bet.stake;
            let net = 0;
            let winnerName = '';

            if (res === 'b1') { 
                net = (bet.s1 * bet.o1) - bet.stake; 
                winnerName = `${bet.b1} Kazandı`; 
            } else if (res === 'b2') { 
                net = (bet.s2 * bet.o2) - bet.stake; 
                winnerName = `${bet.b2} Kazandı`; 
            } else { 
                net = -bet.stake; 
                winnerName = 'Komple Kayıp'; 
            }

            if (bonusTaken === 'evet' && bonusVal > 0) {
                state.bonus += bonusVal;
                net += bonusVal;
            }

            state.balance += net;
            state.netProfit += net;
            if (net > 0) {
                state.dailyProfit += net;
                state.weeklyProfit += net;
                state.monthlyProfit += net;
            }

            settledBets.push({
                title: bet.title, b1: bet.b1, b2: bet.b2,
                o1: bet.o1, o2: bet.o2, s1: bet.s1, s2: bet.s2,
                stake: bet.stake, winner: winnerName, net: net,
                bonus: bonusVal, note: bet.note
            });

            pendingBets.splice(currentSettleIndex, 1);
            updateUI();
            closeSettleModal();
        }

        function openDetailModal(idx) {
            currentDetailIndex = idx;
            const b = settledBets[idx];
            document.getElementById('detailContent').innerHTML = `
                <div class="flex justify-between border-b border-slate-800 pb-1"><span>Maç:</span> <strong class="text-white">${b.title}</strong></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span>1. Büro Stake:</span> <span>${b.b1} (${b.o1}) - ${fmt(b.s1)}</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span>2. Büro Stake:</span> <span>${b.b2} (${b.o2}) - ${fmt(b.s2)}</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span>Toplam Yatırım:</span> <span>${fmt(b.stake)}</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span>Kayıp Bonusu:</span> <span class="text-blue-400 font-bold">${fmt(b.bonus)}</span></div>
                <div class="flex justify-between border-b border-slate-800 pb-1"><span>Sonuç / Kazanan:</span> <span class="text-amber-400 font-bold">${b.winner}</span></div>
                <div class="flex justify-between font-bold pt-1"><span>Gerçekleşen Net Kâr:</span> <span class="${b.net >= 0 ? 'text-emerald-400' : 'text-rose-400'}">${fmt(b.net)}</span></div>
            `;
            document.getElementById('detailNoteText').value = b.note || '';
            document.getElementById('detailModal').classList.remove('hidden');
        }

        function closeDetailModal() { document.getElementById('detailModal').classList.add('hidden'); }
        
        function revertSettledBet() {
            if (currentDetailIndex !== null) {
                const b = settledBets[currentDetailIndex];
                state.balance -= b.net;
                state.netProfit -= b.net;
                state.bonus -= b.bonus;
                if(b.net > 0) {
                    state.dailyProfit -= b.net;
                    state.weeklyProfit -= b.net;
                    state.monthlyProfit -= b.net;
                }
                state.risk += b.stake;

                pendingBets.push({
                    title: b.title, b1: b.b1, b2: b.b2,
                    o1: b.o1, o2: b.o2, s1: b.s1, s2: b.s2,
                    stake: b.stake, note: b.note
                });

                settledBets.splice(currentDetailIndex, 1);
                updateUI();
                closeDetailModal();
                switchTab('track');
            }
        }

        function deleteSettledBet() {
            if (currentDetailIndex !== null) {
                const b = settledBets[currentDetailIndex];
                state.balance -= b.net;
                state.netProfit -= b.net;
                state.bonus -= b.bonus;
                if(b.net > 0) {
                    state.dailyProfit -= b.net;
                    state.weeklyProfit -= b.net;
                    state.monthlyProfit -= b.net;
                }
                settledBets.splice(currentDetailIndex, 1);
                updateUI();
                closeDetailModal();
            }
        }

        function saveDetailNote() {
            if (currentDetailIndex !== null) {
                settledBets[currentDetailIndex].note = document.getElementById('detailNoteText').value;
                renderSettled();
            }
            closeDetailModal();
        }

        function confirmResetAll() {
            if (confirm("Tüm kasayı, bahisleri ve verileri sıfırlamak istediğinize emin misiniz?")) {
                state = { balance: 10000, startBalance: 10000, goal: 20000, risk: 0, netProfit: 0, bonus: 0, currency: 'TRY', dailyProfit: 0, weeklyProfit: 0, monthlyProfit: 0 };
                bookies = [{ name: 'Bet365', balance: 5000 }, { name: '1xBet', balance: 5000 }];
                pendingBets = []; settledBets = [];
                updateUI();
                alert("Tüm veriler sıfırlandı!");
            }
        }

        function openBalanceModal() {
            document.getElementById('inputBalance').value = state.balance;
            document.getElementById('inputGoal').value = state.goal;
            document.getElementById('balanceModal').classList.remove('hidden');
        }
        function closeBalanceModal() { document.getElementById('balanceModal').classList.add('hidden'); }
        function saveBalanceModal() {
            state.balance = parseFloat(document.getElementById('inputBalance').value) || 0;
            state.goal = parseFloat(document.getElementById('inputGoal').value) || 0;
            updateUI();
            closeBalanceModal();
        }

        function changeCurrency() { state.currency = document.getElementById('currencySelect').value; updateUI(); }
        function changeTheme() {
            const theme = document.getElementById('themeSelect').value;
            document.getElementById('bodyRoot').className = `${theme} pb-36 p-3 max-w-lg mx-auto space-y-4`;
        }

        function exportData(type) { alert(`Veriler ${type.toUpperCase()} formatında indiriliyor...`); }

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
            print("Webhook başarıyla tanımlandı!")
        except Exception as e:
            print(f"Webhook hatası: {e}")

    asyncio.run(main_setup())

    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
