import discord
import graphics

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'leave',
    description = 'Leaves the lobby you are in.'
)
async def leave(interaction: discord.Interaction) -> None:
    """
    Leaves the lobby the user is in when they execute this command.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    await update_players(interaction=interaction)