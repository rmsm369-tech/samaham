import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from agent import run_agent_query

load_dotenv()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = run_agent_query(user_input)
    await update.message.reply_text(response)

def main():
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("OmniAgent Telegram Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()