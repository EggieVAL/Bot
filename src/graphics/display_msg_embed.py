import discord
import discord.ext.commands

from room import Room

async def display_msg_embed(
    obj: discord.ext.commands.Context | discord.Interaction | discord.Thread | Room,
    *,
    title: str,
    description: str,
    color: discord.Color,
    ephemeral: bool = True
) -> discord.Message | None:
    """
    Displays an embed to either one of these three different objects: a context,
    interaction, or thread.
    
    This function helps east the tedious task of building and displaying an embed.
    
    Returns:
        The message that was displayed, or None if 'obj' is an interaction.
    """
    
    try:
        embed = discord.Embed(title=title, description=description, color=color)
        
        if isinstance(obj, discord.Interaction):
            if obj.response.is_done():
                await obj.followup.send(embed=embed, ephemeral=ephemeral)
            else:
                await obj.response.send_message(embed=embed, ephemeral=ephemeral)
        elif isinstance(obj, discord.ext.commands.Context):
            return await obj.send(embed=embed, ephemeral=ephemeral)
        elif isinstance(obj, discord.Thread):
            return await obj.send(embed=embed)
        elif isinstance(obj, Room):
            return await obj.thread.send(embed=embed)
        else:
            raise ValueError('obj is not of type Context, Interaction, Thread, or Room.')
    except:
        pass