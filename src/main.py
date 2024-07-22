import sys
from configurations import Configurations
from constants import Constants
from udp_handler import UDPHandler

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import logging

class NotifierBot:
    """
    Main class of a bot for notifying events from a HLDS server.
    """
    def __init__(self):
        """
        Initializes the NotifierBot with a logger, a bot instance, and a dispatcher. Also registers command handlers.
        """
        self.logger = logging.getLogger(NotifierBot.__name__)
        self.bot = Bot(token=Configurations.token)
        self.dp = Dispatcher()
        self.register_handlers()

    def register_handlers(self):
        """
        Registers command handlers for the bot, including commands to start, get info, and list channels.
        """
        @self.dp.message(Command("start"))
        async def start(message: types.Message):
            await message.answer("👋 This is a HLDS bot that fetches events from server and posts them to several channels.")
        @self.dp.message(Command("info"))
        async def info(message: types.Message):
            await message.answer(f"ℹ️ HLDS Notifier Bot: version {Constants.version}, repo origin url {Constants.github_url}. Fetching events from {Configurations.game}, waiting for you to join on {Configurations.hlds_machine_ip}:{Configurations.hlds_game_port}")
        @self.dp.message(Command("channels"))
        async def channels(message: types.Message):
            reply = f"☕️ Available channels:\n\n"
            
            public_chat = await Configurations.public_channel.create_invite_link(self.bot)
            private_chat = await Configurations.private_channel.create_invite_link(self.bot) if message.from_user.id in Configurations.admin_ids else None
            chat_channel = await Configurations.chat_channel.create_invite_link(self.bot)

            if public_chat: reply += f"🔓 Public channel: {public_chat}\n"
            if private_chat: reply += f"🔒 Private channel: {private_chat}\n"
            if chat_channel: reply += f"💬 Chat channel: {chat_channel}"
            await message.answer(reply)

    async def sanity_check(self):
        """
        Performs a sanity check to ensure all configured channels are available.
        """
        self.logger.info("Starting sanity check")

        await self.channels_check()
        self.logger.info("Sanity check OK")
    
    async def channels_check(self):
        """
        Checks the availability of all channels and logs warnings if any are unavailable. Exits the application if no channels are available.
        Exits the program if no channels are available.
        """
        error_count = 0
        public_chat = await Configurations.public_channel.create_invite_link(self.bot)
        private_chat = await Configurations.private_channel.create_invite_link(self.bot)
        chat_channel = await Configurations.chat_channel.create_invite_link(self.bot)

        if not public_chat: 
            self.logger.warning("Public chat unavailable")
            error_count += 1
        if not private_chat: 
            self.logger.warning("Private chat unavailable")
            error_count += 1
        if not chat_channel: 
            self.logger.warning("Chat channel unavailable")
            error_count += 1

        if error_count == Constants.channels_amount:
            self.logger.error("No available channels, re-check id's.")
            sys.exit(-1)
        else: self.logger.info(f"channels_check OK")
    
    async def start_udp_server(self):
        """
        Starts the UDP server to listen for incoming UDP datagrams and handle them with UDPHandler.
        """
        self.logger.info("Start UDP server")
        loop = asyncio.get_event_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UDPHandler(self.bot),
            local_addr=(Configurations.hlds_machine_ip, Configurations.udp_port)
        )
        self.logger.info(f"Run UDP server for {Configurations.hlds_machine_ip}:{Configurations.udp_port}")

    async def main(self):
        """
        Main entry point for the bot. Performs a sanity check, starts the UDP server, and begins polling for Telegram messages.
        """
        await self.sanity_check()
        await self.start_udp_server()
        await self.dp.start_polling(self.bot)

if __name__ == "__main__":
    logging.basicConfig(level=Configurations.log_level)

    instance = NotifierBot()
    asyncio.run(instance.main())