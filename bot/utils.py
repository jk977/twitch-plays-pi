# utils.py

import re
import config
from time import sleep


# IRC functions
# =============

def send_msg(sock, msg):
    print(':' + config.NICK + '!' + config.NICK + '@' + config.NICK + '.tmi.twitch.tv PRIVMSG #' + config.CHAN + ' :' + msg + '\r\n')
    sock.send(bytes('PRIVMSG #' + config.CHAN + ' :' + msg + '\r\n', 'utf-8'))
    sleep(config.RATE)


def ban(sock, user):
    if is_op(config.NICK):
        send_msg(sock, '.ban {}'.format(user))


def timeout(sock, user, seconds=600):
    if is_op(config.NICK):
        send_msg(sock, '.timeout {}'.format(user, seconds))

# Bot-specific functions
# ======================

def format_button_input(message):
    """Formats input to be sent to lua script"""
    # support for inputs prefixed by ! since a lot of people seem to try it
    if message.startswith('!'):
        message = message[1:]

    has_leading_num = bool(re.search('^[1-9]', message))
    has_trailing_num = bool(re.search('[1-9]$', message))

    if has_leading_num:
        mult = message[0]
        button = message[1:]
    elif has_trailing_num:
        mult = message[-1]
        button = message[:-1]
    else:
        mult = '1'
        button = message

    button = button.strip().lower()

    # capitalizes 'a' and 'b' due to FCEUX input format
    if button == 'a' or button == 'b':
        button = button.upper()

    if button not in config.button_opts or not re.match('[1-9]', mult):
        return

    return mult + button
