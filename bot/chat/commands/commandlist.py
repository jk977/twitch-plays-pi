import chat.commands.admin as admin
import chat.commands.info as info

from chat.commands.command import Command


class CommandList:
    _map = {
        'help': info.show_help,
        'map': info.game_map,
        'song': info.song,
        'restart': admin.restart
    }

    def get(name, chat, message, default=None):
        if name.startswith('!'):
            name = name[1:]

        command = CommandList._map.get(name, None)
        kwargs = {'chat': chat,'message': message}
        return Command(command, kwargs) if command else default
    
    def validate(name):
        if name.startswith('!'):
            name = name[1:]

        return name in CommandList._map