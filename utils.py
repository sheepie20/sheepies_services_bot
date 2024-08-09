import discord
from discord.ext import commands
import os
import settings
import tickets
from keep_alive import keep_alive
keep_alive()

async def load_cogs(bot: commands.Bot):
    await bot.load_extension("cogs.hire")
    await bot.load_extension("cogs.owner")

async def get_transcript(member: discord.Member, channel: discord.TextChannel, token: str):
    # Run the export command
    os.system(f"chat_exporter\\DiscordChatExporter.Cli.exe export --channel {channel.id} --token {token} --output chat_exporter/ticket.html --fuck-russia")

    file_path = "chat_exporter/ticket.html"
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:  # Open in binary mode
            return discord.File(f, filename="ticket.html")
    else:
        return None


async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color, file: discord.File):
    log_channel = guild.get_channel(tickets.ticket_transcripts_channel_id)
    if not log_channel:
        return

    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    if file:
        await log_channel.send(embed=embed, file=file)
    else:
        await log_channel.send(embed=embed)
    
