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
