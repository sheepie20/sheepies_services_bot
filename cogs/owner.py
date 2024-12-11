from discord.ext import commands
import discord

class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="sync-tree")
    @commands.is_owner()
    async def sync_tree(self, ctx: commands.Context) -> None:
        self.bot.tree.copy_global_to(guild=self.bot.guilds[0])
        await self.bot.tree.sync()
        print("Tree loaded successfully")
        await ctx.send("Tree loaded successfully")

async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))
