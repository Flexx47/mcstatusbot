# -*- coding: utf-8 -*-

import discord
from discord.ext import commands, tasks
import asyncio
import requests

# Config
SERVER_ADDRESS = "your.epic.serveradress" 
SERVER_PORT = 25566  # Your epic server port

PREFIX = "!"
TOKEN = "YOUR-EPIC-BOT-TOKEN"  
CHANNEL_ID = 0000000000000000000 # Your epic Discord server channel ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

async def get_server_info():
    try:
        response = requests.get(f"https://api.mcsrvstat.us/2/{SERVER_ADDRESS}")
        data = response.json()
        if response.status_code == 200 and data["online"]:
            return data["players"]["online"], True
        else:
            return 0, False
    except Exception as e:
        print(f"Errorcode: {e}")
        return 0, False

@bot.command()
async def refresh(ctx):
    await update_status()
    await ctx.send("McStatus was force refreshed!")

@tasks.loop(seconds=60)
async def update_status():
    online_players, server_online = await get_server_info()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        if server_online:
            await channel.edit(name=f"\U0001F7E2\u200Bonline\U0001F465{online_players}")
        else:
            await channel.edit(name="\U0001F534\u200Bmaintenance")
    else:
        print("Channel not found!")

@bot.event
async def on_ready():
    print("McStatus is up and running!")
    update_status.start()

bot.run(TOKEN)
