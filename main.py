import os
import asyncio
import discord
from utils import *
import settings
from discord.ext import commands
import pretty_help
import discord_android
from dotenv import load_dotenv
load_dotenv()
from keep_alive import keep_alive
keep_alive()

bot = commands.Bot(
    command_prefix=settings.PREFIX, 
    intents=settings.INTENTS, 
    help_command=pretty_help.PrettyHelp(typing=False),
    status=settings.STATUS
)

async def main():
    async with bot:
        await load_cogs(bot)
        await bot.start(settings.TOKEN)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name='Do /hire to hire Sheepie!' ,emoji='👑'))
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

if __name__ == "__main__":
    asyncio.run(main())
