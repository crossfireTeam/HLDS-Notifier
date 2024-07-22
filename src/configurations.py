import logging
from channel import Channel
from event_enum import Events
from games_enum import Games

class Configurations:
    """
    Class for storing configuration settings for the application.
    """
    log_level = logging.DEBUG
    token = ""
    admin_ids = []
    public_channel = Channel(0)
    private_channel = Channel(0)
    chat_channel = Channel(0)
    
    private_events_treshold = [Events.parse_error, Events.unknown]
    disabled_events = [Events.connected, Events.cvars_start, Events.cvar, Events.cvars_end]
    hlds_machine_ip = '0.0.0.0'
    hlds_game_port = 27015
    game = Games.hl
    udp_port = 27115