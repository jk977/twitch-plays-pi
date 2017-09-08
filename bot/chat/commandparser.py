import re
import chat.commands as commands

from chat.commands import Command


class CommandParser:
    prefix = '!'

    def parse(chat, message):
        """Parses message and returns a command to execute."""
        if not message.content.startswith(CommandParser.prefix):
            return

        cmds = {
                'help': commands.get_help,
                'map': commands.get_map,
                'mods': commands.get_mods,
                'banlist': commands.get_banlist,
                'ban': commands.ban,
                'unban': commands.unban,
                'roles': commands.get_roles,
                'mod': commands.mod,
                'unmod': commands.unmod,
                'prune': commands.prune,
                'restart': commands.restart
        }

        parts = re.split(',?\\s+', message.content)
        action = cmds.get(parts[0][1:], None)
        args = tuple(parts[1:])

        kwargs = {'user': message.author, 'args': args, 'chat': chat}
        cmd = Command(action=action, **kwargs) if action else None

        return cmd
