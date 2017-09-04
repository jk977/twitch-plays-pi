# main.py

import config
import os
import re
import utils

from settings import Settings
from stoppablethread import StoppableThread
from time import sleep
from utils import send_msg

from chat.user import User
from chat.commandparser import CommandParser


def notify_restarts(sock):
    """Notifies chat when stream is restarting by checking for flag file."""
    try:
        os.remove('../restartfile')
        send_msg(sock, 'Stream is restarting!')
    except FileNotFoundError:
        pass


if __name__ == '__main__':
    CHAT_MSG = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')

    # loads settings from json
    Settings.load_settings()

    # gets socket connected to irc
    sock = utils.irc_connect()
    send_msg(sock, 'Bot online!')

    # polls restart file every second and posts stream status if restarting
    stream_thread = StoppableThread(period=1, after=utils.finalize_thread, target=notify_restarts, args=(sock,), daemon=True)
    stream_thread.start()
    config.threads.append(stream_thread)

    # periodically saves current users to settings file
    settings_thread = StoppableThread(period=10, after=utils.finalize_thread, target=Settings.save_settings)
    settings_thread.start()
    config.threads.append(settings_thread)

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

            # ignores tmi messages
            if username == 'tmi':
                continue

           # adds user to list if not present
            if username not in config.users:
                is_owner = username == config.CHAN
                config.users[username] = User(name=username, owner=is_owner)

            user = config.users[username]
            cmd = CommandParser.parse(msg, user, sock)

            try:
                cmd.run()
            except PermissionError as e:
                send_msg(sock, str(e))
            except AttributeError:
                pass

            if not user.is_banned:
                utils.read_button_input(msg, user)
