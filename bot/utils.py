# utils.py

import config
from chatter import Chatter
from time import sleep


# IRC functions
# =============

def send_msg(sock, msg):
    print(':' + config.NICK + '!' + config.NICK + '@' + config.NICK + '.tmi.twitch.tv PRIVMSG #' + config.CHAN + ' :' + msg + '\r\n')
    sock.send('PRIVMSG #{} :{}\r\n'.format(config.CHAN, msg))
    sleep(config.RATE)


def ban(sock, user):
    if is_op(config.NICK):
        send_msg(sock, '.ban {}'.format(user))


def timeout(sock, user, seconds=600):
    if is_op(config.NICK):
        send_msg(sock, '.timeout {}'.format(user, seconds))


# Bot-specific functions
# ======================

def clear_button_inputs():
    for user in config.chatters:
        config.chatters[user].clear_button()

    for button in config.button_inputs:
        config.button_inputs[button] = 0


def add_chatter(user):
    chatter = Chatter()
    config.chatters[user] = chatter
