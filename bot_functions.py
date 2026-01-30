import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from stockmarket import get_stock_message
from weather import get_weather_message
from steam_extraction import get_message_cases, get_message_stockholm_capsules
import os
from white_list import get_whitelist_users


GREEN = "\033[32m"
RESET = "\033[0m"
RED = "\033[31m"


'''
To generate API for your telegram bot simply just find @BotFather on telegram and send him:

/newbot

then he will ask you for name and will generate api key for you
'''


TOKEN = os.getenv("TELEGRAM_BOT")
KOMENDY = ['pogoda', 'stock', 'skrzynki', 'stockholm']


if not TOKEN:
    raise RuntimeError("Brak TELEGRAM_BOT_TOKEN w zmiennych środowiskowych")


def user_flag(user_id) ->bool:
    white_list = get_whitelist_users()
    if user_id in white_list:
        return True
    else: False


# returns sender a message with available list command
def reply_echo_error(input_text):
    message = f"{input_text}" + " nie ma w słowniku komend\n" + f"dostepne komendy znajdziesz pod funkcja komendy"
    return message

def get_komendy():
    output = "Dostępne komendy: \n"
    for i in KOMENDY:
        output += i + "\n"
    return output

# Hangling input messages right now make it primitive simple commands no room for errors
async def pick_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_message = update.message.text.strip().lower()
    print(input_message)
    if user_flag(update.effective_user.id):
        if input_message in ["pogoda", "Pogoda", "pgda"]:
            message = get_weather_message([53.4285, 14.5528]) # Default szczecin

        elif input_message in ["gielda", "giełda", "stock"]:
            message = get_stock_message()
        
        elif input_message in ["lokalikzacja", "lokacja", "gdzie jestem"]:
            message = "Narazie nie wiem jak handlowac pobieranie lokalizacji jestem tylko glupim botem ;("

        elif input_message in ["skrzynki"]:
            message = get_message_cases()

        elif input_message in ["stockholm", "kapsuly stockholm"]:
            message = get_message_stockholm_capsules()

        elif input_message in ["komendy"]:
            message = get_komendy()

        elif input_message in ["id"]:
            await update.message.reply_text(update.effective_user.id)

        else:
            message = reply_echo_error(input_message)
    else:
        print(f"{GREEN}DEBUG{RESET} ID: {update.effective_user.id} is not on the whitelist")
        message = f"User \n\n{update.effective_user.name}\n\n nie ma na whiteliscie"
    await update.message.reply_text(message)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pick_message))
    app.run_polling()



if __name__ == "__main__":
    main()
