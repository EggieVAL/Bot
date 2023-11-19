import discord

class DropdownNavigationOptions(discord.ui.Select):
    def __init__(
        self,
        *,
        menus: dict[str, discord.Embed],
        options: dict[str, str]
    ) -> None:
        selections = [discord.SelectOption(label=key, description=value) for key, value in options.items()]
        super().__init__(options=selections)
        self.menus = menus
        'All the menus that can be navigated'
        
    async def callback(self, interaction: discord.Interaction) -> None:
        """
        Navigates to the menu the user selected.
        """
        
        label = self.values[0]
        await interaction.response.edit_message(embed=self.menus[label])

class DropdownNavigationMenu(discord.ui.View):
    def __init__(
        self,
        *,
        menus = dict[str, discord.Embed],
        options = dict[str, str],
        timeout: float | None = None
    ) -> None:
        super().__init__(timeout=timeout)
        self.add_item(DropdownNavigationOptions(menus=menus, options=options))
        
    @staticmethod
    async def create_and_display(
        *,
        interaction: discord.Interaction,
        menus: dict[str, discord.Embed],
        options: dict[str, str],
        timeout: float | None = None,
        ephemeral: bool = True
    ) -> None:
        """
        Creates and displays the menus as a dropdown navigation menu.
        """
        
        menu = list(menus.values())[0]
        
        if interaction.response.is_done():
            await interaction.followup.send(
                embed = menu,
                ephemeral = ephemeral,
                view = DropdownNavigationMenu(menus=menus, options=options, timeout=timeout)
            )
        else:
            await interaction.response.send_message(
                embed = menu,
                ephemeral = ephemeral,
                view = DropdownNavigationMenu(menus=menus, options=options, timeout=timeout)
            )