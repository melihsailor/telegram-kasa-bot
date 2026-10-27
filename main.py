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

        <div class="grid grid-cols-3 gap-
