from configurations import Configurations
from event_enum import Events
import re

class EventParser:
    @staticmethod
    def get_json_data(message: str):
        """
        Processes log message and returns event enum and dict with data.

        :param message: log message to process
        :return: tuple containing event enum and a dict with processed data.
        """

        # for parsing event enum, remove all whitespaces and non-alphabetic characters from message
        plain = ''.join(filter(lambda char: char.isalpha() or char.isspace(), message))
        event_enum = EventParser.__get_event_enum(plain)

        # if event marked as disabled, abandon parse
        if event_enum in Configurations.disabled_events:
            return Events.disabled
        
        methods_dict = {
            Events.shutdown: EventParser.__parse_shutdown,
            Events.loading_map: EventParser.__parse_loading_map,
            Events.started_map: EventParser.__parse_map_started,
            Events.cvars_start: EventParser.__get_empty_dict,
            Events.cvars_end: EventParser.__get_empty_dict,
            Events.say: EventParser.__parse_say,
            Events.kill: EventParser.__parse_kill,
            Events.suicide: EventParser.__parse_suicide,
            Events.entered_game: EventParser.__parse_enter,
            Events.connected: EventParser.__get_empty_dict,
            Events.disconnected: EventParser.__parse_disconnect,

            Events.unknown: EventParser.__get_unknown_log_dict,
        }

        if event_enum in methods_dict:
            try:
                return event_enum, methods_dict[event_enum](message)
            except ValueError as e:
                return Events.parse_error, EventParser.__get_invalid_log_dict(event_enum, e, message)
        else:
            return event_enum, {}

    @staticmethod
    def __get_event_enum(plain: str):
        """
        Maps a part of log to event enum.

        :param plain: cleaned message without special characters.
        :return: corresponding event enum.
        """
        enum_map = {
            "Server shutdown": Events.shutdown,
            "Loading map": Events.loading_map,
            "Started map": Events.started_map,
            "Server cvar": Events.cvar,
            "Server cvars start": Events.cvars_start,
            "Server cvars end": Events.cvars_end,
            "entered the game": Events.entered_game,
            " connected,": Events.connected,
            "disconnected": Events.disconnected,
            "killed": Events.kill,
            "committed suicide with": Events.suicide,
            "say": Events.say
        }

        for key in enum_map:
            if key in plain:
                return enum_map[key]
        return Events.unknown
    
    @staticmethod
    def __get_invalid_log_dict(event_enum: Events, exception: Exception, message: str):
        """
        Creates a dict with details of a parsing error.
        """
        return {'event': event_enum, 'exception': exception, 'log_line': message}
    
    @staticmethod
    def __get_unknown_log_dict(message: str):
        """
        Creates a dict with unknown event message.
        """
        return {'log_line': message}
    
    @staticmethod
    def __get_empty_dict(message: str):
        """
        For some events which doesn't require parsing.
        """
        return {}
    
    @staticmethod
    def __parse_shutdown(message: str):
        """
        Returns empty dict, since there's no data to parse.
        """
        return {}

    @staticmethod
    def __parse_map(message: str):
        """
        Currently placeholder
        """
        pass
    
    #TODO: merge 2 methods below
    @staticmethod
    def __parse_loading_map(message: str):
        """
        Parses a map-loading event.

        :param message: log message to parse.
        :return: dict containing the map name.
        """
        pattern = r"log L \d{2}\/\d{2}\/\d{4} - \d{2}:\d{2}:\d{2}: Loading map \"(.+)\""
        
        result = re.findall(pattern, message)
        if result == []:
            raise ValueError("Invalid log string!")
        
        return {'map_name': result[0]}

    @staticmethod
    def __parse_map_started(message: str):
        """
        Parses a map-started event.

        :param message: log message to parse.
        :return: dict containing the map name.
        """
        pattern = r"log L \d{2}\/\d{2}\/\d{4} - \d{2}:\d{2}:\d{2}: Started map \"(.+)\" \(.+\)"
        
        result = re.findall(pattern, message)
        if result == []:
            raise ValueError("Invalid log string!")
        
        return {'map_name': result[0]}
    
    @staticmethod
    def __parse_say(message: str):
        """
        Parses a say event from a player.

        :param message: log message to parse.
        :return: dict containing player's name and their message.
        """
        pattern = r"log L \d{2}\/\d{2}\/\d{4} - \d{2}:\d{2}:\d{2}: \"(.+)<\d+><.+><\d+>\" say (.+)"

        result = re.findall(pattern, message)[0]
        if len(result) != 2:
            raise ValueError(f"Invalid log string! Expected 2 args got {len(result)}")
        
        return {'name': result[0], 'message': result[1]}

    @staticmethod
    def __parse_kill(message: str):
        """
        Parses a kill event.

        :param message: log message to parse.
        :return: dict containing killer and victim's name and weapon name.
        """
        pattern = r"log L \d{2}\/\d{2}\/\d{4} - \d{2}:\d{2}:\d{2}: \"(.+)<\d+><.+><\d+>\" killed \"(.+)<\d+><.+><\d+>\" with \"(.+)\""
        
        result = re.findall(pattern, message)[0]
        if len(result) != 3:
            raise ValueError(f"Invalid log string! Expected 3 args got {len(result)}")

        return {'killer': result[0], 'victim': result[1], 'weapon': result[2]}
    
    @staticmethod
    def __parse_suicide(message: str):
        """
        Parses a suicide event.

        :param message: log message to parse.
        :return: dict containing victim's name and reason.
        """
        pattern = r"log L \d{2}\/\d{2}\/\d{4} - \d{2}:\d{2}:\d{2}: \"(.+)<\d+><.+><\d+>\" committed suicide with \"(.+)\""
        
        result = re.findall(pattern, message)[0]
        if len(result) != 2:
            raise ValueError(f"Invalid log string! Expected 2 args got {len(result)}")

        return {'name': result[0], 'reason': result[1]}

    @staticmethod
    def __parse_enter(message: str):
        """
        Parses a entered game event.

        :param message: log message to parse.
        :return: dict containing player's name.
        """
        pattern = r"log L \d{2}\/\d{2}\/\d{4} - \d{2}:\d{2}:\d{2}: \"(.+)<\d+><.+><\d+>\" entered the game"

        result = re.findall(pattern, message)
        return {'name': result[0]}
    
    @staticmethod
    def __parse_disconnect(message: str):
        """
        Parses a disconnect event.

        :param message: log message to parse.
        :return: dict containing player's name.
        """
        pattern = r"log L \d{2}\/\d{2}\/\d{4} - \d{2}:\d{2}:\d{2}: \"(.+)<\d+><.+><\d+>\" disconnected"

        result = re.findall(pattern, message)
        return {'name': result[0]}


