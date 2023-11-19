import asyncio
import discord
import game
import graphics

from player import *

class Lobby(discord.ui.View):
    def __init__(
        self,
        *,
        player: Player,
        max_players: int | None = None,
        timeout: int | None = None
    ) -> None:
        super().__init__(timeout=timeout)
        self.players: dict[Player, dict[str, bool]] = {}
        'All the players who have joined the lobby.'
        self.owner = player
        'The owner of this lobby.'
        self.mode = 'Standard'
        'The mode of this lobby.'
        self.max_players = max_players
        'The maximum number of players this lobby can have.'
        self.players_ready: int = 0
        'The number of players who have readied.'
        
        self.add_player(player, True)
    
    @staticmethod
    def build_menu(user: discord.Member | discord.User) -> discord.Embed:
        menu = discord.Embed(
            title = f"{user.display_name.capitalize()}'s Lobby",
            color = discord.Color.greyple()
        )
        menu.set_thumbnail(url=user.avatar.url)
        menu.add_field(
            name = f'**Leader:** {user.name}',
            value = '',
            inline = True
        )
        menu.add_field(
            name = f'**Mode:** Standard',
            value = '',
            inline = True
        )
        menu.add_field(
            name = '**Players**',
            value = '',
            inline = False
        )
        menu.add_field(
            name = '',
            value = f'{user.display_name} ({user.name})',
            inline = False
        )
        return menu
        
    @staticmethod
    async def create_and_display(
        interaction: discord.Interaction,
        *,
        player: player.Player,
        max_players: int | None = None
    ) -> None:
        """
        Creates and displays the lobby
        """
        if interaction.response.is_done():
            await interaction.followup.send(
                embed = Lobby.build_menu(interaction.user),
                ephemeral = False,
                view = Lobby(player=player, max_players=max_players)
            )
        else:
            await interaction.response.send_message(
                embed = Lobby.build_menu(interaction.user),
                ephemeral = False,
                view = Lobby(player=player, max_players=max_players)
            )
    
    def add_player(self, player: Player, owner: bool = False) -> dict[str, bool] | None:
        if player not in self.players:
            self.players[player] = {
                'owner': owner,
                'ready': False,
                'finished': False
            }
            player.in_game = self
            return self.players[player]
            
    def remove_player(self, player: Player) -> dict[str, bool] | None:
        try:
            data = self.players.pop(player)
            player.in_game = None
            if len(self.players) == 0:
                return
            if data['owner']:
                key, value = list(self.players.items())[0]
                value['owner'] = True
                self.owner = key
                return data
        except:
            pass
        
    @discord.ui.button(label='Join', style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        guild = interaction.guild
        await update_players(user=user, guild=guild)
        
        if self.add_player(PLAYERS[user.name]):
            menu = interaction.message.embeds[0]
            menu.add_field(
                name = '',
                value = f'{user.display_name} ({user.name})',
                inline = False
            )
            await interaction.response.edit_message(embed=menu)
        
    @discord.ui.button(label='Leave', style=discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, _) -> None:
        user = interaction.user
        guild = interaction.guild
        await update_players(user=user, guild=guild)
        player = PLAYERS[user.name]
        
        index = list(self.players.keys()).index(player)
        data = self.remove_player(player)
        
        menu = interaction.message.embeds[0]
        menu.remove_field(index + 3)
        if not data:
            await interaction.response.edit_message(embed=menu, view=None)
        elif data['owner']:
            menu.set_thumbnail(url=self.owner.user.avatar.url)
            await interaction.response.edit_message(embed=menu)
        
    @discord.ui.button(label='Ready', style=discord.ButtonStyle.blurple)
    async def ready(self, interaction: discord.Interaction, _) -> None:
        if len(self.players) == 1:
            await graphics.display_msg_embed(
                obj = interaction,
                title = 'At least two players are required to start',
                description = 'Invite some of your friends',
                color = discord.Color.red()
            )
            return
        
        user = interaction.user
        guild = interaction.guild
        await update_players(user=user, guild=guild)
        player = PLAYERS[user.name]
        
        index = list(self.players.keys()).index(user.name)
        menu = interaction.message.embeds[0]
        menu.set_field_at(
            index = index + 3,
            name = '',
            value = f'**READY**ㅤ{user.display_name} ({user.name})',
            inline = False
        )
        self.players_ready += 1
        if self.players_ready == len(self.players):
            await interaction.message.delete()
            
        await interaction.response.edit_message(embed=menu)
        while self.players_ready != len(self.players):
            await asyncio.sleep(1)
        
        player.in_game = None
        await (await game.create_game(interaction=interaction, mode=self.mode, player=player)).run(interaction)