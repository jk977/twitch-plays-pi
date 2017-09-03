import config
import re
import socket
import sys
import utils

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
    target_name = args[0].lower().replace('@', '').strip()
    if not target_name in config.users:
        target = User(name=target_name)
        config.users[target_name] = target
    else:
        target = config.users[target_name]
        
    if user.is_owner or not (target.is_owner or target.is_moderator):
        target.ban()
        send_msg(sock, 'Banned {} from playing.'.format(target_name))


@permissions(Roles.MOD, silent=True)
def unban(sock, user, args):
    target_name = args[0].lower().replace('@', '').strip()
    target = config.users.get(target_name, None)

    if not target:
        send_msg(sock, 'Couldn\'t find user.')
    elif target.is_banned:
        target.unban()
        send_msg(sock, 'Unbanned {}.'.format(target_name))


@permissions(Roles.OWNER, silent=True)
def restart(sock, user, args):
    send_msg(sock, 'Restarting chat bot... Inputs won\'t work until restart is finished.')
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    utils.stop_all_threads()
    sys.exit(0)
