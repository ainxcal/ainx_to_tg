import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()

###
# .env config
# DC bot token
dctoken = os.getenv("DC_BOT_TOKEN")


# TG bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TG_TOPIC_ID = os.getenv("MESSAGE_THREAD_ID")

if not dctoken:
    raise ValueError("NULL DC_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("NULL TELEGRAM_BOT_TOKEN")
if not TG_CHAT_ID:
    raise ValueError("NULL TELEGRAM_CHAT_ID")
if not TG_TOPIC_ID:
    raise ValueError("NULL MESSAGE_THREAD_ID")
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
    msg_id = 0
    if message.author == bot.user:
        return

    await asyncio.sleep(1)

    print(f"ID: {message.id}, mentions: {message.mentions}")

    if msg_id == message.id:
        print(f"don't send msg")
    else:
        await send_to_telegram(message.content)
        msg_id = message.id


async def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "message_thread_id": TG_TOPIC_ID
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=payload) as response:
                if response.status == 200:
                    print("success to Telegram")
                else:
                    print(f"failed Telegram:  {response.status}")
                    await asyncio.sleep(5)
        except aiohttp.ClientError as e:
            print(f"failed Telegram: {e}")
            await asyncio.sleep(5)


#RUN BOT
if __name__ == "__main__":
    bot.run(dctoken)
