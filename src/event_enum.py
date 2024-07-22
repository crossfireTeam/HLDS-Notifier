from enum import Enum

class Events(Enum):
    """
    Enum for representing various game events.
    """
    disabled = -2
    parse_error = -1
    unknown = 0
    map = 1
    cvar = 2
    cvars_start = 3
    cvars_end = 4
    loading_map = 5
    started_map = 6
    connected = 7
    steam_validated = 8
    entered_game = 9
    suicide = 10
    kill = 11
    say = 12
    say_team = 13
    kick = 14
    disconnected = 15
    shutdown = 16

    def get_message_to_send(event, data: list):
        """
        Returns a message to be sent to channel/chat based on event and data.

        :param event: event to process (instance of Events)
        :param data: dict with parsed data to be included in message
        :return: formatted message corresponding to provided
        """
        event_messages = {
            Events.parse_error: lambda: f"🐹☕️ Log parse error! Event {data['event']}, exception {data['exception']}, input {data['log_line']}",
            Events.unknown: lambda: f"❓ Unknown event {data['log_line']}",
            Events.loading_map: lambda: f"🏆 Prepare to win on {data['map_name']}!",
            Events.started_map: lambda: f"🚀 Map update: {data['map_name']} is now live on the server!",
            Events.cvars_start: lambda: f"⏳ Server starting...",
            Events.cvars_end: lambda: "✅ Server started! Let's play!",
            Events.entered_game: lambda: f"✳️ {data['name']} joined to server!",
            Events.suicide: lambda: f"💀 {data['name']} committed suicide with {data['reason']}!",
            Events.kill: lambda: f"🤕 🔫 🫡\n\n{data['killer']} killed {data['victim']} with {data['weapon']}!",
            Events.say: lambda: f"🗣️ {data['name']} said: {data['message']}",
            Events.disconnected: lambda: f"🤧 {data['name']} disconnected!",
            Events.shutdown: lambda: f"🔒 Server is shutting down.",
        }

        return event_messages.get(event)()