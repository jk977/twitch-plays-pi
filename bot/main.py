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


def send_emulator_input(emu_cmd):
    for i in range(10):
        try:
            with open('../inputs.txt', 'w+') as file:
                print('Writing to file: ' + str(time()))
                file.write(emu_cmd)
                print('Closing file: ' + str(time()))
                print('>>>Sent ' + emu_cmd + ' to emulator.')
                break
        except:
            sleep(1)


def send_cheat(cheat):
    for i in range(10):
        try:
            with open('../cheats.txt', 'w+') as file:
                print('Writing to cheat file: ' + str(time()))
                file.write(cheat)
                print('Closing cheat file: ' + str(time()))
                print('>>>Sent ' + cheat + ' to emulator.')
                break
        except:
            sleep(1)


def read_cheat_input(cheat, user):
    if user not in config.chatters:
        utils.add_chatter(user)

    if config.chatters[user].cheat:
        old_cheat = config.chatters[user].cheat
        config.cheat_inputs[old_cheat] -= 1

    if cheat and cheat in config.cheat_opts:
        if cheat not in config.cheat_inputs:
            config.cheat_inputs[cheat] = 0

        config.chatters[user].cheat = cheat
        config.cheat_inputs[cheat] += 1

    for cht in config.cheat_inputs:
        print(cht, ': ', str(config.cheat_inputs[cht]))

        # sends input to emulator in parallel if count exceeds threshold
        if config.cheat_inputs[cht] >= config.vote_threshold:
            t = threading.Thread(target=send_cheat, args=(cht,))
            t.start()
            utils.clear_cheat_inputs()
            break


def read_button_input(message, user):
    cmd = re.match(r'^([a-zA-Z]+)\s*([1-9])?$', message)
    button, mult = None, None # mult is the number of times to press button

    # initializes button and multiplier value
    try:
        button = cmd.group(1)
        mult = cmd.group(2)
    except:
        pass
    finally:
        # converts 'a' and 'b' inputs to uppercase due to FCEUX input format
        if button and button == 'a' or button == 'b':
            button = button.upper()
        elif button:
            button = button.lower()

        button = button if button and button in config.button_opts else None
        mult = mult if mult else 1 # sets to 1 if mult is None

    print(button, ' ', mult)

    # initializes user if not in list
    if user not in config.chatters:
        utils.add_chatter(user)

    # removes user's old selection
    if config.chatters[user].button:
        old_button = config.chatters[user].button
        config.button_inputs[old_button] -= 1

    # adds new input to list of inputs
    if button and button in config.button_opts:
        formatted_input = str(mult) + button

        # initializes new input
        if formatted_input not in config.button_inputs:
            config.button_inputs[formatted_input] = 0

        # assigns new input to chatter's button and update button counts
        config.chatters[user].button = formatted_input
        config.button_inputs[formatted_input] += 1

    for btn in config.button_inputs:
        print(btn, ': ', str(config.button_inputs[btn]))

        # sends input to emulator in parallel if count exceeds threshold
        if config.button_inputs[btn] >= config.vote_threshold:
            t = threading.Thread(target=send_emulator_input, args=(btn,))
            t.start()
            utils.clear_button_inputs()
            break


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

            if msg.startswith('!help'):
                send_msg(sock, 'https://pastebin.com/VFMGMjpb')
            elif msg.startswith('!game '):
                cheat = parts[1].lower()
                read_cheat_input(cheat, username)
            else:
                read_button_input(msg, username)
