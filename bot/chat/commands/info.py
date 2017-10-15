# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/chat/commands/info.py
# Compiled at: 2017-10-13 04:27:54
# Size of source mod 2**32: 455 bytes
import config
import os

def show_help(chat, message):
    path = os.path.join(config.info_dir, 'help.cfg')
    with open(path, 'r') as file:
        help_link = file.read()
    chat.send_message(help_link)


def song(chat, message):
    chat.send_message('Dragon Quest 1 and 2 Symphonic Suites - ' + 'https://www.youtube.com/playlist?list=PL2jLKwo6ZTmQ0vKgGwbcp5m2sp7vy9GXY')


def game_map(chat, message):
    chat.send_message('')