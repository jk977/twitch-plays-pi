from chat.commands.admin import *
from chat.commands.info import *

class CommandList:
    _map = {
        'help': help,
        'song': song,
        'restart': restart
    }

    def get(name):
        return CommandList._map.get(name, None)

    def validate(name):
        if name.startswith('!'):
            name = name[1:]

        return name in CommandList._map