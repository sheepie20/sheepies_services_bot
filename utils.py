import discord
from discord.ext import commands
import os
import aiohttp
import uuid
import tickets
from discord.ui import Button, View

async def load_cogs(bot: commands.Bot):
    await bot.load_extension("cogs.hire")
    await bot.load_extension("cogs.owner")

async def send_log(title: str, guild: discord.Guild, description: str, color: discord.Color, file: discord.File = None, url=None):
    log_channel = guild.get_channel(tickets.ticket_transcripts_channel_id)
    if not log_channel:
        return

    embed = discord.Embed(
        title=title,
        url=url,
        description=description,
        color=color
    )

    await log_channel.send(embed=embed)

async def get_transcript(member: discord.Member, channel: discord.TextChannel, token: str):
    # Generate a unique UUID for the file
    unique_id = str(uuid.uuid4())
    
    # Export the chat transcript
    os.system(f"chat_exporter//DiscordChatExporter.Cli.exe export --channel {channel.id} --token {token} --output chat_exporter/{unique_id}_{channel.topic.split(' ')[0]}_ticket.html --fuck-russia")

    new_file_path = f"chat_exporter/{unique_id}_{channel.topic.split(' ')[0]}_ticket.html"

    if os.path.exists(new_file_path):
        print(f"File {new_file_path} exists, preparing to upload...")

        async with aiohttp.ClientSession() as session:
            with open(new_file_path, "rb") as f:
                form_data = aiohttp.FormData()
                form_data.add_field(
                    'file',  # 'file' matches the field name expected by the Flask app
                    f,
                    filename=os.path.basename(new_file_path),
                    content_type='text/html'
                )
                
                # Post request with form data
                async with session.post("https://sheepie.pythonanywhere.com/upload", data=form_data) as response:
                    response_text = await response.text()
                    if response.status == 200:
                        print("File uploaded successfully!")
                        log_channel = channel.guild.get_channel(tickets.ticket_transcripts_channel_id)
                        embed = discord.Embed(title="Ticket closed.", description=f"Click [here](https://sheepie.pythonanywhere.com/uploads/{unique_id}_{channel.topic.split(' ')[0]}_ticket.html) for the transcript.", color=discord.Color.red())
                        await log_channel.send(embed=embed)
                    else:
                        print(f"Failed to upload file. Status code: {response.status}")
                        print(f"Response text: {response_text}")
    else:
        print(f"File {new_file_path} does not exist!")

    try:
        os.remove(f"chat_exporter/{unique_id}_{channel.topic.split(' ')[0]}_ticket.html")
    except:
        pass
