import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'delroom',
    description = 'Deletes your personalized gaming room'
)
async def delroom(interaction: discord.Interaction) -> None:
    """
    Deletes the user's gaming room when executing this command.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    user = interaction.user
    guild = interaction.guild
    await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    player.room.thread = await room.search_room(user=user, guild=guild)
    if player.room.thread is None:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Your room does not exist',
            description = 'Type /createroom or start a game to create your room',
            color = discord.Color.red()
        )
        player.in_game = None
    elif player.in_game:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'You are currently in a game',
            description = 'Type /quit to exit your game',
            color = discord.Color.red()
        )
    else:
        await player.room.thread.delete()
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Deleted your room',
            description = 'Type /createroom or start a game to create your room',
            color = discord.Color.blurple()
        )
        player.room.thread = None