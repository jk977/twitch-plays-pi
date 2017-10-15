# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/chat/commands/commandlist.py
# Compiled at: 2017-10-14 02:08:13
# Size of source mod 2**32: 701 bytes
import chat.commands.admin as admin
import chat.commands.info as info
from chat.commands.command import Command

class CommandList:
    _map = {'help': info.show_help,
     'map': info.game_map,
     'song': info.song,
     'restart': admin.restart}

    def get(name, chat, message):
        if name.startswith('!'):
            name = name[1:]
        command = CommandList._map.get(name, None)
        kwargs = {'chat': chat,'message': message}
        if not command:
            return
        return Command(command, kwargs)

    def validate(name):
        if name.startswith('!'):
            name = name[1:]
        return name in CommandList._map