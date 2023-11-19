import discord
import graphics

from player import *
from ..bot import bot

@bot.tree.command(
    name = 'stats',
    description = 'Displays your statistics'
)
async def stats(
    interaction: discord.Interaction,
    user: discord.Member | discord.User | None = None,
    showoff: bool = False,
    dropdown: bool = True
) -> None:
    """
    Displays the statistics of a player.
    """
    await interaction.response.defer(ephemeral=(not showoff), thinking=True)
    
    user = interaction.user if user is None else user
    guild = interaction.guild
    await update_players(user=user, guild=guild)
    player = PLAYERS[user.name]
    
    if dropdown:
        menus: dict[str, discord.Embed] = {}
        options: dict[str, str] = {}
        
        for mode in player.data['stats']:
            menus[mode] = build_stats_menu(player, mode)
            options[mode] = f'Display {mode} statistics'
        
        await graphics.DropdownNavigationMenu.create_and_display(interaction=interaction, menus=menus, options=options)
    else:
        menus = [build_stats_menu(player, mode) for mode in player.data['stats']]
        await graphics.ArrowNavigationMenu.create_and_display(interaction=interaction, menus=menus)

def build_stats_menu(player: Player, mode: str) -> discord.Embed:
    """
    Builds a statistics embed of the player.
    """
    
    stats: dict[str, int] = player.data['stats'][mode]
    total_games_completed = stats['wins'] + stats['losses']
    total_games_played = total_games_completed + stats['forfeits']
    winrate = None if total_games_completed == 0 else stats['wins'] * 100 / total_games_completed
    
    menu = discord.Embed(
        title = f'{mode} Statistics',
        color = discord.Color.greyple(),
        description = f"""
                       {'***1 Game Completed***' if total_games_completed == 1 else f'***{total_games_completed} Games Completed***'}
                       {'***1 Game Played***' if total_games_played == 1 else f'***{total_games_played} Games Played***'}
                       """
    )
    menu.set_thumbnail(url=player.user.avatar.url)
    menu.add_field(
        name = '',
        value = f'**Win Rate**: N/A' if winrate is None else f'**Win Rate**: {winrate:.2f}%',
        inline = False 
    )
    
    for key, value in stats.items():
        name = ' '.join(key.split('_')).title()
        
        if key == 'fastest_guess':
            value = 'N/A' if value < 0 else f'{value:.2f} seconds'
            
        menu.add_field(name=name, value=value, inline = True)
    return menu