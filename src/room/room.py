import discord

from .roomconfig import *

class Room:
    def __init__(
        self,
        *,
        user: discord.Member | discord.User,
        thread: discord.Thread | None = None
    ) -> None:
        self.user = user
        'The owner of this room.'
        self.thread = thread
        'The thread for this room.'
        self.banned_users: list[discord.User | discord.Member] = []
        'A list of banned users from this room.'
        
    async def invite(self, user: discord.Member | discord.User) -> bool:
        """
        Invites a user to the room.
        
        Returns:
            True if the user was successfully invited.
        """
        try:
            if user not in self.banned_users:
                await self.thread.add_user(user)
                return True
        except:
            pass
        return False
    
    async def kick(self, user: discord.Member | discord.User) -> bool:
        """
        Kicks a user from the room.
        
        Returns:
            True if the user was successfully kicked.
        """
        try:
            await self.thread.remove_user(user)
            return True
        except:
            return False
        
    async def ban(self, user: discord.Member | discord.User) -> bool:
        """
        Bans a user from the room.
        
        Returns:
            True if the user was successfully banned.
        """
        try:
            index = self.banned_users.index(user)
            self.banned_users.pop(index)
            return True
        except:
            return False
        
async def create_room(
    *,
    user: discord.Member | discord.User,
    guild: discord.Guild,
    channel: discord.Thread | discord.TextChannel,
    duplicate: bool = False,
    private: bool | None = None,
    invitable: bool | None = None,
    auto_archive_duration: int | None = None,
    slowmode_delay: int | None = None
) -> tuple[discord.Thread, bool]:
    """
    Attempts to create a room for the user of the interaction.
    
    Returns:
        The first element is the room that belongs to the user.
        The second element is whether the room was created or not.
    """
    
    if invitable is None:
        invitable = DefaultConfig.invitable()
    if auto_archive_duration is None:
        auto_archive_duration = DefaultConfig.auto_archive_duration()
    if slowmode_delay is None:
        slowmode_delay = DefaultConfig.slowmode_delay()
        
    if not duplicate:
        room = await search_room(user=user, guild=guild)
        if room is not None:
            return (room, False)
        
    channel = channel.parent if isinstance(channel, discord.Thread) else channel
    thread = await channel.create_thread(
        name = get_room_name(user),
        type = get_room_type(private),
        invitable = invitable,
        auto_archive_duration = auto_archive_duration,
        slowmode_delay = slowmode_delay
    )
    return (thread, True)

async def search_room(
    *,
    user: discord.Member | discord.User,
    guild: discord.Guild
) -> discord.Thread | None:
    """
    Searches for the user's room in the guild.
    """
    
    room_name = get_room_name(user)
    for thread in guild.threads:
        if thread.name == room_name:
            return thread
        
    for channel in guild.channels:
        if not isinstance(channel, discord.TextChannel):
            continue
        async for thread in channel.archived_threads(private=True):
            if thread.name == room_name:
                return thread
        async for thread in channel.archived_threads(private=False):
            if thread.name == room_name:
                return thread
            
def get_room_type(private: bool | None = None) -> discord.ChannelType:
    """
    Gets the room type based on the value of 'private.' If 'private' is None, then
    return the default configuration for a room's type.
    """
    
    if private is None:
        return discord.ChannelType.private_thread if DefaultConfig.private() else discord.ChannelType.public_thread
    if private:
        return discord.ChannelType.private_thread
    return discord.ChannelType.public_thread


def get_room_name(user: discord.Member | discord.User) -> str:
    """
    Gets the name of the user's room.
    """
    return f"{user.name.capitalize()}'s Room"