from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from handlers.start import start

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("✅ Admin Bot Running")
    app.run_polling()

if __name__ == "__main__":
    main()
