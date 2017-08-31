# main.py
# bot code

import random
import re
import socket
import threading
import time

import config
import utils

from time import sleep, time
from utils import send_msg
from user import User


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
        t = threading.Thread(target=send_input, args=('cheats.txt', cheat))
        t.start()
        config.vm.reset()

    
def read_button_input(message, user):
    vote = utils.format_button_input(message)

    if not vote:
        return

    vote_count = user.vote(config.vm, vote)

    # if vote brought vote count over threshold
    if vote_count >= config.vm.threshold:
        t = threading.Thread(target=send_input, args=('inputs.txt', vote))
        t.start()
        config.vm.reset()
   

if __name__ == '__main__':
    CHAT_MSG = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')

    # sets up connection to IRC
    sock = socket.socket()
    sock.connect((config.HOST, config.PORT))
    sock.send('PASS {}\r\n'.format(config.PASS).encode('utf-8'))
    sock.send('NICK {}\r\n'.format(config.NICK).encode('utf-8'))
    sock.send('JOIN #{}\r\n'.format(config.CHAN).encode('utf-8'))

    while True:
        response = sock.recv(1024).decode('utf-8')

        if response.startswith('PING :tmi.twitch.tv'):
            sock.send(bytes(response.replace('PING', 'PONG'), 'utf-8'))

        else:
            username = re.search(r'(\w+)', response).group(0).strip()
            msg = CHAT_MSG.sub('', response).strip()
            parts = re.split('\\s+', msg) # array of words in message
            print(response)

            # adds user to list if not present
            if username not in config.users:
                config.users[username] = User(name=username)

            user = config.users[username]

            if msg.startswith('!help'):
                # TODO see if optimizing is necessary to prevent repeated opens
                with open('info/help.cfg', 'r') as file:
                    help_msg = file.read().strip();
                send_msg(sock, help_msg)

            elif msg.startswith('!game '):
                cheat = parts[1].lower()
                read_cheat_input(cheat, user)

            else:
                read_button_input(msg, user)
