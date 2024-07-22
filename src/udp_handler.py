import logging
import asyncio
import traceback

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from channel import Channel
from configurations import Configurations
from event_parser import EventParser
from event_enum import Events

class UDPHandler(asyncio.DatagramProtocol):
    """
    Handles incoming UDP datagrams, processes them to extract events, and sends messages to appropriate channels.
    """
    def __init__(self, bot: Bot):
        """
        Initializes the UDPHandler with a bot instance for sending messages and sets up logging.
        """
        self.bot = bot
        self.logger = logging.getLogger(UDPHandler.__name__)

    def datagram_received(self, data, addr):
        """
        Processes received UDP datagrams, extracts event data, and determines the appropriate channel for sending messages.
        """
        message = data.decode(errors='ignore')
        self.logger.debug(message)
        event_enum, data = EventParser.get_json_data(message)
        if event_enum is Events.disabled: return

        self.logger.info(f"Received {event_enum} log")
        try:
            channel = Configurations.public_channel
            message_to_send = Events.get_message_to_send(event_enum, data)  

            if event_enum in Configurations.private_events_treshold:
                channel = Configurations.private_channel
                asyncio.create_task(self.send_message_to_chat(channel, message_to_send))
            else:
                if event_enum is Events.say:
                    channel = Configurations.chat_channel

                asyncio.create_task(self.send_message_to_chat(channel, message_to_send))
        except:
            channel = Configurations.private_channel
            asyncio.create_task(self.send_message_to_chat(channel, f"😅🧠 Got inner exception\n{traceback.format_exc()}"))


    async def send_message_to_chat(self, channel: Channel, message: str):
        """
        Sends a message to specified channel. If channel is unavailable, it is marked as such (should be already marked?).

        :param channel: channel instance where the message should be sent.
        :param message: message to be sent.
        """
        if not channel.is_available(): return
        try:
            await self.bot.send_message(chat_id=channel.id, text=message)
        except Exception as e:
            if isinstance(e, TelegramBadRequest):
                channel.set_availability(False)
                self.logger.warn(f"channel {channel.id} is now marked as not available!")
            self.logger.error(f"Failed to send message: {e}")