# utils.py

import config
import json
import re
import urllib.request

from stoppablethread import StoppableThread
from time import sleep
from chat.user import User


# IRC functions
# =============

def send_msg(sock, msg):
    with config.socket_lock:
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

def stop_all_threads():
    """Stops created threads."""
    stoppables = [t for t in config.threads if isinstance(t, StoppableThread)]
    for thread in stoppables:
        thread.stop()


def finalize_thread(thread):
    """Removes thread from thread list after thread finishes."""
    with config.thread_list_lock:
        try:
            config.threads.remove(thread)
        except:
            pass


# TODO finish function
# uncomment when config.users is thread safe
#
# def update_roles():
#     chat_url = 'tmi.twitch.tv/group/user/{}/chatters'
#     with urllib.request.urlopen(chat_url.format(config.CHAN)) as url:
#         content = json.loads(url.read().decode())
#         chatters = content['chatters']
#         mods = chatters['moderators']
#         admins = chatters['admins']


def validate_cheat(message):
    for cheat in config.cheat_opts:
        if re.match(cheat, message):
            return True
    return False
    

def format_button_input(message):
    """Formats input to be sent to lua script"""
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
