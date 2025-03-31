import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

# 从环境变量中获取 token
token = os.getenv("TOKEN")
if token is None:
    raise ValueError("token null")

# 创建 Intents 对象
intents = discord.Intents.default()
intents.message_content = True  # 确保你启用了这个权限

# 创建一个 Bot 客户端，传入代理连接器
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} 已经成功上线！")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"接收到消息：{message.content}")
    # 自动回应消息
    await message.channel.send("Hello from bot!")

# 启动 Bot（注意：使用 bot.run() 方法，不需要显式创建事件循环）
if __name__ == "__main__":
    bot.run(token)  # 使用 bot.run() 启动 Bot
