import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import aiohttp  # 异步 HTTP 请求库

load_dotenv()

###
# .env config
# DC bot token
dctoken = os.getenv("DC_BOT_TOKEN")

# TG bot token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TG_TOPIC_ID = os.getenv("MESSAGE_THREAD_ID")
###

# -------------------
#  Intents class
intents = discord.Intents.default()
intents.message_content = True

# 创建 bot client
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
    await send_to_telegram(message.content)



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


# 启动 bot
if __name__ == "__main__":
    bot.run(dctoken)
