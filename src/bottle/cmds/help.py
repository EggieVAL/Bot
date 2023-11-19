import discord

from player import update_players
from ..bot import bot

@bot.tree.command(
    name = 'help',
    description = 'Displays available commands'
)
async def help(interaction: discord.Interaction) -> None:
    """
    Displays available commands to the user who executed this command.
    """
    await interaction.response.defer(ephemeral=True, thinking=True)
    await update_players(interaction=interaction)
    
    embed = discord.Embed(
        title = 'Help',
        description = 'List of all commands',
        color = discord.Color.greyple()
    )
    embed.set_thumbnail(url=bot.user.avatar.url)
    
    for slash_cmd in bot.tree.walk_commands():
        embed.add_field(
            name = f'**/{slash_cmd.name}**',
            value = slash_cmd.description,
            inline = True
        )
    await interaction.followup.send(embed=embed)