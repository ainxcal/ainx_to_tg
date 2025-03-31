import asyncio
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests

load_dotenv()

###
# .env config
# DC bot token
dctoken = os.getenv("DC_BOT_TOKEN")

#TG bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TG_TOPIC_ID = os.getenv("MESSAGE_THREAD_ID")
###


# -------------------
#  Intents class
intents = discord.Intents.default()
intents.message_content = True

# create bot client
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} up！")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await asyncio.sleep(1)

    print(f"get msg：{message.content}")
    # send to tg
    send_to_telegram({message.content})


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "message_thread_id": TG_TOPIC_ID
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("success to Telegram")
    except requests.exceptions.RequestException as e:
        print(f"failed Telegram: {e}")
        time.sleep(5)

# start
if __name__ == "__main__":
    bot.run(dctoken)
