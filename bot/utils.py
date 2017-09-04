# utils.py

import config
import json
import re
import socket
import urllib.request

from stoppablethread import StoppableThread
from time import sleep
from chat.user import User


# IRC functions
# =============

def irc_connect():
    """Sets up connection to IRC"""
    sock = socket.socket()
    sock.connect((config.HOST, config.PORT))
    sock.send('PASS {}\r\n'.format(config.PASS).encode('utf-8'))
    sock.send('NICK {}\r\n'.format(config.NICK).encode('utf-8'))
    sock.send('JOIN #{}\r\n'.format(config.CHAN).encode('utf-8'))
    return sock


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
    with config.threads_lock:
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


def read_button_input(message, user):
    vote = format_button_input(message)

    if not vote:
        return

    vote_count = user.vote(config.vm, vote)

    # if vote brought vote count over threshold
    if vote_count >= config.vm.threshold:
        t = StoppableThread(after=finalize_thread, target=send_input, args=('inputs.txt', vote))
        config.threads.append(t)
        t.start()

        config.vm.reset()


def read_cheat_input(cheat, user):
    if cheat not in config.cheat_opts:
        return

    vote_count = user.vote(config.vm, cheat)

    # if vote brought vote count over threshold
    if vote_count >= config.vm.threshold:
        t = StoppableThread(after=finalize_thread, target=send_input, args=('cheats.txt', cheat))
        config.threads.append(t)
        t.start()

        config.vm.reset()
        

def send_input(filename, contents):
    for i in range(10):
        try:
            with open('../' + filename, 'w+') as file:
                file.write(contents)
                print('>>>Sent ' + contents + ' to emulator.')
                break
        except:
            sleep(1)
