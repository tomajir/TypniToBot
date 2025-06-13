
import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

with open("tipy.json", "r", encoding="utf-8") as f:
    TIPY = json.load(f)
with open("vip_whitelist.json", "r", encoding="utf-8") as f:
    VIP_USERS = json.load(f)["users"]

def format_tip(tip):
    return (
        f"{tip['sport']} *{tip['zapas']}*\n"
        f"💰 Kurz: {tip['kurz']}\n"
        f"💸 Vklad: {tip['vklad']}\n"
        f"📈 Důvěra: {tip['duvera']}\n"
        f"🕒 Začátek: {tip['cas']}\n"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Vítej v *TipniToBotu* – denní tipy a VIP obsah.\n"
        "Použij příkazy:\n"
        "/dnes – dnešní tipy\n"
        "/zitra – tipy na zítřek\n"
        "/vip – VIP tikety (jen pro členy)\n"
        "/kontakt – kontakt na admina",
        parse_mode="Markdown"
    )

async def dnes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tips = TIPY.get("dnes", [])
    if not tips:
        return await update.message.reply_text("Dnes nejsou žádné tipy.")
    await update.message.reply_text("*🎯 DNEŠNÍ TIPY:*", parse_mode="Markdown")
    for tip in tips:
        await update.message.reply_text(format_tip(tip), parse_mode="Markdown")

async def zitra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tips = TIPY.get("zitra", [])
    if not tips:
        return await update.message.reply_text("Zatím nejsou tipy na zítřek.")
    await update.message.reply_text("*🔜 TIPY NA ZÍTRA:*", parse_mode="Markdown")
    for tip in tips:
        await update.message.reply_text(format_tip(tip), parse_mode="Markdown")

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in VIP_USERS:
        tips = TIPY.get("vip", [])
        await update.message.reply_text("*🔥 VIP TIPY:*", parse_mode="Markdown")
        for tip in tips:
            await update.message.reply_text(format_tip(tip), parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Tento obsah je dostupný jen VIP členům.")

async def kontakt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📬 Kontakt na admina: @tvujTelegramNick")

def main():
    token = os.getenv("TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dnes", dnes))
    app.add_handler(CommandHandler("zitra", zitra))
    app.add_handler(CommandHandler("vip", vip))
    app.add_handler(CommandHandler("kontakt", kontakt))
    app.run_polling()

if __name__ == "__main__":
    main()
