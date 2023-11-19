import discord
import room

from .game import Game, graphics, player
from .modes import *

async def create_game(
    interaction: discord.Interaction,
    *,
    mode: str,
    player: player.Player,
) -> Game | None:
    """
    Creates a Wordle game with the given mode.
    """
    if player.in_game:
        action = 'quit' if isinstance(player.in_game, Game) else 'leave'
        obj_type = 'game' if isinstance(player.in_game, Game) else 'lobby'
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Already in game',
            description = f'Type /{action} to {action} the {obj_type}.',
            color = discord.Color.red()
        )
        return
    
    player.room.thread, created = await room.create_room(
        user = player.user,
        guild = player.guild,
        channel = interaction.channel
    )
    try: await player.room.thread.add_user(player.user)
    except: pass
    
    if created:
        await graphics.display_msg_embed(
            obj = interaction,
            title = 'Created your personal gaming room',
            description = f'Access your room here: [{player.room.thread.mention}]',
            color = discord.Color.blurple()
        )
    else:
        await player.room.thread.edit(archived=False)
        if interaction.channel.name == player.room.thread.name:
            await graphics.display_msg_embed(
                obj = interaction,
                title = 'Clearing your room',
                description = f'Please wait for a moment for a new game to be created',
                color = discord.Color.blurple()
            )
        else:
            await graphics.display_msg_embed(
                obj = interaction,
                title = 'Clearing your room',
                description = f'Please wait in [{player.room.thread.mention}] for a new game to be created',
                color = discord.Color.blurple()
            )
        try: await player.room.thread.purge()
        except: pass
        
    match mode:
        case 'Standard':
            return Standard(player=player)
        case 'Daily':
            return Daily(player=player)
        case 'Feudle':
            return Feudle(player=player)
        case _:
            raise ValueError(f'{mode} is not a valid gamemode')