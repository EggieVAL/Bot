import discord
import graphics
import room

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'createroom',
    description = 'Creates your personalized gaming room'
)
async def createroom(
    interaction: discord.Interaction,
    private: bool | None = None
) -> None:
    """
    Creates a personalized gaming room for the user who uses this command.
    
    Create a public room by setting 'private' to false.
    Create a private room by setting 'private' to true.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    
    user = interaction.user
    guild = interaction.guild
    channel = interaction.channel
    await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    player.room.thread, created = await room.create_room(user=user, guild=guild, channel=channel, private=private)
    if created:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Created your personalized gaming room',
            description = f'Access your room here: [{player.room.thread.mention}]',
            color = discord.Color.blurple()
        )
        await player.room.thread.edit(archived=True)
        await player.room.thread.add_user(user)
    else:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Your room already exists',
            description = f'Visit your gaming room here: [{player.room.thread.mention}]',
            color = discord.Color.red()
        )