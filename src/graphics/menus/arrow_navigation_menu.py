import discord

class ArrowNavigationMenu(discord.ui.View):
    def __init__(
        self,
        *,
        menus: list[discord.Embed],
        timeout: float | None = None
    ) -> None:
        super().__init__(timeout=timeout)
        self.menus = menus
        'All the menus that can be navigated.'
        self.value: int = 0
        'The current menu it is displaying.'
        
    @discord.ui.button(label='<', style=discord.ButtonStyle.gray)
    async def navigate_left(self, interaction: discord.Interaction, _) -> None:
        """
        Navigates to the menu that's left of the current one.
        """
        
        self.value = (self.value - 1) % len(self.menus)
        await interaction.response.edit_message(embed=self.menus[self.value])
        
    @discord.ui.button(label='>', style=discord.ButtonStyle.gray)
    async def navigate_right(self, interaction: discord.Interaction, _) -> None:
        """
        Navigates to the menu that's right of the current one.
        """
        
        self.value = (self.value + 1) % len(self.menus)
        await interaction.response.edit_message(embed=self.menus[self.value])
        
    @staticmethod
    async def create_and_display(
        *,
        interaction: discord.Interaction,
        menus: list[discord.Embed],
        timeout: float | None = None,
        ephemeral: bool = True
    ) -> None:
        """
        Creates and displays the menus as an arrow navigation menu.
        """
        
        if interaction.response.is_done():
            await interaction.followup.send(
                embed = menus[0],
                ephemeral = ephemeral,
                view = ArrowNavigationMenu(menus=menus, timeout=timeout)
            )
        else:
            await interaction.response.send_message(
                embed = menus[0],
                ephemeral = ephemeral,
                view = ArrowNavigationMenu(menus=menus, timeout=timeout)
            )