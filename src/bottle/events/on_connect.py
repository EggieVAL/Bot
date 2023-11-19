from discord import Game
from ..bot import bot

@bot.event
async def on_connect() -> None:
    await bot.change_presence(activity=Game('Wordle'))