import re
import chat.commands as commands

from chat.commands import Command


class CommandParser:
    prefix = '!'

    def parse(message, user, sock):
        """Parses message and returns a command to execute."""
        if not message.startswith(CommandParser.prefix):
            return

        cmds = {
                'help': commands.get_help,
                'map': commands.get_map,
                'game': commands.game_command,
                'mods': commands.get_mods,
                'banlist': commands.get_banlist,
                'ban': commands.ban,
                'unban': commands.unban,
                'roles': commands.get_roles,
                'mod': commands.mod,
                'unmod': commands.unmod,
                'restart': commands.restart
        }

        parts = re.split('\\s+', message)
        action = cmds.get(parts[0][1:], None)
        args = tuple(parts[1:])

        kwargs = {'user': user, 'args': args, 'sock': sock}

        if action:
            cmd = Command(action=action, **kwargs)
        else:
            cmd = None

        return cmd
