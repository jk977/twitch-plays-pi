import chat.commands.admin as admin
import chat.commands.info as info

class CommandList:
    _map = {
        'help': info.show_help,
        'map': info.game_map,
        'song': info.song,
        'restart': admin.restart
    }

    def get(name):
        return CommandList._map.get(name, None)

    def validate(name):
        if name.startswith('!'):
            name = name[1:]

        return name in CommandList._map