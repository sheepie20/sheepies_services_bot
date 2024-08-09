import os
import asyncio
import discord
from utils import *
import settings
from discord.ext import commands
import pretty_help
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix=settings.PREFIX, intents=settings.INTENTS, help_command=pretty_help.PrettyHelp(typing=False))

async def main():
    async with bot:
        await load_cogs(bot)
        await bot.start(settings.TOKEN)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')






if __name__ == "__main__":
    asyncio.run(main())
