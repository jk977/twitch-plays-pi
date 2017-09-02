# main.py
# TODO
#   - separate commands (and chat functions?) into their own module
#       e.g.,
#         class Command: __init__(self, socket)
#           or
#         class Chat: __init__(self, socket)
#         class Command: __init__(self, chat) 
#   - add decorators for thread-safe resource accessors/mutators
#     instead of repeated with blocks?

import os
import random
import re
import socket
import sys
import threading
import time

import config
import utils

from roles import Roles
from stoppablethread import StoppableThread
from time import sleep, time
from user import User
from utils import send_msg


def send_input(filename, contents):
    for i in range(10):
        try:
            with open('../' + filename, 'w+') as file:
                file.write(contents)
                print('>>>Sent ' + contents + ' to emulator.')
                break
        except:
            sleep(1)


def read_cheat_input(cheat, user):
    if cheat not in config.cheat_opts:
        return

    vote_count = user.vote(config.vm, cheat)

    # if vote brought vote count over threshold
    if vote_count >= config.vm.threshold:
        t = StoppableThread(after=utils.finalize_thread, target=send_input, args=('cheats.txt', cheat))
        config.threads.append(t)
        t.start()

        config.vm.reset()

    
def read_button_input(message, user):
    vote = utils.format_button_input(message)

    if not vote:
        return

    vote_count = user.vote(config.vm, vote)

    # if vote brought vote count over threshold
    if vote_count >= config.vm.threshold:
        t = StoppableThread(after=utils.finalize_thread, target=send_input, args=('inputs.txt', vote))
        config.threads.append(t)
        t.start()

        config.vm.reset()


def notify_restarts(sock):
    """Notifies chat when stream is restarting by checking for flag file."""
    try:
        os.remove('../restartfile')
        send_msg(sock, 'Stream is restarting!')
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    CHAT_MSG = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')

    # sets up connection to IRC
    sock = socket.socket()
    sock.connect((config.HOST, config.PORT))
    sock.send('PASS {}\r\n'.format(config.PASS).encode('utf-8'))
    sock.send('NICK {}\r\n'.format(config.NICK).encode('utf-8'))
    sock.send('JOIN #{}\r\n'.format(config.CHAN).encode('utf-8'))

    send_msg(sock, 'Bot online!')

    # polls restart file every second and posts stream status if exists
    thread = StoppableThread(period=1, after=utils.finalize_thread, target=notify_restarts, args=(sock,))
    thread.start()
    config.threads.append(thread)

    # main loop
    while True:
        response = sock.recv(1024).decode('utf-8')

        if response.startswith('PING :tmi.twitch.tv'):
            sock.send(bytes(response.replace('PING', 'PONG'), 'utf-8'))
            continue

        else:
            username = re.search(r'(\w+)', response).group(0).strip()
            msg = CHAT_MSG.sub('', response).strip()
            parts = re.split('\\s+', msg) # array of words in message
            print(response)

           # adds user to list if not present
            if username not in config.users:
                is_owner = username == config.CHAN
                config.users[username] = User(name=username, owner=is_owner)

            user = config.users[username]

            if msg.startswith('!'):
                cmd = parts[0][1:]

                if cmd == 'help':
                    with open('info/help.cfg', 'r') as file:
                        help_msg = file.read().strip();
                    send_msg(sock, help_msg)

                elif cmd == 'game' and not user.is_banned:
                    cheat = parts[1].lower()
                    read_cheat_input(cheat, user)

                elif cmd == 'banlist':
                    banlist = [u.name for u in config.users.values() if u.is_banned]

                    if len(banlist) == 0:
                        message = 'No one is currently banned.'
                    else:
                        message = 'Banned users: ' + ', '.join(banlist)

                    send_msg(sock, message)

                # owner-only commands
                elif user.is_owner:
                    if cmd == 'restart':
                        send_msg(sock, 'Restarting chat bot... Inputs won\'t work until restart is finished.')
                        sock.shutdown(socket.SHUT_RDWR)
                        sock.close()
                        utils.stop_all_threads()
                        sys.exit(0)

                    elif cmd == 'ban' and len(parts) > 1:
                        target_name = parts[1].lower().replace('@', '').strip()

                        if not target_name in config.users:
                            target = User(name=target_name)
                            config.users[target_name] = target
                        else:
                            target = config.users[target_name]
                            
                        try:
                            target.ban()
                            send_msg(sock, 'Banned {} from playing.'.format(target.name))
                        except PermissionError as e:
                            send_msg(sock, str(e))

                    elif cmd == 'unban':
                        target_name = parts[1].lower().replace('@', '').strip()
                        target = config.users.get(target_name, None)

                        if not target:
                            send_msg(sock, 'Couldn\'t find user.')
                        elif target.is_banned:
                            target.unban()
                            send_msg(sock, 'Unbanned {}.'.format(target_name))

            elif not user.is_banned:
                read_button_input(msg, user)
