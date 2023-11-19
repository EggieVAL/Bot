import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'myroom',
    description = 'Displays your room'
)
async def myroom(interaction: discord.Interaction) -> None:
    """
    Displays the player's room information when executing this command.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    user = interaction.user
    guild = interaction.guild
    await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    player.room.thread = await room.search_room(user=user, guild=guild)
    if player.room.thread:
        await graphics.display_msg_embed(
            obj = interaction,
            title = player.room.thread.name,
            description = f'Access your gaming room here: [{player.room.thread.mention}]',
            color = discord.Color.greyple()
        )
    else:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Your room does not exist',
            description = f'Type /createroom or start a game to create your room',
            color = discord.Color.red()
        )