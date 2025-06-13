import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Načtení tokenu z prostředí
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Chybí proměnná prostředí BOT_TOKEN. Nastav ji v Railway.")

# Základní příkaz /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Vítej u TipniToBota! 📊\nZde budeš dostávat tipy na tikety.")

# Inicializace aplikace
def hlavni():
    aplikace = ApplicationBuilder().token(TOKEN).build()
    aplikace.add_handler(CommandHandler("start", start))

    aplikace.run_polling()

if __name__ == "__main__":
    hlavni()
