from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

class Channel:
    """
    Class representing TG channelID and availability
    """
    def __init__(self, id):
        self.id = id
        self.available = True

    def is_available(self):
        return self.available

    async def create_invite_link(self, bot: Bot):
        """
        Attempts to create an invite link to channel using provided bot instance.
        
        :return: invite link if successful, None if channel is not available
        """
        try:
            link = await bot.create_chat_invite_link(self.id)
            return link.invite_link
        except TelegramBadRequest:
            self.available = False
            return None