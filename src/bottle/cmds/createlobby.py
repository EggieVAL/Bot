import discord
import lobby

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'createlobby',
    description = 'Creates a lobby where players can play against each other'
)
async def createlobby(interaction: discord.Interaction) -> None:
    """
    Creates a gaming lobby where players can join. This enables players to face against each other
    players in a Wordle game.

    The owner of the lobby can customize the game the players will be playing by initiating
    additional commands. For example, to change or select the gamemode, the owner of the lobby will
    type in the respective command. So, if they wanted to play Feudle, they will type /feudle after
    they created a lobby.
    """
    await interaction.response.defer(ephemeral=False, thinking=True)
    await update_players(interaction=interaction)
    player = PLAYERS[interaction.user.name]
    
    await interaction.followup.send(
        embed = lobby.Lobby.build_menu(interaction.user),
        ephemeral = False,
        view = lobby.Lobby(player=player)
    )
