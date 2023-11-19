import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'quit',
    description = 'Quits (forfeits) the game you are playing'
)
async def quit(interaction: discord.Interaction) -> None:
    """
    Quits the user's game when they execute this command.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    user = interaction.user
    guild = interaction.guild
    await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    if not player.in_game:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'You are currently not in a game',
            description = 'Type /<gamemode> to start one',
            color = discord.Color.red()
        )
        return
    
    player.room.thread = await room.search_room(user=user, guild=guild)
    player.in_game.terminate()
    
    await graphics.display_msg_embed(
        obj = interaction,
        title = 'Forfeited',
        description = 'You have left the game',
        color = discord.Color.red()
    )
    if player.room.thread is not None:
        await player.room.thread.edit(archived=True)