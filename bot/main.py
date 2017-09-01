# main.py
# TODO separate commands (and chat functions?) into their own module
#   e.g.,
#     class Command: __init__(self, socket)
#	or
#     class Chat: __init__(self, socket)
#     class Command: __init__(self, chat) 

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

    # polls restart file every second and posts stream status if exists
    thread = StoppableThread(period=1, after=utils.finalize_thread, loop=True, target=notify_restarts, args=(sock,))
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
                roles = [Roles.OWNER] if username == config.CHAN else []
                config.users[username] = User(name=username, roles=roles)

            user = config.users[username]

            if msg.startswith('!') and Roles.BANNED not in user.roles:
                cmd = parts[0][1:]

                if cmd == 'help':
                    with open('info/help.cfg', 'r') as file:
                        help_msg = file.read().strip();
                    send_msg(sock, help_msg)

                elif cmd == 'game':
                    cheat = parts[1].lower()
                    read_cheat_input(cheat, user)

                # lets button inputs be prefixed with !
                elif cmd in config.button_opts:
                    read_button_input(cmd, user)

                # owner-only commands
                elif Roles.OWNER in user.roles:
                    # restarts bot
                    if cmd == 'restart':
                        utils.stop_all_threads()
                        sys.exit(0)

                    elif cmd == 'ban' and len(parts) > 1:
                        target = config.users.get(parts[1], None)
                        if target and Roles.OWNER not in target.roles:
                            target.add_role(Roles.BANNED)

                    elif cmd == 'unban':
                        target = config.users.get(parts[1], None)
                        if target:
                            target.remove_role(Roles.BANNED)

            else:
                read_button_input(msg, user)
