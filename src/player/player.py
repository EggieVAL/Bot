import discord
import game
import json
import lobby
import os
import room
import shutil

from .playerconfig import *

class Player:
    """
    A player is a discord member or user. The difference is that a member belongs to a
    guild.
    
    Players have records of all games they have played. For every game they play, they
    accumulate points and scores. These are their statistics, which can be seen by any
    player.
    """
    
    def __init__(
        self,
        *,
        user: discord.Member | discord.User,
        guild: discord.Guild
    ) -> None:
        self.user = user
        'The discord member or user representing this player.'
        self.guild = guild
        'The guild they were last seen interacting with BOTTLE.'
        self.room: room.Room = room.Room(user=user)
        'The gaming room the player owns.'
        self.in_game: game.Game | lobby.Lobby | None = None
        'The game the player is in.'
        self.data = Player.get_data(user)
        'The data of this player.'
        
    @staticmethod
    def get_data_file(user: discord.Member | discord.User) -> str:
        """
        Returns the data file for the given user.
        """
        
        return os.path.join(DefaultConfig.path(), f'{user.name}.json')
    
    @staticmethod
    def get_data(user: discord.Member | discord.User) -> dict:
        """
        Returns the data of the given user.
        """
        
        file = Player.get_data_file(user)
        if not (os.path.isfile(file) and os.access(file, os.R_OK)):
            try:
                template = os.path.join(DefaultConfig.path(), DefaultConfig.template())
                shutil.copy(template, file)
            except:
                pass
        
        with open(file, 'r') as file:
            data = json.load(file)
            data['userid'] = user.name
            return data
        
    def update_fastest_guess(self, mode: str, time: float) -> None:
        stats = self.data['stats'][mode]
        fastest_guess = stats['fastest_guess']
        stats['fastest_guess'] = time if fastest_guess == -1 else min(fastest_guess, time)
        
    def update_data_file(self) -> None:
        with open(Player.get_data_file(self.user), 'w') as file:
            json.dump(self.data, file, indent=4)
        
PLAYERS: dict[str, Player] = dict()
'The list of all players who has interacted with the bot or was detected by the bot.'

async def update_players(
    *,
    interaction: discord.Interaction | None = None,
    user: discord.Member | discord.User | None = None,
    guild: discord.Guild | None = None
) -> None:
    """
    Updates the player. Adds the player to the PLAYERS list if they aren't in it.
    """
    if interaction:
        user = interaction.user
        guild = interaction.guild
    
    player = PLAYERS.get(user.name)
    
    if player is None:
        player = Player(user=user, guild=guild)
        # player.room.thread = await room.search_room(user=user, guild=guild)
        PLAYERS[user.name] = player
    elif player.guild != guild:
        player.guild = guild
        # player.room.thread = await room.search_room(user=user, guild=guild)
        if player.in_game:
            player.in_game.terminate()

def update_players_data() -> None:
    for player in PLAYERS.values():
        player.update_data_file()