import discord
from discord.ext import commands

class MessageSender:
    def __init__(self, bot: commands.Bot, gamechannel_id: int):
        """
        Initialize the MessageSender with a bot instance and game channel ID.

        :param bot: An instance of discord.ext.commands.Bot
        :param gamechannel_id: The ID of the game channel
        """
        self.bot = bot
        self.gamechannel_id = gamechannel_id

    async def send_to_channel(self, channel_id: int, message: str):
        """
        Send a specified message to a specified channel.

        :param channel_id: The ID of the channel to send the message to
        :param message: The message to send
        """
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            raise ValueError(f"Channel with ID {channel_id} not found.")

    async def send_to_gamechannel(self, message: str):
        """
        Send a specified message to the game channel.

        :param message: The message to send
        """
        await self.send_to_channel(self.gamechannel_id, message)

    async def send_to_person(self, user_id: int, message: str):
        """
        Send a message to a specified person.

        :param user_id: The ID of the user to send the message to
        :param message: The message to send
        """
        user = await self.bot.fetch_user(user_id)
        if user:
            await user.send(message)
        else:
            raise ValueError(f"User with ID {user_id} not found.")