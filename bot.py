import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import aiohttp

# -------------------
#  设置日志
logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

load_dotenv()
ALLOWED_USER_IDS = {1352654147735785624, 159985870458322944}
processed_messages = set()

# -------------------
# .env config
DC_BOT_Token = os.getenv("DC_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID", "0"))
TG_TOPIC_ID = int(os.getenv("MESSAGE_THREAD_ID", "0"))

if not DC_BOT_Token:
    logging.critical("NULL DC_BOT_TOKEN, exiting...")
    raise ValueError("NULL DC_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logging.critical("NULL TELEGRAM_BOT_TOKEN, exiting...")
    raise ValueError("NULL TELEGRAM_BOT_TOKEN")
if TG_CHAT_ID == 0:
    logging.critical("NULL TELEGRAM_CHAT_ID, exiting...")
    raise ValueError("NULL TELEGRAM_CHAT_ID")
if TG_TOPIC_ID == 0:
    logging.critical("NULL MESSAGE_THREAD_ID, exiting...")
    raise ValueError("NULL MESSAGE_THREAD_ID")

# -------------------
#  Intents class
intents = discord.Intents.default()
intents.message_content = True

# create bot client
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logging.info(f"Bot {bot.user} is up and running!")


@bot.event
async def on_message(message):
    if message.author.id not in ALLOWED_USER_IDS:
        return

    if message.author == bot.user:
        return

    if message.id in processed_messages:
        logging.debug(f"Skipping duplicate message ID: {message.id}")
        return

    logging.info(f"Received message ID {message.id} from {message.author}: {message.content}")

    await send_to_telegram(message.content)
    processed_messages.add(message.id)  # save msg ID


async def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "message_thread_id": TG_TOPIC_ID
    }

    retry_delay = 2  # 初始重试间隔（秒）

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.post(url, data=payload) as response:
                    if response.status == 200:
                        logging.info("Message successfully sent to Telegram")
                        return
                    elif response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", retry_delay))
                        logging.warning(f"Rate limited, retrying in {retry_after}s...")
                        await asyncio.sleep(retry_after)
                    else:
                        logging.error(f"Failed to send Telegram message: {response.status}")
                        return
            except aiohttp.ClientError as e:
                logging.error(f"Telegram request failed: {e}, retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 30)


# RUN BOT
if __name__ == "__main__":
    logging.info("Starting Discord bot...")
    bot.run(DC_BOT_Token)
