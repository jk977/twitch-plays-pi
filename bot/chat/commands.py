# TODO merge command functions into command class?
#   - Likely slower to do that, since command instances would contain data for all commands
#     Separate into Command and CommandList class, with CommandList containing parse()?
#       - Name would be misleading

import config
import re
import socket
import sys
import utils

from settings import Settings
from utils import send_msg

from chat.permissions import permissions
from chat.roles import Roles
from chat.user import User


class Command:
    def __init__(self, action=None, **kwargs):
        if not callable(action):
            raise TypeError('"action" must be callable.')

        self._action = action
        self._kwargs = kwargs

    def run(self):
        self._action(**self._kwargs)


def get_roles(sock, user, args):
    roles = []

    if user.is_moderator:
        roles.append('moderator')
    if user.is_owner:
        roles.append('owner')
    if user.is_banned:
        roles.append('banned')

    msg = 'Your roles are: '

    if roles:
        msg += ', '.join(roles)
    else:
        msg += 'default'

    send_msg(sock, msg)


@permissions(Roles.DEFAULT)
def get_map(sock, user, args):
    send_msg(sock, 'http://ff1maps.com/img/worldmap-small.png')


@permissions(Roles.DEFAULT)
def get_mods(sock, user, args):
    mod_list = [u.name for u in config.users.values() if u.is_moderator]

    if len(mod_list) == 0:
        message = 'No moderators currently.'
    else:
        message = 'Moderators: ' + ', '.join(mod_list)

    send_msg(sock, message)


@permissions(Roles.DEFAULT)
def get_banlist(sock, user, args):
    banlist = [u.name for u in config.users.values() if u.is_banned]

    if len(banlist) == 0:
        message = 'No one is currently banned.'
    else:
        message = 'Banned users: ' + ', '.join(banlist)

    send_msg(sock, message)


@permissions(Roles.DEFAULT)
def get_help(sock=None, user=None, args=None):
    with open('info/help.cfg', 'r') as file:
        help_msg = file.read().strip();
    send_msg(sock, help_msg)


@permissions(Roles.DEFAULT)
def game_command(sock, user, args):
    """Sends game command to emulator."""
    cheat = args[0].lower()
    utils.read_cheat_input(cheat, user)


@permissions(Roles.MOD, silent=True)
def ban(sock, user, args):
    def true_ban(name):
        """Contains ban logic."""
        name = name.lower().replace('@', '').strip()

        if not name in config.users:
            target = User(name=name)
            config.users[name] = target
        else:
            target = config.users[name]
            
        if user.role > target.role:
            target.ban()
            return True
        else:
            return False


    args = [utils.extract_username(user) for user in args]
    banned_users = []

    if user.is_owner:
        for name in args:
            if true_ban(name):
                banned_users.append(name)
    else:
        if true_ban(args[0]):
            banned_users = [args[0]]

    if banned_users:
        send_msg(sock, 'Banned {}.'.format(', '.join(banned_users)))
    

@permissions(Roles.MOD, silent=True)
def unban(sock, user, args):
    args = [utils.extract_username(user) for user in args]
    unbanned_list = []

    for name in args:
        target = config.users.get(name, None)

        if target and target.is_banned:
            target.unban()
            unbanned_list.append(name)

    if unbanned_list:
        send_msg(sock, 'Unbanned {}.'.format(', '.join(unbanned_list)))


@permissions(Roles.OWNER, silent=True)
def restart(sock, user, args):
    send_msg(sock, 'Restarting chat bot... Inputs won\'t work until restart is finished.')
    Settings.save_settings()
    utils.stop_all_threads()
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    sys.exit(0)


@permissions(Roles.OWNER, silent=True)
def mod(sock, user, args):
    args = [utils.extract_username(user) for user in args]

    for name in args:
        if not name in config.users:
            target = User(name=name)
            config.users[name] = target
        else:
            target = config.users[name]
            
        target.mod()


@permissions(Roles.OWNER, silent=True)
def unmod(sock, user, args):
    args = [utils.extract_username(user) for user in args]

    for name in args:
        target = config.users.get(name, None)

        if target:
            target.unmod()
