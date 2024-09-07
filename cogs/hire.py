import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import settings
from utils import send_log, get_transcript
from tickets import ticket_mod_role_id, closed_tickets_category_id, opened_tickets_category_id
import os

class Hire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def package_autocomplete(self, interaction: discord.Interaction, current: str):
        options = [
            "Bot - Starter",
            "Bot - Hobbyist",
            "Bot - Professional",
            "DC Server - $3",
            "DC Server - $5",
            "DC Server - $10",
            "MC Server",
            "Combined Package",
            "Bot host - $3/mo",
            "Server host $10/mo"
        ]
        choices = []

        print("before for loop")

        for option in options:
            if current.lower() in option.lower():
                choice = app_commands.Choice(name="hello", value="hello")
                choices.append(choice)

        print("after")

        print(choices)
        return choices

    @app_commands.command(name="hire", description="Hire Sheepie for a project.")
    @app_commands.describe(
        package="Select the package",
        budget="Specify your budget",
        description="Describe the project you need"
    )
    @app_commands.autocomplete(package=package_autocomplete)
    async def hire(self, interaction: discord.Interaction, package: str, budget: str, description: str):
        await interaction.response.defer(ephemeral=True)

        if package == 'bot_starter':
            package = 'Bot - Starter'
        elif package == 'bot_hobbyist':
            package = 'Bot - Hobbyist'
        elif package == 'bot_professional':
            package = 'Bot - Professional'
        elif package == 'dc_server_3':
            package = 'DC Server - $3'
        elif package == 'dc_server_5':
            package = 'DC Server - $5'
        elif package == 'dc_server_10':
            package = 'DC Server - $10'
        elif package == 'mc_server':
            package = 'MC Server'
        elif package == 'combined_package':
            package = 'Combined Package'
        elif package == 'bot_host_3_mo':
            package = 'Bot host - $3/mo'
        elif package == 'server_host_10_mo':
            package = 'Server host $10/mo'
        else:
            package = 'Unknown package'

        # Create the ticket channel
        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=opened_tickets_category_id)
        for ch in category.text_channels:
            if ch.topic == f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL, IT WILL BREAK THINGS!":
                await interaction.followup.send(f"You already have a ticket in {ch.mention}", ephemeral=True)
                return

        r1: discord.Role = interaction.guild.get_role(ticket_mod_role_id)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        }
        channel = await category.create_text_channel(
            name=f"{interaction.user}'s-ticket",
            topic=f"{interaction.user.id} DO NOT CHANGE THE TOPIC OF THIS CHANNEL, IT WILL BREAK THINGS!",
            overwrites=overwrites
        )

        # Send the user message and ticket creation info to the ticket channel
        await channel.send(f"<@{interaction.user.id}>, your ticket is ready!")
        await channel.send(f"<@&{ticket_mod_role_id}> will be with you soon.",
            embed=discord.Embed(
                title="Ticket Created!",
                description="Do not spam! You will get support soon.",
                color=discord.Color.green()
            ),
            view=CloseButton()
        )
        await channel.send(
            embed=discord.Embed(
                title="Project Details",
                description=f"**Package:** {package}\n**Budget:** {budget}\n**Description:** {description}",
                color=discord.Color.blue()
            )
        )
        await interaction.followup.send(
            embed=discord.Embed(
                description=f"Ticket created in {channel.mention}",
                color=discord.Color.random()
            ), 
            ephemeral=True
        )
        # Log ticket creation
        await send_log(title="Ticket Created",
            description=f"Created by {interaction.user.mention}",
            color=discord.Color.random(),
            guild=interaction.guild,
            closing=False
        )


class CloseButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Close the ticket", style=discord.ButtonStyle.red, custom_id="closeticket", emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        await interaction.channel.send("Closing this ticket...")

        await asyncio.sleep(3)

        category: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=closed_tickets_category_id)

        r1: discord.Role = interaction.guild.get_role(ticket_mod_role_id)
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            r1: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        await interaction.channel.edit(category=category, overwrites=overwrites)
        await interaction.channel.send(
            embed=discord.Embed(
                title="Ticket Closed!",
                color=discord.Color.red()
            ),
            view=TrashButton()
        )
        # Add transcript and log actions here

        transcript = await get_transcript(
            member=interaction.user,
            channel=interaction.channel,
            token=settings.TOKEN
        )

        await send_log(
            title="Ticket Closed",
            description=f"Closed by: {interaction.user.mention}",
            color=discord.Color.random(),
            guild=interaction.guild,
            closing=True
            # file=transcript
        )

        await asyncio.sleep(10)
        if os.path.exists('chat_exporter/ticket.html'):
            os.remove('chat_exporter/ticket.html')

class TrashButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Delete this ticket", style=discord.ButtonStyle.red, emoji="🗑️", custom_id="trash")
    async def trash(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.send("Deleting the ticket...")
        await asyncio.sleep(3)

        await interaction.channel.delete()

async def setup(bot):
    await bot.add_cog(Hire(bot))
