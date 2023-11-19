import discord

from discord.ext import commands
from .botconfig import *

__intents = discord.Intents.default()
__intents.guilds = True
__intents.members = True
__intents.message_content = True

def __get_prefix(_, message: discord.Message) -> str:
    if DefaultConfig.enable_command_prefix():
        return DefaultConfig.command_prefix()
    return message.content + '!'

bot = commands.Bot(command_prefix=__get_prefix, intents=__intents)

import lobby
import game
import bottle.events
import bottle.cmds

def run() -> None:
    bot.run(TOKEN)