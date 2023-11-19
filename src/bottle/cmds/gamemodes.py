import discord
import game
import graphics
import lobby

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'standard',
    description = 'Starts a standard Wordle game'
)
async def standard(interaction: discord.Interaction) -> None:
    """
    Starts a standard Wordle game for the user who used the slash command: /standard.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    await update_players(interaction=interaction)
    player = PLAYERS[interaction.user.name]
    await __run_game(interaction=interaction, mode='Standard', player=player)

@bot.tree.command(
    name = 'daily',
    description = 'Starts the daily Wordle challenge'
)
async def daily(interaction: discord.Interaction) -> None:
    """
    Starts the daily Wordle challenge for the user who used the slash command: /daily.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    await update_players(interaction=interaction)
    player = PLAYERS[interaction.user.name]
    await __run_game(interaction=interaction, mode='Daily', player=player)

@bot.tree.command(
    name = 'feudle',
    description = 'Starts a Feudle game'
)
async def feudle(interaction: discord.Interaction) -> None:
    """
    Starts a Feudle game for the user who used the slash command: /feudle.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    await update_players(interaction=interaction)
    player = PLAYERS[interaction.user.name]
    await __run_game(interaction=interaction, mode='Feudle', player=player)
        
async def __run_game(
    interaction: discord.Interaction,
    *,
    mode: str,
    player: Player
) -> None:
    if not await __is_lobby_owner(interaction=interaction, mode=mode, player=player):
        wordle = await game.create_game(interaction=interaction, mode=mode, player=player)
        await wordle.run(interaction)
    
async def __is_lobby_owner(
    interaction: discord.Interaction,
    *,
    mode: str,
    player: Player
) -> bool:
    if not isinstance(player.in_game, lobby.Lobby):
        return False
    if player.in_game.players[player.user.name]['owner']:
        player.in_game.mode = mode
    
        await graphics.display_msg_embed(
            obj = interaction,
            title = f'Changed mode to {mode}',
            description = '',
            color = discord.Color.blurple()
        )
        return True
    return False