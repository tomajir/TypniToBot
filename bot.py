
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from datetime import datetime

TIPS_FILE = "data/tipy.json"
VIP_FILE = "data/vip_whitelist.json"
STATS_FILE = "data/statistiky.json"

def load_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Vítej u TipniToBot! 📊 Zadej /nápověda pro seznam příkazů.")

async def napoveda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Dostupné příkazy:
/tipy – Dnešní tipy
/vip – Ověření VIP členství
/viptipy – Tipy jen pro VIP
/statistiky – Úspěšnost a ROI
/minule – Poslední výsledky
/hlasuj – Hlasování o příštím tipu
/dotaz – Pošli dotaz adminovi
/balíčky – Nabídka VIP tarifů""")

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    vip_data = load_data(VIP_FILE)
    if user_id in vip_data["vip_users"]:
        await update.message.reply_text("✅ Jsi VIP uživatel.")
    else:
        await update.message.reply_text("❌ Nejsi VIP. Zadej /balíčky pro zobrazení nabídek.")

async def tipy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now().strftime("%Y-%m-%d")
    tipy = load_data(TIPS_FILE)
    dnesni_tipy = [t for t in tipy if t["datum"] == today]
    if not dnesni_tipy:
        await update.message.reply_text("Dnes zatím nejsou žádné tipy.")
    else:
        msg = "📌 *Dnešní tipy:*

"
        for t in dnesni_tipy:
            msg += f"🏟️ {t['zapas']}\n⚽ {t['sport']}\n🎯 Tip: *{t['tip']}*\n💰 Kurz: {t['kurz']}\n
"
        await update.message.reply_markdown(msg)

async def viptipy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    vip_data = load_data(VIP_FILE)
    if user_id not in vip_data["vip_users"]:
        await update.message.reply_text("⚠️ Tato sekce je pouze pro VIP. Zadej /balíčky pro přístup.")
        return
    await tipy(update, context)

async def statistiky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = load_data(STATS_FILE)
    msg = (
        f"📊 *Statistiky TipniToBot:*

"
        f"Celkem tipů: {stats['celkem_tipu']}
"
        f"✅ Výher: {stats['vyher']}
"
        f"❌ Proher: {stats['proher']}
"
        f"📈 ROI: {stats['roi']} %"
    )
    await update.message.reply_markdown(msg)

async def minule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tipy = load_data(TIPS_FILE)
    posledni = tipy[-5:] if len(tipy) >= 5 else tipy
    msg = "🕘 *Poslední tipy:*

"
    for t in reversed(posledni):
        msg += f"{t['datum']} – {t['zapas']}\nTip: {t['tip']} | Kurz: {t['kurz']} | Výsledek: {t['vysledek']}\n
"
    await update.message.reply_markdown(msg)

async def hlasuj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("⚽ Fotbal", callback_data='fotbal'),
                 InlineKeyboardButton("🏒 Hokej", callback_data='hokej')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("O který tip máš zájem zítra?", reply_markup=reply_markup)

async def dotaz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Napiš mi dotaz a přepošlu ho adminovi (zatím neaktivní).")

async def balicky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""🎁 VIP balíčky:
1️⃣ 7 dní – 99 Kč
2️⃣ 30 dní – 299 Kč
3️⃣ 90 dní – 699 Kč
(Pro aktivaci napiš adminovi.)""")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nápověda", napoveda))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("tipy", tipy))
    app.add_handler(CommandHandler("viptipy", viptipy))
    app.add_handler(CommandHandler("statistiky", statistiky))
    app.add_handler(CommandHandler("minule", minule))
    app.add_handler(CommandHandler("hlasuj", hlasuj))
    app.add_handler(CommandHandler("dotaz", dotaz))
    app.add_handler(CommandHandler("balíčky", balicky))

    app.run_polling()

if __name__ == "__main__":
    main()
