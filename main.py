import discord
import settings
from settings import utils
from discord.ext import commands
import pretty_help
from keep_alive import run
run()


bot = commands.Bot(
    command_prefix=settings.COMMAND_PREFIX, 
    intents=settings.INTENTS,
    help_command=pretty_help.PrettyHelp(typing=False),
    status=settings.STATUS
)

@bot.event
async def on_ready():
    await utils.init_db()
    await bot.load_extension("cogs.tickets")
    await bot.load_extension("cogs.owner")
    await bot.change_presence(activity=discord.CustomActivity(name='👑Visit #hire-sheepie to hire!'))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f"logged in as {bot.user} ({bot.user.id})")
    print('------')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(error)

if __name__ == "__main__":
    bot.run(settings.TOKEN)
